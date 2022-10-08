---
title: "Git Notes(to be continued...)"
date: 2022-10-06T19:02:07+08:00
draft: false 
tags: 
    - git
---


## Quick start


下面的demo选择了openstack社区的tripleo-quickstart快速开始，我们首先克隆该仓库。

```shell
git clone https://review.opendev.org/openstack/tripleo-quickstart
```

Openstack 相关的仓库大多使用 git-notes来保存commit自身包含信息之外的其他信息。
                                                                                                                                      
Gerrit 使用特殊的引用 `refs/notes/review`来记录"notes"，默认情况下，clone的仓库
中是不会包含该引用的，但是我们可以通过`git fetch` 子命令将其获取到本地。

```shell
git fetch origin refs/notes/review:refs/notes/review
```

然后, 我们可以执行`git log --notes=refs/notes/review --no-merge`帮助显示非merge
节点提交的"notes"：

```shell
commit dc26b849018e3d5f2ecfe625fca7264877fe75ae (HEAD -> master, origin/master, origin/HEAD)
Author: PranaliD <pdeore@redhat.com>
Date:   Wed Sep 28 11:20:43 2022 +0530

    [CS8][Train] Exclude container-selinux-2:2.189.0
    
    Similar to wallaby[1], latest container-selinux-2:2.189.0 needs
    to be excluded for train as well.
    
    Related-Bug: #1990810
    [1]: https://review.opendev.org/c/openstack/tripleo-quickstart/+/859213
    
    Change-Id: I56d3c199b89997238c50638c9813900a26a3dadb

Notes (review):
    Code-Review+2: yatin <ykarel@redhat.com>
    Code-Review+2: chandan kumar <chkumar@redhat.com>
    Workflow+1: chandan kumar <chkumar@redhat.com>
    Verified+1: RDO Third Party CI <dmsimard+rdothirdparty@redhat.com>
    Verified+2: Zuul
    Submitted-by: Zuul
    Submitted-at: Wed, 28 Sep 2022 12:58:46 +0000
    Reviewed-on: https://review.opendev.org/c/openstack/tripleo-quickstart/+/859516
    Project: openstack/tripleo-quickstart
    Branch: refs/heads/master

commit 61973b67be2a5bf91815aadf7bb99f50a100eed7
Author: Chandan Kumar (raukadah) <chkumar@redhat.com>
Date:   Mon Sep 26 11:36:10 2022 +0530

    [CS8][Wallaby] Exclude container-selinux-2:2.189.0
    
    Latest version of udica[1] requires container-selinux.
    In ffu upgrade job, during container-selinux installation,
    It gives following error:
    ```
    package container-selinux-2:2.189.0-1.module_el8.7.0+1217+ea57d1f1.noarch
    conflicts with udica < 0.2.6-1 provided by udica-0.2.4-1.module_el8.7.0+1217+ea57d1f1.noarch
    ```
    Excluding latest container-selinux-2:2.189.0 fixes the issue
    as it works with existing udica-0.2.4-1.module_el8.
    
    [1]. https://koji.mbox.centos.org/koji/buildinfo?buildID=22871
    
    Related-Bug: #1990810
    
    Signed-off-by: Chandan Kumar (raukadah) <chkumar@redhat.com>
    Change-Id: Ied21dbba59dbfe174036d2301ab9543c924c1de5

Notes (review):
    Code-Review+1: Ananya <anbanerj@redhat.com>
    Code-Review+2: Sandeep Yadav <sandyada@redhat.com>
    Code-Review+2: Marios Andreou <marios@redhat.com>
    Code-Review+2: Cedric Jeanneret <cjeanner@redhat.com>
    Verified+1: RDO Third Party CI <dmsimard+rdothirdparty@redhat.com>
    Verified+2: Zuul
    Workflow+1: Cedric Jeanneret <cjeanner@redhat.com>
    Submitted-by: Zuul
    Submitted-at: Mon, 26 Sep 2022 15:29:34 +0000
    Reviewed-on: https://review.opendev.org/c/openstack/tripleo-quickstart/+/859213
    Project: openstack/tripleo-quickstart
    Branch: refs/heads/master

...
...
omits the older commits outputs
```

关于上面的输出内容，有一些点需要一些解释:

`Notes（review）：`是"notes"的标记，表示接下来的信息是"notes"，而不是
"commit-message"。实际上, 虽然"notes"的能力是git实现的，但是该仓库的注释并不是由
git命令直接生成，而是由 Gerrit Review Notes 插件提供的(JGit)，并且内容和内容格式根据用
户需要定制，它包括批准审查的审查人，测试是否通过如果经过验证以及谁得分，甚至是有
关 Codereview 的一些信息系统、存储库和分支等。

## "notes" 的存储方式 

现在，我们通过 gerrit 使用演示对notes有了一个大致的认识，下一步，我们将尝试从头
开始研究其实现。

我们首先创建一个空仓库，随后创建第一个提交：

```shell
➜  Downloads git init git-notes-test
Initialized empty Git repository in /Users/tenglong.tl/Downloads/git-notes-test/.git/
➜  Downloads cd git-notes-test
➜  git-notes-test git:(master) echo > 1.txt && git add 1.txt && git commit -m "First Commit"
 1 file changed, 1 insertion(+)
 create mode 100644 1.txt
➜  git-notes-test git:(master) ✗ git --no-pager log
commit 7e5ad57b724ecdd911154302b84d5cfba05f8a05 (HEAD -> master)
Author: tenglong.tl <tenglong.tl@alibaba-inc.com>
Date:   Sat Oct 8 20:28:01 2022 +0800

    First Commit
```

这里面没有太多的惊喜，下一步我们尝试直接执行"git notes add"，并解释其效果：


```shell
➜  git-notes-test git:(master) git notes add
```

该命令用于对某个commit添加"notes", 执行之后，终端会出现一个编辑器（默认行为），
我选择在其中添加一些 Gerrit 可能会添加的一些信息（事实上可以写其他你喜好的信息）：

```shell
    Code-Review+2: John Trowbridge <trown@redhat.com>
    Workflow+1: John Trowbridge <trown@redhat.com>
    Verified+2: Jenkins
    Submitted-by: Jenkins
    Submitted-at: Fri, 01 Apr 2016 15:17:54 +0000
    Reviewed-on: https://review.openstack.org/300547
    Project: openstack/tripleo-quickstart
    Branch: refs/heads/master
```

接下来， 我们执行`git --no-pager log` 命令：

```shell
➜  git-notes-test git:(master) git --no-pager log
commit 7e5ad57b724ecdd911154302b84d5cfba05f8a05 (HEAD -> master)
Author: tenglong.tl <tenglong.tl@alibaba-inc.com>
Date:   Sat Oct 8 20:28:01 2022 +0800

    First Commit

Notes:
    Code-Review+2: John Trowbridge <trown@redhat.com>
    Workflow+1: John Trowbridge <trown@redhat.com>
    Verified+2: Jenkins
    Submitted-by: Jenkins
    Submitted-at: Fri, 01 Apr 2016 15:17:54 +0000
    Reviewed-on: https://review.openstack.org/300547
    Project: openstack/tripleo-quickstart
    Branch: refs/heads/master
```

输出显示了我们刚刚为第一个提交添加的"notes"，有意思的事，我们没有指定为哪个提交，
git按照习惯性的方式，选择了`HEAD`，即`7e5ad57b724ecdd911154302b84d5cfba05f8a05`.

如果添加之后发现需要修改已经添加的部分，该怎么办？

```shell
➜  git-notes-test git:(master) git notes add -f
Overwriting existing notes for object 7e5ad57b724ecdd911154302b84d5cfba05f8a05
```

可以使用 `-f` 选项来强制更新某个对象的"notes"。输出表明了一条很关键的输出信息，
那就是刚刚更新覆盖了commit的"notes"， 而不是创建一个新的commit。而这，其实是
"git-notes" 的重要作用和设计目的之一，西面的输出内容证明了"notes"修改之后，commit
本身并没有重新生成，即`7e5ad57b724ecdd911154302b84d5cfba05f8a05`.

```shell
commit 7e5ad57b724ecdd911154302b84d5cfba05f8a05 (HEAD -> master)
Author: tenglong.tl <tenglong.tl@alibaba-inc.com>
Date:   Sat Oct 8 20:28:01 2022 +0800

    First Commit

Notes:
    Code-Review+2: John Trowbridge <trown@redhat.com>
    Workflow+1: John Trowbridge <trown@redhat.com>
    Verified+2: Jenkins
    Submitted-by: Jenkins
    Submitted-at: Fri, 01 Apr 2016 15:17:54 +0000
    Reviewed-on: https://review.openstack.org/300547
    Project: openstack/tripleo-quickstart
    Branch: refs/heads/master
    What-to-add: what we added
```

下一部分, 让我们关注notes是如何存储的。因为commit中不存在修改，那么为了做到看起
来存储额外的信息，势必需要建立commit到notes之间的关联关系，这样我们才能根据一个
commit来搜索其notes的内容，这其中git使用了一种特殊的 ref 来存储笔记的关系。

```shell
git-notes-test git:(master) git show-ref
7e5ad57b724ecdd911154302b84d5cfba05f8a05 refs/heads/master
899773d07250dfc83da9e14c45bd05976af0b124 refs/notes/commits
```

当我们添加notes之后，会产生一个新的ref为`refs/notes/commits`(默认且可配)， 该ref
的commit为`899773d07250dfc83da9e14c45bd05976af0b124`。 紧接着，我们尝试分析这个
commit存储的内容：

```shell
➜  git-notes-test git:(master) git ls-tree -r  899773d07250dfc83da9e14c45bd05976af0b124
100644 blob 0c92279bea1cfd75646ca487bb22bb7d5588251e    7e5ad57b724ecdd911154302b84d5cfba05f8a05
```

`0c92279bea1cfd75646ca487bb22bb7d5588251e`是一个blob对象，存储了文件 
`7e5ad57b724ecdd911154302b84d5cfba05f8a05`, 实际上，这个文件名正是我们创建的第一
个commit，这就是"notes"和commit关联的方式。

`refs/notes/commits`这个引用，通过提交历史的方式，记录了notes的更新历史，而且只
要不是我们人工干预，这个历史讲永远是线性的而不会产生分叉。

```shell
➜  git-notes-test git:(master) git --no-pager log 899773d07250dfc83da9e14c45bd05976af0b124
commit 899773d07250dfc83da9e14c45bd05976af0b124
Author: tenglong.tl <tenglong.tl@alibaba-inc.com>
Date:   Mon Oct 10 18:46:15 2022 +0800

    Notes added by 'git notes add'

commit d49c657d9d0d4be1fb160cb9738c82053c0c9112
Author: tenglong.tl <tenglong.tl@alibaba-inc.com>
Date:   Sat Oct 8 21:09:50 2022 +0800

    Notes added by 'git notes add'
```

根提交是针对我们的第一个`git notes add`，而提示提交是针对我们的第二个`git notes
add -f`操作进行强制更新。下面的输出信息展示了二者之间的改动差异:

```shell
commit 899773d07250dfc83da9e14c45bd05976af0b124
Author: tenglong.tl <tenglong.tl@alibaba-inc.com>
Date:   Mon Oct 10 18:46:15 2022 +0800

    Notes added by 'git notes add'

diff --git a/7e5ad57b724ecdd911154302b84d5cfba05f8a05 b/7e5ad57b724ecdd911154302b84d5cfba05f8a05
index a0ef3e5..0c92279 100644
--- a/7e5ad57b724ecdd911154302b84d5cfba05f8a05
+++ b/7e5ad57b724ecdd911154302b84d5cfba05f8a05
@@ -6,3 +6,4 @@ Submitted-at: Fri, 01 Apr 2016 15:17:54 +0000
 Reviewed-on: https://review.openstack.org/300547
 Project: openstack/tripleo-quickstart
 Branch: refs/heads/master
+What-to-add: what we added
```

## 在commits之外的对象上的存储

Notes 同样可以作用于其他对象之上， 例如：标签。

```
➜  git-notes-test git:(master) git tag -a -m "test commit"
➜  git-notes-test git:(master) git --no-pager tag
v1.0
➜  git-notes-test git:(master) git show-ref --tags
769baa18c813add6d99d85bbb7e0ab7b7c19e491 refs/tags/v1.0
➜  git-notes-test git:(master) git notes add 769baa18c813add6d99d85bbb7e0ab7b7c19e491
➜  git-notes-test git:(master) git --no-pager notes show 769baa18c813add6d99d85bbb7e0ab7b7c19e49
Add-notes-on-tag: added
```

随后可以执行ls-tree， 查看存储情况：

```shell
➜  git-notes-test git:(master) git ls-tree refs/notes/commits
100644 blob 1daee75c5d07890f8a86869aa4b2553f60554b31    769baa18c813add6d99d85bbb7e0ab7b7c19e491
100644 blob 0c92279bea1cfd75646ca487bb22bb7d5588251e    7e5ad57b724ecdd911154302b84d5cfba05f8a05
```

git 之所以可以这样做是因为SHA的不可变性，我们需要使用"git notes show" 去查看标签
的notes信息，如果使用git show， 则不会显示，因为git show只会展示commit的notes，
而不会展示标签的notes。

## notes存储上的哈希化路径

当refs/notes/commits下存储的文件过多的时候，将对查询性能造成影响，所以notes存储
上也支持哈希化的路径，提升查询效率。

## 其他的子命令

### list

list 子命令可以查询某个ref上的notes信息，格式为<note object>， 如果没有指定ref则
列出所有notes信息，格式为<note object> <annotated object>。
```shell
➜  git-notes-test git:(master) git notes list master
0c92279bea1cfd75646ca487bb22bb7d5588251e
➜  git-notes-test git:(master) git notes list v1.0
1daee75c5d07890f8a86869aa4b2553f60554b31
➜  git-notes-test git:(master) git notes list
1daee75c5d07890f8a86869aa4b2553f60554b31 769baa18c813add6d99d85bbb7e0ab7b7c19e491
0c92279bea1cfd75646ca487bb22bb7d5588251e 7e5ad57b724ecdd911154302b84d5cfba05f8a05
```


