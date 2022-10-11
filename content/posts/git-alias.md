---
title: "The git aliases worth trying"
date: 2022-10-11T14:47:33+08:00
draft: false
tag:
    - git
---

## Get the nice sort of tags

git config --global alias.tags 'tag -l --sort=-version:refname "v*"'
