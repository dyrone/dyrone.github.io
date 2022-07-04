---
title: "Git Test 1"
date: 2022-06-25T16:45:34+08:00
draft: true
---

# 如何正确unset环境变量

sane_unset () {
	unset "$@"
	return 0
}