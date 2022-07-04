---
title: "Make"
date: 2022-06-24T12:03:11+08:00
draft: true
---


## Support custom build options in `config.*` file

Support custom build options in config.* file
```make
include config.mak.uname
-include config.mak.autogen
-include config.mak
```