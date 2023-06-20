---
title: "Git 2.41 版本介绍"
date: 2023-06-20T14:46:46+08:00
draft: false
tags:
    - git
    - git-release
---
<br />
* Git 作为一个开源项目刚刚发布了 [2.41 版本](https://lore.kernel.org/git/xmqqleh3a3wm.fsf@gitster.g/ "2.41 版本")，其中共有 95 位开发者贡献了新的特性以及已有缺陷的修复，而他们中的 29 位是新的贡献者。我们上次聊到 Git 的最新发布动态是在[Git 2.40 版本](https://github.blog/2023-03-13-highlights-from-git-2-40/ "Git 2.40 版本")。

* 这篇博文是 Github 对新引入的一些最有新的特性和变化的介绍，本文的原作者是 [Taylor Blau](https://github.com/ttaylorr "Taylor Blau"), 本文的中文译者是 [滕龙（花名：澳明）](https://github.com/dyrone "滕龙（花名：澳明）")，该博文已经由原作者同意由本人进行翻译以及在中国进行传播，让更多的开发者了解和追踪 Git 的演进。

* 本文[托管在 github 上的仓库](https://github.com/dyrone/dyrone.github.io/blob/master/content/posts/highlights-Git-2.41.md)中，如果有发现文字或翻译错误， 欢迎通过 Pull Request 的方式来提交修改。

<br />
## 中文术语表
<br />

可以[从 Git 中文本地化文件](https://github.com/git/git/blob/master/po/zh_CN.po)中查看对应术语，如果缺少某个术语或者建议添加，可以随时提供建议。

<br />
## 格式说明

* 中文（Git中的术语）。
* 如 commit, blob，tree，branch，tag 等基础词汇不进行翻译。

<br />
## 处理“不可达对象”上的优化
<br />

每个 Git 仓库的本质都由“一组对象”构成， 如果你还不了解为什么如此设计，你可以通过
[此篇文章](https://github.blog/2020-12-17-commits-are-snapshots-not-diffs/ "此篇
文章")了解 Git 对象模型的复杂性。 一般来说，你的 Git 仓库正是由这些对象如添砖加
瓦般罗列而成。blob 表示单个文件的内容，而 tree 将许多blob（以及其他tree）组合在一起，表
示一个目录。commit 通过指向一个特定的 tree 将所有关联的对象联系在一起， 这个特定
的tree 其实就代表了生成 commit 时对应仓库的状态。


Git对象存在两种状态: “可达（reachable）” 或 “不可达（unreachable）”。假如，我们从存储库中的某个分支或标签开始，并沿着提交的历史从新到老的进行遍历（walk），对于沿途我们经过的对象们，认为他们是可达的。遍历（walk）仅仅是为了，寻找一个对象，并且进而寻找到这个对象关联的其他对象，一个 commit 对象对外可能有0个或多个父提交（parents），对内可能关联很多 tree 和 blob 对象。

可能存在这样一些对象，他们在任何分支或标签或者其他引用上经历 walk 后均无法找到，这些对象将被认为是不可达的对象。 为了压缩存储库的大小，git 每隔一段时间，就会决定删除一些不可达对象， 比如你可能看到过类似的提示：

```shell
Auto packing the repository in background for optimum performance.
See "git help gc" for manual housekeeping.
```

或者我们可以执行运行 `git gc`, 自主决定是否要立即清理这些不可达的对象。

但是，Git 并不一定在第一次运行 git gc 时就会清理不可达对象。因为从一个活跃的仓库中删除他们是存在一定风险的[1]，git 此时会选择延迟执行。 另外，如果通过一个给定的参数（`--prune`）来提供一个给定的截止时间点时，只有足够老的不可达对象才会被删除。即，如果执行 `git gc --prune=2.week.ago`:

* 所有可达的对象都会收集，并打到一个包（pack）中。
* 2周内写入的不可达对象，单独存储在其他位置（作为松散对象：loose object 的存储在
  仓库中）。
* 剩余的不可达对象将会被忽略。

在 Git 2.37 之前，Git通过将不可达对象存储为松散对象文件，并使用文件的 `mtime`作为对象最后写入时间的评判依据，来跟踪不可达对象的最后写入时间。然而，将不可访问的对象作为松散存储直到它们老化可能会产生许多负面的副作用。如果有许多不可访问的对象，它们可能会导致存储库的大小膨胀，耗尽系统上可用的inode。

Git 2.37 引入了一种新的包(pack)，叫做 “废弃包（cruft pack）”，它将不可达的对象全部存储在一个单独的 pack 中, 同时生成一个与之对应的辅助的文件：
[*.mtime](https://git-scm.com/docs/gitformat-pack/2.41.0/#_pack_mtimes_files_have_the_format)。mtime 文件用户帮助追踪 pack 中不可达对象的年龄，通过这种方式，可以防止 inode 耗尽并且允许这些不可达对象以 [增量对象（delta）](https://en.wikipedia.org/wiki/Delta_encoding)的方式存储在 pack 中，降低仓库的大小。

<img src="/images/cruft.png" alt= “” width="500">

上图体现了一个废弃包，以及预期对应的 *.idx 文件以及 *.mtimes 文件. 将不可达对象在包中集中存储可以让 Git 更高效的访问这些不可达的数据，而不必担心给系统资源带来的压力。

在 Git 2.41 中， 生成废弃包的特性已经作为 Git 默认的行为，即执行 `git gc` 就会为你的仓库生成一个废弃包（如果有满足清理条件的不可达对象）。如果希望学习更多有关废弃包的内容，可以查看此前的文章：[扩展 Git 垃圾回收机制](https://github.blog/2022-09-13-scaling-gits-garbage-collection/#object-deletion-raciness)。

<br />
## 反向索引已经作为 Git 默认行为生效
<br />

从 2.41 版本开始，你可能会注意到，在你的仓库中可能会产生一个新的文件， 位于
`.git/objects/pack` 下的 `*.rev` 文件。

这个新的文件中保存的信息与 packfile 索引文件中保存的信息是类似的。 如果你在包目录中发现了文件后缀为 `*.idx` 文件的话，这些正是包文件对应的索引文件。

包索引文件与包文件中记录的对象是一一映射的，映射时涉及两种不同的顺序。第一种是名称序（name order），就是在 packfile 索引文件中，根据对象ID（OID）的名称排序后的顺序。另外一种是压缩序（pack order），是在 packfile 中存储的对象的顺序。Git通常需要频繁的在这两种顺序之间进行转换， 例如。如果你希望得到一个特定对象的信息，可能通过执行 `git cat-file -p` 完成。 Git 会查找所有的 `*.idx` 文件，并通过[二分查找](https://en.wikipedia.org/wiki/Binary_search_algorithm "二分查找")来检索给定对象在包文件的名称序（name order）中的位置。如果二分查找命中了，那么进而通过 `*.idx` 文件可以快速定位位于包中的对象，进而转储对象的内容。

但是如果是反过来呢？ Git 如何能够通过一个“包文件的位置 + 包文件本身” 得知 “这个对象是什么？”。为了达成这个目的，Git 实现了反向索引（reverse index）,从而可以将压缩序（pack order） 映射到 名称序 (name order)，顾名思义，这个数据结构是上面提到的 packfile 索引的倒置。

<img src="/images/rev.png" alt= “” width="500">

上图显示了反向索引的查询过程。 为了发现黄色对象的字典序（索引）位置，Git 读取反向索引中的相应条目，其值为字典序位置。 在这个例子中，假设黄色对象是包中的第 4 个对象，因此 Git 读取 `.rev` 文件中的第 4 个条目，其值为 1。通过读取 `*.idx` 文件，我们就可以获取到黄色的对象。

在以前的 Git 版本中，反向索引是通过在列表中存储“一对数据”（一个对象保存一对数据，分为为对象的名称序以及压缩序） 来完成[即时构建](https://github.com/git/git/blob/v2.41.0/pack-revindex.c#L27-L178 "即时构建")。这个策略的副作用较多，最显著的是在时间和内存消耗上。

在 Git 2.31 版本中，引入了磁盘持久化的反向索引[2]。反向索引的内容其实并没有变化，但是文件只会生成一次，其结果作为 `*.rev` 存储在磁盘下[3]. 预计算并存储反向索引可以显著提供大型存储库的性能，特别是对于推送或者确定对象的磁盘大小等场景。

在 Git 2.41 中，Git 现在会默认生成反向索引。 这意味着下次升级后在存储库上运行 `git gc` 时，您应该会注意到可能你仓库性能在某些场景下变得更快了。 在测试新的默认行为时，我们在 `torvalds/linux` 中推送最后 30 次提交时，`git push` 作为 Git 中一种 CPU 密集型作业，其[速度提高了 1.49倍](https://github.com/git/git/commit/a8dd7e05b1c033917b900ea3d930e79eea3ff9a4)。而对于一些琐碎的操作星座，例如使用 `git cat-file --batch='%(objectsize:disk)'` 计算单个对象的大小时，速度提高了近 77 倍。

要了解有关磁盘反向索引的更多信息，您可以查看之前的另一篇文章“[Scaling monorepo maintenance](https://github.blog/2021-04-29-scaling-monorepo-maintenance/)”，其中[有一章节](https://github.blog/2021-04-29-scaling-monorepo-maintenance/#reverse-indexes)是关于反向索引的相关介绍。

[[源码](https://github.com/git/git/compare/2807bd2c10606e590886543afe4e4f208dddd489...9f7f10a282d8adeb9da0990aa0eb2adf93a47ca7)]

---

您之前可能了解 [Git credential helper](https://git-scm.com/docs/gitcredentials#_custom_helpers/2.41.0) 机制，该机制用于在访问存储库时提供所需的凭据。凭据助手实现了[凭据助手协议](https://git-scm.com/docs/git-credential#IOFMT/2.41.0)和特定凭据存储（如Keychain.app 或 libsecret）之间的转换的支持。 这允许 Git 通过通用协议与不同的凭证助手实现透明地通信，从而允许用户基于更倾向使用的机制来存储对应凭证。传统上，Git 支持基于密码的身份验证。 对于希望使用 [OAuth](https://oauth.net/) 进行身份验证的服务，凭据助手通常采用变通方法，例如通过 [basic authorization](https://en.wikipedia.org/wiki/Basic_access_authentication) 传递
bearer 令牌，而不是直接使用 [bearer authorization](https://datatracker.ietf.org/doc/html/rfc6750) 进行身份验证。

凭据助手没有一种机制来理解生成凭据所需的其他信息，例如 [OAuth Scopes](https://oauth.net/2/scope/)，这些信息通常通过 [WWW-Authenticate](https://datatracker.ietf.org/doc/html/rfc7235#autoid-11) 标头传递。

在 Git 2.41 中，凭证助手协议被扩展以支持在凭证助手和它们试图通过身份验证的服务之间传递 `WWW-Authenticate` 标头。 这可用于允许认证服务方通过让用户确定其请求的 Scope，来支持对 Git 存储库资源进行更细粒度的访问。

[[源码](https://github.com/git/git/compare/af5388d2ddb0bc7c22fbe698078f4ca07879d954...5f2117b24f568ecc789c677748d70ccd538b16ba)]

---

如果您查看过 GitHub 上存储库的[分支页面](https://github.com/git/git/branches)，您可能已经注意到页面上存在一个指示器，用于显示相对于存储库默认分支的“领先或者落后的”提交的数量。 如果您没有注意到，没关系：让我们快速了解它。 当一个分支已经提交而另一方没有提交，它就“领先于”另一个分支。 提前量取决于唯一此类提交的数量。同样，当一个分支缺少另一方独有的提交时，它就“落后于”另一个分支。

以前版本的 Git 允许通过运行两个可达性查询来进行这种比较：`git rev-list --count
main..my-feature`（计算 my-feature 独有的提交数）和 `git rev-list --count
my-feature..main`（反过来）。 这种方法可以奏效，但涉及两个单独的查询还是会带来一
些不便。 如果将许多分支与一个公共基础进行比较（如上面的Github的 `/branches` 页
面），Git 最终可能会多次遍历重复的提交。

在 Git 2.41 中，您现在可以通过新的 `for-each-ref` 格式化的参数，
`%(ahead-behind:<base>)` 直接请求此信息。 Git 将仅使用一次遍历来计算其输出，这使
其比以前的版本更加高效。

例如，假设我想列出我未合并的主题分支以及它们相对于上游主线的领先和落后程度。 以
前，我不得不写这样的东西：

```SHELL
$ git for-each-ref --format='%(refname:short)' --no-merged=origin/HEAD \
  refs/heads/tb |
  while read ref
  do
    ahead="$(git rev-list --count origin/HEAD..$ref)"
    behind="$(git rev-list --count $ref..origin/HEAD)"
    printf "%s %d %d\n" "$ref" "$ahead" "$behind"
  done | column -t
tb/cruft-extra-tips 2 96
tb/for-each-ref--exclude 16 96
tb/roaring-bitmaps 47 3
```

产生结果需要超过 500 毫秒。 在上面，我首先要求 `git for-each-ref` 列出我所有未合
并的分支。 然后遍历结果，手动计算它们的前后值，最后格式化输出。

在 Git 2.41 中，可以使用更简单的调用来完成相同的操作：

```shell
$ git for-each-ref --no-merged=origin/HEAD \
  --format='%(refname:short) %(ahead-behind:origin/HEAD)' \
  refs/heads/tb/ | column -t
tb/cruft-extra-tips 2 96
tb/for-each-ref--exclude 16 96
tb/roaring-bitmaps 47 3
[...]
```

这会产生相同的输出，但编写更少的脚本！并且它只执行一次 walk[4] 而不是多次
walk。 与早期版本相比，上述版本仅需 28 毫秒即可产生输出，性能提升超过 17 倍。

[[源码](https://github.com/git/git/compare/ae73b2c8f1da39c39335ee76a0f95857712c22a7...cbfe360b140fe92d9c4a763bf630c3b8ba431522)]

---

当使用 `git fetch` 从远程获取更新时，Git 的输出将包含有关从远程更新了哪些引用的相关信息，例如：

```shell
+ 4aaf690730..8cebd90810 my-feature -> origin/my-feature (forced update)
```

虽然人类阅读起来很方便，但机器解析起来要困难得多。 Git 将简短化包引用名称，而且不会打印正在更新的引用的完整前后值，并对其输出进行分栏，所有这些都使得编写脚本变得更加困难。

在 Git 2.41 中，`git fetch` 现在可以采用新的 `--porcelain` 选项，该选项将其输出
更改为更容易编写脚本的形式。 通常，`--porcelain` 输出格式如下所示：

```shell
<flag> <old-object-id> <new-object-id> <local-reference>
```

当使用 `--porcelain` 调用时，`git fetch` 牺牲了默认的人类可读的便利性，而是发出
更容易让机器解析的数据格式。 四个字段，每个字段由一个空格字符分隔，从而可以更容
易地围绕 `git fetch` 的输出编写脚本。

[[源码](https://github.com/git/git/compare/955abf5f72617f6044fdadeeaee7e9b78735340a...d6606e02aaff963f51fe9cbda048613ff0cd5870)，[源码](https://github.com/git/git/compare/ef06676c3646271e505c255372b667568faf88f8...dd781e3856bccd3793122f7f4e604e5a89ae517d)]

---

说到 `git fetch`，Git 2.41 还有一个可以提升其性能的新特性：`fetch.hideRefs`。在开始介绍之前，回顾一下我们之前对 `git rev-list` 的 `--exclude-hidden` 选项的[介绍
  ](https://github.com/git/git/compare/173fc54b005c92dc0da0fe5e71034128eddbacc8...bcec6780b2ec77ea5f846d5448771f97110041e1)会提供一些帮助。 如果你是刚开始了解他，别担心：这个选项[最初](https://github.com/git/git/compare/173fc54b005c92dc0da0fe5e71034128eddbacc8...bcec6780b2ec77ea5f846d5448771f97110041e1)是为了提高 Git “连接检查（connectivity check）” 的性能而引入的，这个过程检查一个推送包含的内容是否与仓库已经“[完全连接](https://en.wikipedia.org/wiki/Connectivity_(graph_theory))”，它不能引用远程没有的对象，或者推送本身包含的对象。
  
Git 2.39 支持通过让远端忽略向客户端公告（advertise）部分的引用，从而加快连接检查的效率：即[隐藏引用特性](https://git-scm.com/docs/git-config/2.41.0/#Documentation/git-config.txt-transferhideRefs)。 由于这些引用未公告给推送客户端，因此相关对象中的任何一个都不太可能终止连接检查的过程，因此跟踪它们通常只需要额外的记录而已。

Git 2.41 为客户端的 `git fetch` 引入了类似的选项。 通过适当地设置`fetch.hideRefs`，您可以从客户端执行的连接检查中排除本地存储库中的部分引用，以确保服务器没有向您发送不完整的对象们。当检查一个 fetch 的连接性时，搜索过程将终止于完成全部 远端（remote） 的分支和标签的检查之后，而不仅仅是你当前指定的 remote。 如果配置了大量 remote，这可能会花费大量时间，尤其是在资源受限的系统上。

在 Git 2.41 中，您可以缩小连接检查的范围，只关注您当前正获取数据的远端。 （请注意，以 `!` 开头的 `transfer.hideRefs` 值被解释为取消隐藏这些引用，并以相反的顺序生效。）如果您从名为 `$remote` 的远程获取，您可以这样做：

```shell
$ git -c fetch.hideRefs=refs -c fetch.hideRefs=!refs/remotes/$remote \
fetch $remote
```

上面的代码首先隐藏了连接检查中的所有引用 (`fetch.hideRefs=refs`)，然后取消隐藏与该特定远端 (`fetch.hideRefs=!refs/remotes/$remote`) 相关的引用。 在具有多远端下的跟踪引用的代码库，完成无其他参数的 fetch 操作从 20 分钟降低到大约 30 秒。

[[源码](https://github.com/git/git/compare/92c56da09683fa3331668adec073b6769da8f0b7...c6ce27ab08d30dd9d626d7a56cb928bc5792eb27)]

---

如果您曾寻找存储库中是否有损坏的情况，那么想必你应该知道 `[git fsck](https://git-scm.com/docs/git-fsck/2.41.0)`。 此工具用于检查存储库中的对象是否完好无损且已连接。 换句话说，如果命令执行成功，那么你的存储库没有任何损坏或丢失的对象。`git fsck` 还可以检查存储库损坏的其他方式，如恶意的 `.gitattributes` 或 `.gitmodules` 文件，以及格式错误的对象（如 tree 乱序，或提交中不包含作者）。 它执行的全套检查范围可以[在 fsck 配置](https://git-scm.com/docs/git-fsck/2.41.0#_fsck_messages)中查阅。

在 Git 2.41 中，`git fsck` 学习了如何检查可达性位图（bitmap）和磁盘反向索引（rev）中的损坏。 通过检查并警告不正确的尾随校验和，从而判断前面的数据是否已被破坏。 在检查磁盘上的反向索引时，`git fsck` 还将检查 `*.rev` 文件是否包含正确的值。

了解更多 `fsck` 中新的检查项的实现，可以参阅[文档](https://git-scm.com/docs/git-fsck/2.41.0#_fsck_messages)。

[[源码](https://github.com/git/git/compare/849c8b3dbf8e850020951e81a42df4dc0b1e5b5d...5a6072f631dcf4d9f65e83b08d14c82e2af45dd8)，[源码](https://github.com/git/git/compare/29b8a3f49d3c521431650b670fa2fbcd9ad571b3...cf9cd8b55c55794cc5eb38a157855f1ca2edd5ab)]

<br />
## 本次 Release 回顾
<br />


本文只是 Git 最新发行版中的部分变化的介绍。如果你想了解更多发布内容，可以查看[2.41 的发布日志](https://github.com/git/git/blob/v2.41.0/Documentation/RelNotes/2.41.0.txt),于此同时还可以[在 Git 仓库](https://github.com/git/git/branches)中查看[历史发布内容](https://github.com/git/git/tree/v2.41.0/Documentation/RelNotes)。

<br />
## 注释和引用
<br />

[1]. 风险基于很多因素， 最常见的就是并发写入的场景，比如 git 接收到的对象依赖一个 gc 正要清理的对象。 也就是，正在写入的对象引用了一个已经删除的对象，此时仓库就会损坏（corrupt）. 如果你感兴趣了解更多的内容，可以查看这个[文章](https://github.blog/2022-09-13-scaling-gits-garbage-collection/#object-deletion-raciness "章节")。
<br />
[2] https://github.blog/2021-03-15-highlights-from-git-2-31/#on-disk-reverse-indexes
<br />
[3] https://git-scm.com/docs/gitformat-pack/2.41.0/#_pack_rev_files_have_the_format
<br />
[4] walk： 指的是 Git 遍历 objects 的过程。

