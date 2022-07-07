---
title: "Locale and Priority"
date: 2022-07-07T10:38:21+08:00
tags:
    - "libc"
draft: false 
---

## Scenarios

I found an article which represent well about the locale commu uses I think, and I will excerpt part from [Differences between the C Locale and the C++ Locales](https://stdcxx.apache.org/doc/stdlibug/24-3.html "Differences between the C Locale and the C++ Locales")

> **Default locale.** As a developer, you may never require internationalization features, and thus you may never call std::setlocale(). If you can safely assume that users of your applications are accommodated by the classic US English ASCII behavior, you have no need for localization. Without even knowing it, you always use the default locale, which is the US English ASCII locale.
> 
> **Native locale.** If you do plan on localizing your program, the appropriate strategy may be to retrieve the native locale once at the beginning of your program, and never, ever change this setting again. This way your application adapts itself to one particular locale, and uses this throughout its entire runtime. Users of such applications can explicitly set their favorite locale before starting the application. On UNIX systems, they do this by setting environment variables such as LANG; other operating systems may use other methods.
> 
> In your program, you can specify that you want to use the user's preferred native locale by calling std::setlocale("") at startup, passing an empty string as the locale name. The empty string tells setlocale to use the locale specified by the user in the environment.
> 
> **Multiple locales.** It may well happen that you do have to work with multiple locales. For example, to implement an application for Switzerland, you might want to output messages in Italian, French, and German. As the C locale is a global data structure, you must switch locales several times.
> 
> Let's look at an example of an application that works with multiple locales. Imagine an application that prints invoices to be sent to customers all over the world. Of course, the invoices must be printed in the customer's native language, so the application must write output in multiple languages. Prices to be included in the invoice are taken from a single price list. If we assume that the application is used by a US company, the price list is in US English.
> 
> The application reads input (the product price list) in US English, and writes output (the invoice) in the customer's native language, say German. Since there is only one global locale in C that affects both input and output, the global locale must change between input and output operations. Before a price is read from the English price list, the locale must be switched from the German locale used for printing the invoice to a US English locale. Before inserting the price into the invoice, the global locale must be switched back to the German locale. To read the next input from the price list, the locale must be switched back to English, and so forth. Figure 6 summarizes this activity.
> 

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
