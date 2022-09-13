---
title: "Git Index Format"
date: 2022-09-13T19:19:59+08:00
draft: false 
tags:
    - "git"
    - "c"
---

## what's index acting in git?

* to reproduce a single and global tree(or root-tree).
* to fast recognize between the tree in index and the tree in workspace. 
* to recognize and supply merge conflicts info between different tree objects,
  allowing each pathname to be associated with sufficient information about the
  trees involved that you can create a three-way merge between them.
  
## init test repo

Init a repo which has a blob as "1.txt" in workspace:

```bash
➜  dyroneteng git:(master) ✗ pwd
/Users/tenglong.tl/Downloads/dyroneteng
➜  dyroneteng git:(master) ✗ ls
1.txt
```

Read the blob object:

```bash
➜  d0 git:(master) pwd
/Users/tenglong.tl/Downloads/dyroneteng/.git/objects/d0
➜  d0 git:(master) ls
0491fd7e5bb6fa28c517a0bb32b8b506539d4d
➜  d0 git:(master) git cat-file -p d00491fd7e5bb6fa28c517a0bb32b8b506539d4d
1
➜  d0 git:(master) git cat-file -t d00491fd7e5bb6fa28c517a0bb32b8b506539d4d
blob
```
## structure of the "index" file

* HEADER: 12 bytes header data
* Entries: a number of sorted index entries (asc by "name")
* Extensions: with signature(If the first byte is 'A'..'Z' the extension is
optional and can be ignored.), size of extension, extension data
* Hash Checksum: 20 bytes checksum data

## Understand the "index" file content

```bash
➜  .git git:(master) cat index  | hexdump -C
00000000  44 49 52 43 00 00 00 02  00 00 00 01 63 18 61 d6  |DIRC........c.a.|
00000010  0a 50 73 12 63 18 61 d6  0a 50 73 12 01 00 00 07  |.Ps.c.a..Ps.....|
00000020  06 ef 71 d3 00 00 81 a4  00 00 01 f5 00 00 00 14  |..q.............|
00000030  00 00 00 02 d0 04 91 fd  7e 5b b6 fa 28 c5 17 a0  |........~[..(...|
00000040  bb 32 b8 b5 06 53 9d 4d  00 05 31 2e 74 78 74 00  |.2...S.M..1.txt.|
00000050  00 00 00 00 84 08 b0 29  87 16 de c9 d4 7c 4e ac  |.......).....|N.|
00000060  ec 96 7d d1 6e 95 50 22                           |..}.n.P"|
00000068
```

Let's try to understand the content with each part.

> https://git-scm.com/docs/index-format

* 44 49 52 43: signature is { 'D', 'I', 'R', 'C' } (stands for "dircache")
* 00 00 00 02: version number. 2, 3 and 4 are supported.
* 00 00 00 01: number of the indexed entries in current "index".
* 63 18 61 d6: ctime(the seconds part) of the entry. digit(63 18 61 d6) = 1662542294 and we could
show the ctime by gstat when you on macOS.

```bash
➜  dyroneteng git:(master)  gstat --printf="ctime: %Z" 1.txt
ctime: 1662542294%
```
* 0a 50 73 12: the nanosecond fractions part of ctime

* 63 18 61 d6: mtime(the seconds part) of the entry. digit(63 18 61 d6) =
1662542294 and we could show the mtime by gstat when you on macOS.

```bash
➜  .git git:(master) gstat --printf="mtime: %Y" ../1.txt 
mtime: 1662542294% 
```

* 0a 50 73 12: the nanosecond fractions part of mtime 

* 01 00 00 07: the dev info

* 06 ef 71 d3: the inode number. digit(06 ef 71 d3) = 116355539

```bash
$ gstat --printf="ino: %i" 1.txt
ino: 116355539%
```

* 00 00 81 a4: the unix permission. Only 0755 and 0644 are valid for regular
files. Symbolic links and gitlinks have value 0 in this field.

hex(81 a4) = 100644 in octal 

* 00 00 01 f5: uid of the file

```bash
$ gstat --printf="uid: %u" 1.txt
uid: 501%
```

* 00 00 00 14: gid of the file 

```bash
$ gstat --printf="gid: %g" 1.txt
gid: 20%
```

* 00 00 00 02: file size.

* d0 04 91 fd | 7e 5b b6 fa | 28 c5 17 a0 | bb 32 b8 b5 | 06 53 9d 4d: obj name.

* 00 05: 16-bit "flags". 00 05 = 0000 0000 0000 0101

    * 1-bit assume-valid flag 
    * 1-bit extended flag (must be zero in version 2) 
    * 2-bit stage (during merge) 
    * 12-bit name length if the length is less than 0xFFF; otherwise 0xFFF is
stored in this field. here the lengh is "5".

* 31 2e 74 78 74: entry path name. relative to top level directory (without
  leading slash). '/' is used as path separator. The special path components
  ".", ".." and ".git" (without quotes) are disallowed. Trailing slash is also
  disallowed. "31 2e 74 78 74" in Ascii means "1.txt".

* 00: byte as necessary fpr pading (1-8 nul bytes) while keeping the name
  NUL-terminated.

* 84 08 b0 29 87 16 de c9 d4 7c 4e ac ec 96 7d d1 6e 95 50 22: 20 bytes checksum

## Extensions 

### Cache Tree Extension

When we execute "git commit", the changes in stage(cache, index, they are the
same thing) will be packaged as a commit. Then, the "index" file will be like:

```bash
➜  .git git:(master) cat index | hexdump -C
00000000  44 49 52 43 00 00 00 02  00 00 00 01 63 18 61 d6  |DIRC........c.a.|
00000010  0a 50 73 12 63 18 61 d6  0a 50 73 12 01 00 00 07  |.Ps.c.a..Ps.....|
00000020  06 ef 71 d3 00 00 81 a4  00 00 01 f5 00 00 00 14  |..q.............|
00000030  00 00 00 02 d0 04 91 fd  7e 5b b6 fa 28 c5 17 a0  |........~[..(...|
00000040  bb 32 b8 b5 06 53 9d 4d  00 05 31 2e 74 78 74 00  |.2...S.M..1.txt.|
00000050  00 00 00 00 54 52 45 45  00 00 00 19 00 31 20 30  |....TREE.....1 0|
00000060  0a 38 fd 29 69 7b 22 0f  7e 4c a1 5b 04 4c 32 22  |.8.)i{".~L.[.L2"|
00000070  ee fe 5a fd c1 7b 52 30  32 fd 1b 69 c3 d5 6a da  |..Z..{R02..i..j.|
00000080  c7 00 8e 7b 01 95 34 bd  f3                       |...{..4..|
00000089
```

Actually, the data before "00 05 31 2e 74 78 74 00" is as same as we did the
"git commit" before. So, let's focus on the left parts. Here, it introduces a
new data region: TREE extension.

### Why 

* "index" does not record entries for directories, only record the pathnames.
* extension data stores an recursive tree structure that describes the trees
  already exist (completely match sections of the cache entries) in ODB

  * so for a new commit we could only computing the trees that are "new" to that
    commit, but not to compute the trees by checking each file entry..

  * for comparing the index to another tree, if the tree comparison demonstrates
    euqality, the tree can be skipped, or if there is no cached tree infos in
    index, it will be slow for comparing each file entry.

* although the extension tracks the full directory structurem but generally
  smaller than the full cache entry list.

* when a path is updated in index, all it's related parent trees (nodes in
  recursive tree structure) will mark as invalid by using "-1" as the number of
  cache entries. Invalid nodes still store a span of index entries, allowing Git
  to focus its efforts when reconstructing a full cache tree.

> More info at: https://git-scm.com/docs/index-format#_cache_tree

* checksum: 7b 52 30  32 fd 1b 69 c3 d5 6a da c7 00 8e 7b 01 95 34 bd  f3

### TREE extension data structure:

```bash
00
31
20
30
0a
38 fd 29 69 7b 22 0f 7e 4c a1 5b 04 4c 32 22 ee fe 5a fd c1
```

Struture of the recursive tree currently(we just "add", but not "commit" yet):

* NUL-terminated path component (relative to its parent directory);

> In current case, we have one file locates in root dir, there is no parent
> directories here, so will be directly stored as NUL(00) here.

* ASCII decimal number of entries in the index that is covered by the tree this
  entry represents (entry_count);

> here is "31" in hex represents "1" in Ascii, we only have 1 path entry under
> the root dir that is "1.txt".

* A space (ASCII 32);

> 20 in hex represents SPACE in ASCII.

* ASCII decimal number that represents the number of subtrees this tree has;

> here is "30" in hex represents "0" in Ascii, we do not have a tree(dir), so 
> we do not have any subtrees under it as also.  

* A newline (ASCII 10);

> as "0a".

* Object name for the object that would result from writing this span of index
  as a tree.

> as the left 20 bytes.

### After the "add" 

Next step, we add the new directories and files.

```bash
➜  dyroneteng git:(master) tree
.
├── 1.txt
└── parent
    ├── p.txt
    └── son
        └── s.txt

```

Print out the index content:

```bash
➜  .git git:(master) cat index  | hexdump -C
00000000  44 49 52 43 00 00 00 02  00 00 00 03 63 18 61 d6  |DIRC........c.a.|
00000010  0a 50 73 12 63 18 61 d6  0a 50 73 12 01 00 00 07  |.Ps.c.a..Ps.....|
00000020  06 ef 71 d3 00 00 81 a4  00 00 01 f5 00 00 00 14  |..q.............|
00000030  00 00 00 02 d0 04 91 fd  7e 5b b6 fa 28 c5 17 a0  |........~[..(...|
00000040  bb 32 b8 b5 06 53 9d 4d  00 05 31 2e 74 78 74 00  |.2...S.M..1.txt.|
00000050  00 00 00 00 63 22 d9 2b  30 8d 15 3c 63 22 d9 2b  |....c".+0..<c".+|
00000060  30 8d 15 3c 01 00 00 08  06 fa ed 65 00 00 81 a4  |0..<.......e....|
00000070  00 00 01 f5 00 00 00 14  00 00 00 06 f7 c6 dd 01  |................|
00000080  64 fe 0e b4 fd e7 67 f9  e7 31 a6 c8 ad e0 b6 9f  |d.....g..1......|
00000090  00 0c 70 61 72 65 6e 74  2f 70 2e 74 78 74 00 00  |..parent/p.txt..|
000000a0  00 00 00 00 63 22 d9 37  2e 30 7a 78 63 22 d9 37  |....c".7.0zxc".7|
000000b0  2e 30 7a 78 01 00 00 08  06 fa ed 8e 00 00 81 a4  |.0zx............|
000000c0  00 00 01 f5 00 00 00 14  00 00 00 05 c7 dc 98 9f  |................|
000000d0  80 44 a4 fc f1 63 61 41  49 98 e1 46 94 e1 ac 7e  |.D...caAI..F...~|
000000e0  00 10 70 61 72 65 6e 74  2f 73 6f 6e 2f 73 2e 74  |..parent/son/s.t|
000000f0  78 74 00 00 54 52 45 45  00 00 00 06 00 2d 31 20  |xt..TREE.....-1 |
00000100  30 0a 88 b9 49 96 42 81  1f 2e ef df a4 d3 ac f0  |0...I.B.........|
00000110  06 56 7f cb 1a 38                                 |.V...8|
00000116
```

Let's focus on the part after the TREE extension signature:

```bash
000000f0  .. .. .. .. 54 52 45 45  00 00 00 06 00 2d 31 20  |xt..TREE.....-1 |
00000100  30 0a 88 b9 49 96 42 81  1f 2e ef df a4 d3 ac f0  |0...I.B.........|
00000110  06 56 7f cb 1a 38                                 |.V...8|
00000116
```

* 00 00 00 06: data size 6
* 00 2d 31 20 30 0a 
  
We only "git-add" the related filepaths but not "git-commit", so the new file
entries are written to the INDEX, but the TREE extension data will not.


### After the "commit"

Let's cut the part before TREE extension signature and the
tailing checksum part.

```bash
000000f0  .. .. .. .. 54 52 45 45  00 00 00 54 00 33 20 31  |xt..TREE...T.3 1|
00000100  0a dc 2f b0 3f 28 4b 1f  f6 21 2e 99 9e 3e d6 4d  |../.?(K..!...>.M|
00000110  ac 56 5c 6f 39 70 61 72  65 6e 74 00 32 20 31 0a  |.V\o9parent.2 1.|
00000120  8b e9 ba e5 9d fe 61 49  61 f1 31 04 f0 8c 32 77  |......aIa.1...2w|
00000130  33 e0 54 5f 73 6f 6e 00  31 20 30 0a e4 6d 15 1e  |3.T_son.1 0..m..|
00000140  5b bb d1 78 21 d0 c3 ba  67 03 b2 d2 .. .. .. ..  |[..x!...g...b.Z.|
00000150  .. .. .. .. .. .. .. ..  .. .. .. .. .. .. .. ..  |.X....@...>..U..|
00000160  .. .. .. .. 
```

* 00 00 00 54 : TREE extension data size 84 (54 in hex)

* 00 33 20 31 : 

  * 00 : NUL-terminated path component
  * 33: ASCII decimal number of entries in the index that is covered by the tree
    this entry represents (entry_count). Here is 3, there are 3 entries under
    root tree dir.
  * 20: SPACE
  * 31: ASCII decimal number that represents the number of subtrees this tree
    has. Here is 1 subtree, it's "parent".
* 0a: NEW LINE
* dc 2f b0 3f | 28 4b 1f f6 | 21 2e 99 9e | 3e d6 4d ac | 56 5c 6f 39: the root
  tree.
  
```bash
➜  objects git:(master) git cat-file -p dc2fb03f284b1ff6212e999e3ed64dac565c6f39
100644 blob d00491fd7e5bb6fa28c517a0bb32b8b506539d4d    1.txt
040000 tree 8be9bae59dfe614961f13104f08c327733e0545f    parent
```

* 70 61 72  65 6e 74 00: NUL-terminated path component. Here is "parent".

* 32 20 31 0a :
  * 32: Here is 2. There are 2 entries under parent dir.
  * 20: SPACE
  * 31: Here is 1. There is 1 subtree, it's "son".
  * 0a: NEW LINE
* 8b e9 ba e5 9d fe 61 49 61 f1 31 04 f0 8c 32 77 33 e0 54 5f: tree as "parent"
  dir.

```bash
➜  8b git:(master) git cat-file -p 8be9bae59dfe614961f13104f08c327733e0545f
100644 blob f7c6dd0164fe0eb4fde767f9e731a6c8ade0b69f    p.txt
040000 tree e46d151e5bbbd17821d0c3ba6703b2d262f75a01    son
```

* 73 6f 6e 00:  NUL-terminated path component. Here is "son".
* 31 20 30 0a:
  * 31: Here is 1. There is 1 entry under son dir.
  * 20: SPACE
  * 30: 0. There are no subtrees under son dir.
  * 0a: NEW LINE
* e4 6d 15 1e .. : tree as "son" dir.

> To be continued...
