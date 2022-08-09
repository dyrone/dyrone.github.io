---
title: "k6 series [5] - Ramping Vus"
date: 2022-08-08T21:06:58+08:00
draft: false
tags: 
    - "testing"
---

> NOTICE: Base and excerpt from the official k6 documentation 

A variable number of VUs execute as many iterations as possible for a specified
amount of time. This executor is equivalent to the global stages option.

## Options


```
OPTION	TYPE	DESCRIPTION	DEFAULT

stages(required)	array	Array of objects that specify the target number of VUs to ramp up or down to.	[]

startVUs	integer	Number of VUs to run at test start.	1

gracefulRampDown	string	Time to wait for an already started iteration to finish before stopping it during a ramp down.
```

## When

This executor is a good fit if you need VUs to ramp up or down during specific
periods of time.

## Example 

```
import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  discardResponseBodies: true,
  scenarios: {
    contacts: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '20s', target: 10 },
        { duration: '10s', target: 0 },
      ],
      gracefulRampDown: '0s',
    },
  },
};

export default function () {
  http.get('https://test.k6.io/contacts.php');
  // We're injecting a processing pause for illustrative purposes only!
  // Each iteration will be ~515ms, therefore ~2 iterations/second per VU maximum throughput.
  sleep(0.5);
}
```

> Note the setting of gracefulRampDown to 0 seconds, which could cause some
> iterations to be interrupted during the ramp down stage.


In this example, we'll run a two-stage test, ramping up from 0 to 10 VUs over 20
seconds, then down to 0 VUs over 10 seconds.

![ramping](https://k6.io/docs/static/ad4a4ec4534d20df652e008b48943375/b8e6a/ramping-vus.png "ramping")


## Get the stage index


To get the current running stage index, use the getCurrentStageIndex helper
function from the k6-jslib-utils library. It returns a zero-based number equal
to the position in the shortcut stages array or in the executor's stages array.


```js
import { getCurrentStageIndex } from 'https://jslib.k6.io/k6-utils/1.3.0/index.js';

export const options = {
  stages: [
    { target: 10, duration: '30s' },
    { target: 50, duration: '1m' },
    { target: 10, duration: '30s' },
  ],
};

export default function () {
  if (getCurrentStageIndex() === 1) {
    console.log('Running the second stage where the expected target is 50');
  }
}
```
