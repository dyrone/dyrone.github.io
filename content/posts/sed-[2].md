
---
title: "Sed Section[2] - Exit Code In Sed"
date: 2022-07-03T17:00:04+08:00
tags: 
    - "sed"
draft: false
---

In this article, we will talk about the exit code when executing **sed** command.

# Exit Code: 0

When the sed command executes successfully, the execution will exit as **0** which means the procedure is now as completion.

The result is the same whether the sed is matched or unmatched, the exit code only take the responsibility for the running correctness but not the matching logicalness. For an example:

``` sh
➜   echo 'abc' | sed -e 's/d/e/1'                                                         <<<
abc
➜  echo 'abc' | sed -e 's/b/e/1'                                                         <<<
aec
```

# Exit Code: 1

Code 1 means you are executing an invalid command, invalid syntax, invalid regular expression or a GNU sed extension command used with `--posix` 

## invalid command

For example, we specify an invalid option `-x`, the following execution will exit with code **1**:
``` sh
➜ echo 'abc' | sed -x 's/b/e/1' ; echo
sed: illegal option -- x
usage: sed script [-Ealn] [-i extension] [file ...]
       sed [-Ealn] [-i extension] [-e script] ... [-f script_file] ... [file ...]
1
```

## invalid syntax

For example, we specify an invalid substitute flag, the following execution will exit with code **1**:

``` sh
➜  posts git:(master) ✗ echo 'abc' | sed -e 's/b/e/1/' ; echo $? 
sed: 1: "s/b/e/1/
": bad flag in substitute command: '/'
1
```

## invalid regular expression

For example, by default the regular expression of sed is not allowd yo be empty, so the following execution will exit with code **1**:

```sh
➜  posts git:(master) ✗ echo 'abc' | sed -e 's//replacement/1' ; echo $?                                 sed: first RE may not be empty
1
```

# Exit Code: 2 

## input file could not be opened

e.g. if a file is not found, or read permission is denied,

For example, we specify an unexist input file which named **input.txt**, and the execution result is:
```sh
# sed 's/1/2/g' input.txt
sed: can't read input.txt: No such file or directory
# echo $?
2
# uname -a
Linux 94cb2f1a7253 4.19.76-linuxkit #1 SMP Tue May 26 11:42:35 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
```

Unfortunately, the result is different if I execute the same command on my Mac, the result will be like:

```sh
➜  /tmp sed 's/1/2/g' input.txt ; echo $?
sed: input.txt: No such file or directory
1

➜  /tmp sed '1p' unexist.file ; echo $?
sed: unexist.file: No such file or directory
1
```

But why and what happended to the Mac-sed? This is because the **sed** on Mac is not a GNU sed, and so on, Mac doesn't support the GNU extension too. The detailed information I will write on the following article.``

# Exit Code: 4

When An I/O error occured, or a serious **processing** error during runtime, GNU sed will be aborted immediately with **4**.

# Custom Exit Code

This is a GNU sed extension, **q** and **Q** can be used to terminate **sed** with a custom exit code value.

``` sh
$ echo 'abc' | sed -e 'q42' -e 's/a/A/g' ; echo $?
abc
42
```

And then, as the tips before, If I execute is on my Mac, the `q` can not be recognized by **sed** and will return the **1** as exit code. 
