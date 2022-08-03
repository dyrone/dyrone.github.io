---
title: "K6 Result Output"
date: 2022-08-03T16:07:59+08:00
draft: false
tags:
    - "testing"
---

## Output flow overview

![overview](https://k6.io/docs/static/dba3ddf4f3ab26e38c2bb8014a3f6910/e1d57/k6-results-diagram.png
"overview")

By default, k6 provides an end-of-test summary report. This report aggregates
the test results, with information about all groups, checks, and thresholds in
the load test. It also gives basic, summary statistics about each metric (e.g.
mean, median, p95, etc).

For analysis, you can stream all the data that your test generates to an
external output. It might be a structured file format like **CSV** or **JSON**.
But you could also stream to another program, like Prometheus.

## Standard output

![stdout](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/2601/1659514672911-a902f22d-2314-4491-bb6c-7dd1ebfa91f7.png?x-oss-process=image%2Fresize%2Cw_1267%2Climit_0
"stdout")

It includes three kinds of test result information:

* **test details**: general test information and load options
* **progress bar**: test status and how much time has passed
* **test summary**: the test results

## Built-in metrics

* **vus**: Current number of active virtual users

* ****vus_max**: Max possible number of virtual users (VU resources are pre-allocated,
  ensuring performance will not be affected when scaling up the load level)

> For example, if we specify the VUs option is 20, the `vus_max` will always be
> 20, when the test starts running, will be 20 vus parallelly running, but
> imagine that some VUs are finished quickly and the others might be slow, than
> the vus field will changes at realtime representing that the currently how
> many VUs are running , such as one of the 20 VUs have a large latency than the
> other 19 VUs, then at the tailing time of testing, the vus in the output will
> be 1 for a corresponding long time.

* **iterations**: how many times the VUs executed the `default` function.

* **iteration_duration**: The time it took to complete one full iteration, including
  time spent in setup and teardown.

* **dropped_iterations**: The number of iterations that weren't started due to
  lack of VUs (for the arrival-rate executors) or lack of time (expired
  maxDuration in the iteration-based executors).

* **data_received**: The amount of received data.

* **data_sent**: The amount of data sent.

* **checks**: The rate of successful checks.

## HTTP builtin metrics

* **http_reqs**: how many total http requests generated.

* **http_req_blocked**： Time spent blocked (waiting for a free TCP connection
  slot) before initiating the request. The connection preparation cost before
  establishment.
  
* **http_req_connecting**: Time spent establishing TCP connection to the remote
  host.
  
* **http_req_tls_handshaking**: Time spent handshaking TLS session with remote
  host.

* **http_req_sending**: Time spent sending data to the remote host.

* **http_req_waiting**: Time spent waiting for response from remote host (a.k.a.
  “time to first byte”, or “TTFB”).

* **http_req_receiving**: Time spent receiving response data from the remote
  host.

* **http_req_duration**: Total time for the request. It's equal to
  `http_req_sending + http_req_waiting + http_req_receiving`` (i.e. how long did
  the remote server take to process the request and respond, without the initial
  DNS lookup/connection times).

* **http_req_failed**: The rate of failed requests according to
  setResponseCallback.
  
### Accessing HTTP timing from a script

To access the timing information from an individual HTTP request, the
`Response.timings` object provides the time spent on the various phases in ms:

```jsts
import http from 'k6/http';

export default function () {
  const res = http.get('http://httpbin.test.k6.io');
  console.log('Response time was ' + String(res.timings.duration) + ' ms');
}
```

The output will be liking:
```
k6 run script.js

  INFO[0001] Response time was 337.962473 ms               source=console
```

### Custom metrics

```jsts
import http from 'k6/http';
import { Trend } from 'k6/metrics';

const myTrend = new Trend('waiting_time');

export default function () {
  const r = http.get('https://httpbin.test.k6.io');
  myTrend.add(r.timings.waiting);
  console.log(myTrend.name); // waiting_time
}
```
The preceding code creates a Trend metric called waiting_time. In the code, it's
referred to with the variable name myTrend.

Custom metrics are reported at the end of a test. Here's how the output might
look:

```jsts
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

INFO[0001] waiting_time                                  source=console

running (00m01.1s), 0/1 VUs, 1 complete and 0 interrupted iterations
default ✓ [======================================] 1 VUs  00m01.1s/10m0s  1/1 iters, 1 per VU

     data_received..................: 15 kB 14 kB/s
     data_sent......................: 454 B 424 B/s
     http_req_blocked...............: avg=794.56ms min=794.56ms med=794.56ms max=794.56ms p(90)=794.56ms p(95)=794.56ms
     http_req_connecting............: avg=251.49ms min=251.49ms med=251.49ms max=251.49ms p(90)=251.49ms p(95)=251.49ms
     http_req_duration..............: avg=274.07ms min=274.07ms med=274.07ms max=274.07ms p(90)=274.07ms p(95)=274.07ms
       { expected_response:true }...: avg=274.07ms min=274.07ms med=274.07ms max=274.07ms p(90)=274.07ms p(95)=274.07ms
     http_req_failed................: 0.00% ✓ 0        ✗ 1  
     http_req_receiving.............: avg=506µs    min=506µs    med=506µs    max=506µs    p(90)=506µs    p(95)=506µs   
     http_req_sending...............: avg=99µs     min=99µs     med=99µs     max=99µs     p(90)=99µs     p(95)=99µs    
     http_req_tls_handshaking.......: avg=341.23ms min=341.23ms med=341.23ms max=341.23ms p(90)=341.23ms p(95)=341.23ms
     http_req_waiting...............: avg=273.46ms min=273.46ms med=273.46ms max=273.46ms p(90)=273.46ms p(95)=273.46ms
     http_reqs......................: 1     0.933729/s
     iteration_duration.............: avg=1.06s    min=1.06s    med=1.06s    max=1.06s    p(90)=1.06s    p(95)=1.06s   
     iterations.....................: 1     0.933729/s
     vus............................: 1     min=1      max=1
     vus_max........................: 1     min=1      max=1
     waiting_time...................: avg=273.466  min=273.466  med=273.466  max=273.466  p(90)=273.466  p(95)=273.466
```

### Counter 

```jsts
import http from 'k6/http';
import { Counter } from 'k6/metrics';
export const options = {
  discardResponseBodies: true,
  scenarios: {
    contacts: {
      executor: 'constant-vus',
      vus: 10,
      duration: '10s',
      gracefulStop: '3s',
    },
  },
};
const myCounter = new Counter('my_counter');

export default function () {
  const r = http.get('https://httpbin.test.k6.io');
  myCounter.add(2);
}
```

The omitted output might be :

```shell
...
     iterations.....................: 311    29.711229/s
     my_counter.....................: 311    29.711229/s
     vus............................: 10     min=10      max=10
     vus_max........................: 10     min=10      max=10
```
