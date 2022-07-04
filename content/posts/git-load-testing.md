---
title: "Git Load Testing"
date: 2022-06-27T14:42:35+08:00
draft: true
tag:  "testing"
---


# What's Load Testing


> Load Testing is a type of performance testing which determines the performance of a system, software product or software application under real life based load conditions.

# Benchmark inputs

* virtual users (VUs) : define the scale of the parallel loops
* schedule: define how long will the test running 


# What's the difference between Load Testing and Stress Testing

| Load Testing  | Stress Testing  |
|:--|:--|
|Load Testing is performed to test the performance of the system or software application under extreme load.	   |Stress Testing is performed to test the robustness of the system or software application under extreme load.|
| Stress Testing is performed to test the robustness of the system or software application under extreme load.
  | In stress testing load limit is above the threshold of a break.|
|In load testing, the performance of the software is tested under multiple number of users.	   |In stress testing, the performance is tested under varying data amounts. |
|Huge number of users.	   | Too much users and too much data. |
|Load testing is performed to find out the upper limit of the system or application.	   | Stress testing is performed to find the behavior of the system under pressure. |
| The factor tested during load testing is performance.	  | The factor tested during stress testing is robustness and stability.  |

| The factor tested during load testing is performance.	  | The factor tested during stress testing is robustness and stability.  |

> From: https://www.geeksforgeeks.org/difference-between-load-testing-and-stress-testing/#:~:text=Load%20testing%20is%20performed%20to%20find%20out%20the%20upper%20limit,testing%20is%20robustness%20and%20stability.


# Popular Load Testing Opensource Tools


## JMeter



## The cloud native load testing framework:  K6

# base on command line API
# base on javaScript

支持 cloud tests， 即基于docker (compose)进行测试， https://k6.io/cloud/

> From: https://www.youtube.com/watch?v=Hu1K2ZGJ_K4
> Repo: https://github.com/cajames/performanc...
> k6: https://k6.io/


* CI支持: https://k6.io/docs/integrations/#continuous-integration-and-continuous-delivery

* 转化：

* HAR: https://github.com/grafana/har-to-k6
* Postman-to-k6: https://github.com/apideck-libraries/postman-to-k6
* Swagger/OpenAPI: https://k6.io/blog/load-testing-your-api-with-swagger-openapi-and-k6/

* 数据存储和可视化：https://k6.io/docs/integrations/#result-store-and-visualization

* 命令行扩展：
除了API之外，还支持扩展命令行执行，https://github.com/grafana/xk6-exec， 我们可以基于k6+hyperfine进行集成。

	* sharness负责编写用例
    * k6进行API的测试用例编写
	* hyperfine进行CLI的测试用例编写
	
* 数据：不管是API还是CLI，最终都通过统一的数据格式完成组装，该数据格式与测试的基线格式一直，用于比对。



支持IDE集成

#
