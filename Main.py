#!/bin/python
#encoding=utf-8
#@author:liangyunge@baidu.com
#@version:1.0
#@desc:搜索引擎主程序
#@date:2012-11-21

from Spider import spider
from Parser import parser
from Indexer import indexer

class explorer:
	def __init__(self,urllist = []):
		self.spider = spider()
		self.indexer = indexer()
		self.parser = parser()
		self.urllist = urllist
	
	def start(self):
		if len(self.urllist) == 0:
			return False
		self.spider.addurllist(self.urllist)
		self.spider.setparser(self.parser)
		self.spider.setindexer(self.indexer)
		spider.run()
		return True

	def cleanup(self):
		self.indexer.closedb()
	

if __name__ == "__main__":

	spider = spider()
	#spider.addurl('http://localhost:9080/setest/test.php')
	spider.addurl('http://hq.booksarefun.com/')
	parserobj = parser()
	indexobj = indexer()
	spider.setparser(parserobj)
	spider.setindexer(indexobj)
	spider.run()
	indexobj.closedb()
	print 'done!'
