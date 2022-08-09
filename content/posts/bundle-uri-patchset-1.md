---
title: "[wip] About Bundle Uri Patchset 1"
date: 2022-07-26T16:54:32+08:00
draft: true 
tags: 
  - "git"
---

## Original patchset address

https://lore.kernel.org/git/e0f003e1b5fae07e98e89875c047c795396ea494.1658757188.git.gitgitgadget@gmail.com/

## Directly read  v3 patch

### commit 1: design document

#### Design Goals

> Forgive me to repeat some text from the original patch, because they are
> important.

* bundle: packfile + refs + necessary commits(opt)

* bundle uri: locations where git can download one or more bundles

* benifits: speed up download progress + reduce load on server(heavy users: CI
  build)

* how to enable: using command-line options or server advertise one or mor URIs
  via a protocol v2 capability.
  
* bundle name: to immutable data by using a hash of the bundle contents

* full clone and incremental fetch are supported: the bundle provider must
  decide on one of serveral organization schemes to minimize clietn downloads
  during incrementail fetches. But the git client can also choose whether to use
  bundles for either of these bundles.
  
* partial clone is supported: the bundle provider can choose to support full
  clones, partial clones, or both. The client can detect which bundles are
  appropriate for the repository's partial clone filter, if any.
  
* The bundle provider can use a single bundle (for clones only), or a list of
  bundles. When using a list of bundles, the provider can specify whether or not
  the client need all of the bundle URIs for a full clone, or if any one of the
  bundle URIs is sufficient. This allows the bundle provider to sue different
  URIs for different geographies. 
  
* The bundle provider can organize the bundles using heuristics, such as
  creation tokens, to help the client prevent downloading bundles it does not
  need. When the bundle provider does not provide these heuristics the client
  can use optimizations to minimize how much of the data is downloaded.

* The bundle provider does not need to be associated with the git server. The
  client can choose to use the bundle provider without it being advertised by
  the git server.
  
* The client can choose to discover bundle providers that are advertised by the
  git server. this could happen during  `git clone`, during `git fetch`, both,
  or neither. The user can choose which combination works best for them.

* The client can choose to configure a bundle provider manually at any time. The
  client can also choose to specify  a bundle provider manually as a
  command-line option to `git clone`.

#### Server Design

* protocol: HTTPS only now and expect a 200 returned code  

* authentication: credential helper

* file parse: git attempts to parse the file as a bundle file of version 2 or
higher. if the fileis not a bundle, then the file is parsed as a plain-text file
using git's config parser. The key-value pairs in that config file are expected
to describe a list of bundle URIs. 

#### Bundle lists

Bundle list is a plain-text file in git config format containing these same
key=value pairs. The pairs specify information about the bundles that the client
can use to make decisions for which bundles to download and which to ignore.

* bundle.version: The only current version number is 1

* bundle.mode: "all" or "any"

    ** "all": the client should expect to need all of the listed bundle URIs that match
    their repository's requirements.
    
    ** "any": the client should expect that any one of the bundle URIs that
    match their repository's requirements will suffice. Typically, the "any"
    option is used to list a number of different bundle servers localted in
    different geographies.

* bundle.heuristic (Optional): if this string valued key exists, then the bundle list is
  designed to work well with incremental `git fetch` command.

The remaining keys include an `<id>` segment which is a server-designated
name for each available bundle. The `<id>` must contain only alphanumeric
and `-` characters.
