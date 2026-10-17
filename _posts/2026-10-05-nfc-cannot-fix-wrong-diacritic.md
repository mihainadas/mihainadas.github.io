---
layout: post
title: "NFC Cannot Fix the Wrong Diacritic"
date: 2026-10-05 09:35:34 +0300
last_modified_at: 2026-10-17 13:42:57 +0300
post_type: engineering note
description: "Unicode normalization joins composed and decomposed Romanian letters, but legacy cedillas require a separate, language-aware policy."
context_reviewed: 2026-10-17
editorial_reviewed: 2026-10-17
lang: en
translation_key: romanian-unicode
tags: [romanian-nlp, unicode, evaluation, data-quality]
---

Romanian diacritic restoration takes text with missing marks and reconstructs the intended spelling while preserving everything else. Modern Romanian uses **ș** and **ț**, with a comma below. Older software and converted corpora often contain the similar-looking cedilla characters **ş** and **ţ** instead. A system importing customer records or scoring restored text has to decide what to do with those older forms. Should it accept them as the same letters, or flag them because modern Romanian output was required?

Unicode normalization gives equivalent encodings a consistent representation. Its NFC form can compose a base letter and a combining mark into one character. My earlier note on [restoration metrics](/2025/09/29/romanian-diacritics-challenge.html) included legacy cedillas among the positions that may need repair, but that repair needs a separate rule. Normalization can reconcile a precomposed **ț** with a sequence made from `t` and a combining comma below. It does not change a cedilla into a comma.

This note isolates the boundary with four encodings of `fața`, meaning _the face_. Two use the modern comma below and two use the legacy cedilla. NFC reduces four code-point sequences to two Unicode strings, not one. A Romanian-specific mapping can join the remaining pair, but it must be an explicit language and evaluation policy.

## Four spellings form two normalization groups

The visible word can be represented with a precomposed letter or with a base letter followed by a combining mark:

| Form | Python literal | Relevant code points |
| --- | --- | --- |
| modern, precomposed | `fața` | `U+021B` |
| modern, decomposed | `fat\u0326a` | `U+0074 U+0326` |
| legacy, precomposed | `faţa` | `U+0163` |
| legacy, decomposed | `fat\u0327a` | `U+0074 U+0327` |

U+0326 is COMBINING COMMA BELOW. U+0327 is COMBINING CEDILLA. The distinction can be hard to see in a small font, but it is present in the text.

Python exposes the Unicode normalization algorithm through [`unicodedata.normalize`](https://docs.python.org/3/library/unicodedata.html). The four cases can be checked directly:

```python
from unicodedata import normalize


samples = {
    "modern precomposed": "fața",
    "modern decomposed": "fat\u0326a",
    "legacy precomposed": "faţa",
    "legacy decomposed": "fat\u0327a",
}

for name, value in samples.items():
    print(name, repr(normalize("NFC", value)))
```

The result is:

```text
modern precomposed 'fața'
modern decomposed  'fața'
legacy precomposed 'faţa'
legacy decomposed  'faţa'
```

NFC makes each group internally consistent. It does not join the groups. NFKC produces the same result for these characters.

## The decomposition table explains the result

[Unicode Standard Annex #15](https://www.unicode.org/reports/tr15/) defines NFC as canonical decomposition followed by canonical composition. NFKC starts from compatibility decomposition instead. Neither operation is a visual-similarity rule or a language-specific spelling corrector.

The decisive data is in the Unicode Character Database. Its current [`UnicodeData.txt`](https://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt) gives these canonical decompositions:

```text
U+021B LATIN SMALL LETTER T WITH COMMA BELOW
    -> U+0074 LATIN SMALL LETTER T
     + U+0326 COMBINING COMMA BELOW

U+0163 LATIN SMALL LETTER T WITH CEDILLA
    -> U+0074 LATIN SMALL LETTER T
     + U+0327 COMBINING CEDILLA
```

The base letter is the same. The combining marks are not. There is no canonical or compatibility decomposition from the cedilla form to the comma-below form, so none of the four normalization forms is allowed to invent one.

This is a useful constraint. Normalization has stable, language-independent semantics. If it silently changed one mark into another because a particular language treats them as historical variants, it could corrupt text in a language where the cedilla is the intended character.

## Romanian equivalence is a higher-level rule

The [Unicode Standard's discussion of Romanian](https://unicode.org/versions/Unicode18.0.0/core-spec/chapter-7/) prefers U+0219 **ș** for modern Romanian and identifies U+015F **ş** as the Turkish s with cedilla. It also records the practical complication: legacy Romanian data often contains the cedilla code point and Romanian processing should treat the two forms as equivalent.

Those statements describe a language-aware operation above Unicode normalization. A compact implementation is:

```python
import unicodedata


ROMANIAN_LEGACY = str.maketrans({
    "Ş": "Ș",
    "ş": "ș",
    "Ţ": "Ț",
    "ţ": "ț",
})


def normalize_romanian(text):
    composed = unicodedata.normalize("NFC", text)
    return composed.translate(ROMANIAN_LEGACY)
```

The order matters. NFC first turns `s` plus U+0327 into precomposed U+015F, so the explicit table handles precomposed and decomposed legacy input with the same four entries. A final NFC call would be harmless here but is unnecessary because every replacement is already precomposed.

The function must not be presented as general Unicode cleanup. U+015F is valid Turkish text. Mapping it unconditionally in a multilingual corpus would replace the intended Turkish cedilla with a Romanian comma below. The input's declared language, field, or corpus contract must authorize the mapping.

Byte decoding belongs before both steps. If an ISO-8859-2 byte stream was decoded with the wrong character encoding, Unicode normalization cannot reconstruct the lost byte interpretation. A replacement character such as U+FFFD is evidence that the pipeline crossed that boundary without enough information.

## Measure spelling and output format separately

Suppose the reference contains `fața știe`, while a system returns `faţa ştie`. Three comparisons answer three different questions:

```python
reference = "fața știe"
prediction = "faţa ştie"

raw_equal = prediction == reference
nfc_equal = (
    unicodedata.normalize("NFC", prediction)
    == unicodedata.normalize("NFC", reference)
)
romanian_equal = (
    normalize_romanian(prediction)
    == normalize_romanian(reference)
)
```

The values are `False`, `False`, and `True`. The raw comparison is sensitive to every code-point choice. NFC removes accidental composition differences but still requires the correct mark. The Romanian fold measures the intended letters while accepting a declared legacy representation.

For a restoration benchmark, I would keep at least two views:

- a content score after NFC and the declared Romanian legacy fold;
- an output-contract score after NFC but before the legacy fold.

The first avoids treating old corpus encoding practice as a language error. The second detects a system that keeps emitting legacy code points when the delivery contract requires modern Romanian text. Reporting only the folded score would hide that integration defect. Reporting only the strict score could turn a historical encoding convention into an apparent restoration failure.

The raw form should remain available for provenance and debugging. Dataset hashes, import logs, and audit samples need to show whether the source contained decomposed marks, cedillas, or already-modern text. Destructive normalization at ingestion can otherwise make a later metric impossible to interpret.

## Test the distinctions, not only the function

A small regression table is enough to protect the policy:

```text
modern precomposed   -> modern precomposed
modern decomposed    -> modern precomposed
legacy precomposed   -> modern precomposed, Romanian fields only
legacy decomposed    -> modern precomposed, Romanian fields only
Turkish s-cedilla    -> unchanged outside Romanian fields
invalid byte decode  -> rejected or recorded, never guessed
```

The test should cover uppercase **Ș/Ț**, lowercase **ș/ț**, both combining marks, and mixed strings. It should also assert that unrelated characters and string length at the grapheme level are preserved. A restoration pipeline that changes punctuation, URLs, or names has a different failure from one that chooses the wrong Romanian mark.

For a Romanian-only import, the sequence is small: decode correctly, apply NFC, then apply the declared legacy-character mapping. For a multilingual field, keep the language boundary explicit. Two letters that look almost identical are enough to make an otherwise reasonable cleanup rule change the wrong text.
