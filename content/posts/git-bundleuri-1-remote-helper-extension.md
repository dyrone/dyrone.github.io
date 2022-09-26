---
title: "Git Bundleuri 1 Remote Helper Extension"
date: 2022-08-23T15:39:04+08:00
draft: true
tags: 
    - "c"
    - "git"
---

> From: Derrick Stolee <derrickstolee@github.com>
> 
> A future change will want a way to download a file over HTTP(S) using
> the simplest of download mechanisms. We do not want to assume that the
> server on the other side understands anything about the Git protocol but
> could be a simple static web server.
> 
> Create the new 'get' capability for the remote helpers which advertises
> that the 'get' command is avalable. A caller can send a line containing
> 'get <url> <path>' to download the file at <url> into the file at
> <path>.



## New Test Tricks

### test_path_is_missing
  * [ ] 
