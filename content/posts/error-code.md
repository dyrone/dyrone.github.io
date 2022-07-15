---
title: "About errno "
date: 2022-07-14T22:44:37+08:00
tags:
    - "errno"
draft: false 
---

_This article mainly introduces errno related content. If I get new input, I
will add the content one after another._

## About errno

> errno - number of last error

You can take a look at https://man7.org/linux/man-pages/man3/errno.3.html to
know about what's errno and how the errno is supported in POSIX and C99.


## Man Page

```adoc
       errno {name-or-code}

       errno [-ls] [--list]

       errno [-s] [--search] {word}

       errno [-S] [--search-all-locales] {word}
```

```shell
➜  git git:(tl/bitmap-append-trace2-outputs) ✗ errno -s direct 
ENOENT 2 No such file or directory
ENOTDIR 20 Not a directory
EISDIR 21 Is a directory
ENOTEMPTY 66 Directory not empty
```


## 20: ENOTDIR

In a recent Git patch, Junio C Hamano, the maintainer of the Git community, gave
me the following advice about ENOTDIR:

> One thing you should consider when writing a "this is an optional
> file and not finding it is perfectly fine" logic like this one is
> that you may or may not want to ignore ENOTDIR.  ENOTDIR is what you
> get when you say open("a/b") and "a" exists as something other than
> a directory.  If you have a path with a slash in bitmap_name, and if
> in a sane and healthy repository the leading path should always
> exist (i.e. the file "a/b" may be missing, but the directory "a/"
> should be there), then getting ENOTDIR is a noteworthy event.  There
> may be cases where ENOTDIR can justifiably and should be ignored.
> 
> from  https://public-inbox.org/git/xmqqpmibmjjs.fsf@gitster.g/

