---
title: "K6 Result Output"
date: 2022-08-03T16:07:59+08:00
draft: false
tags:
    - "testing"
---

> NOTICE: Base and excerpt from the official k6 documentation

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

### Counter: cumulative

```jsts
import { Counter } from 'k6/metrics';

const myCounter = new Counter('my_counter');

export default function () {
  myCounter.add(1);
  myCounter.add(3);
  myCounter.add(2);
}
```

The omitted output might be, `my_counter` value will be 6:

```shell
     data_received........: 0 B 0 B/s
     data_sent............: 0 B 0 B/s     
     iteration_duration...: avg=39.81µs min=39.81µs med=39.81µs max=39.81µs p(90)=39.81µs p(95)=39.81µs
     iterations...........: 1   1233.045623/s
     my_counter...........: 6   7398.273736/s
```

### Gause (keep the latest value only)

```jsts
import { Gauge } from 'k6/metrics';

const myGauge = new Gauge('my_gauge');

export default function () {
  myGauge.add(3);
  myGauge.add(1);
  myGauge.add(2);
}
```

Output might be:
```shell
$ k6 run script.js

  ...
  iteration_duration...: avg=21.74µs min=21.74µs med=21.74µs max=21.74µs p(90)=21.74µs p(95)=21.74µs
  iterations...........: 1   1293.475322/s
  my_gauge.............: 2   min=1         max=3
```

### Trend (collect trend statistics (min/max/avg/percentiles) for a series of
values)

```jsts
import { Trend } from 'k6/metrics';

const myTrend = new Trend('my_trend');

export default function () {
  myTrend.add(1);
  myTrend.add(2);
}
```

Ouput might like:

```shell
k6 run script.js

  ...
  iteration_duration...: avg=20.78µs min=20.78µs med=20.78µs max=20.78µs p(90)=20.78µs p(95)=20.78µs
  iterations...........: 1   1217.544821/s
  my_trend.............: avg=1.5     min=1       med=1.5     max=2       p(90)=1.9     p(95)=1.95

```

A trend metric holds a set of sample values, which it can output statistics
about (min, max, average, median, or percentiles). By default, k6 prints
average, min, max, median, 90th percentile, and 95th percentile.


### Rate (keeps track of the percentage of values in a series that are non-zero)

```jsts
import { Rate } from 'k6/metrics';

const myRate = new Rate('my_rate');

export default function () {
  myRate.add(true);
  myRate.add(true);
  myRate.add(1);
  myRate.add(0);
}
```

Output might be:

```shell
  execution: local
     script: pt-1-0001-stages.ts
     output: -

  scenarios: (100.00%) 1 scenario, 1 max VUs, 10m30s max duration (incl. graceful stop):
           * default: 1 iterations for each of 1 VUs (maxDuration: 10m0s, gracefulStop: 30s)


running (00m00.0s), 0/1 VUs, 1 complete and 0 interrupted iterations
default ✓ [======================================] 1 VUs  00m00.0s/10m0s  1/1 iters, 1 per VU

     data_received........: 0 B    0 B/s
     data_sent............: 0 B    0 B/s
     iteration_duration...: avg=48.57µs min=48.57µs med=48.57µs max=48.57µs p(90)=48.57µs p(95)=48.57µs
     iterations...........: 1      1485.884101/s
     my_rate..............: 75.00% ✓ 3           ✗ 1
```

And the output might be:

```shell
...
     data_received........: 0 B    0 B/s
     data_sent............: 0 B    0 B/s
     iteration_duration...: avg=48.57µs min=48.57µs med=48.57µs max=48.57µs p(90)=48.57µs p(95)=48.57µs
     iterations...........: 1      1485.884101/s
     my_rate..............: 75.00% ✓ 3           ✗ 1

```

## Checks

Checks are true/false criteria for your test runtime values.

In practice, checks oftern evaluate whether the system under test responds with
a certain value. A check may evaluate:

* That the system responds with a 200 status
* That a response body contains certain text
* That the response body is of a specified size


### Check HTTP response code

```jsts
import { check } from 'k6';
import http from 'k6/http';

export default function () {
  const res = http.get('http://test.k6.io/');
  check(res, {
    'is status 200': (r) => r.status === 200,
  });
}
```

The output might like:

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


running (00m01.7s), 0/1 VUs, 1 complete and 0 interrupted iterations
default ✓ [======================================] 1 VUs  00m01.7s/10m0s  1/1 iters, 1 per VU

     ✓ is status 200

     checks.........................: 100.00% ✓ 1        ✗ 0  
     data_received..................: 17 kB   10 kB/s
     ...
```

### Check for text in response body

```jsts
import { check } from 'k6';
import http from 'k6/http';

export default function () {
  const res = http.get('http://test.k6.io/');
  check(res, {
    'verify homepage text': (r) =>
      r.body.includes('Collection of simple web-pages suitable for load testing'),
  });
}
```
### Add multiple checks

```jsts
import { check } from 'k6';
import http from 'k6/http';

export default function () {
  const res = http.get('http://test.k6.io/');
  check(res, {
    'is status 200': (r) => r.status === 200,
    'body size is 11,105 bytes': (r) => r.body.length == 11105,
  });
}
```

The output will be like:

```shell
running (00m01.4s), 0/1 VUs, 1 complete and 0 interrupted iterations
default ✓ [======================================] 1 VUs  00m01.4s/10m0s  1/1 iters, 1 per VU

     ✓ is status 200
     ✗ body size is 11,105 bytes
      ↳  0% — ✓ 0 / ✗ 1
...
```

### Failing a load test using checks

When a iteration failed, the test will continue running, if you want to stop the
test procedure and exit, you can use `threshold`.

```jsts
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 50,
  duration: '10s',
  thresholds: {
    // the rate of successful checks should be higher than 90%
    checks: ['rate>0.9'],
  },
};

export default function () {
  const res = http.get('http://httpbin.test.k6.io');

  check(res, {
    'status is 500': (r) => r.status == 500,
  });

  sleep(1);
}
```

The output might be: 

```shell
  scenarios: (100.00%) 1 scenario, 50 max VUs, 40s max duration (incl. graceful stop):
           * default: 50 looping VUs for 10s (gracefulStop: 30s)


running (11.5s), 00/50 VUs, 349 complete and 0 interrupted iterations
default ✓ [======================================] 50 VUs  10s

     ✗ status is 500
      ↳  0% — ✓ 0 / ✗ 349

   ✗ checks.........................: 0.00%  ✓ 0         ✗ 349 
     data_received..................: 3.8 MB 334 kB/s
...
```

Using `tags` for particular check or group checks, for example:

```jsts
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 50,
  duration: '10s',
  thresholds: {
    'checks{myTag:hola}': ['rate>0.9'],
  },
};

export default function () {
  let res;

  res = http.get('http://httpbin.test.k6.io');
  check(res, {
    'status is 500': (r) => r.status == 500,
  });

  res = http.get('http://httpbin.test.k6.io');
  check(
    res,
    {
      'status is 200': (r) => r.status == 200,
    },
    { myTag: 'hola' }
  );

  sleep(1);
}
```

Output: 

```shell
running (11.2s), 00/50 VUs, 250 complete and 0 interrupted iterations                                                     
default ✓ [======================================] 50 VUs  10s                                                            
                                                                                                                          
     ✗ status is 500                                                                                                      
      ↳  0% — ✓ 0 / ✗ 250                                                                                                 
     ✓ status is 200                                                                                                      
                                                                                                                          
     checks.........................: 50.00%  ✓ 250       ✗ 250                                                           
     ✓ { myTag:hola }...............: 100.00% ✓ 250       ✗ 0                                                             
     data_received..................: 5.4 MB  480 kB/s                                                                    
     data_sent......................: 130 kB  12 kB/s                                                                     
     http_req_blocked...............: avg=54.33ms min=2µs      med=7µs      max=623.04ms p(90)=43.13ms  p(95)=570.77ms    
     http_req_connecting............: avg=22.22ms min=0s       med=0s       max=251.35ms p(90)=19.96ms  p(95)=219.92ms    
     http_req_duration..............: avg=228.8ms min=198.66ms med=227.1ms  max=504.86ms p(90)=245.68ms p(95)=253.3ms     
       { expected_response:true }...: avg=228.8ms min=198.66ms med=227.1ms  max=504.86ms p(90)=245.68ms p(95)=253.3ms     
     http_req_failed................: 0.00%   ✓ 0         ✗ 1000                                                          
     http_req_receiving.............: avg=1.06ms  min=25µs     med=132µs    max=250.05ms p(90)=622.6µs  p(95)=1.71ms      
     http_req_sending...............: avg=33.21µs min=6µs      med=28µs     max=207µs    p(90)=47.1µs   p(95)=72.04µs     
     http_req_tls_handshaking.......: avg=13.53ms min=0s       med=0s       max=328.63ms p(90)=0s       p(95)=11.52ms     
     http_req_waiting...............: avg=227.7ms min=198.54ms med=226.64ms max=426.7ms  p(90)=245.22ms p(95)=252.71ms    
     http_reqs......................: 1000    89.379587/s                                                                 
     iteration_duration.............: avg=2.13s   min=1.83s    med=1.91s    max=3.24s    p(90)=3.02s    p(95)=3.1s        
     iterations.....................: 250     22.344897/s
     vus............................: 5       min=5       max=50
     vus_max........................: 50      min=50      max=50
```
