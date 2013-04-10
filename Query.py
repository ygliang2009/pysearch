#!/usr/bin/python
#encoding=utf-8
#@author:liangyunge@baidu.com
#@version:1.0
#@desc:query请求模块
#@date:2012-11-23

from Logger import logger
from DbControl import dbcontrol
from ConfParser import confparser
from Ranker import ranker

class query:
	def __init__(self,query_words):
		if isinstance(query_words,str):
			self.wordlist = query_words.split(' ')
			#reslist 存放wordlist的对应结果
			self.reslist = []
			confdictory = confparser.confdictory('database')
			if not confdictory.has_key('user'):# or !confdictory.has_key['dbpass']:
				logger.warning('config parser can not be loaded')
				return None
			self.engine = dbcontrol(confdictory['user'],confdictory['password'])
			if self.engine == None:
				logger.warning({'msg':'database connect error','dbname':confdictory['dbuser'],'dbpass':confdictory['dbpass']})
				return None
		else:
			logger.warning('query words format error')

	def __search(self):
		resultlist = []
		if len(self.wordlist) == 0:
			return None
		for word in self.wordlist:
			result = self.engine.queryword(word)
			#如果当前这个检索词没有匹配结果，则继续查找下一个单词
			if result == None:
				continue
			resultlist.append(result)
		if len(resultlist) == 0:
			return None
		return resultlist

	def __sort(self,reslist):
		if len(reslist) == 0:
			logger.warning('result list is empty')
			return None
		#对结果进行分析后，排序
		rankobj = ranker(reslist)
		#返回以URL为key的链接列表，以weight降序排序
		resultlist = rankobj.rank()
		return resultlist

	def run(self):
		#从请求查询词中检索结果，结果保存到reslist中
		resultlist = self.__search()
		if resultlist == None:
			self.reslist = None
		else:
		#结果排序，排序后的结果保存到reslist中
			self.reslist = self.__sort(resultlist)
		logger.notice(self.reslist)
	
	def getreslist(self):
		if self.reslist == None or len(self.reslist) > 0:
			return self.reslist
		else:
			return None

if __name__ == '__main__':
	query_obj = query('link1')
	query_obj.run()
	#print query_obj.getreslist()
