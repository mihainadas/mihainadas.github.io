---
layout: post
title: "Count the Raster After Decoding"
date: 2026-09-30 09:35:35 +0300
post_type: engineering note
description: "An ESC/P 2 raster command declares its decoded image size, so a streaming emulator must frame compressed input by output bytes."
context_reviewed: 2026-09-30
tags: [systems, emulation, printers, parsing]
---

86Box emulates historical PC hardware and several peripherals, including printers that accept Epson's ESC/P 2 control language. A guest printer driver sends commands and data as one byte stream. The emulator has to decide which bytes are command parameters, which are raster pixels, and where normal command parsing resumes.

The `ESC .` Print Raster Graphics command makes that boundary less obvious than a fixed-size record. Its six-byte header declares a compression mode, horizontal and vertical densities, a band height, and a width in dots. In uncompressed mode, those fields determine the number of payload bytes directly. In run-length encoded mode, the stream carries counters whose encoded length varies with the image.

An earlier [86Box debugging note](/2026/08/27/three-emulator-bugs.html) recorded the integration result: after the command was implemented, a Windows 95 Epson LQ-2500 test page changed from seven malformed PNG files and an emulator termination to one complete page. This note examines the parser invariant behind that result. The command ends when it has produced the declared raster rectangle, not after a fixed number of compressed input bytes.

## The header describes the decoded image

Epson's [ESC/P Reference Manual](https://files.support.epson.com/pdf/general/escp2ref.pdf#page=179) gives the command in this form:

```text
ESC . c v h m nL nH d1 d2 ... dk
```

The `c` byte selects uncompressed data (`0`) or run-length encoding (`1`). The `v` and `h` bytes select vertical and horizontal density as `3600 / value` dots per inch. The band height `m` is 1, 8, or 24 dot rows. The two little-endian bytes `nL` and `nH` give the width in dots:

```text
width = nL + 256 * nH
```

Pixels are packed most-significant bit first. A row therefore occupies the ceiling of the width divided by eight, and the complete decoded payload size is:

```text
bytes_per_row = (width + 7) / 8
decoded_bytes = m * bytes_per_row
```

Integer division is intentional in the first expression. A 13-dot row still needs two bytes. The final three bits belong to padding rather than pixels. An eight-row band at that width contains 16 decoded bytes regardless of how well or poorly it compresses.

The [merged 86Box setup code](https://github.com/86Box/86Box/blob/0b09291183131b12f85c90f226aeed917c81ec5d/src/printer/prt_escp.c#L770-L803) turns the header into this state. It validates the compression mode, densities, band height, and nonzero width; computes the row and band byte counts; records the current print position as the origin; and activates raster handling.

This is the first useful separation in the parser. The header defines an output rectangle. Compression only defines how subsequent input bytes reconstruct it.

## RLE changes the transport length

The manual defines two kinds of RLE counter. Values from 0 through 127 mean that the following `counter + 1` bytes are literals. Values from 128 through 255 mean that the next single byte must be repeated `257 - counter` times.

For the 16-byte band above, this six-byte compressed payload produces the required decoded length:

```text
02 80 00 FF F4 00
```

The first counter, `02`, copies the following three bytes literally: `80 00 FF`. The second counter, `F4` or 244, repeats `00` thirteen times. Three literal bytes plus thirteen repeated bytes fill the band.

The same raster could require seventeen encoded bytes if it were sent as one literal run: a counter of 15 followed by all sixteen data bytes. Nothing in the six-byte command header declares either encoded length. Counting bytes received would make the command boundary depend on the compression ratio, which the parser does not know in advance.

The counter rule also deserves a literal implementation. A byte value of 128 requests 129 copies because `257 - 128 = 129`. Treating 128 as a no-operation would silently substitute the rule from a different run-length format. The protocol's arithmetic is a better specification than a familiar compression name.

## Three states preserve the boundary

86Box consumes printer data one byte at a time. Its [raster decoder](https://github.com/86Box/86Box/blob/0b09291183131b12f85c90f226aeed917c81ec5d/src/printer/prt_escp.c#L2013-L2051) uses three states:

```text
COUNTER -> LITERAL -> COUNTER
        -> REPEAT  -> COUNTER
```

In `COUNTER`, one input byte selects a run type and length. In `LITERAL`, each input byte emits one decoded byte until that run is exhausted. In `REPEAT`, one input byte can emit as many as 129 decoded bytes. Uncompressed mode bypasses the RLE states and emits each input byte directly.

The invariant is independent of those paths:

```text
0 <= decoded_so_far <= decoded_bytes
```

Every emitted byte increments `decoded_so_far`. When it reaches the band size computed from the header, the implementation advances the horizontal print position by `width / horizontal_density` and deactivates raster handling. The next input byte returns to the ordinary ESC/P interpreter.

This design makes compressed input a producer of raster bytes rather than a second command-framing scheme. Literal runs, repeat runs, and uncompressed bytes all meet at one output counter. The command boundary has one owner.

It also identifies the malformed-stream policy that needs an explicit test. A valid RLE sequence must produce exactly the declared rectangle. A counter that promises more output than remains must not be allowed to draw outside the band, and an incomplete stream must not be mistaken for a complete command. The merged change validates header fields and stops rendering at the declared output count. It does not claim a general recovery mechanism for every truncated or overlong printer stream.

## Decoded order determines pixel position

The output counter carries enough information to place a byte without retaining the whole band. The [rendering function](https://github.com/86Box/86Box/blob/0b09291183131b12f85c90f226aeed917c81ec5d/src/printer/prt_escp.c#L1961-L2011) derives a row and byte offset as follows:

```text
row    = decoded_so_far / bytes_per_row
byte_x = decoded_so_far % bytes_per_row
dot_x  = byte_x * 8 + bit
```

Bits are tested from `0x80` down to `0x01`, so the leftmost pixel in a byte is emitted first. The `dot_x < width` check discards padding bits in the last byte of a non-byte-aligned row. Horizontal and vertical densities then map the dot coordinates to positions on the emulator's page bitmap.

This mapping depends only on decoded order. It gives identical pixel positions when the input is uncompressed, split across several literal runs, or expressed with repeat counters. It also prevents input packet boundaries from becoming image boundaries. Whether the emulated parallel port delivers the six bytes above continuously or with pauses does not change the reconstructed sequence.

The current print position moves only after the complete band. Advancing it for every compressed byte would produce different layout for two encodings of the same pixels. Again, decoded geometry owns the visible result.

## Test framing before judging the page

The Windows 95 test page remains useful. It exercises a real driver, color selection, raster graphics, text, page completion, and the transition back from image data to later commands. One correct page establishes that the reproduced job crosses those subsystem boundaries successfully.

A smaller parser test should make the framing claim direct. For a 13-by-8 band, it can feed 16 known decoded bytes through both uncompressed mode and several RLE partitions, then compare the resulting pixels and final print position. The test should place another ESC/P command immediately after the raster payload and verify that it is parsed as a command rather than consumed as image data.

Boundary cases add information that a screenshot cannot:

- a width not divisible by eight, with set padding bits that must not draw;
- literal and repeat counters at both ends of their ranges, including counter 128;
- a run ending exactly on the final decoded byte;
- declared output that is shorter or longer than the supplied RLE expansion;
- the same decoded bytes divided into different legal runs.

The last case is the core equivalence test. If two byte streams decode to the same rectangle, compression choices must not change the page or the parser state that follows it.

The [merged pull request](https://github.com/86Box/86Box/pull/7774) repaired one concrete Windows 95 printing path and documented the page-level result. The deeper contract is smaller: derive the output length from the raster geometry, count bytes after decompression, and return control to the command interpreter at that exact boundary. A streaming parser stays synchronized when it measures the object the protocol actually declared.
