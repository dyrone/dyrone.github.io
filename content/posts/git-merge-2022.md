---
title: "Git Merge 2022"
date: 2022-11-17T10:36:01+08:00
draft: false 
---

## (Git Merge)² By Elijah Newren (Git Merge的平方——新版Merge介绍)

2020年开始研究git merge的优化，截止到2022才完成git 新版merge全部的实现。

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h87xhbhpztj31d80q4n0t.jpg)

### 三路合并(three-way content merge)

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h87xicw3yrj31d20o6n11.jpg)

假设我们有一个简单的文件，存在于我们感兴趣的两个分支上，我将分支命名为<side-one>
和<side-two>，假设我们有三行在<side-one>的这个感兴趣的文件中，而我们在<side-two>
的文件中有三个非常相似的行。但是， 现在如果我们合并这些分支，中间行在两个分支之
间是不同的，那条中间线在合并的最后会发生什么，除非您知道历史上的共同点（称为
merge base）中发生了什么，否则很难说清楚。

所以如果合并基础恰好与<side-one>匹配，那么我们可以说很好，<side-two>没有进行任何
更改，因此合并结果应该与<side-two>对比，如果合并基础与<side-two>匹配，那么我们会
说<side-two>没有进行任何更改，所以我们应该从<siede-one>对比。

当然也有可能是<merge base>与任何一方都不匹配，然后我们都知道这会产生合并冲突，尽
管我们可能不是那么喜欢它。

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h883mmrdu3j31lr0u0dm1.jpg)

### 新特性：--remerge-diff

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8847n3kszj31i80qagra.jpg)

> when you want to look at a previous merge and say how did
> this person resolve the conflicts in this merge?
> then you can pass this remerge flag.

同时，remerge的输出信息回展示两侧合并时的<commid-oid>, 以及最终解决后
的结果, 其背后是通过将 <merge commit> 的两个parent进行再次合并，同时创建一个临时的
<tree object>用来保存合并后的结果（比如包含了conflict的信息）。 当临时的<tree
object> 还原后，与实际的 <merge commit> 进行 diff 操作，便可以的到执行的结果。 

```diff
commit f45e25cb6665291ab6ee7167ca6cdb72b468a3c9 (HEAD -> master)
Merge: eb1d27b f93af98
Author: tenglong.tl <tenglong.tl@alibaba-inc.com>
Date:   Thu Nov 17 14:40:18 2022 +0800

    Merge branch 'topic'

diff --git a/1.txt b/1.txt
remerge CONFLICT (content): Merge conflict in 1.txt
index f40bda6..de663a0 100644
--- a/1.txt
+++ b/1.txt
@@ -1,5 +1 @@
-<<<<<<< eb1d27b (3)
-2022年11月17日 星期四 14时39分17秒 CST
-=======
-2022年11月17日 星期四 14时38分58秒 CST
->>>>>>> f93af98 (2)
+ I need a new date!!

```

### 新特性：AUTO_MERGE

可以在解决冲突的过程中，回顾你最近的冲突解决的相关信息 :

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h884ti21rsj31ik0pydkx.jpg =200x20)

具体的提交为5291828df8386ebeb01039d1403d9f845d2f6e20
```shell

commit 5291828df8386ebeb01039d1403d9f845d2f6e20
Author: Elijah Newren <newren@gmail.com>
Date:   Sat Mar 20 00:03:52 2021 +0000

    merge-ort: write $GIT_DIR/AUTO_MERGE whenever we hit a conflict
    
    There are a variety of questions users might ask while resolving
    conflicts:
      * What changes have been made since the previous (first) parent?
      * What changes are staged?
      * What is still unstaged? (or what is still conflicted?)
      * What changes did I make to resolve conflicts so far?
    The first three of these have simple answers:
      * git diff HEAD
      * git diff --cached
      * git diff
    There was no way to answer the final question previously.  Adding one
    is trivial in merge-ort, since it works by creating a tree representing
    what should be written to the working copy complete with conflict
    markers.  Simply write that tree to .git/AUTO_MERGE, allowing users to
    answer the fourth question with
      * git diff AUTO_MERGE

```

下面是我本地的一个例子，足以说明conflict tree对象的构造和实现方式：

```shell
➜  remerege-test git:(master) ✗ cat .git/AUTO_MERGE 
46cd09ccb1bc612a6b153fdc4afc6eb57c033dae
➜  remerege-test git:(master) ✗ git show 46cd09ccb1bc612a6b153fdc4afc6eb57c033dae | cat
tree 46cd09ccb1bc612a6b153fdc4afc6eb57c033dae

1.txt
➜  remerege-test git:(master) ✗ git cat-file -p 46cd09ccb1bc612a6b153fdc4afc6eb57c033dae
100644 blob 5afb917ee9420afc90ee7abd194743ab204b20f8    1.txt
➜  remerege-test git:(master) ✗ git cat-file -p 5afb917ee9420afc90ee7abd194743ab204b20f8
<<<<<<< HEAD
2022年11月17日 星期四 14时39分17秒 CST
=======
2022年11月17日 星期四 14时38分58秒 CST
>>>>>>> topic
```

### 新特性：Repository subsets

新的merge实现对于实现仓库的下列实现至关重要：

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h885n22qx3j31he0q2gq8.jpg)

### 新特性：孵化部分

目前Github已经使用新的merge实现进行替换，同时与Newren一起完成其他剩余部分内容。

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h885pji2dsj31cc0hqjul.jpg)

### 性能的挑战

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h885tfmqslj31fa0iedj3.jpg)

### Why renames are important?

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8874ka6yfj31iy0r2q9f.jpg)

### How rename detection works

我们需要从两端进行rename的检测，即根据merge-base到 <side-one> 以及 <side-two> 
, 但是在例子中，可以从随意的一端<given-side>开始举例:

* 如果一个文件，在两端均有出现，那么则不是rename的情况；

* 另外的一种情况，例如在base中存在，而在<given-side不存在>时候，可能是在
  <given-side>做了删除和新增的操作，但是也有可能是rename。

* 针对每一对deleted/added:
  * 做一个2*2矩阵的遍历计算
  * factor = 两个文件<相同内容>的比例

这样做的方式在commit中包含的文件变更较多时，这种计算是比较昂贵的，可能造成一些性
能上的影响。

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h888v2zy7vj31jg0rm0ym.jpg)
