#!/usr/bin/env python
#coding=utf-8
'''
author:Crisschan
time:2016-7-18

list:
2016-7-18 add this FRScript for FriedRing Script api from requests. And I add some new api for performance test.
'''
import requests
from requests.models import Response
class FRScript(requests):
    def Cor(self,response):
        '''
        correlation the key word from respost (include test and header)
        :return Correlation result:
        '''
        resText = response.text
        resHeader = response.headers



