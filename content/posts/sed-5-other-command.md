---
title: "[WIP]Sed  [5] The other Commands"
date: 2022-08-15T11:56:21+08:00
draft: false
tags: 
    - "linux"
    - "sed"
---



## Command **#**


The following example show to use sed to comment the options will affect the
final result: 

```shell
➜  blogs git:(master) ✗ echo 'ls' |gsed 's/ls/ls #-a/e'
README.md
archetypes
config.toml
content
data
docs
layouts
resources
static
test
themes
➜  blogs git:(master) ✗ echo 'ls' |gsed 's/ls/ls -a/e' 
.
..
.git
.gitignore
.gitmodules
README.md
archetypes
config.toml
content
data
docs
layouts
resources
static
test
themes
```

or we could append the comments after each print out:

```shell
➜  blogs git:(master) ✗ seq 3 |gsed 'a# do a respectively print out '
1
# do a respectively print out 
2
# do a respectively print out 
3
# do a respectively print out 
```

## Command **q**

> This command accepts only one address

Exit sed without processing any more commands or input.The ability to return an
exit code from the sed script is a GNU sed extension.

```shell
➜  blogs git:(master) ✗ seq 3 |gsed 2q3
1
2
➜  blogs git:(master) ✗ echo $?
3
```

## Command **d**

```shell
➜  blogs git:(master) ✗ seq 3 |gsed 2d                               
1
3
```

## Command **p**

Print out the pattern space (to the standard output). This command is usually only used in conjunction with the -n command-line option.
Example: print only the second input line:

```shell
➜  blogs git:(master) ✗ seq 3 | gsed 2p
1
2
2
3
➜  blogs git:(master) ✗ seq 3 | gsed -n  2p
2
```

## Command **n**

> This command is useful to skip lines (e.g. process every Nth line).

If auto-print is not disabled, print the pattern space, then, regardless,
replace the pattern space with the next line of input. If there is no more input
then sed exits without processing any more commands.

```shell
$ seq 6 | sed 'n;n;s/./x/'
1
2
x
4
5
x
```

> GNU sed provides an extension address syntax of first~step to achieve the same
> result:

```
$ seq 6 | sed '0~3s/./x/'
1
2
x
4
5
x
```

### { commands }

A group of commands may be enclosed between { and } characters. This is particularly useful when you want a group of commands to be triggered by a single address (or address-range) match.

Example: perform substitution then print the second input line:

```shell
$ seq 3 | sed -n '2{s/2/X/ ; p}' X
```


### Command **y/source-chars/dest-chars/**


Transliterate any characters in the pattern space which match any of the
source-chars with the corresponding character in dest-chars.

Example: transliterate ‘a-j’ into ‘0-9’:

```
$ echo hello world | sed 'y/abcdefghij/0123456789/'
74llo worl3
```

(The / characters may be uniformly replaced by any other single character within
any given y command.) Instances of the / (or whatever other character is used in
its stead), \, or newlines can appear in the source-chars or dest-chars lists,
provide that each instance is escaped by a \. The source-chars and dest-chars
lists must contain the same number of characters (after de-escaping). See the tr
command from GNU coreutils for similar functionality.


```shell
➜  blogs git:(master) ✗ echo -n 'hello worldx' | gsed 'y/abcdefghijx/0123456789\n/'
74llo worl3
➜  blogs git:(master) ✗ 
```


### Command **a** and **a\**
Appending text after a line. This is a GNU extension to the standard a com-
mand - see below for details. Example: Add the word ‘hello’ after the second
line:

```shell
➜  blogs git:(master) ✗ seq 3 | gsed '2a hello'
1
2
hello
3
```

The command resume after the last line without a `\` ‘world’ in following
example:

```shell
➜  blogs git:(master) ✗ seq 3 | sed '2a\
pipe quote> hello\
pipe quote> world
pipe quote> 3s/./X/'
1
2
hello
world
X
```
 
### Command **i** and **i\**

insert text before a line. This is a GNU extension to the standard i command -
see below for details. Example: Insert the word ‘hello’ before the second line:

```shell
$ seq 3 | sed '2i hello'
1
hello
2
3
```
