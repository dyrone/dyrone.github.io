---
title: "Gdb Journey"
date: 2022-10-13T16:00:10+08:00
draft: false 
tags: 
    - tools
    - debugging
    - c
---

## Use m4 for a test

如果发现没有debug详细信息，根据gdb的提示，可以使用`debuginfo-install`安装对应的
依赖包

> DESCRIPTION
>        debuginfo-install is a program which installs the RPMs needed to
>        debug the specified package.  The package argument can be a
>        wildcard, but will only match installed packages.  debuginfo-
>        install will then enable any debuginfo repositories, and install
>        the relevant debuginfo rpm.
> 
> From: https://man7.org/linux/man-pages/man1/debuginfo-install.1.html

```shell
$ debuginfo-install m4-1.4.16-10.1.alios7.x86_64
```

## GDB 指定执行参数

```shell
gdb --args git ls-tree HEAD
```

更多的参数和用法可以参考GDB Cheat Sheet.

> https://darkdust.net/files/GDB%20Cheat%20Sheet.pdf

## 在Git中查看构建调试参数

在git源码中的Makefile中定义了CFLAG的相关参数：

```make
# Set CFLAGS, LDFLAGS and other *FLAGS variables. These might be                                                                                   
# tweaked by config.* below as well as the command-line, both of                                                                                       
# which'll override these defaults.                                                       
# Older versions of GCC may require adding "-std=gnu99" at the end.                                                                                       
CFLAGS = -g -O2 -Wall
LDFLAGS =
CC_LD_DYNPATH = -Wl,-rpath,
BASIC_CFLAGS = -I.
BASIC_LDFLAGS =
```

其中 `-g` 让编译器编译时生成调试信息，`-O2` 让编译器编译时使用最优的编译选项，`-Wall` 让编译器编译时生成警告信息。

关于 `-g` 与其相关等级的进一步说明：

```shell

       -glevel
       -ggdblevel
       -gstabslevel
       -gxcofflevel
       -gvmslevel
           Request debugging information and also use level to specify
           how much information.  The default level is 2.

           Level 0 produces no debug information at all.  Thus, -g0
           negates -g.

           Level 1 produces minimal information, enough for making
           backtraces in parts of the program that you don't plan to
           debug.  This includes descriptions of functions and external
           variables, and line number tables, but no information about
           local variables.

           Level 3 includes extra information, such as all the macro
           definitions present in the program.  Some debuggers support
           macro expansion when you use -g3.

           If you use multiple -g options, with or without level
           numbers, the last such option is the one that is effective.

           -gdwarf does not accept a concatenated debug level, to avoid
           confusion with -gdwarf-level.  Instead use an additional
           -glevel option to change the debug level for DWARF.
```
> From: https://man7.org/linux/man-pages/man1/gcc.1.html

其中 `-O2` 代表了优化等级，git中默认选择 O2 等级，为了更好的debug， 我们可以改为`-O0`, 从而可以让debug信息更丰富和明确。

```adoc
-O0

    Reduce compilation time and make debugging produce the expected results. 
    This is the default.
```

> From: https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html

我们可以查看git的`.gitignore文件`

```shell
/config.mak
/autom4te.cache
/config.cache
/config.log
/config.status
/config.mak.autogen
/config.mak.append
```

我们可以通过修改config.mak的方式进行扩展，而不修改原有的make文件。

在我的开发机器上，重新构建git后，例如执行`gdb --args git ls-tree HEAD` 仍旧在GDB中存在如下警告信息：

>
> Reading symbols from /home/tenglong.tl/repos/git/git...Dwarf Error: wrong version in compilation unit header (is 5, should be 2, 3, or 4) [in module /home
> 
> (no debugging symbols found)...done.     
```

出现这种情况的原因通常是GDB的版本过老，对于`-g3`产生的调试信息无法正确识别，我们选择升级`gdb`的版本即可： 

```shell

$sudo yum upgrade gdb
Last metadata expiration check: 3:09:55 ago on Fri 24 Jun 2022 11:08:04 AM CST.
Dependencies resolved.
...
New leaves:
  gdb.x86_64

Installed:
  gdb-headless.x86_64 8.2-6.5.alios7                                                                                                                      

Upgraded:
  gdb.x86_64 8.2-6.5.alios7                                                                                                                               

Complete!
```

再次执行`gdb --args git ls-tree HEAD`， symbol已经可以正确读取：

```shell
$ gdb --args git ls-tree HEAD
GNU gdb (GDB) Red Hat Enterprise Linux 8.2-6.5.alios7
Copyright (C) 2018 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-redhat-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from git...done.
```

随后我们尝试在git ls-tree的入口方法 "cmd_ls_tree()" 添加断点， 然后通过`step`命令进行单步调试，可以看到调试信息如下：

```shell
(gdb) b cmd_ls_tree
Breakpoint 1 at 0x479b71: file builtin/ls-tree.c, line 333.
(gdb) run
Starting program: /home/tenglong.tl/repos/git/git ls-tree HEAD
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".

Breakpoint 1, cmd_ls_tree (argc=2, argv=0x7fffffffe190, prefix=0x0) at builtin/ls-tree.c:333
333             int i, full_tree = 0;
Missing separate debuginfos, use: debuginfo-install zlib-1.2.7-16.2.alios7.x86_64
(gdb) s
334             read_tree_fn_t fn = NULL;
(gdb) 
[1] 0:
```

我们可以使用`backtrace`(`bt`) 查看调用栈，可以看到调用栈如下：

```shell
(gdb) backtrace
#0  cmd_ls_tree (argc=2, argv=0x7fffffffe190, prefix=0x0) at builtin/ls-tree.c:334
#1  0x0000000000406a8a in run_builtin (p=0x9dbd88 <commands+1512>, argc=2, argv=0x7fffffffe190) at git.c:466
#2  0x0000000000406e65 in handle_builtin (argc=2, argv=0x7fffffffe190) at git.c:720
#3  0x000000000040709c in run_argv (argcp=0x7fffffffe02c, argv=0x7fffffffe020) at git.c:787
#4  0x0000000000407579 in cmd_main (argc=2, argv=0x7fffffffe190) at git.c:920
#5  0x00000000004ea8e1 in main (argc=3, argv=0x7fffffffe188) at common-main.c:5
```

可以使用`print`(`p`) 来查看变量的值，可以看到如下：

```shell
(gdb) print tree
$6 = (struct tree *) 0xa36630
(gdb) print &tree
$7 = (struct tree **) 0x7fffffffdde0
```

## 相关资料

> https://gist.github.com/phil-blain/17c67740bd26e66f4851fe0c07230ea4
> https://darkdust.net/files/GDB%20Cheat%20Sheet.pdf

## FAQ

在使用GDB的过程中，特别是使用Mac GDB的过程中，可能会遇到诸多的问题，下面的链接可
能会对你产生帮助:

### please check gdb is codesigned - see taskgated(8)

```shell
(gdb) run
Starting program: /Users/lurongming/test/cpptest/main
Unable to find Mach task port for process-id 33242: (os/kern) failure (0x5).
(please check gdb is codesigned - see taskgated(8))
```

> https://blog.csdn.net/LU_ZHAO/article/details/104803399

### On macOS 10.12 (Sierra) and later

> https://sourceware.org/gdb/wiki/BuildingOnDarwin

### Hangs after executing "run" and prompt "[New Thread 0x2503 of process 10191]" 

https://timnash.co.uk/getting-gdb-to-semi-reliably-work-on-mojave-macos/

### My own way on macOS(currently solve all the FAQs)

```shell
➜  git-notes-test git:(tl/test) ✗ sudo gdb --args git notes
Password:
GNU gdb (GDB) 12.1
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-apple-darwin19.6.0".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from git...
(gdb) run
Starting program: /usr/local/bin/git notes
[New Thread 0x2603 of process 11838]
[New Thread 0x1b03 of process 11838]
warning: unhandled dyld version (16)
1daee75c5d07890f8a86869aa4b2553f60554b31 769baa18c813add6d99d85bbb7e0ab7b7c19e491
0c92279bea1cfd75646ca487bb22bb7d5588251e 7e5ad57b724ecdd911154302b84d5cfba05f8a05
214bc686ea9a9082763989a36830524c505e5feb ab4cc15ab20a5e14b330204de4c3d05ca1205f27
[Inferior 1 (process 11838) exited normally]
(gdb) exit
➜  git-notes-test git:(tl/test) ✗ cat ~/.gdbinit 
set startup-with-shell off
➜  git-notes-test git:(tl/test) ✗ sudo DevToolsSecurity -disable

Developer mode is already disabled.
➜  git-notes-test git:(tl/test) ✗ 
```

* I select to add "sudo" when executing gdb, due to isolate all the permission
  problems.
* I disable the developer mode by `sudo DevToolsSecurity -disable`.
* I add `set startup-with-shell off` into `~/.gdbinit` make sure the zsh could
  not affect the gdb initialization.
