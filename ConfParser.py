#!/bin/python
#encoding=utf-8
#@author:liangyunge@baidu.com
#@version:1.0
#@date:2012-11-22
#@desc:ini格式的config文件解析器

from ConfigParser import ConfigParser

class confparser:
	def __init__(self):
		pass
	
	@staticmethod
	def confdictory(section,confname='conf/search.conf'):
		confparser = ConfigParser()
		confparser.read(confname)
		confitems = confparser.items(section)
		confdict = {}
		for confitem in confitems:
			confdict[confitem[0]] = confitem[1]
		return confdict

if __name__ == '__main__':
	confdict = confparser.confdictory('backinfo')
	print confdict
