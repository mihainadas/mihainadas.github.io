---
layout: post
title: "One Field Is Not a List Operation"
date: 2026-09-24 06:33:18 +0300
post_type: engineering note
description: "An intrusive-list membership marker must change with the head and neighbor links, or a harmless-looking reset creates an impossible state."
context_reviewed: 2026-09-24
tags: [systems, emulation, debugging, data-structures]
---

86Box emulates historical PC hardware, including the memory maps and x86 processors used by Windows 95 machines. Its new dynamic recompiler translates guest instructions into host code. When the guest modifies a physical page that contains translated code, the emulator must find and invalidate the stale blocks before running them again.

The recompiler tracks pages needing that work in an intrusive eviction list. Each page record stores its own previous and next indices, while a global index names the list head. A special value in `evict_prev` means that the page is not in the list. Those fields describe one relation and have to agree.

A soft restart on an emulated VIA VT82C496G system exposed a state in which they did not. Conventional-memory remapping changed the backing pointers and dirty-code masks of existing page records. The same path also set `evict_prev` to the not-in-list value without unlinking the page. The global head could still point to that page, so the next purge reached it and then aborted because its membership test said it was absent. The [merged correction](https://github.com/86Box/86Box/pull/7787) deleted the two assignments that created this contradiction.

## One relation had three representations

The relevant page fields are small enough to read as a contract. The [page declaration](https://github.com/86Box/86Box/blob/5cf728b4a00e72bdf3d24758e336134289aff4b6/src/include/86box/mem.h#L206-L236) defines `evict_prev`, `evict_next`, and the `EVICT_NOT_IN_LIST` sentinel. Membership is tested only through `evict_prev`:

```c
static inline int
page_in_evict_list(page_t *page)
{
    return page->evict_prev != EVICT_NOT_IN_LIST;
}
```

That predicate is one representation of membership. The list head is another. The forward and backward links are a third. For a live list, at least these conditions must hold:

- the head is zero exactly when the list is empty;
- every page reachable from the head reports that it is in the list;
- adjacent pages agree about their forward and backward links;
- the stored page count equals the number of reachable pages.

The [list insertion and removal functions](https://github.com/86Box/86Box/blob/5cf728b4a00e72bdf3d24758e336134289aff4b6/src/mem/mem.c#L1858-L1888) update those representations together. Insertion rewires the old head, sets both links on the new page, advances the head, and increments the count. Removal rewires the neighbors and head before writing the sentinel and decrementing the count.

Writing only the sentinel is therefore not a smaller removal. It is a different operation with no valid list state as its result.

## The guard reported the contradiction

The removal function begins with a defensive check:

```c
if (!page_in_evict_list(page))
    fatal("page_remove_from_evict_list: not in evict list!\n");
```

The failure message can suggest an invalid removal request. In this case, the caller had obtained the page through valid list state. The [purge path](https://github.com/86Box/86Box/blob/5cf728b4a00e72bdf3d24758e336134289aff4b6/src/codegen_new/codegen_block.c#L164-L176) reads the global head, checks the page's dirty translated-code mask, and eventually [removes the processed page](https://github.com/86Box/86Box/blob/5cf728b4a00e72bdf3d24758e336134289aff4b6/src/codegen_new/codegen_block.c#L491-L504).

The contradiction was already present before removal began:

```text
purgable_page_list_head = page_index
pages[page_index].evict_prev = EVICT_NOT_IN_LIST
```

The first line makes the page reachable. The second makes the membership predicate false. The guard converted a silent structural error into a reproducible abort at the next operation that needed the relation to be coherent.

This distinction matters during diagnosis. Weakening the guard would not repair the list. Forcing removal to continue would use a sentinel as a neighbor index and could corrupt more state. The useful question was not why removal rejected the page, but which earlier operation was allowed to produce an impossible page.

## Remapping did not own list membership

The [page-table allocation path](https://github.com/86Box/86Box/blob/5cf728b4a00e72bdf3d24758e336134289aff4b6/src/mem/mem.c#L2840-L2874) creates the page array and initializes every `evict_prev` field to the sentinel. That is the right time to declare that a newly allocated page is not linked.

Conventional-memory remapping has a narrower job. The [remap function](https://github.com/86Box/86Box/blob/5cf728b4a00e72bdf3d24758e336134289aff4b6/src/mem/mem.c#L2940-L3030) reuses existing page records while changing their RAM pointers, write callbacks, and per-byte mask pointers. It does not allocate a new page table. It does not rebuild the eviction list. It therefore cannot safely reinitialize one of the list fields.

The fix removed one assignment from each of the function's two remapping loops. No replacement list operation was needed because remapping was not supposed to change membership. Preserving the links kept the relation owned by the insertion and removal functions.

Deletion is safe here for a specific reason: the old lines had no independent state transition to express. They partially imitated initialization inside an update path. If remapping had needed to remove pages, the correct repair would have been an explicit unlink operation with defined handling for the list head, neighbors, and count.

## Test the transition that exposes the invariant

The pull request records a narrow regression path: a Windows 95 guest on the 486-VIP-IO2 machine called `ExitWindowsEx(EWX_REBOOT)`. The unmodified debug build aborted during the first guest-initiated restart. With the two assignments removed, three consecutive restarts returned to the Windows network logon dialog.

That test is useful because a soft restart preserves enough emulator state to exercise remapping against an already active recompiler. A cold start initializes the page table and list together, so it is less likely to reach the contradictory state.

The lifecycle test establishes that the reproduced restart no longer triggers the fatal removal check. It does not prove every remapping path or every machine configuration correct. A debug-only structural checker could make the invariant more direct: walk from the head, verify each backlink, reject the sentinel on reachable pages, detect cycles, and compare the visited total with `purgeable_page_count`.

The general lesson is smaller than “test more restarts.” When a relation is stored in several fields, each mutation must either update all of them or leave all of them alone. Reinitializing one field of a live intrusive list is not cleanup. It is corruption that waits for the next honest guard to find it.
