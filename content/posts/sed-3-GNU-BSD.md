---
title: "Sed Part[3]-'GNU sed' and 'BSD sed'"
date: 2022-07-10T23:55:52+08:00
tags:
    - "sed"
draft: false 
---

## Why exists two seds?

Sed is supported on a number of platforms, including some distributions of Linux that are based on GNU, and some common platforms such as MacOS that are based on BSD.

The distribution quirks cause sed to behave differently on different platforms, mainly on some GNU extensions.

For example the command `q`:

> q [exit-code]
> Exit sed without processing any more commands or input.
> This command accepts only one address. Note that the current pattern space is printed if auto-print is not disabled with the -n options. The ability to return an exit code from the sed script is a GNU sed extension.


If run the following command on MacOS:

```sh
➜  ~ uname -v 
Darwin Kernel Version 19.6.0: Thu Jan 13 01:26:33 PST 2022; root:xnu-6153.141.51~3/RELEASE_X86_6

➜  ~ echo "hello" | sed -e 's/hello/world/g' -e 'q42'; echo $?
sed: 1: "q42
": extra characters at the end of q command
1
```

if run the following command on GNU linux:

```sh
$uname -a
Linux ... SMP Fri Jun 4 21:54:18 CST 2021 x86_64 x86_64 x86_64 GNU/Linux

$echo "hello" | sed -e 's/hello/world/g' -e 'q42'; echo $?
world
42
```


## Using GNU sed extension on Mac

If you want to use GNU sed extension features on Mac, you can use `gsed`

> From: https://www.freebsd.org/cgi/man.cgi?query=gsed&apropos=0&sektion=0&manpath=FreeBSD%209.0-RELEASE%20and%20Ports&arch=default&format=html

Then you can use gsed instead now, then you can execute the command again:
```sh
➜  ~ echo "hello" | gsed -e 's/hello/world/g' -e 'q42'; echo $?                                                                <<<
world
42
```
