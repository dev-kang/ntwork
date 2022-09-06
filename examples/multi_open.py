# -*- coding: utf-8 -*-
import sys
import ntwork

# 多开3个企业微信
for i in range(3):
    wework = ntwork.WeWork()
    wework.open(smart=False)

