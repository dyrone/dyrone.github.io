---
title: "k6 series [3] - Tags And Groups"
date: 2022-08-04T20:10:11+08:00
draft: false 
tags:
    - "testing"
---

> NOTICE: Base and excerpt from the official k6 documentation 
## Overview 

k6 provides two scripting APIs to help you visualize, sort, and filter your test
results.

* Tags categorize your checks, thresholds, custom metrics, and requests for
in-depth filtering. 

* Groups apply tags to the script's functions.

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


## Test-wide tags

Besides attaching tags to requests, checks, and custom metrics, you can set
test-wide tags across all metrics. You can set these tags in two ways:

* In the CLI, using one or more --tag NAME=VALUE flags

* In the script itself:

```jsts
export const options = {
  tags: {
    name: 'value',
  },
};
```


### User-defined tags

You can define your own tags to categorize k6 entities based on your test logic.
You can tag the following entities:

* requests
* checks
* thresholds
* custom metrics

There is an example:

```jsts
import http from 'k6/http';
import { Trend } from 'k6/metrics';
import { check } from 'k6';


export const options = {
  scenarios: {
    dyrone: {
      executor: 'constant-vus',
      vus: 1,
      duration: '1s',
    }
  }
}

const myTrend = new Trend('my_trend');

export default function () {
  // Add tag to request metric data
  const res = http.get('http://httpbin.test.k6.io/', {
    tags: {
      my_tag: "I'm a tag",
    },
  });

  const timeoutRes = http.get('http://1.2.3.4/', {
    tags: {
      my_tag: "I'm a connectTimeout tag",
    },
    timeout: "3s"
  });

  // Add tag to check
  check(res, { 'status is 200': (r) => r.status === 200 }, { my_tag: "I'm a tag" });

  // Add tag to custom metric
  myTrend.add(res.timings.connecting, { my_tag: "I'm a tag" });
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

  scenarios: (100.00%) 1 scenario, 1 max VUs, 31s max duration (incl. graceful stop):
           * dyrone: 1 looping VUs for 1s (gracefulStop: 30s)

WARN[0004] Request Failed                                error="Get \"http://1.2.3.4/\": request timeout"

running (04.3s), 0/1 VUs, 1 complete and 0 interrupted iterations
dyrone ✓ [======================================] 1 VUs  1s

     ✓ status is 200

     checks.........................: 100.00% ✓ 1        ✗ 0  
     data_received..................: 16 kB   3.7 kB/s
     data_sent......................: 575 B   135 B/s
     http_req_blocked...............: avg=278.91ms min=0s       med=375.84ms max=460.88ms p(90)=443.87ms p(95)=452.37ms
     http_req_connecting............: avg=139.94ms min=0s       med=197.24ms max=222.59ms p(90)=217.52ms p(95)=220.06ms
     http_req_duration..............: avg=142.42ms min=0s       med=196.92ms max=230.34ms p(90)=223.66ms p(95)=227ms   
       { expected_response:true }...: avg=213.63ms min=196.92ms med=213.63ms max=230.34ms p(90)=227ms    p(95)=228.67ms
     http_req_failed................: 33.33%  ✓ 1        ✗ 2  
     http_req_receiving.............: avg=549.99µs min=0s       med=109µs    max=1.54ms   p(90)=1.25ms   p(95)=1.39ms  
     http_req_sending...............: avg=82.33µs  min=0s       med=39µs     max=208µs    p(90)=174.2µs  p(95)=191.09µs
     http_req_tls_handshaking.......: avg=79.39ms  min=0s       med=0s       max=238.19ms p(90)=190.55ms p(95)=214.37ms
     http_req_waiting...............: avg=141.79ms min=0s       med=196.61ms max=228.76ms p(90)=222.33ms p(95)=225.54ms
     http_reqs......................: 3       0.702815/s
     iteration_duration.............: avg=4.26s    min=4.26s    med=4.26s    max=4.26s    p(90)=4.26s    p(95)=4.26s   
     iterations.....................: 1       0.234272/s
     my_trend.......................: avg=111.299  min=0        med=111.299  max=222.598  p(90)=200.3382 p(95)=211.4681
     vus............................: 1       min=1      max=1
     vus_max........................: 1       min=1      max=1
```

## Groups

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

## Code-defined tags and nested groups

```jsts
import http from 'k6/http';
import exec from 'k6/execution';
import { group } from 'k6';

export const options = {
  thresholds: {
    'http_reqs{container_group:main}': ['count==3'],
    'http_req_duration{container_group:main}': ['max<1000'],
  },
};

export default function () {
  exec.vu.tags.containerGroup = 'main';

  group('main', function () {
    http.get('https://test.k6.io');
    group('sub', function () {
      http.get('https://httpbin.test.k6.io/anything');
    });
    http.get('https://test-api.k6.io');
  });

  delete exec.vu.tags.containerGroup;

  http.get('https://httpbin.test.k6.io/delay/3');
}
```

The output might like:

```shell
➜  pt-samples git:(master) ✗ k6 run  pt-1-0001-stages.ts

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


running (00m02.8s), 0/1 VUs, 1 complete and 0 interrupted iterations
default ✓ [======================================] 1 VUs  00m02.8s/10m0s  1/1 iters, 1 per VU

     █ main

       █ sub

     data_received..................: 44 kB  16 kB/s
     data_sent......................: 1.3 kB 487 B/s
     group_duration.................: avg=1.79s    min=820.77ms med=1.79s    max=2.76s    p(90)=2.56s    p(95)=2.66s   
     http_req_blocked...............: avg=685.71ms min=604.44ms med=720.5ms  max=732.19ms p(90)=729.85ms p(95)=731.02ms
     http_req_connecting............: avg=235.17ms min=211.68ms med=228.33ms max=265.5ms  p(90)=258.06ms p(95)=261.78ms
     http_req_duration..............: avg=235.54ms min=216.25ms med=235.5ms  max=254.85ms p(90)=250.98ms p(95)=252.91ms
     ✓ { container_group:main }.....: avg=0s       min=0s       med=0s       max=0s       p(90)=0s       p(95)=0s      
       { expected_response:true }...: avg=235.54ms min=216.25ms med=235.5ms  max=254.85ms p(90)=250.98ms p(95)=252.91ms
     http_req_failed................: 0.00%  ✓ 0        ✗ 3  
     http_req_receiving.............: avg=140.66µs min=114µs    med=149µs    max=159µs    p(90)=157µs    p(95)=158µs   
     http_req_sending...............: avg=63µs     min=36µs     med=53µs     max=100µs    p(90)=90.6µs   p(95)=95.3µs  
     http_req_tls_handshaking.......: avg=268.53ms min=219.61ms med=263.88ms max=322.1ms  p(90)=310.46ms p(95)=316.28ms
     http_req_waiting...............: avg=235.33ms min=216.1ms  med=235.3ms  max=254.59ms p(90)=250.73ms p(95)=252.66ms
     http_reqs......................: 3      1.084494/s
     ✗ { container_group:main }.....: 0      0/s
     iteration_duration.............: avg=2.76s    min=2.76s    med=2.76s    max=2.76s    p(90)=2.76s    p(95)=2.76s   
     iterations.....................: 1      0.361498/s
     vus............................: 1      min=1      max=1
     vus_max........................: 1      min=1      max=1
```




