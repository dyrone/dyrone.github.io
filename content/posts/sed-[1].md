---
title: "Sed Section[1] - Basic Usage"
date: 2022-07-01T17:00:04+08:00
tag: "sed"
draft: false
---


## About _sed_

The `sed` means as "stream editor", it is used to perform text things from an _input stream_ to an __output stream_.

## Glimpse of _man_ page

> DESCRIPTION
>
> The sed utility reads the specified files, or the
> standard input if no files are specified, modifying the
> input as specified by a list of commands.  The input is then
> written  to the standard output.
>
> A single command may be specified as the first argument to
> sed.  Multiple commands may be specified by using the -e or
> -f options.  All commands are applied to the input 
> the order they are specified regardless of their origin.


Suppress the output, and `p` _command_ to print specific lines.

```shell
➜  /tmp echo 'aabbcc' | sed -n '1p'
aabbcc
➜  /tmp echo 'aabbcc' | sed -n '2p'
➜  /tmp 
```

`$p` command means to ouput the last line of the stream. By the
way, sed treats multiple input files as one long stream.


```shell

# Print the first line of one.txt and the last line of two.txt 
➜  /tmp sed -n '1p;$p' one.txt two.txt
one
end two
```

## Helpful Documentations

It's a good way to use `man sed` to know the options which `sed` supports quickly(but on BSD or GNU released OS, the content maybe exist some difference, like linux and OSX). And also, you can find the official documentations at [here](https://www.gnu.org/software/sed/manual/html_node/index.html "here").

## Know the construct of `sed` command

### Syntax

` sed [-Ealn] [-e command] [-f command_file] [-i extension] [file ...]`

sed commands follow this syntax:

```shell
	[addr]X[options]
```

* X: is a single-letter sed command.
* [addr]: is an optional line address. If specified, the command `X`
  will only executed on the matched lines. [addr] canbe a single line
  number, a regular expression, or a range of lines.


The following example deletes lines 30 to 35 in the input, `30,35` is
an address rage. `d` is the delete command.

```shell
sed ’30,35d’ input.txt > output.txt
```

The following example prints all input until a line starting with the
word "import", then quit with exit code 42. If such line was not
found, sed return with 0. `/^foo/` is a regular expression
address. `q` is the quit command.


```shell
$sed '/^#define/q42' git.c ; echo $?
#include "builtin.h"
#include "config.h"
#include "exec-cmd.h"
#include "help.h"
#include "run-command.h"
#include "alias.h"
#include "shallow.h"

#define RUN_SETUP               (1<<0)
42
```

Commands within a script or script-file can be separated by semicolons (;) or newlines
(ASCII 10). Multiple scripts can be specified with -e or -f options.

The following examples are all equivalent:

```shell
sed ’/^foo/d ; s/hello/world/’ input.txt > output.txt

sed -e ’/^foo/d’ -e ’s/hello/world/’ input.txt > output.txt

echo ’/^foo/d’ > script.sed
echo ’s/hello/world/’ >> script.sed
sed -f script.sed input.txt > output.txt

echo ’s/hello/world/’ > script2.sed
sed -e ’/^foo/d’ -f script2.sed input.txt > output.txt
```
