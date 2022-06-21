
---
title: "About Git Objects and References"
date: 2022-06-21T19:06:02+08:00
tags:
  - "git"
  - "chinese"
draft: false
---

> `This article is written in Chinese. `

## Git 对象(Git Object)

### 1. 了解Git, 离不开了解Git对象

提到版本控制, 大家可能都不太陌生, 作为开发者或者软件工程师, 版本控制一直在频繁发生着, Git作为一款优秀的 VCS版本控制管理工具 (*Version Control System*) , 就是为了解决版本控制问题诞生。以下是来自维基百科中关于VCS的一段描述:

> “几乎与文章写作过程一样，对文本的组织和修订的需求一直存在, 只不过逻辑上的完成手段在各个历史时期有所不同, 书籍的 <版本> 和规范修订的 <编号> 的使用可以追溯到发明印刷术的时代。当计算时代来临之后，修订的逻辑诉求变得更加重要和复杂。如今，最强大或者最复杂的版本控制系统是用于软件开发的系统之中。复杂体现在通常版本需要多个人员同时读取和并发修改。”
> 
> — From: https://en.wikipedia.org/wiki/Version_control

如上述描述所言, “版本控制在逻辑上的完成手段在各个历史时期有所不同”, 而现如今Git便是“逻辑上的完成手段”的极佳实现之一, 为何Git会脱颖而出呢? 依照作者看来主要有以下几个原因:

* `免费并开源` : Git是免费的, 并基于GPL-V2协议的开源软件;

* `存储完整性` : Git可以让每台工作的计算机上都存储一个完整的代码存储仓库 (副本), “完整” 意味着每个副本均具备完整的变更历史记录 (一般场景均适用, 但如·shallow-clone·特性除外, 因为用户可以使用·shallow-clone·去下载一个指定的、裁剪过的提交历史, 而不下载整个Git仓库);

* `网络独立性` : 因为具备了完整的版本跟踪能力, 存储在任何一个计算机上的Git仓库都可以脱离网络而独立工作 (一般场景均适用, 例如·partial-clone·情况除外, 因为用户可以使用·partial-clone·仅仅下载提交的历史, 而不下载任何相关的文本文件, 当在未来需要用到它们的时候“按需下载”, 如果没有网络则可能会造成surprise);

* `协作能力强`:

  * 合并策略 : Git基于三路合并 (`Three-way merge`) 算法进行合并, 对于合并双方存在多个不同祖先的情况 (`Criss-cross-merge`) , Git也可以通过 Recursive three-way merge 支持, 因为其提交历史可以通过作为 有向无环图 (`DAG`) 的方式被加载、分析和模拟合并等操作 (在 *Git* 新版本 *2.33* 中引入了新的merge-ort策略, 可以通过缓存的方式解决大型`merge-recursive`场景下的性能问题, 例如在大量文件rename场景下, 合并性能可提升500倍, Rebase可提升 *9000* 倍) ;

  * 冲突处理 : 除了简单冲突场景可以支持之外 (双方编辑同一个文件的同一段内容). 一些复杂场景也可以支持, 例如文件在一个版本中被修改内容, 而在另一个版本对文件重命名, 这类操作在一些VCS工具中被视作树冲突 (`Tree conflict`) 需要人为介入, 而在Git中可以自动帮我们识别完成;

  * 线性历史 : 除了合并和冲突之外, 另一个协作的方式是补丁交换 (Patch commutation) 来完成变更合并, 它的特点是可以改变补丁的顺序 (`reorder`) 或者是修改补丁描述 (`reword`) , 最终让变更成为一条 线性历史 , 这在Git中也被得以参考实现, 并叫做`Rebase`.

除了以上几个原因, 其实还有例如: Git迁移的能力、Git对大仓的支持、Git传输协议等等一些有优点。

> Git经过16年的发展, 已经从最初Linus的第一个提交 ( *2000* 多行代码) 演变成目前最流行的VCS工具, 过程中也新增了大量令开发者们惊叹的特性。不管是“存储完整”还是“网络独立”, 亦或是“协作能力”和“新诞生的特性”, *Git* 的一些最初的设计还是基本保留了下来。
> 
> 那么这些版本控制中到底有什么不为人知的魔法呢?
> 
> 认识 Git 作为 VCS 机理很好的途径——就是从如何存储版本数据开始,这就是本期要谈的话题:Git对象 (`Objects`) 和引用 (`References`) 。

### 2. 对象类型

Git Objects近乎存储了Git的一切, 了解 Git Objects 是用好Git基础中的基础。

关于 Git 对象的分类, 目前有两种不同的“分法”:

* 第一种: 将 Git 对象分类为 4 个, 这个也是比较常见的分法, 其中包含 blob/tree/commit/tag 4种;

* 第二种: 在 第一种 基础上, 将 packfile (使用zlib来对其他对象压缩后的文件) 作为第5种对象, packfile 在本文章中将不会引申介绍；

### 3. Blob

#### 计算BLOB对象

blob是Git中仅用来存储文件文本内容的对象。

之所以上面用了一个 “仅” 这是因为BLOB中并不存储文件的名称, 时间戳, 或者其他的文件元数据 (例如Unix文件系统中attributes的概念, 例如文件权限信息、链接等) , 而只存储文件中的数据. 我们可以使用 git hash-object 子命令来尝试了解blob对象, 确保本机已经安装Git后, 执行如下命令:


```
➜  git init test.git
➜  cd test.git
➜  echo "some contents" | git hash-object --stdin
f70d6b139823ab30278db23bb547c61e0d4444fb
```

稍做解释, 首先我们创建了一个 `test.git` 目录并使用其初始化为一个 Git 仓库, 随后在仓库中执行了 hash-object 子命令. 当成功执行后, 子命令在 `stdout` 输出了一个难以记忆的字符串 :

`f70d6b139823ab30278db23bb547c61e0d4444fb` 。

`hash-object` 子命令可以让我们方便的计算或生成我们需要的 Git 对象. 其中, 我们可以在执行前指定 `-t` 参数, 告诉 `hash-object` 我们要计算和生成何种类型的对象, 如果没有指定 `-t` 参数, 默认按照 `blob` 类型进行处理。

使用 `git hash-object <file>`  是使用该子命令最基础的方式之一, 不带任何 `option` (换言之: 无 `-t` ), 意味着我们要计算 `blob` 类型的对象, 传入 `argument[1]` 为一个文件名用来读取其文件内部(contents),之后 `hash-object` 就可以根据文件文本进行计算或生成对象了。

在上面的执行过程中, 我们没有传入`<file>`来指定需要被计算的文件名, 而是使用了 `--stdin` 参数的方式让 `hash_object` 从输入流中读取 `contents` , 这种读取输入流的方式与指定 `<file>` 作为参数在这个场景下并没有本质的不同, 有的话直观的体现在无需在磁盘上多生成一个文件。

### 4. Git对象存储本质: key-value

在上面的示例中, 我们只是根据 contents 计算得到了一个 blob object, 这个 object 体现在了一个“难以记忆的字符串”的上面, 似乎除此之外我们对 blob 既看不见, 又摸不着. 那么“f70d6b139823ab30278db23bb547c61e0d4444fb” 究竟代表了什么含义呢?

这个难以记忆的字符串实际上就是Git对象的 `key` 值,  也被叫做 `OID (Object ID)` 。

在Git的世界, 不同的对象有着不同的 `key` 值, 就像这世上没有两个完全相同的叶子一样——key具备 唯一性. Git 对这种 `key` 默认使用 `SHA-1` 格式表示, 即: *40* 位 *16* 进制组成的字符串 。我们可以重复执行上面的 `echo "some contents" | git hash-object --stdin` 命令, 可以发现每次输出的 `key` 值都是相同的。

简单说来, 如果 `key` 值相同, 一定代表两个对象代表同一个含义, 否则就会有大的问题, 这种Git对象之间的 hash碰撞 (collision) 将会引发仓库可靠性和安全性上的严重隐患。实际上 `SHA-1` 也确实在 *2017* 年被证明可以被攻破(https://phys.org/news/2017-02-cwi-google-collision-industry-standard.html), 所以在 Git 新版本中, Git 支持升级更严格的 `SHA-256` 哈希算法, 即 *64* 位的 *16* 进制字符串表示 ,从而增强Git本身的安全性。

Git 对象的 key 我们有了初步了解, 那对象的 `value` 是什么呢? 我们可以执行下面的命令:

```shell
➜  echo "some contents" | git hash-object --stdin -w
f70d6b139823ab30278db23bb547c61e0d4444fb

➜  tree .git/objects
.git/objects
├── f7
│   └── 0d6b139823ab30278db23bb547c61e0d4444fb
├── info
└── pack
```


与之前执行 `hash-object` 子命令所不同的是, 这一次我们添加了 `-w` 选项, 这表示本次执行将不光计算 *blob* 的 *OID*, 还会将 *OID* 对应的 `value` 写入到 Git 仓库当中, 我们可以对 `.git/objects` 目录执行 *tree* 命令来验证这一点, 可以看到随着命令执行成功, 在 `.git/objects` 下产生了 `f7/0d6b139823ab30278db23bb547c61e0d4444fb` 文件. 其中目录名 `f7` 代表的是 `OID` 的前 *2* 位字符, 而OID剩余的 *38* 个字符则为文件名, 这样做的原因是可以让Git对象更加离散的存放到 `00~ff` 范围的 *256* 个目录之中, 提升操作系统查找性能和解决单个目录下可能带来的文件数量的限制, 这种对象的存放方式叫做 松散存储(`loose`) 或者 未打包存储(`unpacked`) 。

另外, 值得注意的是, 在执行 *tree* 命令的输出结果中, 可以发现除了用于存储松散对象的目录之外, 还有 *pack* 和 *info* 目录, 他们其实也是用于存储对象的, 只不过不是在当前仓库中采用松散的形式, 而是采用其他的方式, 比如将对象打包为 `pack-file` 或者从 `alternates` 资源中 (本地 *link* 或者 *http* 协议) 获取对象.。这些内容如果有机会, 也会在后面的视频和文章中会继续介绍, 本文不会过度引申. 对于之前不了解Git的读者来说, 暂知晓松散存储的方式即可。

我们可以执行 cat 命令查看松散文件的内容:

```shell
➜   cat .git/objects/f7/0d6b139823ab30278db23bb547c61e0d4444fb
xblob 14some contents
S[q
```

很明显, 这里并没有直接存储我们期待的文本内容: `"some contents"` , 而看似多了一些其他的内容。这是因为 *Git* 使用了 *zlib* 对文本内容和 对象的头信息(*header*) 进行了压缩, 为了真实还原我们存储的文本内容, 我们可以使用 `git cat-file` 子命令来查看:
```shell
➜  git cat-file -p f70d6b139823ab30278db23bb547c61e0d4444fb
some contents

➜  git cat-file  -t f70d6b139823ab30278db23bb547c61e0d4444fb
blob

```

`git cat-file` 子命令是用于查看 `Object value` 的绝佳助手, 这里我们通过指定的 *OID* 作为执行参数 (*arg*) 并添加 `-p` 选项 (*opt*) 来让 `cat-file` 自动适配对象的类型, 并且以较为美观的输出方式 (*pretty-print*) 对象中存储的数据 (*Git Object Data*) 进行输出。另外, 我们也可以使用 `-t` 选项来获取对象的类型。

以上, 我们简单介绍了 *blob* 对象——这是 *Git* 用来仅存放文件文本内容的一种存储的格式。同时, 我们还介绍了对象的 `key-value` 是如何将对象松散存储在 *Git* 仓库中, 以及如何根据 *OID* 来查看对应的 *data*。

文件的内容得以保存, 那么文件名等信息到底存在哪里呢? 接下来就要给大家介绍另一个对象类型 *tree* 。

### 5. Tree

Git 的一个设计理念是: 在版本控制过程中, Git 针对变更是基于创建 完整快照 (`Snapshots`) 而非增量修改 (`Deltas`) 。需要其他的VCS工具是使用增量编码(压缩)的形式存储增量, 从而节约存储空间 (通常是这个目的) , 但 Git 并没有沿用这一理念, 而是坚定的使用了快照的设计. 快照的方式不可避免的会对带来存储空间的快速增长, 但是也带来了Git对象在存储上不可变性 (`Immutable`) 的优势, 这是设计上的一个权衡 (*trade-off*)。

`Snapshots`得以让 Git 可以针对一个提交、目录树或者文件, 在无需保存任何其他的关联对象的信息的情况下, 随时可以还原某一个历史时刻的仓库状态。

*tree* 对象负责存储一个目录的快照(`snapshot`), 快照包含一组文件的文件类型(`type`)、文件名、文件模式 (`mode`)等信息。

*tree* 对象保存的信息和我们常见的目录结构很类似, 其内部可以递归包含其他的目录和 *blobs*, 这其实和 *Unix* 的文件系统 (树映射) 的设计方式很相似(https://en.wikipedia.org/wiki/Unix_filesystem#Principles)。*tree* 对象其内部的存储方式是使用 哈希树 的结构 (https://en.wikipedia.org/wiki/Merkle_tree)。这样, *Git* 只需要一个 根树 (`root-tree`) 的 `OID` 就足够推演整个目录的状态, 随后将根树和 commit对象 关联, 就可以知道在那个提交的时间节点上工作空间的快照。

#### 根树对象—Root Tree

为了更进一步的解根树的存储方式 (root-tree) , 我们可以执行如下命令:

```shell
➜  echo 'readme' > README.md
➜  git add README.md
➜  git commit -s
[master (root-commit) 3de31e2] COMMIT A
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
➜
➜  git cat-file -p master
tree 764409de08fa4fda9ba6c85a54f5f31d00cec93e
author Dyrone Teng <tenglong.tl@alibaba-inc.com> 1633679101 +0800
committer Dyrone Teng <tenglong.tl@alibaba-inc.com> 1633679101 +0800
COMMIT A
➜
➜  git cat-file -t 764409de08fa4fda9ba6c85a54f5f31d00cec93e
tree
➜  git cat-file -p 764409de08fa4fda9ba6c85a54f5f31d00cec93e
100644 blob 8178c76d627cade75005b40711b92f4177bc6cfc    README.md
➜  git cat-file -p 8178c76d627cade75005b40711b92f4177bc6cfc
readme
```

我们首先创建了一个名为 `README.md` 的文本文件. 随后执行了 `git add` 子命令, 在这个过程中Git会将该文本文件转化为 *blob* 对象进行存储。随后执行 `git commit` 子命令, 在这个过程中Git会生成一个 *tree* 对象来存储当前仓库目录的快照, 之后再生成一个指向该 *tree* 的 *commit* 对象, 这个新生成并被 *commit* 引用的 *tree* 即 *root-tree* 。

我们可以执行 `git cat-file` 子命令来查看某个提交所引用的 *root-tree* 对象, 并递归执行查看查看该 *tree* 对象的类型和内容。

通过上面的输出结果可以看到, 此时 `root-tree` 中包含了 *README.md* 中文本对应的 *blob* 对象: `8178c76d627cade75005b40711b92f4177bc6cfc` , *blob* 中存储了内容: "readme" 。

#### 普通Tree对象

`Root Tree`是一种逻辑含义上特殊的 *tree* 对象, 因为它是由 *Git* 自动生成的对某个目录的映射或索引. 但是在物理含义上, 它与普通的 *tree* 对象并没有本质差别, 我们尝试通过新增目录的方式, 来进一步了解 *tree* 对象:
```shell
➜  mkdir src docs
➜  echo "abc" > src/main.c
➜  echo "efg" > docs/project.txt
➜  git add src docs
➜  git commit -s
[master 87902f9] COMMIT B
 2 files changed, 2 insertions(+)
 create mode 100644 src/main.c
 create mode 100644 src/project.txt
➜
➜  git cat-file -p master
tree 2e6cdc032db0ecfa4e3e898b8f8551acce10db11
parent 3de31e208ae26c6b44d9e6c4a3f0adb32d0c68b6
author Dyrone Teng <tenglong.tl@alibaba-inc.com> 1633681481 +0800
committer Dyrone Teng <tenglong.tl@alibaba-inc.com> 1633681627 +0800
COMMIT B
Signed-off-by: Dyrone Teng <tenglong.tl@alibaba-inc.com>
➜
➜  git cat-file -p 2e6cdc032db0ecfa4e3e898b8f8551acce10db11
100644 blob 8178c76d627cade75005b40711b92f4177bc6cfc    README.md
040000 tree 99b20b290a90e1137e0487f955620db05b229abe    docs
040000 tree 8db636fa1dbc4d704179895bdb6e4322f32cbda6    src
➜
➜  git cat-file -p 99b20b290a90e1137e0487f955620db05b229abe
100644 blob 1505b408c2ef47655f603b9045464e642ab28d97    project.txt
➜
➜  git cat-file -p 8db636fa1dbc4d704179895bdb6e4322f32cbda6
100644 blob 8baef1b4abc478178b004d62031cf7fe6db6f903    main.c
```

我们在工作空间中, 新创建了两个文本文件为 *main.c* 和 *project.txt* 并分别存放在新的目录 *src* 和 *docs* 下, 随后对当前工作空间的更改进行提交。

通过 `git cat-file -p master` 来查看 *master* 分支 (Git自动为我们生成的默认分支名) 上最近提交的 *root-tree* 对象, 随后进一步通过该子命令进行递归查看. 我们可以从输出结果分析出以下绩点(仅分析 *tree* 和 *blob* 对象):

* 创建 *blob* 对象 `1505b408c2ef47655f603b9045464e642ab28d97` 用于存放 `project.txt` 文件的文本内容;
* 创建 *blob* 对象 `8baef1b4abc478178b004d62031cf7fe6db6f903` 用于存放 `main.c` 文件的文本内容;
* 创建 *tree* 对象 `8db636fa1dbc4d704179895bdb6e4322f32cbda6` 用于存放 *src* 目录索引信息, 其中包含了 *main.c* 文件的名称、类型和模式等信息;
* 创建 *tree* 对象 `99b20b290a90e1137e0487f955620db05b229abe` 用于存放 *docs* 目录索引信息, 其中包含了 *project.txt* 文件的名称、类型和模式等a信息;

•创建 *tree* 对象 (`root-tree`) `2e6cdc032db0ecfa4e3e898b8f8551acce10db11` 用于存放当前仓库目录的索引信息, 其中包含了 *src* 以及 *docs* 目录以及 *README.md* 文件的名称、类型和模式等信息;

大家是否注意到, 当我们使用 *cat-file* 查看一个 *tree* 对象时, 其中不仅包含了文件名、*OID* 和对象类型, 还输出了类似 `100644` 以及 `040000` 等信息, 这些信息则代表着文件的 *类型* 和 *模式* 。

#### 文件的类型(*type*)与模式(*mode*)

文件类型 (https://en.wikipedia.org/wiki/Unix_file_types) 和模式 (https://en.wikipedia.org/wiki/File-system_permissions), 是源于 *Unix* 文件系统中的设计, 而在 *Git* 中则进行了选择性的沿用, 可以认为是一个 *Unix* 文件结构设计的迷你版。

Git 采用 *32* 位长存储文件模式，从高位到低位依次:

* 4位: 保存对象类型, 二进制的有效值为 1000（常规文件）、1010（符号链接）和 1110 (gitlinks)
* 3位: 保留
* 9位: unix 权限格式, 只有 0755 和 0644 对常规文件有效, 符号链接和 gitlinks 在该字段中的值为0.

目前的模式有以下几种:

* 0100000000000000 (040000): 目录;
* 1000000110100100 (100644): 普通文件(非可执行);
* 1000000110110100 (100664): 普通文件(非可执行、group可写);
* 1000000111101101 (100755): 普通文件(可执行);
* 1010000000000000 (120000): 符号链接(Symbolic link);
* 1110000000000000 (160000): Gitlink(用于Git Submodule);

### 6. Commit

通过上面的介绍, 我们已经大体了解了 *blob* 和 *tree* 的用途, 其中 *tree* 区别了不同状态下仓库内容的快照, 但光有这些还是不够的, 因为这时候还缺少如下的信息:

* 无法追溯 : 仅有快照, 相当于有了 *What* . 但快照和快照之间的联系没有建立起来, 如前面介绍它们只是松散存储的 *Tree* 对象, 没有形成历史结构存储下来。
  * Who : 不知道快照的参与者是谁。
  * Why/How : 不知道当初创建快照的原因。
  * When : 不知道什么时间创建了快照。

* 提交 (commit) 对象用来解决这些问题:

  * 关联快照 : commit引用了一个 _root-tree_对象, 即仓库顶层目录的快照, 从而将提交对象和树对象关联。
  * Who : commit对象中记录了作者、提交人以及其他参与者的信息, 例如可以通过 git commit 子命令的 -signoff 选项, 在提交末尾添加 Signed-off-by (授权提交) 信息. 诸如此类的还有:

    * Reported-and-tested-by: reported and tested the issue (I assume);
    * Acked-by: acknowledged by the owner of the code, “looks good to me” ;
    * Reviewed-by: reviewed;
    * * Cc: was notified about the patch;

  * When : 提交中通过时间戳记录了创建的时间以及提交的时间. 这是因为, Git的作者和提交者可以是不同的人, 对应的创作时间和提交时间自然就可能不同, 我们可以执行 git log --format=fuller 查看包含了上述全部信息的提交历史列表。

  * Why/How : 提交中还保存了提交的描述信息, 其中可以记录本次提交的原因、背景和实现策略等.
    *  一行标题;
    * 一行空行;
    * 可以包含多个段落的具体描述;

  * 可追溯 : Git commit中可以存储包含指向父提交的引用(parent), 通过这种方式, 新的 commit 和旧的 commits 之间就构成了一个有向无环图 (DAG), 我们可以从图中搜索 commit 并递归追溯其所有的祖先提交 (ancestors)。通常, 一个提交可以有0个或n个父提交, 情况分别为:

    * 0个 : 当提交为根提交(root-commit) 或者使用 git commit-tree 子命令(不加 -p 选项)直接创建的commit对象。
    * 1个 : 非根提交, 或非合并提交的情况下
    * 2个 : 合并提交(merged-commit)

一个较好的参考示例:

•https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/commit/?id=19be0eaffa3ac7d8eb6784ad9bdbc7d67ed8e619


为了很好的理解上面的几点, 我们可以在刚才创建的 test.git 中执行:


```shell
➜  git log --parents --pretty=fuller
commit 6ae8bbeeb4dba091d3c6295d0b3d0f9a3863d32f 3de31e208ae26c6b44d9e6c4a3f0adb32d0c68b6 (HEAD -> master)
Author:     Dyrone Teng <tenglong.tl@alibaba-inc.com>
AuthorDate: Fri Oct 8 16:24:41 2021 +0800
Commit:     Dyrone Teng <tenglong.tl@alibaba-inc.com>
CommitDate: Fri Oct 8 16:27:07 2021 +0800
    
    COMMIT B

    Signed-off-by: Dyrone Teng <tenglong.tl@alibaba-inc.com>

commit 3de31e208ae26c6b44d9e6c4a3f0adb32d0c68b6
Author:     Dyrone Teng <tenglong.tl@alibaba-inc.com>
AuthorDate: Fri Oct 8 15:45:01 2021 +0800
Commit:     Dyrone Teng <tenglong.tl@alibaba-inc.com>
CommitDate: Fri Oct 8 15:45:01 2021 +0800

    COMMIT A

    Signed-off-by: Dyrone Teng <tenglong.tl@alibaba-inc.com>
```

我们通过添加 `--parents` 选项, 让 `git log` 子命令输出 `parents`提交的相关信息, 同时还添加了 `--pretty=fuller` 选项, 让输出结果中同时展示作者, 提交者, 创作时间和提交时间。

#### 小结回顾

Git 对于每一次的文件内容变化, 都会单独保存为一个 zlib 压缩过的 blob 对象(文件), 进一步通过 commit 和 tree 将文件和目录组织起来形成快照, 并将提交和快照关联起来, 建立提交之间的 DAG。

这种设计, 让版本管理变得简单可靠, 但同时, 也不可避免的会造成 Git 仓库存储的 快速膨胀 。Git 可以通过将松散的对象打包为 pack 文件, 来解决这个问题。除此以外, pack 中还支持保存 delta 的方式(`delta compression`), 保存对象之间的 delta 差异 (2进制则会失效)。

### 7. Tag

标签 (`tags`) 的概念并非 Git 独创, 通常用来记录被认为很重要的提交, 例如软件的发行版本。

#### 轻量级标签 (`Lightweight Tags`)

我们可以创建一个不带有任何额外信息的 *tag*, *Git* 称这种类型的标签为 轻量级 *tag* (`lightweight`)。 "签如其名",  轻量级 *tag* 看上去与一个 *commit* 并无太多差别, 事实也确实是这样, 因为其不会保存额外的信息, 只是一个 *commit* 的指针, 我们可以在 `test.git` 中创建一个名为 `v1.0` 的轻量级tag:


```shell
➜  git tag v1.0
➜  git cat-file -t v1.0

commit
```

可以看到, 标签名也支持使用 `git cat-file` 子命令, 我们可以看到其对象类型为 *commit*。

#### 附注标签 (`Annotated Tags`)

另外一类标签叫做 附注标签 (`Annotated Tags`) , 附注标签可以记录额外的信息。例如: 如果一个 tag 被用来标记发行版本, 就可以通过附注的信息记录本次发布了什么内容。此外, 附注标签还可以记录标签的 作者 (*tagger*) 、邮箱 (*tagger email*) 以及 时间戳 , 这些都可以理解为标签说被附注的 元数据(*meta-data*) 。最后, 附注标签还支持使用默认配置的邮箱信息, 用于生成 *GPG* 签名信息并附注在 *tag* 中。

附注标签与轻量级标签不同的是, 附注标签会以tag对象类型进行保存:
```shell
➜  git tag -a v2.0 -m "create v2.0"
➜
➜  git cat-file -t v2.0
tag
➜
➜  git cat-file tag v2.0
object 6ae8bbeeb4dba091d3c6295d0b3d0f9a3863d32f
type commit
tag v2.0
tagger Dyrone Teng <tenglong.tl@alibaba-inc.com> 1633919318 +0800
 
create v2.0
```

如上所示, 我们创建了一个名为 `v2.0` 的附注标签, 其描述信息为 `create v2.0` 。我们可以使用 `cat-file` 子命令查看该标签会发现其对象类型为 *tag* 。进一步, 如果我们希望查看 *tag* 的附注信息, 我们可以执行 `git cat-file tag` 子命令完成。

## Git 引用 (Git Reference)

`OID`, 即 *40* 位的 *16* 进制字符串表示(*SHA-256* 则为 *64* 位), 毫无疑问让我们非常晦涩难记。Git 引用 (References 或 Refs) 就是为此而生的, 引用是一个逻辑概念, 其并非 Git 所独创, 很多的 VCS 工具都有类似的概念和设计, 但是基本通过不同的物理方式实现。

### 1. Git 引用的存储方式

Git 引用存储的文件可以在我们仓库中轻松找到, 并且其存储的内容结构也非常简易。Git refs通常会 松散存储 在仓库的 `.git/refs/` 目录下 (实际上也可以“打包”), 我们可以在此前的仓库中执行 `find` 命令:

```shell
➜  find .git/refs
.git/refs
.git/refs/heads
.git/refs/heads/master
.git/refs/tags
.git/refs/tags/v2.0
.git/refs/tags/v1.0
```

其中 `.git/refs/heads` 和 `.git/refs/tags` 等目录是用来让 Git 区分不同引用类型, 其中包括:

仓库内建引用目录标识:

* `git/refs/heads/` : 分支引用(`Branches`);
* `git/refs/tags/` : 标签引用(`Tags`);
* `git/refs/remotes/` : 远端引用(`Remotes Refs`);
* `git/refs/stash/` : 暂存引用(保存还未提交的对象信息);
* `git/` : 符号引用(例如: *HEAD* 等);
* `git/refs/meta/config` : `Gerrit` 用于保存仓库信息和用户权限等用到的特殊引用;

### 2. 分支和标签引用

分支(`Branches`) 是 `Git refs` 最常见的引用之一, 我们可以通过 `cat` 命令直接查看我们在 `test.git` 仓库中已经默认创建的 `master` 分支:

```shell
➜  cat .git/refs/heads/master
6ae8bbeeb4dba091d3c6295d0b3d0f9a3863d32f
➜
➜  git cat-file -p 6ae8bbeeb4dba091d3c6295d0b3d0f9a3863d32f
tree 2e6cdc032db0ecfa4e3e898b8f8551acce10db11
parent 3de31e208ae26c6b44d9e6c4a3f0adb32d0c68b6
author Dyrone Teng <tenglong.tl@alibaba-inc.com> 1633681481 +0800
committer Dyrone Teng <tenglong.tl@alibaba-inc.com> 1633681627 +0800

COMMIT B

Signed-off-by: Dyrone Teng <tenglong.tl@alibaba-inc.com>
```

可以看到, 在引用文件 `.git/refs/heads/master` 中保存了 `6ae8bbeeb4dba091d3c6295d0b3d0f9a3863d32f` , 这个 `OID` 就是我们刚才创建的 `COMMIT B` 的对象。同理, 我们可以查看 `.git/refs/tags/v1.0` 的引用存储的信息, 我们可以执行:

```shell
➜  cat .git/refs/tags/v1.0 | xargs git cat-file -p
tree 2e6cdc032db0ecfa4e3e898b8f8551acce10db11
parent 3de31e208ae26c6b44d9e6c4a3f0adb32d0c68b6
author Dyrone Teng <tenglong.tl@alibaba-inc.com> 1633681481 +0800
committer Dyrone Teng <tenglong.tl@alibaba-inc.com> 1633681627 +0800

COMMIT B

Signed-off-by: Dyrone Teng <tenglong.tl@alibaba-inc.com>
```

### 3. 符号引用

了解 符号引用(`Symbolic Reference`) 之前, 我们先在 `test.git` 目录中执行 `git log` 子命令:

```shell
➜  git log

commit 6ae8bbeeb4dba091d3c6295d0b3d0f9a3863d32f (HEAD -> master, tag: v2.0, tag: v1.0)
Author: Dyrone Teng <tenglong.tl@alibaba-inc.com>
Date:   Fri Oct 8 16:24:41 2021 +0800

    COMMIT B

    Signed-off-by: Dyrone Teng <tenglong.tl@alibaba-inc.com>

commit 3de31e208ae26c6b44d9e6c4a3f0adb32d0c68b6
Author: Dyrone Teng <tenglong.tl@alibaba-inc.com>
Date:   Fri Oct 8 15:45:01 2021 +0800

    COMMIT A

    Signed-off-by: Dyrone Teng <tenglong.tl@alibaba-inc.com>

```

`git log` 子命令用于查看 *提交历史*, 这里我们没有指定任何一个选项或者参数, 这中情况下子命令会为我们展示 当前所在引用(`the branch currently on`) 分支 的最新提交历史, 那么Git是如何知晓我们当前引用是哪个呢? 原因就在于符号引用。
`Git` 使用 `.git/HEAD` 文件来保存你当前所在分支引用的信息, 与分支引用和标签引用相比不同的是, 后者存储的是引用对象的信息, 而前者保存的是 引用的引用 , 我们执行 :

除了 `HEAD` 之外, 实际上我们可以 `symbolic-ref` 子命令更新和获取, 自定义名称的符号引用:

```shell
➜  git symbolic-ref MARK refs/heads/master
➜  test.git git:(master) cat .git/MARK
ref: refs/heads/master
```


### 4. Remotes引用

*Remotes* 引用, 通常用来存储 已经存在于远程存储库中的对象 信息, 例如在执行 `git push` 子命令后进行维护. 我们此前介绍的内容都是基于本地仓库, 并不涉及与远端仓库的协作. 如果我们添加一个远端仓库 (*remote*) 的地址并将新的提交执行推送 (*push*) ，Git 便会将上次推送的对象的值存储在 `refs/remotes` 目录中的对应分支中。例如，您可以添加一个名为 *origin* 的远程信息并将 *master* 推送上去：

```shell
➜   git remote add origin https://codeup.aliyun.com/rdc2020/dyrone.git
➜
➜   git push origin master
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (9/9), 754 bytes | 754.00 KiB/s, done.
Total 9 (delta 1), reused 0 (delta 0), pack-reused 0
To https://codeup.aliyun.com/rdc2020/dyrone.git
 * [new branch]      master -> master
➜
➜  cat .git/refs/remotes/origin/master
6ae8bbeeb4dba091d3c6295d0b3d0f9a3863d32f
```

现在我们可以看到, 在 `.git/refs/remotes/origin/master` 引用中记录了我们上一次 `push` 到名为 `origin` 的远端仓库上的对象信息。

### 5. 引用维护

了解了引用的存储方式以后, 我们可以通过直接创建文件的方式, 创建一个仓库中的引用:

```shell
➜  git log --graph
* commit 6ae8bbeeb4dba091d3c6295d0b3d0f9a3863d32f (HEAD -> master, tag: v2.0, tag: v1.0, origin/master)
| Author: Dyrone Teng <tenglong.tl@alibaba-inc.com>
| Date:   Fri Oct 8 16:24:41 2021 +0800
|
|     COMMIT B
|
|     Signed-off-by: Dyrone Teng <tenglong.tl@alibaba-inc.com>
|
* commit 3de31e208ae26c6b44d9e6c4a3f0adb32d0c68b6 (topic_aliyun)
  Author: Dyrone Teng <tenglong.tl@alibaba-inc.com>
  Date:   Fri Oct 8 15:45:01 2021 +0800

      COMMIT A

      Signed-off-by: Dyrone Teng <tenglong.tl@alibaba-inc.com>
➜
➜  echo 3de31e23de31e208ae26c6b44d9e6c4a3f0adb32d0c68b6 > .git/refs/heads/topic_aliyun
➜
➜  git log --oneline refs/heads/topic_aliyun
3de31e2 (topic_aliyun) COMMIT A
```

首先我们找到仓库中的第一个提交, 随后基于第一个提交的OID创建一个名为 `topic_aliyun` 的分支引用, 随后执行 `git log` 子命令查看新分支的提交记录, 其中 `--graph` 选项可以在提交历史中附带输出文本形式的简易图形信息, `--oneline` 可以简化我们的输出信息, 只关注提交的 标题 和 简短形式的 `OID`。

直接使用 `echo` 的方式去修改引用其实不是非常安全, 所以 `Git` 设计了 `git update-ref` 子命令专门用来维护引用的数据。例如, 我们可以尝试将分支应用 `refs/heads/topic_aliyun` 更新为 *COMMIT B* 的提交对象:

```shell
➜  git update-ref refs/heads/topic_aliyun 6ae8bbeeb4dba091d3c6295d0b3d0f9a3863d32f
➜  cat .git/refs/heads/topic_aliyun
6ae8bbeeb4dba091d3c6295d0b3d0f9a3863d32f
```

## 总结

本文花了一部分的篇幅用来介绍了 *Git* 的设计思路, 引出了 *Git* 是如何通过对象来完成版本控制数据的存储, 以及如何通过引用来方便的管理和使用这些对象, 希望这些内容对不太了解 *Git* 的同学能够小有帮助, 同时这也是继续了解 *Git* 的重要基础。