---
title: Git Rev News Edition 84 (February 28th, 2022)
layout: default
date: 2022-02-28 12:06:51 +0100
author: chriscool
categories: [news]
navbar: false
draft: true
---


## 版权声明

Git Rev News 是由 Git 官方出品的 Git 开发者文摘，原文参见：https://git.github.io/ 。出于学习的目的，作者对 Git Rev News 相关内容进行再加工，包括但不限于翻译、重点解读、相关知识介绍等。其中引用的博客、图片均为 Git Rev News 所收录，属于原作者版权。文章内容仅可作为学习和交流使用，不能用于商业目的。

本期译自 Git Rev News 第84期。原文链接为：https://git.github.io/rev_news/2022/02/28/edition-84/。

## 社区讨论

### 概览

* [Join us for Review Club!](https://lore.kernel.org/git/Yfl1%2FZN%2FtaYwfGD0@google.com/)

  Josh Steadmon 宣布Google将举办 "Review俱乐部", 这种活动在公司内部已经举办了一段时间，现在开始对所有外部人员开放。

  时间为每两周星期三太平洋时间14:00 (UTC-8)通过谷歌会议开启。第一次的对外会议在2月2日举行，会议上讨论了 [Elijah's "In-core git merge-tree" patch series](https://lore.kernel.org/git/pull.1122.v2.git.1643479633.gitgitgadget@gmail.com/).

  如果你感兴趣参加， 可以联系Josh Steadmon at <steadmon@google.com>。
  
### Reviews

* [[PATCH] `fetch --prune`: exit with error if pruning fails](https://lore.kernel.org/git/20220127153714.1190894-1-t.gummerer@gmail.com/)

   Thomas Gummerer 发送了一个补丁， 关于`git fetch`当配合`--prune`使用时，
   如果在删除某个ref失败时， exit status 仍旧为0的问题。

  Pruning引用的含义是移除远端的tracking引用， 比如一个分支。 例如当`origin` 上存在
  一个名为`feature1`的分支， 那么从`origin` fetch这个分支的时候， 将会在本地创建一个
  用于追踪远程的分支`origin/feauture1`. 当`feature1`分支从远端移除后， 后续的fetch
  如果指定了 `--prune`选项， 那么本地的`origin/feature1` 分支也将被修剪移除。

  Thomas 在他的补丁中说道： 当prune引用删除失败时，srderr端会有错误信息提示， 但是
  `git fetch`仍然可以正常退出（exit status 为 0）似乎是一个bug。于此同时， Thomas
  查看了当时的提交信息，他不能确定这个表现是 “意外疏漏” 还是 “有意为之”。

  Junio Hamano, the Git maintainer, agreed with Thomas about using a
  non-zero exit status when ref pruning failed, but he was unsure about
  which actual exit status would be emitted by the code in Thomas' patch.

  Junio Hamano Git社区的maintainer， 同意Thomas的观点， 但是不确定Thomas的代码
  实际会返回的exit status是什么。

  Junio同时还发现当前代码的一个问题是， 在一些场景下似乎会向 `exit()` 传递 -1, 这会
  让命令返回一个 255 的exit status， 而exit status只有8 bit的 unsigned 长度， 这将
  导致精度溢出， 然后他在评论中留下了一个`#leftoverbits`提醒， 这将有助于后续修复这类
  小的问题。

  Junio还认为当error发生时便输出error信息可能不是一个好的主意。 最好的方式可能是继续执行
  fetch并且尽可能的完成prune操作，"既然我们已经在发现远端引用上投入， 不如让这些投入物有
  所值".

  Thomas的补丁添加了一个新的失败用例， 这也被Junio提供了一些意见并留下了`#leftoverbits`，
  这是因为在这个测试的脚本中，存在一些老风格的测试代码， 可能后续需要一些cleanup工作。

  Dscho(Johannes Schindelin), 回复Junio道： 对于用户来说，当prune失败而fetch继续时，
  可能带来一些困惑的非预期行为。 他建议添加一个`--prune-best-effort`用来区分两种行为。

  Thomas 回复 Dscho说他虽然不确定是否使用某一种方式， 他可以实现新的选项满足这一点。
  但是不确定用户是否会经常使用这个选项， 因为毕竟`--prune`失败是小概率事件。

  Junio回复Thomas和Dscho： 当我们通过fetch来更新多个引用时， 就算第一个ref-update
  失败，我们不会停止后续的更新， 所以`--prune`应该同样做出类似的行为。

  Thomas回复Junio的第一个评论， 他不确定是不是当`git fetch`因`--prune`而失败时，
  应该永远返回 1.

  Thomas 和 Dscho随后讨论了测试的内容， 基于Junio的评论， 他们达成一致的认为应该在
  这个测试上添加一行注释， 从而表达清晰的测试意图。

  Junio reviewed this new version and decided to merge it down, so
  this small improvement will be in the next Git version.

  Thomas随后发送了[v2 patch](https://lore.kernel.org/git/20220131133047.1885074-1-t.gummerer@gmail.com/)，
  Junio 评审了这个新的补丁并决定合入。

<!---
### Support
-->

## 开发者聚光灯: Eric Sunshine

_(Eric 曾经在 [Git Rev News #7, September 2015](https://git.github.io/rev_news/2015/09/09/edition-7/#developer-spotlight-eric-sunshine)接受过采访.)_

* 自从上一次采访，这段时间你有什么变化么？ 最近在忙什么？

  在采访之后的1年，因为需要照顾一个家庭成员占用了我大量的时间，以至于我无法跟上Git项目
  的进度，也无法以任何有意义的方式做出贡献，事实上，他至少有一年半的时间没有参与这个项目。
  自从回到这个项目后，由于“现实生活”的时间限制和我几年前开始的一份新工作，我的贡献变得更
  少了。

* 你曾经是一个长时间使用RCS, CVS和SVN的用户。对比Git， 你是否留恋了这些版本控制系统的一些特性？

  我可以毫不犹豫地说，我没有留恋那些旧版本控制系统的任何功能。事实上，我可以说(也许很高兴)，我几乎
  已经忘记如何使用它们了。Subversion尤其如此，在过去几年中，尽管我是一个有经验的长期用户，但我不得
  不多次查阅文档来处理即使是最简单的任务。

* 最近， 你对Git做了贡献了吗？代码贡献 或者 Codereview？

  在过去,我通常能够跟上邮件列表和阅读大多数或所有提交的补丁和提供详细的评论,但我这些天花费在
  Git的时间很有限,所以我目前更有选择性的去追踪或参与。

  由于我对“git worktree”命令做出了很大的贡献(而且我可能是一个“领域专家”，特别是自从
  Nguyễn Thái Ngọc Duy离开了这个项目之后)，我特别注意关于这个命令的bug报告，或者以一些重要的方式
  涉及它的主题。在错误报告的情况下，我要么自己提供问题的修复，要么帮助指导其他参与者。在主题触及
  “git worktree”的情况下，我试着留出时间来仔细检查该主题的补丁，并随着主题的进展进行跟踪。

  除此之外，当其他主题符合我有限的Git时间时，我还会对它们进行评论，并回答邮件列表中的周期性问题，
  或者如果我在这个主题上有什么有意义的东西可以提供，我同样也会参与讨论。

* 你是否还认为“支持stage” 和“交互式rebase”是你最喜爱的特性么？ 你有“新欢”了嘛？

  事实上，几年前，我开始使用[`src`](http://www.catb.org/~esr/src/)版本控制系统
  来管理独立的文件(尽管它是建立在RCS之上的，但它有一个“现代”的命令行界面，非常像Git，但由与
  RCS的界面完全不同)。虽然我发现“src”对于独立文件的版本控制很方便，但我总是觉得在使用它的时
  候我无能为力，因为它缺乏进行更改和交互式rebase这类非常有用的功能。


  因此，除了对项目进行bug修复和增强外，我还花了一些时间来显著提高“src”的`fast-import`和`fast-export`
  的准确性。这允许我暂时将“src”历史导入到Git中，这让我能够访问Git的staging和交互式rebase，
  并最终将历史转换回“src”。是的，它是一个可怕的组装，一个痛苦的，但至少让我在绝对需要的时候利用这些
  Git特性的方法。目前我使用“src”的频率还不够高，不足以证明开发工作的合理性，但在这个项目中，我希望直接
  在工具中添加staging和交互式rebase的能力。

* 你的邮件列表工作流程是怎样的?

  我明白一些开发人员使用一些特殊工具来建立和中心maillist的Git工作流,但我仍然
  使用普通的电子邮件客户端，这点上没有特别之处, 我可能会继续这个设置, 只要它还可以足够满足我的需求。

  我确实发现Git邮件列表存档在<https://lore.kernel.org/git>非常有用，当研究一些主题或bug报告时，
  我会经常去钻研它，以及获取我可能已经从本地电子邮件客户端删除的补丁集。
  
  最近，我也开始利用它的NNTP feed (nntp.lore.kernel.org)。

* 你可以像是说下你使用的 email 客户端嘛？

  我几乎只在浏览器中使用Gmail。最近，我一直在使用雷鸟访问 lore.kernel.org NNTP feed。
  当我，需要在回复中发送内联补丁并不希望Gmail web界面修改空白或格式时，我使用`mutt`。
  (我还将Emacs设置为电子邮件，因此可以将它用于与`mutt`相同的目的，但实际上我从未这样做过。)  

  [ _编辑的提示: 如果你计划使用浏览器的Gmail客户端， 不要忘记设置"Plain text mode" 
  [Gmail specific format-patch hints](https://git-scm.com/docs/git-format-patch#_gmail)_ ]

* 对于那些希望加入Git开发的人来说， 你有什么建议么？

  参与Git项目是非常让人望而生畏的(我知道这点,即使在这么多年之后,我仍然每次害怕提交补丁), 但在这个
  项目的人们一般都很友好, 评论者的目标是帮助你完善你的提交, 以便它可以最终被接受到这个项目中。毕竟，
  这就是为什么审查人员会花时间仔细阅读提交的内容，并提供(有时是深入和详尽的)评论来改进提交内容。需要
  注意的一点是: 回顾大量补丁的人倾向于(出于必要)精简措辞，只指出补丁中需要改进的部分，而往往忘记表扬
  那些做得很好的部分。因此，评论有时会让人感到冷漠和反感，但这不是目的。评论者真诚地想要提供帮助，否
  则他们也不会做出这样的努力。

  了解项目如何工作的一个好方法是订阅邮件列表，并阅读活跃贡献者的提交和评审者的评论。你可以通过被动式的观察
  来学习。从补丁或补丁系列中，不仅可以了解应该如何构造补丁系列，还可以了解如何编写有效的提交消息。通过阅读
  评论，可以了解评论者在说明什么问题以及他们是如何交互的。

  要积极参与到项目中来，提交一个补丁，即使是一个小补丁，修复你发现的一个bug，或者对文档做一个小的改进。如果
  你有关于功能改进或新特性的想法，可以将其发送到邮件列表。或者，如果只是想在没有任何特别想法的情况下做出贡献，
  那么可以查看邮件列表中的bug报告(就像我在加入项目时所做的那样)，并尝试设计一个修复方案，并以补丁的形式将其
  提交到邮件列表中。

  为项目做出贡献的另一种方式是审查提交的代码。评论不需要是广泛的或详尽的。在一个补丁中指出一个小的逻辑缺陷
  或者在一个注释或提交消息中的一个拼写错误的审查也是很有用的。

* 能否和 Git 开发者分享一个技巧？

  在审查补丁时，要明确指出哪些评论是希望提交者采纳的，哪些建议可以由提交者自行决定。这对于新贡献者
  来说尤其重要，因为他们可能无法区分对补丁的强制更改和“可能会很好”的更改。还要让提交者知道，如果有
  必要的话可以推迟评审意见，因为新来的人可能没有意识到这样做是一个可选项。

  对于提交者，试着回应每个评审意见， 即使只是简单的“OK”或“我同意你所有的意见”或“我不同意这个意见，
  或者“因为……”， 这样评审者就不会觉得他们的努力白费了。

  (哇哦，这可能是两个技巧了)

* 你将如何命名你对Git社区最重要的贡献？

  很难判断各种贡献的重要性。相反，我可以强调一下我所参与的几个领域。

  虽然我现在不做很多评论，但我曾经是一个积极的评论者，并希望我的评论和建议至少在某种程度上帮助改进各种提交。

  从终端用户的角度来看，也许我对Git最显著的贡献是我在改进和增强`git work-tree`命令和multiple-worktree支持方面所做
  的所有工作(尽管大部分是对Nguyễn Thái Ngọc Duy设计和实现机制的赞扬)。

  从一个Git开发人员的角度来看，也许我最有价值的贡献是所谓的 `chainlint`，它识别了Git测试脚本中特定类型的问题，
  如果没有被检测到，它会允许测试忽略失败，并报告成功。

* 最近你在Git项目中在做哪些工作？

  如前所述，我的Git时间是有限的，因此我的参与度被缩减了。我尝试在这里或那里回答一些问题，或在可能的
  情况下参与讨论，并且我定期审查新的提交。

  除了最近提供了一些bug修复补丁和引入了“git worktree repair”命令外，我最近关注的是上面提到的
  一个新的增强版的`chainlint`工具。虽然这个实现已经完成了半年多(在我写这篇文章的时候)，我仍然在
  努力寻找时间去完善这个补丁系列本身。在此期间，我确实设法提交了一些其他一些较长的补丁系列，以准备新的
  `chainlint`。

## 相关发布

+ Git [2.35.1](https://public-inbox.org/git/xmqq1r0rtfw9.fsf@gitster.g/)
+ Git for Windows [2.35.1(2)](https://github.com/git-for-windows/git/releases/tag/v2.35.1.windows.2),
[2.35.1(1)](https://github.com/git-for-windows/git/releases/tag/v2.35.1.windows.1)
+ libgit2 [1.4.1](https://github.com/libgit2/libgit2/releases/tag/v1.4.1),
[1.4.0](https://github.com/libgit2/libgit2/releases/tag/v1.4.0)
+ GitHub Enterprise [3.3.4](https://help.github.com/enterprise-server@3.3/admin/release-notes#3.3.4),
[3.2.9](https://help.github.com/enterprise-server@3.2/admin/release-notes#3.2.9),
[3.1.17](https://help.github.com/enterprise-server@3.1/admin/release-notes#3.1.17),
[3.0.25](https://help.github.com/enterprise-server@3.0/admin/release-notes#3.0.25),
[3.4.0](https://help.github.com/enterprise-server@3.4/admin/release-notes#3.4.0),
[3.3.3](https://help.github.com/enterprise-server@3.3/admin/release-notes#3.3.3),
[3.2.8](https://help.github.com/enterprise-server@3.2/admin/release-notes#3.2.8),
[3.1.16](https://help.github.com/enterprise-server@3.1/admin/release-notes#3.1.16),
[3.0.24](https://help.github.com/enterprise-server@3.0/admin/release-notes#3.0.24)
+ GitLab [14.8](https://about.gitlab.com/releases/2022/02/22/gitlab-14-8-released/)
[14.7.3](https://about.gitlab.com/releases/2022/02/14/gitlab-14-7-3-released/),
[14.7.2](https://about.gitlab.com/releases/2022/02/08/gitlab-14-7-2-released/),
[14.7.1, 14.6.4, and 14.5.4](https://about.gitlab.com/releases/2022/02/03/security-release-gitlab-14-7-1-released/)
+ GitKraken [8.3.0](https://support.gitkraken.com/release-notes/current)
+ GitHub Desktop [2.9.9](https://desktop.github.com/release-notes/),
[2.9.8](https://desktop.github.com/release-notes/),
[2.9.7](https://desktop.github.com/release-notes/)
+ Tower for Mac [8.0](https://www.git-tower.com/release-notes/mac) ([What's New in Tower 8 video](https://youtu.be/US4W1lNEJCE))

## 其他新闻

__杂谈__

* Gitlab如何优化git-fetch的性能[第一部分 1](https://about.git vslab.com/blog/2022/01/20/git-fetch-performance/) and
  [第2部分](https://about.gitlab.com/blog/2022/02/07/git-fetch-performance-2021-part-2/), by the GitLab Scalability team.
* [Mermaid帮助在Markdown中绘制图表](https://github.blog/2022-02-14-include-diagrams-markdown-files-mermaid/),
  automatically rendered on GitHub and possibly also in other
  [CommonMark](https://commonmark.org/) implementations.
* [发现更多同步pull request对应分支版本的方式](https://github.blog/changelog/2022-02-03-more-ways-to-keep-your-pull-request-branch-up-to-date/)
  on GitHub.


__轻阅读__

* [Fork仓库的Git对象共享(并不是bug)](https://people.kernel.org/monsieuricon/cross-fork-object-sharing-in-git-is-not-a-bug)
  by Konstantin Ryabitsev.
* [Git Bash快速入门](https://www.git-tower.com/blog/git-bash/)
  by Bruno Brito on Git Tower blog.
* [Git文件夹中的秘密 - Computerphile](https://youtu.be/bSA91XTzeuA)
  by Dr Max Wilson on Computerphile channel on YouTube.
  如果你想看关于`.git/logs/`文件夹的介绍， 可以看之前的一个视频
  [Git Rev News Edition #83](https://git.github.io/rev_news/2022/01/31/edition-83/)
* [使用clean/smudge filter保护Git仓库中的敏感数据](https://developers.redhat.com/articles/2022/02/02/protect-secrets-git-cleansmudge-filter)
  by Tomer Figenblat on Red Hat Developer blog.
* [Git: 切换Unstaged内容至新的分支](https://css-tricks.com/git-switching-unstaged-changes-to-a-new-branch/)
  by Chris Coyier on CSS-Tricks.


__Git工具和站点__

* [Monorepo.tools](https://monorepo.tools/) -- 关于Monorepo和相关工具链的详细介绍.
  * [monorepo.tools的发表宣言](https://blog.nrwl.io/announcing-monorepo-tools-da605afbb5d5)
    by Juri Strumpflohner for Nrwl.
  * 关于monorepos的优劣分析可以查看
    [Git Rev News Edition #81](https://git.github.io/rev_news/2021/11/29/edition-81/).


## 本期作者

This edition of Git Rev News was curated by
Christian Couder &lt;<christian.couder@gmail.com>&gt;,
Jakub Narębski &lt;<jnareb@gmail.com>&gt;,
Markus Jansen &lt;<mja@jansen-preisler.de>&gt; and
Kaartic Sivaraam &lt;<kaartic.sivaraam@gmail.com>&gt;
with help from Eric Sunshine, Philip Oakley, Bruno Brito
and Josh Steadmon.