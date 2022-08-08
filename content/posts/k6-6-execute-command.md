---
title: "k6 series [6] - Execute Command"
date: 2022-08-08T22:44:24+08:00
draft: false 
tags: 
    - "testing"
---

> NOTICE: Base and excerpt from the official k6 documentation 
## install xk6

https://github.com/grafana/xk6

## install xk6-exec extension

https://github.com/grafana/xk6-exec


> Notice the output tips:

```
2022/08/08 23:02:07 [INFO] Cleaning up temporary folder: /Users/tenglong.tl/Works/Projects/blogs/buildenv_2022-08-08-2301.1466088654

xk6 has now produced a new k6 binary which may be different than the command on your system path!
Be sure to run './k6 run <SCRIPT_NAME>' from the '/Users/tenglong.tl/Works/Projects/blogs' directory.
```

A new binary `k6` will be built at current dir. You should move it to your PATH
to make sure you can invoke the command.

```shell
mv /usr/local/bin/k6 /usr/local/bin/k6-prototype
mv ./k6 /usr/local/bin/k6
```


## Example

```jsts
import exec from 'k6/x/exec';

export default function () {
  console.log(exec.command("date"));
  console.log(exec.command("ls",["-a","-l"]));
}
```

The ouput might be like:

```shell
➜  pt-samples git:(master) ✗ k6 run pt-1-0001-stages.ts

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

INFO[0000] 2022年 8月 8日 星期一 23时06分18秒 CST                 source=console
INFO[0000] total 528
drwxr-xr-x    8 tenglong.tl  staff     256  8  4 19:45 .
drwxr-xr-x   11 tenglong.tl  staff     352  8  2 19:54 ..
drwxr-xr-x    4 tenglong.tl  staff     128  8  2 15:04 .log
-rw-r--r--    1 tenglong.tl  staff      57  8  4 19:46 helpers.js
drwxr-xr-x  145 tenglong.tl  staff    4640  8  2 15:50 node_modules
-rw-r--r--    1 tenglong.tl  staff  249907  8  2 19:58 package-lock.json
-rw-r--r--    1 tenglong.tl  staff    4520  8  2 15:50 package.json
-rw-r--r--    1 tenglong.tl  staff     145  8  8 23:01 pt-1-0001-stages.ts  source=console

running (00m00.0s), 0/1 VUs, 1 complete and 0 interrupted iterations
default ✓ [======================================] 1 VUs  00m00.0s/10m0s  1/1 iters, 1 per VU

     data_received........: 0 B 0 B/s
     data_sent............: 0 B 0 B/s
     iteration_duration...: avg=11.17ms min=11.17ms med=11.17ms max=11.17ms p(90)=11.17ms p(95)=11.17ms
     iterations...........: 1   79.687625/s
```
