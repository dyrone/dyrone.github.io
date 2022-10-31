---
title: "Git Multi Points Representation"
date: 2022-06-12T15:56:16+08:00
tags:
  - "git"
author: "Dyrone Teng"
draft: false
---

If we read the ['git-rev-list.txt'](https://github.com/git/git/blob/8168d5e9c23ed44ae3d604f392320d66556453c9/Documentation/git-rev-list.txt) in git project on github or in `git rev-list --help` output. You can find there are some the related description about multi points in git.

The multiple points notation in `git rev-list` intents to select a range of commits on the repository commit graph.

## Two Points Notation: ".."

> 
> A special notation `<commit1>..<commit2>` can be used as a short-hand for `^'<commit1>' <commit2>`. For example, either of the following may be used interchangeably:
> 
>    $ git rev-list origin..HEAD
> 
>    $ git rev-list HEAD ^origin


### Without Merge commit

The notation "<commit1>..<commit2>" means we want all the commits from commit2 but expect to exclude all the commits from commit1. For example, we have a commit-graph in the following way:

```shell
* 388c28e (HEAD -> master) master-commit-C
| * 0f0623d (topic-1) topic-1-commit-X
|/  
* 0880fe7 master-commit-B
* 9161dc7 master-commit-A
```

If we execute `git rev-list master..topic-1`, the print out result will be:

```shell
$ git rev-list master..topic-1
0f0623d237999ce6fb661f62ab6e6ce0e28abc17
```

Oppositely, if we execute `git rev-list topic-1..master`, the print out result will be:

```bash
$ git rev-list topic-1..master
388c28e27bbf91da99fc04c44da7badc11fd3976
```

### With Merge commit

Now, let's make the scenario a little more complicated. We create a new branch named `topic-2` and make some new commits to it and then we will actually create a new commit on master too. Then we merge `topic-1` into `master`, the commit graph now will look like this:

```shell
*   06e3ed6 (master) Merge branch 'topic-1'
|\  
| * 0f0623d (HEAD -> topic-1) topic-1-commit-X
* | ac7af40 master-commit-D
| | * 154fbae (topic-2) topic-2-commit-Y
| | * 28c5a85 topic-2-commit-X
| |/  
|/|   
* | 388c28e master-commit-C
|/  
* 0880fe7 master-commit-B
* 9161dc7 master-commit-A
```

Now let's find out the results of execting `git rev-list` on these three branches by using the two points notation:

```shell
$ git rev-list topic-1..master
06e3ed6efc9f2d5d1aa025e1bccb4b4dd13fce7e
ac7af405fee6bb53896790e9bc8e2e4006adaac8
388c28e27bbf91da99fc04c44da7badc11fd3976
```

First, commits on `master` are : 9161dc7 0880fe7 388c28e ac7af40 0f0623d 06e3ed6 
Secondly, commits on `topic-1` are : 9161dc7 0880fe7 0f0623d

So, the result of "want all commits on master but not on topic-1" is: 06e3ed6 ,ac7af40 and 388c28e.

```shell
$ git rev-list master..topic-1

```

The `master` contains all the commits which are on `topic-1`. So the second command will return nothing.

### Diverged (No Merge Base)

Now let's see a case where the two commits are diverged from each other.

We can use `git-hash-object` `git write-tree` `git commit-tree` to create a new commit without any parents commits, and point to the new commit by creating a new branch which names as `diverge`,then let's look at the commit graph now:

```shell
$ git log --all --graph --oneline --topo-order
* 9def6a4 (diverge) Diverged commit X
*   06e3ed6 (HEAD -> master) Merge branch 'topic-1'
|\  
| * 0f0623d (topic-1) topic-1-commit-X
* | ac7af40 master-commit-D
| | * 154fbae (topic-2) topic-2-commit-Y
| | * 28c5a85 topic-2-commit-X
| |/  
|/|   
* | 388c28e master-commit-C
|/  
* 0880fe7 master-commit-B
* 9161dc7 master-commit-A
```

Actually the commit graph is not so clear on `diverge`, there are no explicit mark or tip on diverged commit and only exists a "TAB" on the merge commit, so I think this brings a little ambugious meanings, so we can change the command a little bit like:

```shell
$ git log --all --graph --pretty="%h %s%n"
* 9def6a4 Diverged commit X
  
*   06e3ed6 Merge branch 'topic-1'
|\  
| | 
| * 0f0623d topic-1-commit-X
| | 
* | ac7af40 master-commit-D
| | 
| | * 154fbae topic-2-commit-Y
| | | 
| | * 28c5a85 topic-2-commit-X
| |/  
|/|   
| |   
* | 388c28e master-commit-C
|/  
|   
* 0880fe7 master-commit-B
| 
* 9161dc7 master-commit-A
```
Now we use `--pretty="%h %s%n"` to add a LR on each line, we can find out that there are no connected line between `9def6a4` and `06e3ed6`, that's what the diverged commit looks like on commit graph output.

We can execute `git merge-base` to check the merge base of two commits, and we can find out that there are no outputs on the following command:

```shell
$ git merge-base master diverge
# nothing print
```

This also means that the two commits are diverged, it's another representation of no merge bases in git.

Futhermore, we can go on executing `git rev-list` on the two diverged commits to see the result:

```shell
$ git rev-list diverge..master
06e3ed6efc9f2d5d1aa025e1bccb4b4dd13fce7e
ac7af405fee6bb53896790e9bc8e2e4006adaac8
388c28e27bbf91da99fc04c44da7badc11fd3976
0f0623d237999ce6fb661f62ab6e6ce0e28abc17
0880fe76f27cb85258a12f7952233f67cb9b0381
9161dc74e09a248d281cca962cdb42f87bfd0ffb
```

```shell
$ git rev-list master..diverge
9def6a4ffdc6cbacb13c3e75c21178288d98f861
```

The result of `git rev-list` on the two diverge commits is the whole commits on the other side of the commit, the result is in line with our expectations.

## Three Points Notation: "..."

The three points notation is used to represent a range of commits too, in `git-rev-list.txt` it is described as:

> Another special notation is "<commit1>...<commit2>" which is useful for merges. The resulting set of commits is the symmetric difference between the two operands. The following two commands are equivalent:
>
>        $ git rev-list A B --not $(git merge-base --all A B)
>        $ git rev-list A...B
>
> `rev-list` is a very essential Git command, since it provides the ability to build and traverse commit ancestry graphs. For this reason, it has a lot of different options that enables it to be used by commands as different as git bisect and git repack.




### Merge Base

A merge-base is the common ancestors of two commits, two commits may have more than one common ancestors, it's called as a criss-cross merge.

Some of the content below is taken from the documentation `git-merge-base.txt`. First example, given commit A and B, the merge base will be `1`:

```shell
                    o---o---o---B
                   /
           ---o---1---o---o---o---A
```

Second example, first compute M as the virtual merge commit of B and C, then the merge-base of A and M will be `1`. Commit 2 is also a common ancestor between A and M, but 1 is a better common ancestor, because 2 is an ancestor of 1. Hence, 2 is not a merge base.

```shell
                  o---o---o---o---C
                 /
                /   o---o---o---B
               /   /
           ---2---1---o---o---o---A

                  o---o---o---o---o
                 /                 \
                /   o---o---o---o---M
               /   /
           ---2---1---o---o---o---A
```


If we execute `git merge-base --octopus A B C`, the result will be `2`, because `2` is the best common ancestor of all commits.About more information about octopus merge, I found an article[https://www.freblogg.com/git-octopus-merge] from google, maybe helpful.

Third example:

Let's back to the merge-base, a more complex example is `criss-cross merge`, here can be more than one best common ancestor for two commits:

```shell
           ---1---o---A
               \ /
                X
               / \
           ---2---o---o---B
```
Both 1 and 2 are merge-bases of A and B. Neither one is better than the other (both are best merge bases).When the --all option is not given, it is unspecified which best one is output.

```shell
$ git log  --graph --pretty="%h %s%n" criss-cross-1 criss-cross-2
* 2375853 criss-cross-commit-Y
| 
*   1594ff3 Merge branch 'criss-cross-1' into criss-cross-2
|\  
| | 
| | * f6c42b8 criss-cross-commit-X
| | | 
| | * 77fb920 Merge commit '3e872dd' into criss-cross-1
| |/| 
| |/  
|/|   
| |   
* | 3e872dd criss-cross-commit-B
| | 
| * e400d1e criss-cross-commit-A
|/  
|   
* 9def6a4 Diverged commit X
```

We made a scenario about `criss-cross` like above. both `2375853` and `f6c42b8` has two merge-bases. Then we should add `--all` options to get the two best merge-bases:

```shell
$ git merge-base --all criss-cross-1 criss-cross-2
3e872dd196652b779ddeba757add1273c45cfe53
e400d1e4cedfa0e0a64e533a5067cd8d7863f323
```

### three points notation

If you take a look at the relate well-written description in 'git-rev-list.txt', you can see that the three points notation is used to represent a range of commits too, they remove the commits by merge-base and the commits under the merge-base, then give us the left commits which is meaningful for merges:

```shell
Another special notation is "<commit1>...<commit2>" which is useful for merges. The resulting set of commits is the symmetric difference between the two operands. The following two commands are equivalent:

	$ git rev-list A B --not $(git merge-base --all A B)
    $ git rev-list A...B
```

The whole graph now looks like this:

```shell
$git log  --graph --pretty="%h %s%n" --all
* 2375853 criss-cross-commit-Y
| 
*   1594ff3 Merge branch 'criss-cross-1' into criss-cross-2
|\  
| | 
| | * f6c42b8 criss-cross-commit-X
| | | 
| | * 77fb920 Merge commit '3e872dd' into criss-cross-1
| |/| 
| |/  
|/|   
| |   
* | 3e872dd criss-cross-commit-B
| | 
| * e400d1e criss-cross-commit-A
|/  
|   
* 9def6a4 Diverged commit X
  
*   06e3ed6 Merge branch 'topic-1'
|\  
| | 
| * 0f0623d topic-1-commit-X
| | 
* | ac7af40 master-commit-D
| | 
| | * 154fbae topic-2-commit-Y
| | | 
| | * 28c5a85 topic-2-commit-X
| |/  
|/|   
| |   
* | 388c28e master-commit-C
|/  
|   
* 0880fe7 master-commit-B
| 
* 9161dc7 master-commit-A
```

We choose `388c28e` and `0f0623d` as commit range ,they have one best merge-base as their parent, the result is:

```shell
$ git rev-list 388c28e...0f0623d
388c28e27bbf91da99fc04c44da7badc11fd3976
0f0623d237999ce6fb661f62ab6e6ce0e28abc17
```

Another scenario is for two diverged branches, they have no merge-base, so three points notation will return all the commits on the two branches:

```shell
$git rev-list 9def6a4...06e3ed6
9def6a4ffdc6cbacb13c3e75c21178288d98f861
06e3ed6efc9f2d5d1aa025e1bccb4b4dd13fce7e
ac7af405fee6bb53896790e9bc8e2e4006adaac8
388c28e27bbf91da99fc04c44da7badc11fd3976
0f0623d237999ce6fb661f62ab6e6ce0e28abc17
0880fe76f27cb85258a12f7952233f67cb9b0381
9161dc74e09a248d281cca962cdb42f87bfd0ffb
```

Last scenario is for two branches and they are on criss-cross merge, which means they have multi merge-bases.

```shell
$git rev-list criss-cross-1...criss-cross-2
2375853c6b478aefed0316182e7dd4f235f3a674
f6c42b8760affa7c3796554d1dd59cd5ece44fb3
77fb920c1559fa7d6564ee6b42dc4a12fa5d199b
1594ff34beaba8081885f51659233bb7a5840fb
```


## Multi Points In `git log`

The whole graph has been no changes. After the last paragraph, we made `master` and topic branches to test the multi-points notation firstly, then we use diverged branch and criss-cross branches to test the multi-merge-base. But how will `git log` will perform with multi-points?


### Without Merge Base

Thirdly, we choose `9def6a4` and `06e3ed6` as the commit range, they are diverged for each other, the result is still consistent with `git rev-list`

```shell
$ git log --oneline 9def6a4..06e3ed6
06e3ed6 (master) Merge branch 'topic-1'
ac7af40 master-commit-D
388c28e master-commit-C
0f0623d (topic-1) topic-1-commit-X
0880fe7 master-commit-B
9161dc7 master-commit-A
```

```shell
$git log --oneline 06e3ed6..9def6a4
9def6a4 (diverge) Diverged commit X
```

### With Merge Base
Firstly, we choose `388c28e` and `0f0623d` as the commit range, and the merge base of them is "0880fe7", the performance of `git log` in two-points notation are as the consistent meaning with `git rev-list`.
```
$ git log 388c28e..0f0623d --oneline
0f0623d (topic-1) topic-1-commit-X
$ git log 0f0623d..388c28e --oneline
388c28e master-commit-C
```

Secondly, we choose `06e3ed6` and `0f0623d` as the commit range, the result is still consistent with `git rev-list`.

```shell
$ git log --oneline 0f0623d..06e3ed6
06e3ed6 (master) Merge branch 'topic-1'
ac7af40 master-commit-D
388c28e master-commit-C

$ git log --oneline 06e3ed6..0f0623d
# nothing output
```

### With Multiple Merge Base

Next, we use criss-cross branches to test the multi-merge-base in `git log`, from the output result we can get the meaning is still consistent with `git rev-list`.

```shell
[tenglong.tl@code-infra-dev-cbj.ea134 /home/tenglong.tl/test/dyrone_graph]
$ git log --oneline criss-cross-1..criss-cross-2
2375853 (HEAD -> criss-cross-2) criss-cross-commit-Y
1594ff3 Merge branch 'criss-cross-1' into criss-cross-2

[tenglong.tl@code-infra-dev-cbj.ea134 /home/tenglong.tl/test/dyrone_graph]
$ git log --oneline criss-cross-2..criss-cross-1
f6c42b8 (criss-cross-1) criss-cross-commit-X
77fb920 Merge commit '3e872dd' into criss-cross-1
```

## Multi-Points In `git diff`

We already know that `git log` will perform the same effects with multi-points, but how will `git diff` perform with multi-points?

Actually, `git diff` will perform the totally different results as before: here are some partial documentation content from 'git-diff.txt'

>    git diff [<options>] <commit> <commit> [--] [<path>...]
>        This is to view the changes between two arbitrary <commit>.
>
>    git diff [<options>] <commit>..<commit> [--] [<path>...]
>        This is synonymous to the previous form. If <commit> on one side is omitted, it will have the same effect as using HEAD instead.
>
>    git diff [<options>] <commit>...<commit> [--] [<path>...]
>       This form is to view the changes on the branch containing and up to the second <commit>, starting at a common ancestor of both <commit>. "git diff A...B" is equivalent to "git diff $(git-merge-base A B) B". You can omit any one of <commit>, which has the same effect as using HEAD instead.


In conclusion, the multi points notation in `git diff` represents:

* `commit_A commit_B` and `commit_A..commit_B` are identical, they means just the changes between the two commits themself (work tree, files).

* `commit_A...commit_B` means only want to show the diff of the latter side commit, it performs as a similar way with `commit_A..commitB` in `git log` and `git rev-list`.

For example,`388c28e` and `0f0623d` they have the same merge-base, after we use `git diff` to view the changes between them, we can see the difference between `git log` and `git diff` in multi-points notation.

Changes in `388c28e`:

```shell
$ git show 388c28e --text
commit 388c28e27bbf91da99fc04c44da7badc11fd3976
Author: Teng Long <dyroneteng@gmail.com>
Date:   Tue Jun 14 14:47:18 2022 +0800

    master-commit-C
    
    Signed-off-by: Teng Long <dyroneteng@gmail.com>

diff --git a/5.txt b/5.txt
new file mode 100644
index 0000000..d961fa4
--- /dev/null
+++ b/5.txt
@@ -0,0 +1 @@
+232323
```
Changes in `0f0623d`:

``` shell
$ git show 0f0623d --text
commit 0f0623d237999ce6fb661f62ab6e6ce0e28abc17 (topic-1)
Author: Teng Long <dyroneteng@gmail.com>
Date:   Tue Jun 14 14:46:25 2022 +0800

    topic-1-commit-X
    
    Signed-off-by: Teng Long <dyroneteng@gmail.com>

diff --git a/3.txt b/3.txt
index 55bd0ac..80e9add 100644
--- a/3.txt
+++ b/3.txt
@@ -1 +1,2 @@
 333
+4343
```

Two multi points with `388c28e` and `0f0623d` when executing `git rev-list`:

```shell
$ git rev-list 388c28e..0f0623d
0f0623d237999ce6fb661f62ab6e6ce0e28abc17

$ git diff 388c28e..0f0623d
diff --git a/3.txt b/3.txt
index 55bd0ac..80e9add 100644
--- a/3.txt
+++ b/3.txt
@@ -1 +1,2 @@
 333
+4343
diff --git a/5.txt b/5.txt
deleted file mode 100644
index d961fa4..0000000
--- a/5.txt
+++ /dev/null
@@ -1 +0,0 @@
-232323
```

Three multi points with `388c28e` and `0f0623d` when executing `git rev-list`:

```shell
$ git diff 388c28e...0f0623d
diff --git a/3.txt b/3.txt
index 55bd0ac..80e9add 100644
--- a/3.txt
+++ b/3.txt
@@ -1 +1,2 @@
 333
+4343
diff --git a/5.txt b/5.txt
deleted file mode 100644
index d961fa4..0000000
--- a/5.txt
+++ /dev/null
@@ -1 +0,0 @@
-232323
```

## Conclusion

We introduced and explained the use of `multi points notation` in Git, which stands for consistency in `git rev-list` and `git log`. `git diff`, however, is inconsistent in meaning, and there may be some ambiguity in the global expression of git commits range meanings, which I suspect is intended to ensure backward compatibility with earlier diff implementations.

Thank you for reading this article, if you get some places you want to improve or I'm wrong, please feel free to contact me.
