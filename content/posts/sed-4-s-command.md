---
title: "Sed [4] - The 's' Commands"
date: 2022-08-13T13:22:26+08:00
draft: false 
tags:
    - "sed"
    - "linux"
---

## Sed command-line execution format

```
sed OPTIONS... [SCRIPT] [INPUTFILE...]
```

Here the command-line format contains:

* `OPTIONS`: the command-line options

* `[SCRIPT]`: the rules we want to deal with the inputstream

* `[INPUTFILE]`: the FD we want to output to, by default it's `stdout`


## SCRIPT

Sed script constructs by three parts:

````
[addr]X[options]
```

* `addr`: an optional line address.

* `X`: a single letter **sed command**, be noticeable that the sed command here
  is not the same as **sed command-line command**.

* `options` used for some **sed** commands.

The following example deletes lines 30 to 35 in the input. 30,35 is an address range. d is the delete command:

```shell
sed ’30,35d’ input.txt > output.txt
```


Exit with 42 if fould a line starting with 'foo':

```shell
sed ’/^foo/q42’ input.txt > output.txt
```
## Multiple sed commands in script 

Sed command can be separated by semicolons(`;`) or newline(ASCII 10).

The following example performs two sed commands: using `d` command to delete the
mapping lines by given regular expression, using `s` to replace all the
occurrence of 'hello' to 'world'.

```shell
sed ’/^foo/d ; s/hello/world/’ input.txt > output.txt
```

## Multiple sed scripts in cmd-line execution

Another way is to specify multiple sed scripts by `-e` or `-f`:

```shell
sed -e ’/^foo/d’ -e ’s/hello/world/’ input.txt > output.txt
```

Or： 

```shell
echo ’/^foo/d’ > script.sed
echo ’s/hello/world/’ >> script.sed
sed -f script.sed input.txt > output.txt
```

Or:

```shell

echo ’s/hello/world/’ > script2.sed
sed -e ’/^foo/d’ -f script2.sed input.txt > output.txt
```

## The `s` command


The `s` command almost the most frequently used one in `sed` world. The syntax
of the `s` command is :

```
s/regexp/replacement/flags
```


### replacement 

* **\n**: **n** is a number from 1 to 9, which refer to the portion of the
  match which is contained between the `nth` \( and its matching\). 

* **&**: reference the whole matched portion of the pattern space.

* **case replacements**:

    * `\L`: Turn the replacement to lowercase until a \U or \E is found
    * `\l` Turn the next character to lowercase
    * `\U` Turn the replacement to uppercase until a \L or \E is found
    * `\u` Turn the next character to uppercase
    * `\E` Stop case conversion started by \L or \U

For example, the following script will replace 'a-b-' to 'axxB':

```
s/\(b\?\)-/x\u\1/g
```

The following script will replace 'a-b-' to 'aXBx':

```
s/\(b\?\)-/\u\1x/g
```

The following script will replace 'a-b-' to 'axBx':
```
s/\(b\?\)-/\u\1\Ex/g
```
> ESCAPE: To include a literal `\`, `&`, newline in replacement, be sure to

> precede the desired literal char with a `\`.


### flags

#### Flag **g**

> propergate from one occurrence of the regex to anot


#### Flag **<number>**

> Only replace the numberth match of the regexp. interaction in s command Note:
> the posix standard does not specify what should happen when you mix the g and
> number modifiers, and currently there is no widely agreed upon meaning across
> sed implementations. For GNU sed, the interaction is defined to be: ignore
> matches before the numberth, and then match and replace all matches from the
> numberth on.

```shell
echo -n 'aabbcc' | gsed 's/\(a\)/x/2'
axbbcc
```

#### Flag **p**

> If the substitution was made, then print the new pattern space.

```shell
➜  blogs git:(master) ✗ echo -n 'aabbcc' | gsed 's/\(a\)/x/2p'
axbbcc
axbbcc
➜  blogs git:(master) ✗ echo -n 'aabbcc' | gsed 's/\(x\)/x/2p'
aabbcc
```

#### Flag: **w**

```shell
➜  blogs git:(master) ✗ echo  'aabbcc' | gsed 's/\(x\)/x/w/dev/stderr'
aabbcc
```

If the substitution was made, then write out the result to the named file. As a
GNU sed extension, two special values of filename are supported: /dev/stderr,
which writes the result to the standard error, and /dev/stdout, which writes 3
to the standard output.

### Flag **e**

This command allows one to pipe input from a shell command into pattern space.
If a substitution was made, the command that is found in pattern space is
executed and pattern space is replaced with its output. A trailing newline is
suppressed; results are undefined if the command to be executed contains a nul
character. This is a GNU sed extension.

```shell
➜  blogs git:(master) ✗ echo 'ls' |gsed 's/ls/ls -l\n/e'
total 16
-rw-r--r--   1 tenglong.tl  staff   242  7 31 23:15 README.md
drwxr-xr-x   3 tenglong.tl  staff    96  3  7 14:37 archetypes
-rw-r--r--   1 tenglong.tl  staff  3647  6 15 21:27 config.toml
drwxr-xr-x   4 tenglong.tl  staff   128  3  7 17:35 content
drwxr-xr-x   2 tenglong.tl  staff    64  3  7 14:37 data
drwxr-xr-x  16 tenglong.tl  staff   512  8  9 18:56 docs
drwxr-xr-x   2 tenglong.tl  staff    64  3  7 14:37 layouts
drwxr-xr-x   3 tenglong.tl  staff    96  3  7 14:44 resources
drwxr-xr-x   2 tenglong.tl  staff    64  3  7 14:37 static
drwxr-xr-x   3 tenglong.tl  staff    96  7  6 12:14 test
drwxr-xr-x   3 tenglong.tl  staff    96  3  7 15:44 themes
```

The suppressed newline:

```shell
echo -n 'ls' |gsed 's/ls/\n/e'
# no newline is printed
```

#### Flag **I** and **i**


The I modifier to regular-expression matching is a GNU extension which makes sed
match regexp in a case-insensitive manner.

```shell
➜  blogs git:(master) ✗ echo -n 'LS' |gsed 's/ls/printf dyrone/ei'
dyrone
➜  blogs git:(master) ✗ echo -n 'LS' |gsed 's/ls/printf dyrone/e'
LS
```

#### Flag **M** and **m**

The M modifier to regular-expression matching is a GNU sed extension which
directs GNU sed to match the regular expression in multi-line mode. The mod-
ifier causes ^ and $ to match respectively (in addition to the normal behavior)
the empty string after a newline, and the empty string before a newline. There
are special character sequences (\‘ and \’) which always match the beginning or
the end of the buffer. In addition, the period character does not match a
new-line character in multi-line mode.
