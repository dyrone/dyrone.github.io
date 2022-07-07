---
title: "Locale and Priority"
date: 2022-07-07T10:38:21+08:00
tags:
    - "libc"
draft: false 
---

## Default settings

The C locale, also known as the POSIX locale, is the POSIX system default locale for all POSIX-compliant systems. The Oracle Solaris operating system is a POSIX system. The Single UNIX Specification, Version 3, defines the C locale. Register to read and download the specification at: http://www.unix.org/version3/online.html.

# Environment Variables

When a program looks up locale dependent values, it does this according to the following environment variables, in priority order:

`LANGUAGE`:

It can be used to set the primary language, if you understand other languages , you can up a priority list of languages, this is done through **LANGUAGE**. GNU `gettext` gives preference to LANGUAGE over LC_ALL and LANG afor the purpose of message handling.

But be noticed, if the locale is set to **C**, the variable **LANGUAGE** is ignored. In other words ,you have to first enable localization, by setting **LANG** or **LC_ALL**** to a value other than 'c', before you can use a language priority list through the **LANGUAGE** variable.

`LC_ALL`:

It is the environment variable t hat overrides all the other i18n settings, export if `LANGUAGE` envs
specified, it's used for specifying a priority list of languages, more at [here](https://www.gnu.org/software/gettext/manual/html_node/The-LANGUAGE-variable.html#The-LANGUAGE-variable "here")

`LC_xxx`:

According to selected locale category: LC_CTYPE, LC_NUMERIC, LC_TIME, LC_COLLATE, LC_MONETARY, LC_MESSAGES, ...

`LANG`

# Demo 

```sh
$LC_ALL=C man
What manual page do you want?

$LC_ALL=es_ES man
Qu pgina de manual desea?

$LC_ALL=zh_CN.UTF-8 man
您需要什么手册页？

```

`sv.de`` is Swedish.

```sh
$LANGUAGE=sv.de LANG=zh_CN.UTF-8 LC_ALL=es_ES man 
Vilken manualsida vill du ha?
```

The `LANGUAGE` variable` is ignored if we set locale as 'C':
```sh
$LANGUAGE=sv.de LANG=zh_CN.UTF-8 LC_ALL=C man 
What manual page do you want?
```
