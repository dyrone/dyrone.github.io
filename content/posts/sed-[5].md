---
title: "Sed Section[4]"
date: 2022-07-03T16:21:44+08:00
draft: true 
---


# sed commands

There are three usual kinds of command:

* support by GNU sed
* GNU extension
* standard POSIX commands

 ## `s` command

The syntax is : 

	‘s/regexp/replacement/flags’

* regexp:
  https://www.gnu.org/software/sed/manual/html_node/Regexp-Addresses.html#Regexp-Addresses
  
* replacement:

	* contain *\n*: n is a number from 1 to 9  reference, refer to the
      portion.
	* can contain *&* characters which reference the whole matched
      portion of the pattern space.
	* */* characters may be uniformly replaced by `s` command. It can
      appear in regexp or replacement only if it is preceded by a `\`
      character.
	* GNU sed extension:
		
		* `\L`: Turn the replacement to lowercase until a \U or \E is
          found,
		* `\l`: Turn the next character to lowercase,
		* `\U`: Turn the replacement to uppercase until a \L or \E is
          found,
		* `\u`: Turn the next character to uppercase,
		* `\E`: Stop case conversion started by \L or \U.
	* `g`: case conversion does not propagate from one occurrence of
      the regular expression to another. For example:
	  
	  ```shell
	  $ echo 'a-b-' | sed 's/\(b\?\)-/x\u\1/g'
      axxB
	  
	  $ echo 'a-b-' | sed 's/\(b\?\)-/\u\1x/g'
	  aXBx
	  
	  ```

The first example: the output is ‘axxB’. When replacing the first ‘-’, the ‘\u’ 
sequence only affects the empty replacement of ‘\1’. It does not affect the x
character that is added to pattern space when replacing b- with xB.

The second example: On the other hand, \l and \u do affect the remainder of the
replacement text if they are followed by an empty substitution. It will will
replace ‘-’ with ‘X’ (uppercase) and ‘b-’ with ‘Bx’. If this behavior is
undesirable, you can prevent it by adding a ‘\E’ sequence—after ‘\1’ in this case.


> flag: `g`

Apply the replacement to all matches to the regexp, not just the first.

```shell
$ echo 'a-b-' | sed 's/-/=/'
a=b-

$ echo 'a-b-' | sed 's/-/=/g'
a=b=

```

> flag: `number`

Only replace the numberth match of the regexp.

```shell
$ echo 'a-b-' | sed 's/-/=/2'
a-b=

```

> flag: `p`

If the substitution was made, then print the new pattern space.

```shell
$ echo 'a-b-' | sed 's/=/=/p'
a-b-

$ echo 'a-b-' | sed 's/-/=/p'
a=b-
a=b-

```

> flag: `w` *filename*

If the substitution was made, then write out the result to the named file.

the special filename are supported:

* /dev/stderr
* /dev/stdout
* /dev/null

```shell
➜  /tmp cat sed.output 
a-b-
➜  /tmp sed 's/-/=/w /dev/stdout' < sed.output
a=b-
a=b-
➜  /tmp sed 's/-/=/w /dev/null' < sed.output
a=b-
```

> flag `e`

This command is a GNU sed extension, so it may not supported to execute on MacOS terminal env.

This command allows one to pipe input from a shell command into pattern
space. If a substitution was made, the command that is found in pattern space
is executed and pattern space is replaced with its output. A trailing newline
is suppressed; results are undefined if the command to be executed contains a
nul character. This is a GNU sed extension.

<todo> I did not understand how to do with it yet.

> flag `I` `i`

`I` is a GNU extension, and makes sed match regexp in case-insensitive manner. 

The tip you should be noticed is some OS does not support the `GNU extension`, so
when we want to use it in different platform, the usages may cause incompatible as
a failed sed command execution.

> flag `M` `m`

This is a GNU extension, directs GNU sed to match the regular expression in multi-line mode.

<!-- TODO

The modifier causes ^ and $ to match respectively (in addition to the normal behavior)
the empty string after a newline, and the empty string before a newline. There
are special character sequences (\‘ and \’) which always match the beginning
or the end of the buffer. In addition, the period character does not match a
new-line character in multi-line mode.




# `-e`

`-e` is short for `--expression`, `-e` will specify the option value
as the script and  treats all the following  non-option parameters as
input files.  Without `-e` or `-f` options, sed uses the first
non-option parameter as the script, and the following non-option
parameters as input files.

```
sed -e ’s/hello/world/’ input.txt > output.txt
sed --expression=’s/hello/world/’ input.txt > output.txt

echo ’s/hello/world/’ > myscript.sed
sed -f myscript.sed input.txt > output.txt
sed --file=myscript.sed input.txt > output.txt
```


> Append the editing commands specified by the command argument to the list
> of commands.                                                                                                    

git version | sed -e 's/^git version //'



# references

* https://www.gnu.org/software/sed/manual/html_node/index.html
