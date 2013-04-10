#!/bin/python
#encoding=utf-8
#@author:liangyunge@baidu.com
#@version:1.0
#@desc:交互对象

class webnode:
	def __init__(self,url,title,content = '',parse_content = '',linklist=[],wordlist=[]):
		self.url = url
		self.title = title
		self.content = content
		self.parse_content = parse_content
		self.linklist = linklist
		self.wordlist = wordlist
