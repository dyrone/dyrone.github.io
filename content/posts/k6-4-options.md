---
title: "k6 series [4] - Options"
date: 2022-08-04T15:00:25+08:00
draft: false
tags:
    - "testing"
---

> NOTICE: Base and excerpt from the official k6 documentation 

## option scopes

* In CLI flags 
* In environment variables
* In script `options` object

## Order 

![order](https://k6.io/docs/static/cd2ffc633dd58c67e276922851216ab9/0e253/order-of-precedence.png)

* First, k6 uses the option's default value.
* Next, k6 uses the options set by the --config flag.
* Then, k6 uses the script value (if set).
* After, k6 uses the environment variable (if set).
* Finally, k6 takes the value from the CLI flag (if set).

The script `options` object is generally the best place to put your options. This
provides automatic version control, allows for easy reuse, and lets you
modularize your script.

When you want to run a quick test, command-line flags are convenient. You can
also use command-line flags to override files in your script (as determined by
the order of precedence). For example, if your script file sets the test
duration at 60 seconds, you could use a CLI flag to run a one-time shorter test.
With a flag like --duration 30s, the test would be half as long but otherwise
identical.

## Set options in the script

```jsts
import http from 'k6/http';

export const options = {
  hosts: { 'test.k6.io': '1.2.3.4' },
  stages: [
    { duration: '1m', target: 10 },
  ],
  thresholds: { http_req_duration: ['avg<100', 'p(95)<200'] },
  noConnectionReuse: true,
  userAgent: 'MyK6UserAgentString/1.0',
};

export default function () {
  http.get('http://test.k6.io/');
}
```

```shell

  scenarios: (100.00%) 1 scenario, 10 max VUs, 1m30s max duration (incl. graceful stop):
           * default: Up to 10 looping VUs for 1m0s over 1 stages (gracefulRampDown: 30s, gracefulStop: 30s)

WARN[0030] Request Failed                                error="Get \"http://test.k6.io/\": dial: i/o timeout"
WARN[0037] Request Failed                                error="Get \"http://test.k6.io/\": dial: i/o timeout"
WARN[0043] Request Failed                                error="Get \"http://test.k6.io/\": dial: i/o timeout"
WARN[0050] Request Failed                                error="Get \"http://test.k6.io/\": dial: i/o timeout"
WARN[0057] Request Failed                                error="Get \"http://test.k6.io/\": dial: i/o timeout"
WARN[0060] Request Failed                                error="Get \"http://test.k6.io/\": dial: i/o timeout"
WARN[0063] Request Failed                                error="Get \"http://test.k6.io/\": dial: i/o timeout"
WARN[0067] Request Failed                                error="Get \"http://test.k6.io/\": dial: i/o timeout"
WARN[0070] Request Failed                                error="Get \"http://test.k6.io/\": dial: i/o timeout"
WARN[0073] Request Failed                                error="Get \"http://test.k6.io/\": dial: i/o timeout"
WARN[0077] Request Failed                                error="Get \"http://test.k6.io/\": dial: i/o timeout"
WARN[0080] Request Failed                                error="Get \"http://test.k6.io/\": dial: i/o timeout"
WARN[0083] Request Failed                                error="Get \"http://test.k6.io/\": dial: i/o timeout"
WARN[0087] Request Failed                                error="Get \"http://test.k6.io/\": dial: i/o timeout"

running (1m26.7s), 00/10 VUs, 14 complete and 0 interrupted iterations
default ✓ [======================================] 00/10 VUs  1m0s

     data_received..............: 0 B     0 B/s
     data_sent..................: 0 B     0 B/s
     http_req_blocked...........: avg=0s  min=0s  med=0s  max=0s  p(90)=0s  p(95)=0s 
     http_req_connecting........: avg=0s  min=0s  med=0s  max=0s  p(90)=0s  p(95)=0s 
   ✓ http_req_duration..........: avg=0s  min=0s  med=0s  max=0s  p(90)=0s  p(95)=0s 
     http_req_failed............: 100.00% ✓ 14       ✗ 0   
     http_req_receiving.........: avg=0s  min=0s  med=0s  max=0s  p(90)=0s  p(95)=0s 
     http_req_sending...........: avg=0s  min=0s  med=0s  max=0s  p(90)=0s  p(95)=0s 
     http_req_tls_handshaking...: avg=0s  min=0s  med=0s  max=0s  p(90)=0s  p(95)=0s 
     http_req_waiting...........: avg=0s  min=0s  med=0s  max=0s  p(90)=0s  p(95)=0s 
     http_reqs..................: 14      0.161529/s
     iteration_duration.........: avg=30s min=30s med=30s max=30s p(90)=30s p(95)=30s
     iterations.................: 14      0.161529/s
     vus........................: 1       min=1      max=9 
     vus_max....................: 10      min=10     max=10
```

## Set options with environment variables

```jsts
K6_NO_CONNECTION_REUSE=true K6_USER_AGENT="MyK6UserAgentString/1.0" k6 run script.js

k6 run --no-connection-reuse --user-agent "MyK6UserAgentString/1.0" script.js
```

## Set options from k6 variables

For example, you could define a variable for your user agent like this:

```jsts
import http from 'k6/http';

export const options = {
  userAgent: __ENV.MY_USER_AGENT,
};

export default function () {
  http.get('http://test.k6.io/');
}
```

Then execute:
```shell
k6 run script.js --env MY_USER_AGENT="hello"
```

## Options reference

Import ones I prefer are:

### Batch

The maximum number of simultaneous/parallel connections in total that an
http.batch() call in a VU can make. If you have a batch() call that you've given
20 URLs to and --batch is set to 15, then the VU will make 15 requests right
away in parallel and queue the rest, executing them as soon as a previous
request is done and a slot opens. Available in both the k6 run and the k6 cloud
commands.

```
ENV         CLI        CODE     DEFAULT
K6_BATCH	--batch	batch	20
```

```jsts
export const options = {
  batch: 15,
};
```

## Batch per host
The maximum number of simultaneous/parallel connections for the same hostname
that an http.batch() call in a VU can make. If you have a batch() call that
you've given 20 URLs to the same hostname and --batch-per-host is set to 5, then
the VU will make 5 requests right away in parallel and queue the rest, executing
them as soon as a previous request is done and a slot opens. This will not run
more request in parallel then the value of batch.

```
ENV         CLI        CODE     DEFAULT
K6_BATCH_PER_HOST	--batch-per-host	batchPerHost	6
```

```jsts
export const options = {
  batchPerHost: 5,
};
```

## VUs

An integer value specifying the number of VUs to run concurrently, used together with the iterations or duration options. If you'd like more control look at the stages option or scenarios.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_VUS	--vus, -u	vus	1
```

```jsts
export const options = {
  vus: 10,
  duration: '1h',
};
```

## Blacklist IP

Blacklist IP ranges from being called. Available in k6 run and k6 cloud commands.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT
K6_BLACKLIST_IPS	--blacklist-ip	blacklistIPs	null
```

```jsts
export const options = {
  blacklistIPs: ['10.0.0.0/8'],
};
```

## Block hostnames

Blocks hostnames based on a list glob match strings. The pattern matching string
can have a single * at the beginning such as *.example.com that will match
anything before that such as test.example.com and test.test.example.com.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT
K6_BLOCK_HOSTNAMES	--block-hostnames	blockHostnames	null
```

```jsts
export const options = {
  blockHostnames: ['test.k6.io', '*.example.com'],
};
```

## Config

Specify the config file in JSON format. If the config file is not specified, k6
looks for **config.json** in the **loadimpact/k6** directory inside the regular
directory for configuration files on the operating system. Default config
locations on different operating systems are as follows:

* Unix-based: ${HOME}/.config/loadimpact/k6/config.json
* macOS: ${HOME}/Library/Application Support/loadimpact/k6/config.json
* Windows: %AppData%/loadimpact/k6/config.json

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT
N/A	--config <path>, -c <path>	N/A	null
```

## Console output

Redirects logs logged by console methods to the provided output file. 

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT
K6_CONSOLE_OUTPUT	--console-output	N/A	null
```

```shell
$ k6 run --console-output "loadtest.log" script.js
```

## Discard response bodies

Specify if response bodies should be discarded by changing the default value of
responseType to none for all HTTP requests. Highly recommended to be set to true
and then only for the requests where the response body is needed for scripting
to set responseType to text or binary.

Lessens the amount of memory required and the amount of GC - reducing the load
on the testing machine, and probably producing more reliable test results.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT
K6_DISCARD_RESPONSE_BODIES	--discard-response-bodies	discardResponseBodies	false
```

```jsts
export const options = {
  discardResponseBodies: true,
};
```

## DNS

This is a composite option that provides control of DNS resolution behavior with
configuration for cache expiration (TTL), IP selection strategy and IP version
preference. The TTL field in the DNS record is currently not read by k6, so the
ttl option allows manual control over this behavior, albeit as a fixed value for
the duration of the test run.

Note that DNS resolution is done only on new HTTP connections, and by default k6
will try to reuse connections if HTTP keep-alive is supported. To force a
certain DNS behavior consider enabling the **noConnectionReuse** option in your
tests.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT
K6_DNS	--dns	dns	ttl=5m,select=random,policy=preferIPv4
```

Possible `ttl` values are:

* 0: no caching at all - each request will trigger a new DNS lookup.
* inf: cache any resolved IPs for the duration of the test run.
* any time duration like 60s, 5m30s, 10m, 2h, etc.; if no unit is specified (e.g. ttl=3000), k6 assumes milliseconds.

Possible `select` values are:

* first: always pick the first resolved IP.
* random: pick a random IP for every new connection.
* roundRobin: iterate sequentially over the resolved IPs.

Possible `policy` values are:

* preferIPv4: use IPv4 addresses if available, otherwise fall back to IPv6.
* preferIPv6: use IPv6 addresses if available, otherwise fall back to IPv4.
* onlyIPv4: only use IPv4 addresses, ignore any IPv6 ones.
* onlyIPv6: only use IPv6 addresses, ignore any IPv4 ones.
* any: no preference, use all addresses.

Here are some configuration examples:


```shell
K6_DNS="ttl=5m,select=random,policy=preferIPv4" k6 cloud script.js
```

```jsts
export const options = {
  dns: {
    ttl: '1m',
    select: 'roundRobin',
    policy: 'any',
  },
};
```

## Duration 

A string specifying the total duration a test run should be run for. During this
time each VU will execute the script in a loop.

Together with the `vus option`, duration is a shortcut for a single `scenario`
with a `constant VUs executor`.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_DURATION	--duration, -d	duration	null
```

```jsts
export const options = {
  vus: 100,
  duration: '3m',
};
```

## Execution Segment

These options specify how to partition the test run and which segment to run. If
defined, k6 will scale the number of VUs and iterations to be run for that
segment, which is useful in distributed execution. Available in k6 run and k6
cloud commands.

For example, to run 25% of a test, you would specify `--execution-segment`
'25%', which would be equivalent to `--execution-segment` '0:1/4', i.e. run the
first 1/4 of the test. To ensure that each instance executes a specific segment,
also specify the full segment sequence, e.g. `--execution-segment-sequence`
'0,1/4,1/2,1'. This way one instance could run with `--execution-segment`
'0:1/4', another with `--execution-segment` '1/4:1/2', etc. and there would be
no overlap between them.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

N/A	--execution-segment	executionSegment	"0:1"
N/A	--execution-segment-sequence	executionSegmentSequence	"0,1"
```

### Hosts

An object with overrides to DNS resolution, similar to what you can do with
/etc/hosts on Linux/Unix or C:\\Windows\\System32\\drivers\\etc\\hosts on
Windows. For instance, you could set up an override which routes all requests
for test.k6.io to 1.2.3.4.

You can also redirect only from certain ports or to certain ports.

>This does not modify the actual HTTP Host header, but rather where it will be
>routed.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

N/A	N/A	hosts	null
```

```jsts
export const options = {
  hosts: {
    'test.k6.io': '1.2.3.4',
    'test.k6.io:443': '1.2.3.4:8443',
  },
};
```

With the above code any request made to test.k6.io will be redirected to 1.2.3.4 without changing it port unless it's port is 443 which will be redirected to port 8443.

## HTTP debug

Log all HTTP requests and responses. Excludes body by default, to include body use --http-debug=full.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_HTTP_DEBUG	--http-debug,--http-debug=full	httpDebug	false
```

```jsts
export const options = {
  httpDebug: 'full',
};
```

## Include system env vars

Pass the real system environment variables to the runtime. 

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

N/A	--include-system-env-vars	N/A	true for k6 run, but false for all other commands to prevent inadvertent sensitive data leaks.
```

```shell
$ k6 run --include-system-env-vars ~/script.js
```

## Insecure skip TLS verify

A boolean, true or false. When this option is enabled (set to true), all of the
verifications that would otherwise be done to establish trust in a server
provided TLS certificate will be ignored. This only applies to connections
created by VU code, such as http requests.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_INSECURE_SKIP_TLS_VERIFY	--insecure-skip-tls-verify insecureSkipTLSVerify	false
```

## Iterations

An integer value, specifying the total number of iterations of the default
function to execute in the test run, as opposed to specifying a duration of time
during which the script would run in a loop.

Together with the `vus` option, iterations is a shortcut for a single `scenario`
with a `shared iterations executor`.

By default, the maximum duration of a shared-iterations scenario is 10 minutes.
You can adjust that time via the maxDuration option of the scenario, or by also
specifying the duration global shortcut option.

**Note that iterations aren't fairly distributed with this option, and a VU that
executes faster will complete more iterations than others.**

Each VU will try to complete as many iterations as possible,
["stealing"](https://en.wikipedia.org/wiki/Work_stealing) them from the total
number of iterations for the test. So, depending on iteration times, some VUs
may complete more iterations than others. If you want guarantees that every VU
will complete a specific, fixed number of iterations, use the `per-VU iterations
executor`.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_ITERATIONS	--iterations, -i	iterations
```

```jsts
export const options = {
  vus: 10,
  iterations: 100,
};
```

## Linger

A boolean, true or false, specifying whether the k6 process should linger around
after test run completion.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_LINGER	--linger, -l	linger	false
```

```jsts
export const options = {
  linger: true,
};
```

## Local ips 

This option can be used for splitting the network traffic from k6 between
multiple network cards, thus potentially increasing the available network
throughput. For example, if you have 2 NICs, you can run k6 with
`--local-ips="<IP-from-first-NIC>,<IP-from-second-NIC>"` to balance the traffic
equally between them - half of the VUs will use the first IP and the other half
will use the second.

This can scale to any number of NICs, and you can repeat some local IPs to give
them more traffic. For example, `--local-ips="<IP1>,<IP2>,<IP3>,<IP3>"` will
split VUs between 3 different source IPs in a `25%:25%:50%` ratio.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_LOCAL_IPS	--local-ips	N/A	N/A
```

```shell
$ k6 run --local-ips=192.168.20.12-192.168.20.15,192.168.10.0/27 script.js
```

## Log output

This option specifies where to send logs to and another configuration connected
to it.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_LOG_OUTPUT	--log-output	N/A	stderr
```

```shell
$ k6 run --log-output=stdout script.js
```

Possible values are:

* none - disable
* stdout - send to the standard output
* stderr - send to the standard error output (this is the default)
* loki - send logs to a loki server
* file - write logs to a file

## Max redirects

The maximum number of HTTP redirects that k6 will follow before giving up on a
request and erroring out.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_MAX_REDIRECTS	--max-redirects	maxRedirects	10
```

```jsts
export const options = {
  maxRedirects: 10,
};
```

## Minimum iteration duration

Specifies the minimum duration of every single execution (i.e. iteration) of the
default function. Any iterations that are shorter than this value will cause
that VU to sleep for the remainder of the time until the specified minimum
duration is reached.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_MIN_ITERATION_DURATION	--min-iteration-duration	minIterationDuration	0 (disabled)
```

```jsts
export const options = {
  minIterationDuration: '10s',
};
```

## No connection reuse

A boolean, true or false, specifying whether k6 should disable keep-alive
connections.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_NO_CONNECTION_REUSE	--no-connection-reuse	noConnectionReuse	false
```

```jsts
export const options = {
  noConnectionReuse: true,
};
```

## No cookies reset

This disables the default behavior of resetting the cookie jar after each VU
iteration. If it's enabled, saved cookies will be persisted across VU
iterations.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_NO_COOKIES_RESET	N/A	noCookiesReset	false
```

```jsts
export const options = {
  noCookiesReset: true,
};
```

## No summary

Disables end-of-test summary generation, including calls to `handleSummary()`
and `--summary-export`

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_NO_SUMMARY	--no-summary	N/A	false
```

```jsts
$ k6 run --no-summary ~/script.js
```

## No setup and no teardown

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_NO_SETUP	--no-setup	N/A	false
K6_NO_TEARDOWN	--no-teardown	N/A	false
```

```jsts
$ k6 run --no-setup script.js
```

```jsts
$ k6 run --no-teardown script.js
```

## No thresholds

Disables threshold execution.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_NO_THRESHOLDS	--no-thresholds	N/A	false
```

```jsts
$ k6 run --no-thresholds ~/script.js
```

## No VU connection reuse

A boolean, true or false, specifying whether k6 should reuse TCP connections
between iterations of a VU.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_NO_VU_CONNECTION_REUSE	--no-vu-connection-reuse	noVUConnectionReuse	false
```

```jsts
export const options = {
  noVUConnectionReuse: true,
};
```

## Paused 

A boolean, true or false, specifying whether the test should start in a paused state. To resume a paused state you'd use the `k6 resume` command.
```
NV	CLI	CODE / CONFIG FILE	DEFAULT

K6_PAUSED	--paused, -p	paused	false
```

```jsts
export const options = {
  paused: true,
};
```

When paused:

```shell
➜  pt-samples git:(master) ✗ k6 run  pt-1-0001-stages.ts -p
\
          /\      |‾‾| /‾‾/   /‾‾/   
     /\  /  \     |  |/  /   /  /    
    /  \/    \    |     (   /   ‾‾\  
   /          \   |  |\  \ |  (‾)  | 
  / __________ \  |__| \__\ \_____/ .io

  execution: local
     script: pt-1-0001-stages.ts
     output: -

  scenarios: (100.00%) 1 scenario, 2 max VUs, 10m30s max duration (incl. graceful stop):
           * default: 10 iterations shared among 2 VUs (maxDuration: 10m0s, gracefulStop: 30s)


Run       [======================================] paused
default   [--------------------------------------]
```

When resumed:

```shell
➜  pt-samples git:(master) ✗ k6 resume
status: 4
paused: "false"
vus: "0"
vus-max: "2"
stopped: false
running: false
tainted: false
```

## Quiet

A boolean, true or false, that disables the progress update bar on the console output.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

N/A	--quiet, -q	N/A	false
```

```shell
$ k6 run script.js -d 20s --quiet
```

## Result output

Specify the results output.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_OUT	--out, -o	N/A	null
```

```jsts
$ k6 run --out influxdb=http://localhost:8086/k6 script.js
```

## RPS

The maximum number of requests to make per second, in total across all VUs.

> This option is discouraged The --rps option has caveats and is difficult to
> use correctly.
> 
> For example, in the cloud or distributed execution, this option affects every
> k6 instance independently. That is, it is not sharded like VUs are. We
> strongly recommend the arrival-rate executors to simulate constant RPS instead
> of this option.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_RPS	--rps	rps	0 (unlimited)
```

```jsts
export const options = {
  rps: 500,
};
```

# Scenario

Define one or more execution patterns, with various VU and iteration scheduling
settings, running different exported functions (besides default!), using
different environment variables, tags, and more.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

N/A	N/A	scenarios	null
```

```jsts
export const options = {
  scenarios: {
    my_api_scenario: {
      // arbitrary scenario name
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '5s', target: 100 },
        { duration: '5s', target: 0 },
      ],
      gracefulRampDown: '10s',
      env: { MYVAR: 'example' },
      tags: { my_tag: 'example' },
    },
  },
};
```

## Setup timeout 

Specify how long the `setup()` function is allow to run before it's terminated
and the test fails.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_SETUP_TIMEOUT	N/A	setupTimeout	"60s"
```

```jsts
export const options = {
  setupTimeout: '30s',
};
```

## Teardown timeout

Specify how long the `teardown()` function is allowed to run before it's
terminated and the test fails.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_TEARDOWN_TIMEOUT	N/A	teardownTimeout	"60s"
```

```jsts
export const options = {
  teardownTimeout: '30s',
};
```


## Stages

A list of VU { target: ..., duration: ... } objects that specify the target
number of VUs to ramp up or down to for a specific period.

It is a shortcut option for a single `scenario` with a `ramping VUs executor`.
If used together with the `VUs` option, the vus value is used as the startVUs
option of the executor.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_STAGES	--stage <duration>:<target>, -s <duration>:<target>	stages	Based on vus and duration.
```

```jsts
// The following config would have k6 ramping up from 1 to 10 VUs for 3 minutes,
// then staying flat at 10 VUs for 5 minutes, then ramping up from 10 to 35 VUs
// over the next 10 minutes before finally ramping down to 0 VUs for another
// 3 minutes.

export const options = {
  stages: [
    { duration: '3m', target: 10 },
    { duration: '5m', target: 10 },
    { duration: '10m', target: 35 },
    { duration: '3m', target: 0 },
  ],
};

```

## Supply environment variables

Add/override an `environment variable`` with VAR=valuein a k6 script. Available
in k6 run and k6 cloud commands.

To make the system environment variables available in the k6 script via
`__ENV``, use the `--include-system-env-vars` option.

> The `-e` flag does not configure options This flag just provides variables to
> the script, which the script can use or ignore. For example, -e
> K6_ITERATIONS=120 does not configure the script iterations.
> 
> Compare this behavior with K6_ITERATIONS=120 k6 run script.js, which does set
> iterations.


```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

N/A	--env, -e	N/A	null
```

```shell
$ k6 run -e FOO=bar ~/script.js
```

## System tags

Specify which system tags will be in the collected metrics. Some collectors like
the cloud one may require that certain system tags be used. You can specify the
tags as an array from the JS scripts or as a comma-separated list via the CLI.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_SYSTEM_TAGS	--system-tags	systemTags	proto,subproto,status,method,url,name,group,check,error,error_code,tls_version,scenario,service,expected_response
```


```jsts
export const options = {
  systemTags: ['status', 'method', 'url'],
};
```

## Summary time unit

Define which time unit will be used for all time values in the end-of-test
summary. Possible values are `s` (seconds), `ms` (milliseconds) and us
(microseconds). If no value is specified, k6 will use mixed time units, choosing
the most appropriate unit for each value.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_SUMMARY_TIME_UNIT	--summary-time-unit	summaryTimeUnit	null
```

```jsts
export const options = {
  summaryTimeUnit: 'ms',
};
```

## Summary trend stats

Define which stats for [Trend
metrics](https://k6.io/docs/javascript-api/k6-metrics/trend/) (e.g. response
times, group/iteration durations, etc.) will be shown in the end-of-test
summary. Possible values include avg (average), med (median), min, max, count,
as well as arbitrary percentile values (e.g. p(95), p(99), p(99.99), etc.).

For further summary customization and exporting the summary in various formats
(e.g. JSON, JUnit/XUnit/etc. XML, HTML, .txt, etc.), refer to the new
handleSummary() callback.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_SUMMARY_TREND_STATS	--summary-trend-stats	summaryTrendStats	avg,min,med,max,p(90),p(95)
```

```jsts
export const options = {
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(95)', 'p(99)', 'p(99.99)', 'count'],
};
```

```shell
$ k6 run --summary-trend-stats="avg,min,med,max,p(90),p(99.9),p(99.99),count" ./script.js
```

## tags

Specify tags that should be set test wide across all metrics. If a tag with the
same name has been specified on a request, check or custom metrics it will have
precedence over a test wide tag.

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

N/A	--tag NAME=VALUE	tags	null
```

```jsts
export const options = {
  tags: {
    name: 'value',
  },
};
```


## Thresholds

A collection of threshold specifications to configure under what condition(s) a
test is considered successful or not, when it has passed or failed, based on
metric data. To learn more, have a look at the
[Thresholds](https://k6.io/docs/using-k6/thresholds) documentation. 


```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

N/A	N/A	thresholds	null
```

```jsts
export const options = {
  thresholds: {
    'http_req_duration': ['avg<100', 'p(95)<200'],
    'http_req_connecting{cdnAsset:true}': ['p(95)<100'],
  },
};
```

## Throw 

A boolean, true or false, specifying whether k6 should throw exceptions when certain errors occur, or if it should just log them with a warning. Behaviors that currently depend on this option:

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

K6_THROW	--throw, -w	throw	false
```


```jsts
import http from 'k6/http';
import exec from 'k6/execution';
import { group } from 'k6';

export const options = {
  vus: 2,
  iterations: 10,
  throw: true,
 };

export default function () {
  exec.vu.tags.test = 'main';

  group('main', function () {
    http.get('https://test.k6.io1');
    http.get('https://test.k6.io');
  });

  delete exec.vu.tags.test;
}
```

before :

```shell
WARN[0002] Request Failed                                error="Get \"https://test.k6.io1\": lookup test.k6.io1: no such host"
WARN[0003] Request Failed                                error="Get \"https://test.k6.io1\": lookup test.k6.io1: no such host"

running (00m03.1s), 0/2 VUs, 10 complete and 0 interrupted iterations
default ✓ [======================================] 2 VUs  00m03.1s/10m0s  10/10 shared iters

     █ main

     data_received..................: 126 kB 41 kB/s
     data_sent......................: 1.7 kB 538 B/s
```

after:

```shell
ERRO[0000] GoError: Get "https://test.k6.io1": lookup test.k6.io1: no such host
        at go.k6.io/k6/js/modules/k6/http.(*RootModule).NewModuleInstance.func2 (native)
        at file:///Users/tenglong.tl/Works/Projects/test-toolkit/test/pt-samples/pt-1-0001-stages.ts:15:4(5)
        at go.k6.io/k6/js/modules/k6.(*K6).Group-fm (native)
        at file:///Users/tenglong.tl/Works/Projects/test-toolkit/test/pt-samples/pt-1-0001-stages.ts:14:2(11)
        at native  executor=shared-iterations scenario=default source=stacktrace

running (00m00.0s), 0/2 VUs, 10 complete and 0 interrupted iterations
default ✓ [======================================] 2 VUs  00m00.0s/10m0s  10/10 shared iters

     █ main

     data_received..............: 0 B     0 B/s
     data_sent..................: 0 B     0 B/s
```

## User agent

A string specifying the user-agent string to use in **User-Agent** headers when
sending HTTP requests. If you pass an empty string, no User-Agent header is
sent. Available in k6 run and k6 cloud commands

## Verbose

A boolean specifying whether verbose logging is enabled. 

```
ENV	CLI	CODE / CONFIG FILE	DEFAULT

N/A	--verbose, -v	N/A	false
```

The verbose output:

```shell
➜  pt-samples git:(master) ✗ k6 run  pt-1-0001-stages.ts -v
DEBU[0000] Logger format: TEXT                          
DEBU[0000] k6 version: v0.38.3 ((devel), go1.18.2, darwin/amd64) 

          /\      |‾‾| /‾‾/   /‾‾/   
     /\  /  \     |  |/  /   /  /    
    /  \/    \    |     (   /   ‾‾\  
   /          \   |  |\  \ |  (‾)  | 
  / __________ \  |__| \__\ \_____/ .io

DEBU[0000] Resolving and reading test 'pt-1-0001-stages.ts'... 
DEBU[0000] Loading...                                    moduleSpecifier="file:///Users/tenglong.tl/Works/Projects/test-toolkit/test/pt-samples/pt-1-0001-stages.ts" originalModuleSpecifier=pt-1-0001-stages.ts
DEBU[0000] 'pt-1-0001-stages.ts' resolved to 'file:///Users/tenglong.tl/Works/Projects/test-toolkit/test/pt-samples/pt-1-0001-stages.ts' and successfully loaded 311 bytes! 
DEBU[0000] Gathering k6 runtime options...              
DEBU[0000] Initializing k6 runner for 'pt-1-0001-stages.ts' (file:///Users/tenglong.tl/Works/Projects/test-toolkit/test/pt-samples/pt-1-0001-stages.ts)... 
DEBU[0000] Detecting test type for...                    test_path="file:///Users/tenglong.tl/Works/Projects/test-toolkit/test/pt-samples/pt-1-0001-stages.ts"
DEBU[0000] Trying to load as a JS test...                test_path="file:///Users/tenglong.tl/Works/Projects/test-toolkit/test/pt-samples/pt-1-0001-stages.ts"
DEBU[0000] Babel: Transformed                            t=64.869053ms
DEBU[0000] Runner successfully initialized!             
DEBU[0000] Parsing CLI flags...                         
DEBU[0000] Consolidating config layers...               
DEBU[0000] Parsing thresholds and validating config...  
DEBU[0000] Initializing the execution scheduler...      
DEBU[0000] Starting 1 outputs...                         component=output-manager
DEBU[0000] Starting...                                   component=metrics-engine-ingester
DEBU[0000] Started!                                      component=metrics-engine-ingester
  execution: local
     script: pt-1-0001-stages.ts
     output: -

  scenarios: (100.00%) 1 scenario, 2 max VUs, 10m30s max duration (incl. graceful stop):
           * default: 10 iterations shared among 2 VUs (maxDuration: 10m0s, gracefulStop: 30s)

DEBU[0000] Starting the REST API server on localhost:6565 
DEBU[0000] Initialization starting...                    component=engine
DEBU[0000] Starting emission of VUs and VUsMax metrics... 
DEBU[0000] Start of initialization                       executorsCount=1 neededVUs=2 phase=local-execution-scheduler-init
DEBU[0000] Initialized VU #1                             phase=local-execution-scheduler-init
DEBU[0000] Initialized VU #2                             phase=local-execution-scheduler-init
DEBU[0000] Finished initializing needed VUs, start initializing executors...  phase=local-execution-scheduler-init
DEBU[0000] Initialized executor default                  phase=local-execution-scheduler-init
DEBU[0000] Initialization completed                      phase=local-execution-scheduler-init
DEBU[0000] Execution scheduler starting...               component=engine
DEBU[0000] Start of test run                             executorsCount=1 phase=local-execution-scheduler-run
DEBU[0000] Running setup()                               phase=local-execution-scheduler-run
DEBU[0000] Metrics processing started...                 component=engine
DEBU[0000] Start all executors...                        phase=local-execution-scheduler-run
DEBU[0000] Starting executor                             executor=default startTime=0s type=shared-iterations
DEBU[0000] Starting executor run...                      executor=shared-iterations iterations=10 maxDuration=10m0s scenario=default type=shared-iterations vus=2
DEBU[0002] Executor finished successfully                executor=default startTime=0s type=shared-iterations
DEBU[0002] Running teardown()                            phase=local-execution-scheduler-run
DEBU[0002] Regular duration is done, waiting for iterations to gracefully finish  executor=shared-iterations gracefulStop=30s scenario=default
DEBU[0002] Metrics emission of VUs and VUsMax metrics stopped 
DEBU[0002] Execution scheduler terminated                component=engine error="<nil>"
DEBU[0002] Processing metrics and thresholds after the test run has ended...  component=engine
DEBU[0002] Stopping...                                   component=metrics-engine-ingester
DEBU[0002] run: execution scheduler terminated           component=engine
DEBU[0002] Stopped!                                      component=metrics-engine-ingester
DEBU[0002] Engine run terminated cleanly                

running (00m01.7s), 0/2 VUs, 10 complete and 0 interrupted iterations
default ✗ [======================================] 2 VUs  00m01.6s/10m0s  10/10 shared iters
DEBU[0002] Engine: Thresholds terminated                 component=engine

running (00m01.7s), 0/2 VUs, 10 complete and 0 interrupted iterations
default ✗ [======================================] 2 VUs  00m01.6s/10m0s  10/10 shared iters

     █ main

     data_received..................: 126 kB 76 kB/s
     data_sent......................: 1.7 kB 1.0 kB/s
     group_duration.................: avg=329.46ms min=218.79ms med=219.6ms  max=769.38ms p(90)=766.71ms p(95)=768.04ms
     http_req_blocked...............: avg=110.01ms min=1µs      med=2.5µs    max=552.24ms p(90)=548.29ms p(95)=550.27ms
     http_req_connecting............: avg=42.66ms  min=0s       med=0s       max=213.42ms p(90)=213.25ms p(95)=213.34ms
     http_req_duration..............: avg=219.47ms min=216.69ms med=219.26ms max=222.97ms p(90)=221.54ms p(95)=222.25ms
       { expected_response:true }...: avg=219.47ms min=216.69ms med=219.26ms max=222.97ms p(90)=221.54ms p(95)=222.25ms
     http_req_failed................: 0.00%  ✓ 0      ✗ 10 
     http_req_receiving.............: avg=127.7µs  min=60µs     med=99µs     max=432µs    p(90)=154.79µs p(95)=293.39µs
     http_req_sending...............: avg=24.9µs   min=7µs      med=16.5µs   max=78µs     p(90)=40.19µs  p(95)=59.09µs 
     http_req_tls_handshaking.......: avg=66.65ms  min=0s       med=0s       max=335.27ms p(90)=331.64ms p(95)=333.46ms
     http_req_waiting...............: avg=219.32ms min=216.56ms med=219.17ms max=222.85ms p(90)=221.42ms p(95)=222.13ms
     http_reqs......................: 10     6.0535/s
     iteration_duration.............: avg=329.6ms  min=218.86ms med=219.71ms max=769.47ms p(90)=767.28ms p(95)=768.38ms
     iterations.....................: 10     6.0535/s
     vus............................: 2      min=2    max=2
     vus_max........................: 2      min=2    max=2

DEBU[0002] Waiting for engine processes to finish...    
DEBU[0002] Metrics processing winding down...            component=engine
DEBU[0002] Everything has finished, exiting k6!         
DEBU[0002] Stopping 1 outputs...                         component=output-manager
DEBU[0002] Stopping...                                   component=metrics-engine-ingester
DEBU[0002] Stopped!                                      component=metrics-engine-ingester
```
