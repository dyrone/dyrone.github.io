---
title: "K6 Tags and Groups"
date: 2022-08-04T20:10:11+08:00
draft: true 
tags:
    - "testing"
---

## Tags

k6 provides two types of tags:

* System tags are tags that k6 automatically assigns.
* User-defined tags are tags that you add when you write your script.

### System tags

* **proto**: the name of the protocol used (e.g. HTTP/1.1)
* **subproto**: the subprotocol name (used by websockets)
* **status**: the HTTP status code (e.g. 200, 404, etc.)
* **method**: the HTTP method name (e.g. GET, POST, etc.) or the RPC method name for gRPC
* **url**: the HTTP request URL
* **name**: the HTTP request name [What's 'name'?](https://k6.io/docs/using-k6/http-requests/#url-grouping "What's 'name'?") 
* **group**: the full group path, see the preceding explanation for details
  about its value
* **check**: the Check name
* **error**: a string with a non-HTTP error message (e.g. network or DNS error)
* **error_code****: A number specifying an error types; a list of current error
  codes can be found at the [Error Codes](https://k6.io/docs/javascript-api/error-codes/) page
* tls_**version**: the TLS version
* **scenario**: the name of the scenario where the metric was emitted
* **service**: the RPC service name for gRPC
* **expected_response****: true or false based on the responseCallback; by default

## Overview 

k6 provides two scripting APIs to help you visualize, sort, and filter your test
results.

* Tags categorize your checks, thresholds, custom metrics, and requests for
in-depth filtering. 

* Groups apply tags to the script's functions.

## groups

```jsts
import http from 'k6/http';
import exec from 'k6/execution';
import { group } from 'k6';

export default function () {
  group('visit product listing page', function () {
    // ...
  });
  group('add several products to the shopping cart', function () {
    // ...
  });
  group('visit login page', function () {
    // ...
  });
  group('authenticate', function () {
    // ...
  });
  group('checkout process', function () {
    // ...
  });
}
```

The output:

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


running (00m00.0s), 0/1 VUs, 1 complete and 0 interrupted iterations
default ✓ [======================================] 1 VUs  00m00.0s/10m0s  1/1 iters, 1 per VU

     █ visit product listing page

     █ add several products to the shopping cart

     █ visit login page

     █ authenticate

     █ checkout process

     data_received........: 0 B 0 B/s
     data_sent............: 0 B 0 B/s
     group_duration.......: avg=541ns    min=197ns    med=262ns    max=1.68µs   p(90)=1.13µs   p(95)=1.41µs  
     iteration_duration...: avg=138.58µs min=138.58µs med=138.58µs max=138.58µs p(90)=138.58µs p(95)=138.58µs
     iterations...........: 1   705.716302/s
```

## User-defined tags and nested groups

You can tag the following entities:

* requests
* checks
* thresholds
* custom metrics

```jsts
import http from 'k6/http';
import exec from 'k6/execution';
import { group } from 'k6';

export const options = {
  thresholds: {
    'http_reqs{test:main}': ['count==3'],
    'http_req_duration{test:main}': ['max<1000'],
  },
};

export default function () {
  exec.vu.tags.test = 'main';

  group('main', function () {
    http.get('https://test.k6.io');
    http.get('https://test.k6.io');
    group('sub', function () {
      http.get('https://httpbin.test.k6.io/anything');
    });
    // http.get('https://test-api.k6.io');
  });

  delete exec.vu.tags.test;

  http.get('https://httpbin.test.k6.io/delay/3');
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
                                                                                                                                                                                             

running (00m05.0s), 0/1 VUs, 1 complete and 0 interrupted iterations                          
default   [======================================] 1 VUs  00m05.0s/10m0s  1/1 iters, 1 per VU                                                                                                
                                                                                                                                                                                             
     █ main                                                                                   
                                                                                              
       █ sub                                                                                  
                                                                                              
     data_received..................: 35 kB  7.0 kB/s                                         
     data_sent......................: 1.1 kB 221 B/s                                          
     group_duration.................: avg=1.28s    min=815.18ms med=1.28s    max=1.75s    p(90)=1.65s    p(95)=1.7s                                                                          
     http_req_blocked...............: avg=255.91ms min=3µs      med=240.1ms  max=543.46ms p(90)=524.48ms p(95)=533.97ms                                                                      
     http_req_connecting............: avg=131.07ms min=0s       med=112.57ms max=299.14ms p(90)=276.94ms p(95)=288.04ms                                                                      
     http_req_duration..............: avg=1s       min=227.93ms med=250.72ms max=3.27s    p(90)=2.37s    p(95)=2.82s                                                                         
       { expected_response:true }...: avg=1s       min=227.93ms med=250.72ms max=3.27s    p(90)=2.37s    p(95)=2.82s                                                                         
     ✓ { test:main }................: avg=243.13ms min=227.93ms med=229.85ms max=271.6ms  p(90)=263.25ms p(95)=267.42ms                                                                      
     http_req_failed................: 0.00%  ✓ 0        ✗ 4                                   
     http_req_receiving.............: avg=167.25µs min=59µs     med=122.5µs  max=365µs    p(90)=296.3µs  p(95)=330.64µs                                                                      
     http_req_sending...............: avg=49.49µs  min=18µs     med=46.5µs   max=87µs     p(90)=78.6µs   p(95)=82.79µs                                                                       
     http_req_tls_handshaking.......: avg=123.91ms min=0s       med=121.36ms max=252.9ms  p(90)=249.85ms p(95)=251.38ms                                                                      
     http_req_waiting...............: avg=1s       min=227.76ms med=250.44ms max=3.27s    p(90)=2.37s    p(95)=2.82s                                                                         
     http_reqs......................: 4      0.795586/s                                       
     ✓ { test:main }................: 3      0.596689/s                                                                                                                                      
     iteration_duration.............: avg=5.02s    min=5.02s    med=5.02s    max=5.02s    p(90)=5.02s    p(95)=5.02s                                                                         
     iterations.....................: 1      0.198896/s                                       
     vus............................: 1      min=1      max=1                                 
     vus_max........................: 1      min=1      max=1
```


