---
title: "Github Api Glance"
date: 2023-02-28T11:12:13+08:00
draft: false 
---

## API 请求 

### Accept 头

```shell
gh api --header 'Accept: application/vnd.github+json'
```

绝大多数的Github Rest API使用该Accept标头。但是也可能存在其他的类型。

### API Version 头

```
gh api --header 'X-GitHub-Api-Version:2022-11-28'
```

Github API的版本通过header指定，是一个yyyy-MM-dd格式的value。

### Parameters

For `Get`:

```shell
$ curl -i "https://api.github.com/repos/vmg/redcarpet/issues?state=closed"
```

For `POST` `PATCH` `PUT` `DELETE`:

```shell
$ curl -i -u username -d '{"scopes":["repo_deployment"]}' https://api.github.com/authorizations
```

> Many API methods take optional parameters. For GET requests, any parameters not
> specified as a segment in the path can be passed as an HTTP query string
> parameter. In this example, the 'vmg' and 'redcarpet' values are provided for
> the :owner and :repo parameters in the path while :state is passed in the query
> string.
> 
> For POST, PATCH, PUT, and DELETE requests, parameters not included in the URL
> should be encoded as JSON with a Content-Type of 'application/json'



## API 响应

### Response status code

Github使用的是标准的HTTP Response Status:

> https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

### Response Body

Github的响应默认是JSON格式，除非另外指定。

### Response Field

空的字段使用null， 而不是直接忽略:

> Blank fields are included as null instead of being omitted.

 时间使用UTC时间
> All timestamps return in UTC time, ISO 8601 format:
> YYYY-MM-DDTHH:MM:SSZ

区分概览和详细的数据信息:

> Summary representations
> When you fetch a list of resources, the response includes a subset of the attributes for that resource. This is the "summary" representation of the resource. (Some attributes are computationally expensive for the API to provide. For performance reasons, the summary representation excludes those attributes. To obtain those attributes, fetch the "detailed" representation.)
> 
> Example: When you get a list of repositories, you get the summary representation
> of each repository. Here, we fetch the list of repositories owned by the octokit
> organization:
> 
> GET /orgs/octokit/repos
> 
> When you fetch an individual resource, the response typically includes all attributes for that resource. This is the "detailed" representation of the resource. (Note that authorization sometimes influences the amount of detail included in the representation.)
> 
> Example: When you get an individual repository, you get the detailed representation of the repository. Here, we fetch the octokit/octokit.rb repository:
> 
> GET /repos/octokit/octokit.rb


## 鉴权

鉴权支持两种方式：

* Basic Auth
* OAuth2 
** OAuth2 Auth(in header)
** OAuth2 key/secret

### Basic Auth

```
$ curl -u "username" https://api.github.com
```

### OAuth2 in header

```shell
$ curl -H "Authorization: Bearer OAUTH-TOKEN"
https://api.github.com
``` 

> Note: In most cases, you can use Authorization: Bearer or Authorization: token
> to pass a token. However, if you are passing a JSON web token (JWT), you must
> use Authorization: Bearer.

### OAuth with key/secret

> Github在2021年已经不支持基于`query parameter`的方式请求API:
> 
> https://developer.github.com/changes/2020-02-10-deprecating-auth-through-query-param/

```shell
curl -u my_client_id:my_client_secret 'https://api.github.com/user/repos'
```

注意，使用`client_id` 和 `client_secret` 并不会基于用户鉴权，其作用只是提升
对应 OAuth App 的rate limit。

```shell
$ curl -u my_client_id:my_client_secret -I https://api.github.com/user/repos
> HTTP/2 200
> Date: Mon, 01 Jul 2013 17:27:06 GMT
> x-ratelimit-limit: 5000
> x-ratelimit-remaining: 4966
> x-ratelimit-used: 34
> x-ratelimit-reset: 1372700873
```

> https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#increasing-the-unauthenticated-rate-limit-for-oauth-apps

> **故， client_id 和 client_secret 只能用于server-to-server场景，而绝不应
> 用于client-to-server场景，即其不应该泄露给任何的用户，这也是Github一种
> 保护的设计。**

### Auth failed and login limit failed

### Auth failed (401: bad credentials)

```shell
$ curl -I https://api.github.com -u foo:bar
> HTTP/2 401

> {
>   "message": "Bad credentials",
>   "documentation_url": "https://docs.github.com/rest"
> }
```

### Reach login failed limit (403)

当用户短时间内多次鉴权失败， API将会在一段时间内拒绝该用户的鉴权操作。
  
```shell
$ curl -i https://api.github.com -u 
-u VALID_USERNAME:VALID_TOKEN 
> HTTP/2 403
> {
>   "message": "Maximum number of login attempts exceeded. Please try again later.",
>   "documentation_url": "https://docs.github.com/rest"
> }
```

### 错误处理

### 422 Unprocessable Entity

无效的字段将会返回422：

```JSON
 HTTP/2 422
 Content-Length: 149

 {
   "message": "Validation Failed",
   "errors": [
     {
       "resource": "Issue",
       "field": "title",
       "code": "missing_field"
     }
   ]
 }
```

关于此种类型的错误，具体的定义如下：

For :Code: Description"

* missing: A resource does not exist.
* missing_field: A required field on a resource has not been set.
* invalid: The formatting of a field is invalid. Review the documentation for
  more specific information.
* already_exists: Another resource has the same value as this field. This can
happen in resources that must have some
* unique key (such as label names).
* unprocessable: The inputs provided were invalid.

> Resources may also send custom validation errors (where code is custom). Custom
> errors will always have a message field describing the error, and most errors
> will also include a documentation_url field pointing to some content that might
> help you resolve the error.

## 请求重定向

> 301: Permanent redirection. The URI you used to make the request has been
> superseded by the one specified in the Location header field. This and all
> future requests to this resource should be directed to the new URI.
> 
> 302, 307: Temporary redirection. The request should be repeated verbatim to
> the URI specified in the Location header field but clients should continue to
> use the original URI for future requests.

## HTTP verbs

* HEAD: Can be issued against any resource to get just the HTTP header info.
* GET: Used for retrieving resources.
* POST: Used for creating resources.
* PATCH: Used for updating resources with partial JSON data. For instance, an
  Issue resource has title and body attributes. A PATCH request may accept one
  or more of the attributes to update the resource.
* PUT: Used for replacing resources or collections. For PUT requests with no
  body attribute, be sure to set the Content-Length header to zero.
* DELETE: Used for deleting resources.

## 分页

Github默认会对查询出的结果进行分页，与gitlab类似，使用Response Header的方式：

```shell
➜  ~ curl --include --request GET \
--url "https://api.github.com/repos/octocat/Spoon-Knife/issues" \
--header "Accept: application/vnd.github+json" -I
HTTP/2 200 
server: GitHub.com
date: Tue, 28 Feb 2023 07:25:05 GMT
content-type: application/json; charset=utf-8
cache-control: public, max-age=60, s-maxage=60
vary: Accept, Accept-Encoding, Accept, X-Requested-With
etag: W/"4ea7ff18843015a30310314bb43a143f6ca15eb789a620b03631735696920fd1"
x-github-media-type: github.v3; format=json
link: <https://api.github.com/repositories/1300192/issues?page=2>; rel="next", <https://api.github.com/repositories/1300192/issues?page=527>; rel="last"
x-github-api-version-selected: 2022-11-28
access-control-expose-headers: ETag, Link, Location, Retry-After, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Used, X-RateLimit-Resource, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval, X-GitHub-Media-Type, X-GitHub-SSO, X-GitHub-Request-Id, Deprecation, Sunset
access-control-allow-origin: *
strict-transport-security: max-age=31536000; includeSubdomains; preload
x-frame-options: deny
x-content-type-options: nosniff
x-xss-protection: 0
referrer-policy: origin-when-cross-origin, strict-origin-when-cross-origin
content-security-policy: default-src 'none'
x-ratelimit-limit: 60
x-ratelimit-remaining: 55
x-ratelimit-reset: 1677570997
x-ratelimit-resource: core
x-ratelimit-used: 5
accept-ranges: bytes
content-length: 114180
x-github-request-id: 69D2:0867:5DC7510:C1F1115:63FDAC5A
```

在Response Header中，`link`用于进行分页处理：

```
link: <https://api.github.com/repositories/1300192/issues?page=2>; rel="next",                             <https://api.github.com/repositories/1300192/issues?page=527>; rel="last" 
```
* The URL for the previous page is followed by rel="prev".
* The URL for the next page is followed by rel="next".
* The URL for the last page is followed by rel="last".
* The URL for the first page is followed by rel="first".

知道了页数信息之后，我们就可以进行查看其他page的数据：

```
curl --include --request GET \
--url "https://api.github.com/repositories/1300192/issues?page=515" \
--header "Accept: application/vnd.github+json" -I
```

为了避免查询查询和endpoints的参数混淆，所有的case都可以基于`link` header
的方式查询分页数据。

### 设置分页数量: per_page
```
curl --include --request GET \
--url "https://api.github.com/repos/octocat/Spoon-Knife/issues?per_page=2" \
--header "Accept: application/vnd.github+json"
```

在Response的Header中，`link`会自动附带`per_page`参数:

```
link: <https://api.github.com/repositories/1300192/issues?per_page=2&page=2>; rel="next", <https://api.github.com/repositories/1300192/issues?per_page=2&page=7715>; rel="last"
```

## 超时处理

Github默认使用`10s`作为超时时间，如果超时那么返回:
```JSON
{
    "message": "Server Error"
}
```

> Note: GitHub reserves the right to change the timeout window to protect the
> speed and reliability of the API.


## 限流

* 不同的API有不同限流的设定

在API Response Header中进行了描述, 从描述中大概可以看到其基于令牌桶设计：

```
x-ratelimit-limit: 60
x-ratelimit-remaining: 59
x-ratelimit-reset: 1677570997
x-ratelimit-resource: core
x-ratelimit-used: 1
```

### 个人账号限流 (user-to-server)

> GitHub associates all user-to-server requests with the authenticated user. For
> OAuth Apps and GitHub Apps, this is the user who authorized the app. All
> user-to-server requests count toward the authenticated user's rate limit.
> 
> User-to-server requests are limited to 5,000 requests per hour and per
> authenticated user. All requests from OAuth applications authorized by a user
> or a personal access token owned by the user, and requests authenticated with
> any of the user's authentication credentials, share the same quota of 5,000
> requests per hour for that user.

* 已鉴权的请求-非企业用户：5000个限流令牌 / 1 hour / 所有个人鉴权的方式均共享
* 已鉴权的请求-企业用户：15000 / 1 hour / 所有个人鉴权的方式均共享
* 未鉴权的请求: 60 / 1 hour / originating IP address

> The request is from a GitHub App that's owned by a GitHub Enterprise Cloud
> organization. The request is from an OAuth App that's owned or approved by a
> GitHub Enterprise Cloud organization.

### App 调用限流

App的限流可能包括 `user-to-server` 以及`server-to-server`限流。

> https://docs.github.com/en/apps/creating-github-apps/creating-github-apps/rate-limits-for-github-apps

#### server-to-server

* Default:

< 20 installations: 5000 / 1 hour

\+ 20 installations: + 50 / 1 hour

* EE:

15000 / 1 hour

#### user-to-server

* Default:

5000 / 1 hour / oauth token + personal access token + any authetication
credentials

* EE:

15000 / 1 hour

## API Version

Github 的API版本是基于时间的，例如`2022-11-28`，通过请求头`X-GitHub-Api-Version`
进行传递，这样的好处是， 便于发现不兼容的情况时，及时回退， 而Github这种设计
在向后兼容上明显是一个好的开闭原则的设计，并且考虑到了不兼容性缺陷对于用户的
最大程度的弥补措施。

> 如果请求的是一个不在支持的版本， 那么将会返回400的错误

可以通过/versions接口，来查看当前支持的版本信息：

```shell
➜  ~ curl   https://api.github.com/versions
[
  "2022-11-28"
]
```
任何破坏性的API改动都会发布一个新的API version, 破坏性的改动包括：

* removing an entire operation //删除一个API
* removing or renaming a parameter //重命名参数
* removing or renaming a response field //重命名返回字段
* adding a new required parameter //新增一个必填参数
* making a previously optional parameter required //非必填变成必填
* changing the type of a parameter or response field //修改参数或字段类型
* removing enum values //删除枚举
* adding a new validation rule to an existing parameter //参数新增校验规则
* changing authentication or authorization requirements //鉴权或者授权的变化

非破坏性的(扩展)改动包括:

* adding an operation //新增一个接口
* adding an optional parameter //新增一个非必填参数
* adding an optional request header //新增一个非必填的请求头
* adding a response field //新增一个响应字段
* adding a response header //新增一个响应头
* adding enum values //新增枚举

## 多媒体类型

### 通用类型

* application/vnd.github+json
* application/json
* application/vnd.github.raw+json

### 评论类型

* application/vnd.github.raw+json: Return the raw markdown body. Response will
  include body. This is the default if you do not pass any specific media type.
* application/vnd.github.text+json: Return a text only representation of the
  markdown body. Response will include body_text.
* application/vnd.github.html+json: Return HTML rendered from the body's
  markdown. Response will include body_html.
* application/vnd.github.full+json: Return raw, text and HTML representations.
  Response will include body, body_text, and body_html:
  
### BLOB类型

* application/vnd.github+json 或者 application/json: Return JSON representation
  of the blob with content as a base64 encoded string. This is the default if
  nothing is passed.
* application/vnd.github.raw: Return the raw blob data.

### Commits, commit comparison, and pull requests类型

* application/vnd.github.diff
* application/vnd.github.patch
* application/vnd.github.sha

### 仓库文件（Repository contents）

* application/vnd.github.raw: Return the raw contents of a file. This is the
  default if you do not pass any specific media type.
* application/vnd.github.html: For markup files such as Markdown or AsciiDoc,
  you can retrieve the rendered HTML using the .html media type. Markup
  languages are rendered to HTML using our open-source Markup library.


### OpenAPI Description

> https://docs.github.com/en/rest/overview/openapi-description?apiVersion=2022-11-28

OpenAPI是一个用户描述REST APIs的标准, 其遵守OpenAPI 3.0协议。

Github的 OpenAPI Description 如下：

> https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md

作用如下：
* 自动生成API客户端代码
* 校验和测试 API
* 使用Insomnia 或 Postman等三方工具完成对API的管理和调用
* 自动生成API文档: https://docs.github.com/en/rest?apiVersion=2022-11-28

## 特殊API

### 根接口

根接口定义了Github REST API 对于一些通用规范支持等能力：

```shell
➜  ~ curl -I https://api.github.com
HTTP/2 200 
server: GitHub.com
date: Tue, 28 Feb 2023 06:56:30 GMT
content-type: application/json; charset=utf-8
cache-control: public, max-age=60, s-maxage=60
vary: Accept, Accept-Encoding, Accept, X-Requested-With
etag: W/"4f825cc84e1c733059d46e76e6df9db557ae5254f9625dfe8e1b09499c449438"
x-github-media-type: github.v3; format=json
x-github-api-version-selected: 2022-11-28
access-control-expose-headers: ETag, Link, Location, Retry-After, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Used, X-RateLimit-Resource, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval, X-GitHub-Media-Type, X-GitHub-SSO, X-GitHub-Request-Id, Deprecation, Sunset
access-control-allow-origin: *
strict-transport-security: max-age=31536000; includeSubdomains; preload
x-frame-options: deny
x-content-type-options: nosniff
x-xss-protection: 0
referrer-policy: origin-when-cross-origin, strict-origin-when-cross-origin
content-security-policy: default-src 'none'
x-ratelimit-limit: 60
x-ratelimit-remaining: 59
x-ratelimit-reset: 1677570997
x-ratelimit-resource: core
x-ratelimit-used: 1
accept-ranges: bytes
content-length: 2262
x-github-request-id: 5FEE:1F16:7C51F70:FFE6F11:63FDA5A4
```

### 扮演Github App应用身份-可调用的API列表 以及 创建时的API权限对应关系

可访问API列表：

> https://docs.github.com/en/rest/overview/endpoints-available-for-github-apps?apiVersion=2022-11-28

创建Github App时，勾选的权限（set permissions）与API的对应关系：

> https://docs.github.com/en/rest/overview/permissions-required-for-github-apps?apiVersion=2022-11-28

### fine-grained 个人访问令牌-可调用的API列表

可访问API列表：

> https://docs.github.com/en/rest/overview/endpoints-available-for-fine-grained-personal-access-tokens?apiVersion=2022-11-28

创建fine-grained 个人访问令牌时， 勾选的权限与API的对应关系：

> https://docs.github.com/en/rest/overview/permissions-required-for-fine-grained-personal-access-tokens?apiVersion=2022-11-28


个人访问令牌类型介绍：
> https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

## API 开源库

> https://docs.github.com/en/rest/overview/libraries?apiVersion=2022-11-28

* ruby
* .net
* Clojure
* Dart
* Emacs Lisp
* Erlang
* Go
* Haskell
* Java
* JavaScript
* Julia
* OCaml
* Perl
* PHP
* PowerShell
* Shell
* ....

## API 列表和排期任务


| group  | endpoint  | link  | status  | priority|
|:-:|:-:|:-:|:-:|:-:|
| Action  |   |   |   |   |
| Activity  |   |   |   |   |
| Apps  |   |   |   |   |
| Billing |   |   |   |   |
| Branches |   |   |   |   |
| Checks |   |   |   |   |
| Codes of conduct  |   |   |   |   |
| Code Scanning |   |   |   |   |
| Codespaces  |   |   |   |   |
| Collaborators |   |   |   |   |
| Commits  |   |   |   |   |
| Dependabot  |   |   |   |   |
| Dependency Graph |   |   |   |   |
| Deploy keys |   |   |   |   |
| Deployments |   |   |   |   |
| Emojis |   |   |   |   |
| Gists |   |   |   |   |
| Git database  |   |   |   |   |
| Gitignore |   |   |   |   |
| Interactions |   |   |   |   |
| Issues |   |   |   |   |
| Licenses |   |   |   |   |
| Markdown |   |   |   |   |
| Meta |   |   |   |   |
| Metrics |   |   |   |   |
| Migration |   |   |   |   |
| Orgs |   |   |   |   |
| Packages |   |   |   |   |
| Pages |   |   |   |   |
| Project(classic) |   |   |   |   |
| Pulls |   |   |   |   |
| Rate limit |   |   |   |   |
| Reactions |   |   |   |   |
| Releases |   |   |   |   |
| Repositories |   |   |   |   |
| Search |   |   |   |   |
| Secret scanning |   |   |   |   |
| Teams |   |   |   |   |
| Users |   |   |   |   |
| Repository webhooks |   |   |   |   |

