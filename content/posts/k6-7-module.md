---
title: "k6 series [7] - Module"
date: 2022-08-08T23:52:08+08:00
draft: false
tags:
    - "testing"
---

> NOTICE: Base and excerpt from the official k6 documentation 

## Modules 

There are three types of modules:

* Builtin 
* Local file system
* Remote HTTP(s) 

## Builtin modules

These modules are provided through the k6 core, and gives access to the
functionality built into k6.

```jsts
import http from 'k6/http';
```

## Local filesystem modules

```jsts
// helpers.js
export function printHello(){
    console.log("hello");
}
```

```jsts
import http from 'k6/http';
import { printHello } from './helpers.js'

export default function () {
  printHello();
}
```
The output might like:

```shell
     /\  /  \     |  |/  /   /  /    
    /  \/    \    |     (   /   ‾‾\  
   /          \   |  |\  \ |  (‾)  | 
  / __________ \  |__| \__\ \_____/ .io

  execution: local
     script: pt-1-0001-stages.ts
     output: -

  scenarios: (100.00%) 1 scenario, 1 max VUs, 10m30s max duration (incl. graceful stop):
           * default: 1 iterations for each of 1 VUs (maxDuration: 10m0s, gracefulStop: 30s)

INFO[0000] hello                                         source=console

running (00m00.0s), 0/1 VUs, 1 complete and 0 interrupted iterations
default ✓ [======================================] 1 VUs  00m00.0s/10m0s  1/1 iters, 1 per VU

     data_received........: 0 B 0 B/s
     data_sent............: 0 B 0 B/s
     iteration_duration...: avg=80.16µs min=80.16µs med=80.16µs max=80.16µs p(90)=80.16µs p(95)=80.16µs
     iterations...........: 1   1088.139282/s
```

## Remote HTTP(S) modules

These modules are accessed over HTTP(S), from a source like the k6 JSLib or from
any publicly accessible web server. The imported modules will be downloaded and
executed at runtime, making it extremely important to make sure the code is
legit and trusted before including it in a test script.

```jsts
import { randomString } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export default function () {
  console.log(randomString(6));
}
```

The output will be like on my env:

```shell
         /\      |‾‾| /‾‾/   /‾‾/   
     /\  /  \     |  |/  /   /  /    
    /  \/    \    |     (   /   ‾‾\  
   /          \   |  |\  \ |  (‾)  | 
  / __________ \  |__| \__\ \_____/ .io

  execution: local
     script: pt-1-0001-stages.ts
     output: -

  scenarios: (100.00%) 1 scenario, 1 max VUs, 10m30s max duration (incl. graceful stop):
           * default: 1 iterations for each of 1 VUs (maxDuration: 10m0s, gracefulStop: 30s)

INFO[0000] fborfd                                        source=console

running (00m00.0s), 0/1 VUs, 1 complete and 0 interrupted iterations
default ✓ [======================================] 1 VUs  00m00.0s/10m0s  1/1 iters, 1 per VU

     data_received........: 0 B 0 B/s
     data_sent............: 0 B 0 B/s
     iteration_duration...: avg=144.76µs min=144.76µs med=144.76µs max=144.76µs p(90)=144.76µs p(95)=144.76µs
     iterations...........: 1   989.119683/s
```
