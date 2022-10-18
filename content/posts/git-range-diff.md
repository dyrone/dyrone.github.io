---
title: "Git Range Diff"
date: 2022-10-18T19:18:41+08:00
draft: true
tags:
    - git
    -gerrit
---

## How gerrit make the diff between changes

Gerrit是single-commit的评审模式，每一个评审被称之为一个change， change中包含了评
审的历史， 而历史的含义为包含贡献者提交的补丁（patch）， 通过对比patch与patch之
间的差异，可以帮助评审者高效的评审代码。

![patch diff](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/2601/1666092237575-fd335b8a-c8dc-4d78-a2f1-e024a8cce0a4.png?x-oss-process=image%2Fresize%2Cw_1875%2Climit_0 "patch diff")

> From: https://gerrit-review.googlesource.com/c/gerrit/+/345774/2..3

我们可以下载Gerrit的源码，以及ID为345774的change到本地，从而更好的了解这种patch
之间的diff是如何计算的。

> 仓库地址： https://gerrit.googlesource.com/gerrit

```shell
➜  gerrit git:(master) git fetch origin +refs/changes/74/345774/*:refs/changes/74/345774/*                                             
remote: Finding sources: 100% (54/54)
remote: Total 54 (delta 3), reused 42 (delta 3)
Unpacking objects: 100% (54/54), 30.66 KiB | 190.00 KiB/s, done.
From https://gerrit.googlesource.com/gerrit
 * [new ref]               refs/changes/74/345774/1    -> refs/changes/74/345774/1
 * [new ref]               refs/changes/74/345774/2    -> refs/changes/74/345774/2
 * [new ref]               refs/changes/74/345774/3    -> refs/changes/74/345774/3
 * [new ref]               refs/changes/74/345774/4    -> refs/changes/74/345774/4
 * [new ref]               refs/changes/74/345774/meta -> refs/changes/74/345774/meta

 ➜  gerrit git:(master) git show-ref |grep changes  
60e06e2a7aa5fc15902b5b7b0b33c3d3f2379af7 refs/changes/74/345774/1
8df9520ad716546f7e2381f641c87fdd32ed39d3 refs/changes/74/345774/2
90ef1416cbf5ae339bcc049f2e71348d795fe289 refs/changes/74/345774/3
bf40424ba2b0ae97e7d6a205b3eb14259a3e9728 refs/changes/74/345774/4
95f89047cf973d4645f8b206a83bc7fd7d97ac03 refs/changes/74/345774/meta
```

Each ref represent the information about a change patch, the change ID, patch
sequence, and the commiti SHA;

## The range diff

By Gerrit UI, if we 

