---
title: "page table"
date: 2022-07-25T19:24:48+08:00
draft: true
tags:
    - "c"
---


## Sharing pages

![page table](https://en.wikipedia.org/wiki/File:Virtual_address_space_and_physical_address_space_relationship.svg "PageTable-Wiki")

Page table is the brige of communitcating between virtual address space in
process and physical address space in memory.

The noticeable thing is the "direction", page table can be used for mapping from
the virtual memory addr to physical memory addr, it's single direction.

## Memory management unit (MMU)

MMU locates inside the CPU stores a cache of recentlyused mappings from the
operating system's page table. This is called the translation lookaside buffer
(TLB), which is an associative cache.

When a virtual address needs to to translated into a physical address, the TLB
is searched first. When a virtual address needs to be translated into a physical
address, the TLB is searched first. If a match is found, which is known as a TLB
hit, the physical address is returned and memory access can continue. However,
if there is no match, which is called a TLB miss, the MMU or the operating
system's TLB miss handler will typically look up the address mapping in the page
table to see whether a mapping exists, which is called a page walk. If one
exists, it is written back to the TLB, which must be done because the hardware
accesses memory through the TLB in a virtual memory system, and the faulting
instruction is restarted, which may happen in parallel as well. The subsequent
translation will result in a TLB hit, and the memory access will continue.

![TLB Hit/Miss/Walk](https://en.wikipedia.org/wiki/File:Page_table_actions.svg "TLB Hit/Miss/Walk")
