---
title: "Exit Status"
date: 2022-10-11T14:47:33+08:00
draft: false 
tag:
    - bash
---

## Description of GNU doc

The exit status of an executed command is the value returned by the waitpid
system call or equivalent function. Exit statuses fall between 0 and 255,
though, as explained below, the shell may use values above 125 specially. Exit
statuses from shell builtins and compound commands are also limited to this
range. Under certain circumstances, the shell will use special values to
indicate specific failure modes.

For the shell’s purposes, a command which exits with a zero exit status has
succeeded. A non-zero exit status indicates failure. This seemingly
counter-intuitive scheme is used so there is one well-defined way to indicate
success and a variety of ways to indicate various failure modes. When a command
terminates on a fatal signal whose number is N, Bash uses the value 128+N as the
exit status.

If a command is not found, the child process created to execute it returns a
status of 127. If a command is found but is not executable, the return status is
126.

If a command fails because of an error during expansion or redirection, the exit
status is greater than zero.

The exit status is used by the Bash conditional commands (see Conditional
Constructs) and some of the list constructs (see Lists of Commands).

All of the Bash builtins return an exit status of zero if they succeed and a
non-zero status on failure, so they may be used by the conditional and list
constructs. All builtins return an exit status of 2 to indicate incorrect usage,
generally invalid options or missing arguments.

The exit status of the last command is available in the special parameter $?
(see Special Parameters).

> From https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html

## Exit Codes With Special Meanings

|  Exit Code Number  | Meaning | Example | Comments  |
|:--|:--|:--|:--|
| 1  | Catchall for general errors   | let "var1 = 1/0"	  | Miscellaneous errors, such as "divide by zero" and other impermissible operations|
| 2  | Misuse of shell builtins (according to Bash documentation) | empty_function() {}	| Missing keyword or command, or permission problem (and diff return code on a failed binary file comparison). |
| 126  | Command invoked cannot execute	| /dev/null	| Permission problem or command is not an executable |
| 127  | "command not found"  | illegal_command | Possible problem with $PATH or a typo  |
| 128  | Invalid argument to exit | exit 3.14159  | exit takes only integer args in the range 0 - 255 (see first footnote)  |
| 128+n  | Fatal error signal "n"  | kill -9 $PPID of script  | $? returns 137 (128 + 9)  |
| 130  | Script terminated by Control-C	  | Ctl-C | Control-C is fatal error signal 2, (130 = 128 + 2, see above)  |
| 255* | Exit status out of range  | exit -1  | exit takes only integer args in the range 0 - 255  |

According to the above table, exit codes 1 - 2, 126 - 165, and 255 [1] have
special meanings, and should therefore be avoided for user-specified exit
parameters. Ending a script with exit 127 would certainly cause confusion when
troubleshooting (is the error code a "command not found" or a user-defined
one?). However, many scripts use an exit 1 as a general bailout-upon-error.
Since exit code 1 signifies so many possible errors, it is not particularly
useful in debugging.


There has been an attempt to systematize exit status numbers (see
/usr/include/sysexits.h), but this is intended for C and C++ programmers. A
similar standard for scripting might be appropriate. The author of this document
proposes restricting user-defined exit codes to the range 64 - 113 (in addition
to 0, for success), to conform with the C/C++ standard. This would allot 50
valid codes, and make troubleshooting scripts more straightforward. [2] All
user-defined exit codes in the accompanying examples to this document conform to
this standard, except where overriding circumstances exist, as in Example 9-2.

Issuing a $? from the command-line after a shell script exits gives results
consistent with the table above only from the Bash or sh prompt. Running the
C-shell or tcsh may give different values in some cases.

> From: https://tldp.org/LDP/abs/html/exitcodes.html#FTN.AEN23629


