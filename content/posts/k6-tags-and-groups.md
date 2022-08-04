---
title: "K6 Tags and Groups"
date: 2022-08-04T20:10:11+08:00
draft: false
tags:
    - "testing"
---

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

## User-defined tags

You can tag the following entities:

* requests
* checks
* thresholds
* custom metrics
