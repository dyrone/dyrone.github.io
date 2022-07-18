---
title: "mmap"
date: 2022-07-18T19:24:48+08:00
draft: true
---

## munmap 

If you use mmap successfully, it's usually need to munmap when the work
finished.

## mmap

It's recommanded to read the mmap manpage at first. What I read is the
Linux Programmer's Manual version, I think the BSD revison(like Darwin
on MacOS) maybe exist some difference but should be compatible.

> mmap, munmap - map or unmap files or devices into memory

What's the first "m" letter means "memory" I think, it's all about the
data of memory.

```C
    // mmap()  creates  a  new  mapping  in  the  virtual address space of the calling process.
    void *mmap(void *addr, size_t length, int prot, int flags,
                  int fd, off_t offset);
```

## size of memory mapping

The address `addr` must be a multiple of the page size (but `length` need not
be ).

A file is mapped in multiples of the page size.  For a file that
is not a multiple of the page size, the remaining bytes in the
partial page at the end of the mapping are zeroed when mapped,
and modifications to that region are not written out to the file.

### arg addr:

The starting address for the new mapping is specified in addr ** If addr
  is NULL, then the kernel chooses the address at which to create the mapping;
  ** If addr is not NULL, then the kernel takes it as a hint about where to
  place the mapping; (on Linux, the mapping will be created at a nearby page
  boundary. The address of the new mapping is returned as the result of the
  call.)

### arg length:

initialized size in bytes.


### arg offset:

the starting positon of file( offset must be a multiple of the page
size as returned by `sysconf(_SC_PAGE_SIZE)` syscall or executing
`getconf PAGEZIDE`)  

### arg fd:

the file descriptor

### prot:

Memory protection controlling, It is either PROT_NONE or the bitwise OR of one
or more of the following flags::

* PROT_EXEC: Pages may be executed.

* PROT_READ: Pages may be read.

* PROT_WRITE: Pages may be written.

* PROT_NONE:  Pages may not be accessed.
 
 
### flags

The common flags are:

* MAP_SHARED: visible to other processes mapping the same region, and are
  carried through to the underlying file. 
 
* MAP_SHARED_VALIDATE: same behavior as MAP_SHARED except MAP_SHARED mappings
  unknow flags in "flags" 
  
* MAP_PRIVATE: create a private copy-on-write mapping. Updates to the mapping
  are not visible to other processes mapping the same file. and are not carried
  through to the underlying file.It is unspecified whether changes made to the
  file after the mmap() call are visible in the mapped region.

The tree above are the basic flag, in addition, zero or more of the other
flags can be ORed with them :

MAP_32BIT, MAP_ANON, MAP_ANONYMOUS, MAP_DENYWRITE, MAP_EXECUTABLE, MAP_FILE, 
MAP_FIXED, MAP_FIXED_NOREPLACE, MAP_GROWSDOWN, MAP_HUGETLB,  MAP_HUGE_2MB,
MAP_HUGE_1GB, MAP_LOCKED, MAP_NONBLOCK, MAP_NORESERVE, MAP_POPULATE, MAP_STACK,
MAP_SYNC, MAP_UNINITIALIZED.

## munmap

The system call deletes the mappings for the specified address range, and causes
further references to addressed within the range to generate invalid memory
references. The region is also automatically unmapped when the process is
terminated. On the other hand, closing the file descriptor does not unmap the
region. 

All pages containing a part of the indicated range are unmapped, and subsequent
references to these pages will generate `SIGSEGV`. It's not an error if the
indicated range does not contain any mapped pages.

  
## mmap in git

In git mmap is packages as function xmmap(). 

The call stack: 

> xmmap(..) 
> xmmap_gently(...)
> mmap_limit_check(..) then mmap(...)

