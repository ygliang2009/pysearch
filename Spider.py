#!/bin/python
#encoding=utf-8
#@author:liangyunge@baidu.com
#@version:1.0
#@desc:爬虫程序
#@date:2012-11-21

from urllib2 import *
from urlparse import urljoin
from WebNode import webnode
from Parser import parser
from Indexer import indexer
from ConfParser import confparser
from SLogger import slogger

class spider:
	def __init__(self,deep=2,timeout=5,retry=3):
		#保存解析出来的抓取页面url子链接
		self.urlbuffer = []
		#html解析器，解析html的a标签和文本
		self.parser = None
		#索引，建好索引后存入到数据库中
		self.indexer = None
		#爬虫深度
		self.deep = deep
		#爬取超时时间设置
		self.timeout = timeout
		#爬取重试次数
		self.retry = retry
		try:
			confdict = confparser.confdirectory('spider')
			if confdict.has_key('deep'):
				self.deep = int(confdict['deep'])
				self.timeout = int(confdict['timeout'])
				self.retry = int(confdict['retry'])
			else:
				pass
		except:
			slogger.warning('config load error for spider deep parameter')

	def setparser(self,parser):
		self.parser = parser
	
	def setindexer(self,indexer):
		self.indexer = indexer
	
	def getparser(self):
		return self.parser
	
	def getindexer(self):
		return self.indexer
	
	def addurl(self,url):
		self.urlbuffer.append(url)
	
	def addurllist(self,urllist):
		self.urlbuffer.extend(urllist)
	
	def run(self):
		if len(self.urlbuffer) == 0:
			return
		depth = 0
		for url in self.urlbuffer:
			#爬取URL
			failed = 0
			doneflag = 0
			while not doneflag == 1:
				try:
					if failed > self.retry:
						break
					#仿造Mozilla User Agent
					user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:13.0) Gecko/20100101 Firefox/13.0.1"
					headers = {'User-Agent':user_agent}
					reqobj = Request(url=url,headers=headers)
					urlobj = urlopen(reqobj,timeout = self.timeout)
					content = urlobj.read()
					if len(content) == 0:
						failed += 1
						continue
					doneflag = 1
				#抛出HTMLError或URLError
				except :
					failed += 1
			if failed > self.retry:
				continue
			#slogger.notice({'msg':'url get success','url':url})
			##############?????????????可改进为多线程?????????????###################
			#爬完的网页需要解析后才能放入到数据库中
			parseobj = parser()
			self.setparser(parseobj)
			#解析抓取到的文本
			if self.parser.parsetext(content) == False:
				continue
			parse_content = ""
			for word in self.parser.wordlist:
				#保存的文本去掉换行符号
				word = word.replace('\r\n',' ').replace('\n',' ').replace('\r',' ')
				parse_content += word + ' '
			try:
				self.parser.close()
			except:
				continue
			webnodeobj = None
			#整合获取到的url信息
			newlinklist = []
			for link in self.parser.linklist:
				newlinklist.append(urljoin(url,link))
			#建立实体bean交互给indexer
			if len(self.parser.wordlist) > 0:
				webnodeobj = webnode(url,self.parser.title,content,parse_content,newlinklist,self.parser.wordlist)
			#加入到爬虫队列中
			if self.deep >= depth:
					depth += 1
			for link in newlinklist:
				if self.deep >= depth:
					self.urlbuffer.append(link)
			#解析词表，对词表建立索引
			if self.indexer != None and webnodeobj != None:
				self.indexer.index(webnodeobj)
			#if self.indexer != None and len(wordlist) != 0:
			#	#把parser解析的程序添加索引入库
			#	self.indexer.addindex(wordlist)
			#print cont

if __name__ == '__main__':
	print 'xxxx'
