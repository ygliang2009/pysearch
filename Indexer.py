#!/bin/python
#encoding=utf-8
#@author:liangyunge@baidu.com
#@date:2012-11-21
#@version:1.0
#@desc:索引制造器

from WebNode import webnode
from DbControl import dbcontrol
from ConfParser import confparser
from BackControl import backcontrol
from Logger import logger

class indexer:
	def __init__(self):
		self.fromurl = ''
		self.linklist = []
		self.parse_content = ''
		self.content = ''
		self.wordlist = []
		confdictory = confparser.confdictory('database')
		if len(confdictory) == 0:
			logger.warning('config file load error')
			return
		self.dbcontrol = dbcontrol(confdictory['user'], \
					confdictory['password'])
	
	def index(self,webnode):
		self.fromurl = webnode.url
		self.title = webnode.title
		self.titlelist = self.wordfilter(self.title.lower().strip().split(' '))
		self.linklist = webnode.linklist
		self.parse_content = webnode.parse_content
		self.content = webnode.content
		self.wordlist = self.wordfilter(webnode.wordlist)
		
		#持久化工作
		self.persistent()	
	
	#持久化页面信息，包括单词信息，网页信息，网页单词关系，网页和其链接关系等
	def persistent(self):
		if self.dbcontrol == None:
			#to be add log module
			print 'db init error'
			return
		#把当前页的url持久化
		urlres = self.dbcontrol.unique_urlinsert(self.fromurl,self.title)
		
		if urlres == False:
			return False
		
		for location in range(len(self.titlelist)):
			res =  self.dbcontrol.unique_titleinsert(self.titlelist[location])
			res2 = False
			if res == True:
				res2 = self.dbcontrol.insertrelation({'url':self.fromurl,'word':self.titlelist[location],'location':location},1)
			else:
				continue

		for location in range(len(self.wordlist)):
			try:
				#持久化word
				res = self.dbcontrol.unique_wordinsert(self.wordlist[location])
				if res == True:
					#持久化(word,url)关系
					self.dbcontrol.insertrelation({'url':self.fromurl,\
						'word':self.wordlist[location],'location':location},0)
				else:
					continue
			except:
				continue
		#持久化链接关系，以便pagerank方法排序
		#for link in self.linklist:

		#持久化url和word关系图
	#将wordlist中的单词进行整合，记录所在文档位置
		
		#备份抓取过来的文件内容
		urlidxlist = self.dbcontrol.select('urllist','url=\'' + self.fromurl + '\' limit 1')
		urlidx = None
		if len(urlidxlist) > 0 and len(urlidxlist[0]) > 0:
			urlidx = urlidxlist[0][0]
		backobj = backcontrol()
		backobj.backhtml(urlidx,self.content)
		backobj.backtext(urlidx,self.parse_content)

	#过滤格式非法的单词
	def wordfilter(self,wordlist):
		retlist = []
		for word in wordlist:
			word = word.replace('\r\n',' ').replace('\r',' ').replace('\n',' ')\
				.replace(',',' ').replace('.',' ').replace('?',' ').replace('!',' ')\
				  .replace('\"',' ').replace('\'',' ').replace('\t',' ').lower()
			listtmp = word.split(' ')
			for tmp in listtmp:
				#把过短的单词删去
				if len(tmp) > 1 and not self.invalid(tmp):
					retlist.append(tmp)
				
		return retlist

	def invalid(self,word):
		valid_array = ['&amp;','()','[]','{}','();','[];']
		return word in valid_array

	def closedb(self):
		self.dbcontrol.close()

if __name__ == '__main__':
	wordlist = ["I am a good guy,can you believe?all though I look like a bad apple,but i'm kindness deep in my heart.So please give me a chance to certificate myself. I will be appreciated for your trust."]
	indexobj = indexer()
	retlist = indexobj.wordfilter(wordlist)
	print retlist
