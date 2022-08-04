---
title: "K6 Options"
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

