---
title: "stat and fstat"
date: 2022-07-24T23:11:16+08:00
draft: false
tags:
    - "c"
---

## stat

stat() retrieve information about the file pointed to by pathname;

## lstat

lstat() is identical to stat(), except that if pathname is a
symbolic link, then it returns information about the link itself,
not the file that the link refers to.

## fstat

stat() is identical to stat(), except that the file about which
information is to be retrieved is specified by the file
descriptor fd.

## fstat and stat 

If "stat()" could return the information about the file too, why we still need
to first call "open()" to make a FD then use fstat?

The main reason is security, if you first "stat()" the file and then "open()"
it, there is a small window of time in between where the file could have been
modified or had its permissions changed, or replaced by a symlink. You can
understand its a READ but not EXCLUSIVE operation.

"fstat()" make it OK in this scence. Because if you call "open()" first, then
the file can not change by other process now.
