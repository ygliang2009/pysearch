#!/usr/bin/python
#encoding=utf-8
#@author:liangyunge@baidu.com
#@version:1.0
#@desc:排名模块
#@date:2012-11-23

from ConfParser import confparser
from Logger import logger

class ranker:
	def __init__(self,resultlist):
		if len(resultlist) == 0:
			return None
		self.originlist = resultlist
		self.weighter = weighter()

	def rank(self):
		resdict = {}
		urliddict = {}
		titledict = {}
		#规则化参数
		for origin in self.originlist:
			for relate in origin:
				if not resdict.has_key(relate['url']):
					resdict[relate['url']] = {}
					urliddict[relate['url']] = relate['urlid']
					titledict[relate['url']] = relate['title']
				if not resdict[relate['url']].has_key(relate['word']):
					resdict[relate['url']][relate['word']] = []
				resdict[relate['url']][relate['word']].append({'location':relate['location'],'type':relate['type']})
		scoredict = self.weighter.weight(resdict)
		#重组返回结果，以链接为单位，加入权重信息
		reslist = self.buildreslist(resdict,scoredict,urliddict,titledict)
		#按照weight降序排列
		reslist = sorted(reslist,key = lambda resnode:resnode['weight'],reverse=True)
		
		return reslist
	
	#整合请求处理结果信息，加入weight和urlid信息
	def buildreslist(self,resdict,scoredict,urliddict,titledict):
		reslist = []
		for res in resdict:
			resnode = {}
			if not urliddict.has_key(res):
				logger.warning({'msg':'no urlid in urllist','urliddict':urliddict,'url':res})
				continue
			resnode['urlid'] = urliddict[res]
			resnode['title'] = titledict[res]
			resnode['url'] = res
			if scoredict.has_key(res):
				resnode['weight'] = scoredict[res]
			else:
				resnode['weight'] = -1
			resnode['wordinfo'] = resdict[res]
			reslist.append(resnode)
		return reslist

class weighter:
	def __init__(self):
		confdict = confparser.confdictory('rank')
		if len(confdict) == 0:
			logger.warning('config file load error')
		self.weightdict = {}
		#根据文件配置生成排名函数			
		if confdict.has_key('frequence'):
			self.weightdict['frequence'] = {}
			self.weightdict['frequence']['caller'] = self.frequence
			self.weightdict['frequence']['weight'] = int(confdict['frequence'])
		if confdict.has_key('position'):
			self.weightdict['position'] = {}
			self.weightdict['position']['caller'] = self.position
			self.weightdict['position']['weight'] = int(confdict['position'])
		if confdict.has_key('distance'):
			self.weightdict['distance'] = {}
			self.weightdict['distance']['caller'] = self.querydistance
			self.weightdict['distance']['weight'] = int(confdict['distance'])
		if confdict.has_key('titleweight'):
			self.weightdict['titleweight'] = {}
			self.weightdict['titleweight']['caller'] = self.titleweight
			self.weightdict['titleweight']['weight'] = int(confdict['distance'])
	
	def addweight(self,resultdict):
		scoredict = self.weight(resultdict)
		for result in resultdict:
			if scoredict.has_key(result):
				resultdict[result]['weight'] = int(scoredict[result])
			else:
				resultdict[result]['weight'] = -1
		return resultdict

	def weight(self,resultdict):
		#保存每个链接的打分结果
		scoredict = dict([(url,0) for url in resultdict])
		for policy in self.weightdict:
			scores = self.weightdict[policy]['caller'](resultdict)
			if not isinstance(self.weightdict[policy]['weight'],int) or \
					not isinstance(scores,dict):
				logger.warning('weight parameter config error or caller function return type false')
				return None
			for score in scores:
				if not scoredict.has_key(score):
					log.warning('scorelist return score error')
					return None
				scoredict[score] += scores[score] * self.weightdict[policy]['weight'] 
		return scoredict
	
	#规格化函数，由于各个计量标准计量方式不统一，所以用这个方法对
	#各个函数进行规格化
	def normalize(self,scoredict):
		maxnum = max(scoredict.values())
		newscore = {}
		if maxnum > 0:
			newscore = dict([(url,scoredict[url]/maxnum) for url in scoredict])
		else:
			logger.warning('how can scoredict has number 0 in it???')
			return scoredict
		return newscore
	
	def titleweight(self,resultdict):
		scoredict = dict([(result,0) for result in resultdict])
		for result in resultdict:
			for word in resultdict[result]:
				for i in range(len(resultdict[result][word])):
					#query word命中title的情况
					if resultdict[result][word][i]['type'] == 1:
						scoredict[result] += 1
						continue
		#该排序算法不进行规格化
		return scoredict

	#单词位置打分，越靠近文档前面的单词得分越高
	#@param resultdict ranker规格后的搜索词典
	def position(self,resultdict):
		scoredict = {}
		for result in resultdict:
			#所有搜索词没有加权，等同对待出现位置，将所有位置相加返回结果列表
			sum_total = 0
			for word in resultdict[result]:
				sum_word = sum([resultdict[result][word][i]['location'] for i in range(len(resultdict[result][word]))])
				sum_total += sum_word
			scoredict[result] = sum_total
		#经过规格化后的参数介于0-1之间
		scoredict = self.normalize(scoredict)
		return scoredict

	#单词匹配频率打分，单词在文档出现的频率越多得分越高
	#@param resultdict ranker规格后的搜索词典
	def frequence(self,resultdict):
		scoredict = {}
		for result in resultdict:
			#所有搜索词没有加权，等同对待文档出现频率，将频率相加的结果返回
			scoredict[result] = sum([len(resultdict[result][word]) \
					for word in resultdict[result]])
		#经过规格化后的参数介于0-1之间
		scoredict = self.normalize(scoredict)
		return scoredict
	
	#搜索的单词彼此距离越近，得分越高
	#@param resultdict ranker规格后的搜索词典
	def querydistance(self,resultdict):
		# to be realized
		return {}

if __name__ == '__main__':
	reslist = [[{'url': 'http://localhost:9080/setest/test.php', 'word': 'link1', 'location': 2L}], [{'url': 'http://localhost:9080/setest/test.php', 'word': 'link2', 'location': 3L}], []]
 	rankobj = ranker(reslist)
	resultlist = rankobj.rank()
	print resultlist
