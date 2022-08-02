---
title: "k6 overview"
date: 2022-08-01T21:24:42+08:00
draft: false 
tags:
    - "testing"
---

## Concepts 

* virtual users (VUs):  VUs are essentially parallel while(true) loop.

* init context: use the default function, this function defines the entry point
for your VUsi. Init code runs first and is called only once per VU. On the other
hand, default code executes as many times as the test options set.

```js
export default function () {
  // vu code: do things here...
}
```

## Test life cycle

In last section, we introduced the init context, here we will talk about the
test life cycle.

```js
// 1. init code

export function setup() {
  // 2. setup code
}

export default function (data) {
  // 3. VU code
}

export function teardown(data) {
  // 4. teardown code
}
```

Overview:

![overview](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/2601/1659421018537-928345fb-3b75-416b-bc8f-498e1bbf6488.png?x-oss-process=image%2Fresize%2Cw_1349%2Climit_0 "overview")

### init stage

The init stage is required. Separating the init stage from the VU stage removes
irrelevant computation from VU code, which both improves k6 performance and
makes test results more reliable.

```js
// init context: importing modules
import http from 'k6/http';
import { Trend } from 'k6/metrics';

// init context: define k6 options
export const options = {
  vus: 10,
  duration: '30s',
};

// init context: global variables
const customTrend = new Trend('oneCustomMetric');

// init context: define custom function
function myCustomFunction() {
  // ...
}

```

### VU stage

The code inside `default()` function is VU code.

```js
export default function () {
  // do things here...
}
```

VU code runs over and over through the test duration.

VU code can make HTTP requests, emit metrics, and generally do everything you'd
expect a load test to do. The only exceptions are the jobs that happen in the
init context.

* VU code does not load files from your local filesystem.
* VU code does not import any other modules.

Again, instead of VU code, init code does these jobs.

### setup and teardown stages


Like default, setup and teardown functions must be exported functions. But
unlike the default function, k6 calls setup and teardown only once per test.

setup is called at the beginning of the test, after the init stage but before
the VU stage. teardown is called at the end of a test, after the VU stage
(default function). You can call the full k6 API in the setup and teardown
stages, unlike the init stage. For example, you can make HTTP requests:

```js
import http from 'k6/http';

export function setup() {
  const res = http.get('https://httpbin.test.k6.io/get');
  return { data: res.json() };
}

export function teardown(data) {
  console.log(JSON.stringify(data));
}

export default function (data) {
  console.log(JSON.stringify(data));
}


```

![flow](https://k6.io/docs/static/2c69d22ae34cc91f7514f63bd2a787ea/5d70e/lifecycle.png "flow")

## Running k6

### first run 

```js
import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
  http.get('https://test.k6.io');
  sleep(1);
}

```

```shell
k6 run script.js
```

### options

You can specifiy `--vus 10 and` `--duration 30s` similar way to run test each time,
or you can include the options in your js file.

```js
import http from 'k6/http';
import { sleep } from 'k6';
export const options = {
  vus: 10,
  duration: '30s',
};
export default function () {
  http.get('http://test.k6.io');
  sleep(1);
}
```

#### stages: ramping up/down VUs

You can ramp the number if VUs up and down during the test.
```js
import { check, sleep } from 'k6';
import http from 'k6/http';

export const options = {
  stages: [
  {duration : '5s', target: 20},
  {duration : '3s', target: 10},
  {duration : '5s', target: 0},
  ]
};

export default function () {
  const res = http.get('https://httpbin.test.k6.io/get');
  check(res, {'status was 200': (r) => r.status == 200});
  sleep(1);
}


export function teardown(data) {
  console.log('test done...');
}
```

#### Scenarios 

Benefits of using scenarios include:

* Multiple scenarios can be declared in the same script, and each one can
  independently execute a different JavaScript function, which makes organizing
  tests easier and more flexible.
  
* Every scenario can use a distinct VU and iteration scheduling pattern, powered
  by a purpose-built `executor`. This enables modeling of advanced execution
  patterns which can better simulate real-world traffic.
  
* Scenarios are independent from each other and run in parallel, though they can
  be made to appear sequential by setting the startTime property of each
  carefully.
  
* Different environment variables and metric tags can be set per scenario.

For example:

```jsts
import http from 'k6/http';

export const options = {
  scenarios: {
    example_scenario: {
      executor: 'shared-iterations',
      startTime: '0s'
    },
    another_scenario: {
      executor: 'shared-iterations',
      startTime: '5s'
    },
  },
};

export default function () {
  http.get('https://google.com/');
}
```

Executors are the workhorses for k6 execution. Each one schedules VUs and
iterations differently, you will choose one depending on the type of traffic you
want to model to test your services, they are:

* **shared-iterations**: A fixed amount of iterations are "shared" between a
number of VUs.

* **per-vu-iterations**: Each VU executes an exact number of iterations.

* **constant-vus**: A fixed number of VUs execute as many iterations as possible
for a specified amount of time.

* **ramping-vus**: A variable number of VUs execute as many iterations as
possible for a specified amount of time.

* **constant-arrival-rate**: A fixed number of iterations are executed in a
specified period of time.

* **ramping-arrival-rate**: A variable number of iterations are
executed in a specified period of time.

* **externally-controlled**: Control and scale execution at runtime via k6's
REST API or the CLI.

Common options for `scenario`:

* **executor (required)**: Unique executor name. See the list of possible values
  in the executors (last part).

* **startTime**: Default set to '0s'. Time offset since the start of the test,
  at which point this scenario should begin execution.
  
* **gracefulStop**: Default set to '30s'. Time to wait for iterations to finish
  executing before stopping them forcefully. Read more about gracefully stopping
  a test run here.

* **exec**: Default set to 'default'. Name of exported JS function to execute.

* **env**: default set to {}, Environment variables specific to this scenario.

* **tags*: Default set to {}, tags specific to his scenario.

For example, the following script defines two minimal scenarios (1 VU, default
duration):

```jsts

import http from 'k6/http';

export const options = {
  scenarios: {
    example_scenario: {
      executor: 'shared-iterations',
      startTime: '0s'
    },
    another_scenario: {
      executor: 'shared-iterations',
      startTime: '5s'
    },
  },
};

export default function () {
  http.get('https://google.com/');
}
```
The output will be :

```shell
          /\      |‾‾| /‾‾/   /‾‾/
     /\  /  \     |  |/  /   /  /
    /  \/    \    |     (   /   ‾‾\
   /          \   |  |\  \ |  (‾)  |
  / __________ \  |__| \__\ \_____/ .io

  execution: local
     script: .\scenario_example.js
     output: -

  scenarios: (100.00%) 2 scenarios, 2 max VUs, 10m35s max duration (incl. graceful stop):
           * example_scenario: 1 iterations shared among 1 VUs (maxDuration: 10m0s, gracefulStop: 30s)
           * another_scenario: 1 iterations shared among 1 VUs (maxDuration: 10m0s, startTime: 5s, gracefulStop: 30s)


running (00m05.2s), 0/2 VUs, 2 complete and 0 interrupted iterations
example_scenario ✓ [======================================] 1 VUs  00m00.2s/10m0s  1/1 shared iters
another_scenario ✓ [======================================] 1 VUs  00m00.2s/10m0s  1/1 shared iters

     data_received..................: 54 kB  11 kB/s
     data_sent......................: 2.5 kB 486 B/s
     http_req_blocked...............: avg=53.45ms  min=46.56ms  med=48.42ms  max=70.4ms   p(90)=64.25ms  p(95)=67.32ms
     http_req_connecting............: avg=19.95ms  min=18.62ms  med=19.93ms  max=21.3ms   p(90)=21.26ms  p(95)=21.28ms
     http_req_duration..............: avg=46.16ms  min=25.82ms  med=45.6ms   max=67.6ms   p(90)=65.63ms  p(95)=66.61ms
       { expected_response:true }...: avg=46.16ms  min=25.82ms  med=45.6ms   max=67.6ms   p(90)=65.63ms  p(95)=66.61ms
     http_req_failed................: 0.00%  ✓ 0        ✗ 4
     http_req_receiving.............: avg=3.56ms   min=305.8µs  med=3.05ms   max=7.84ms   p(90)=7.01ms   p(95)=7.43ms
     http_req_sending...............: avg=132.85µs min=0s       med=0s       max=531.4µs  p(90)=371.98µs p(95)=451.68µs
     http_req_tls_handshaking.......: avg=32.68ms  min=27.63ms  med=27.99ms  max=47.09ms  p(90)=41.43ms  p(95)=44.26ms
     http_req_waiting...............: avg=42.46ms  min=24.78ms  med=42.64ms  max=59.75ms  p(90)=58.45ms  p(95)=59.1ms
     http_reqs......................: 4      0.771306/s
     iteration_duration.............: avg=199.23ms min=182.79ms med=199.23ms max=215.67ms p(90)=212.38ms p(95)=214.03ms
     iterations.....................: 2      0.385653/s
     vus............................: 0      min=0      max=0
     vus_max........................: 2      min=2      max=2

```

#### Graceful stop

This option is available for all executors except `externally-controlled` and
allows the user to specify a duration to wait before forcefully interrupting
them. The default value is `30s`.

For example:

```jsts
import { check, sleep } from 'k6';
import http from 'k6/http';

export const options = {
  // k6 will return null as the body. The whole body will be ignored.
  // This is the default when discardResponseBodies is set to true.
  discardResponseBodies: true,
  scenarios: {
    contacts: {
      // A fixed number of VUs execute as many iterations as possible for
      // a specified amount of time.
      executor: 'constant-vus',
      vus: 100,
      duration: '10s',
      gracefulStop: '3s',
    },
  },
};

export default function () {
  const delay = Math.floor(Math.random() * 5) + 1;
  // this address support a customized delayed payload.
  http.get(`https://httpbin.test.k6.io/delay/${delay}`);
}

// export default function () {
//   const res = http.get('https://httpbin.test.k6.io/get');
//   check(res, {'status was 200': (r) => r.status == 200});
//   sleep(1);
// }
```
The ouput is like: 

```shell
          /\      |‾‾| /‾‾/   /‾‾/   
     /\  /  \     |  |/  /   /  /    
    /  \/    \    |     (   /   ‾‾\  
   /          \   |  |\  \ |  (‾)  | 
  / __________ \  |__| \__\ \_____/ .io

  execution: local
     script: pt-1-0001-stages.ts
     output: -

  scenarios: (100.00%) 1 scenario, 100 max VUs, 13s max duration (incl. graceful stop):
           * contacts: 100 looping VUs for 10s (gracefulStop: 3s)


running (13.0s), 000/100 VUs, 304 complete and 27 interrupted iterations
contacts ✓ [======================================] 100 VUs  10s

     data_received..................: 712 kB 55 kB/s
     data_sent......................: 73 kB  5.6 kB/s
     http_req_blocked...............: avg=334.76ms min=2µs   med=7µs   max=2.54s    p(90)=945.15ms p(95)=996.46ms
     http_req_connecting............: avg=81.15ms  min=0s    med=0s    max=276.62ms p(90)=256ms    p(95)=261.4ms 
     http_req_duration..............: avg=3.16s    min=1.22s med=3.24s max=5.29s    p(90)=5.25s    p(95)=5.26s   
       { expected_response:true }...: avg=3.16s    min=1.22s med=3.24s max=5.29s    p(90)=5.25s    p(95)=5.26s   
     http_req_failed................: 0.00%  ✓ 0         ✗ 304  
     http_req_receiving.............: avg=94.97µs  min=28µs  med=87µs  max=1.02ms   p(90)=121µs    p(95)=132.69µs
     http_req_sending...............: avg=36.02µs  min=12µs  med=33µs  max=495µs    p(90)=46µs     p(95)=54.69µs 
     http_req_tls_handshaking.......: avg=192.62ms min=0s    med=0s    max=2.11s    p(90)=497.04ms p(95)=540.7ms 
     http_req_waiting...............: avg=3.16s    min=1.22s med=3.24s max=5.29s    p(90)=5.25s    p(95)=5.25s   
     http_reqs......................: 304    23.377036/s
     iteration_duration.............: avg=3.5s     min=1.22s med=3.25s max=7.79s    p(90)=5.27s    p(95)=6.1s    
     iterations.....................: 304    23.377036/s
     vus............................: 27     min=27      max=100
     vus_max........................: 100    min=100     max=100
```

Notice that `running (13.0s)`, even though the total test duration is 10s, the
actual execution time was 13s because of `gracefulStop`, giving the VUs a 3s
additional time to complete iterations in progress. 27 iterations are
interrupted or did not complete within this window and was therefore
interrupted.

### Execution modes

* **Local**: the test execution happens entirely on a single machine.

* **Distributed**: the test execution is distributed across a K8s cluster.(I
  have't try it yet)

* **Cloud**: the test execution happens on k6 clould.(I haven't try it yet)

## integrate in Emacs 

Emacs supports automatic language server installation, so the first time you run
`M-x lsp`` in a JavaScript file opened in it, you will be prompted for a
language server to install. (Here I use jsts-ls lsp server)

Then, everything will be done by Emacs and lsp server for you.

> https://emacs-lsp.github.io/lsp-mode/tutorials/reactjs-tutorial/

Commanded to use VsCode directly (with autocompletion support): 
> https://marketplace.visualstudio.com/items?itemName=k6.k6
