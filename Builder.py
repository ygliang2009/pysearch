#!/usr/bin/python
#encoding=utf-8
#@author:liangyunge@baidu.com
#@version:1.0
#@desc:页面整合渲染模块
#@date:2012-11-25

from ConfParser import confparser
from Query import query
from Logger import logger
import zipfile
import os,re
import json

class builder:
	def __init__(self,querywords):
		if len(querywords.strip()) == 0 or not isinstance(querywords,str):
			logger.warning('querywords invalid!')
			return
		self.querywords = querywords.strip().split(' ')
		self.query = query(querywords)
		self.resultlist = []
		confmap = confparser.confdictory('backinfo')
		buildmap = confparser.confdictory('build')
		if confmap == None  or buildmap == None:
			log.warning('config error for backinfo section')
			return None
		if not confmap.has_key('backpath'):
			self.backpath = 'backup'
		else:
			self.backpath = confmap['backpath']
		
		if not confmap.has_key('rawtext'):
			self.rawtext = '.file'
		else:
			self.rawtext = confmap['rawtext']
		if not confmap.has_key('rawhtml'):
			self.rawhtml = '.html'
		else:
			self.rawhtml = confmap['backtext']
		
		if not confmap.has_key('backtext'):
			self.backtext = '.file.zip'
		else:
			self.backtext = confmap['backtext']
		if not confmap.has_key('backhtml'):
			self.backhtml = '.htm.zip'
		else:
			self.backhtml = confmap['backhtml']
		if not buildmap.has_key('block'):
			self.block = 128
		else:
			self.block = int(buildmap['block'])
	
	#构建整合渲染信息
	def build(self):
		if self.query == None:
			logger.warning('query instance invalid')
			return None
		self.query.run()
		self.resultlist = self.query.getreslist()
		if self.resultlist == None:
			logger.warning('query module return null!')
			return json.dumps({'status':'1','desc':'no matche result'})
		results_list = []
		for result in self.resultlist:
			if result == None or not result.has_key('urlid'):
				logger.warning({'msg':'lack of parameter urlid in this query','query':result})
				continue
			backfile = self.backpath + '/' + str(result['urlid']) + self.backtext 
			zipf = zipfile.ZipFile(backfile)
			olddir = os.getcwd()
			os.chdir(self.backpath)
			zipf.extractall()
			zipf.close()
			rawtext_handler = open(str(result['urlid']) + self.rawtext,'r')
			string = rawtext_handler.read()
			renderstr = self.rendertext(string,self.querywords)
			rawtext_handler.close()
			os.remove(str(result['urlid']) + self.rawtext)
			os.chdir(olddir)
			urlinfo = result['url']
			titleinfo = result['title']
			titlestr = titleinfo
			if titleinfo != 'undefined':
				titlestr = self.rendertitle(titleinfo,self.querywords)
			results_list.append({'url':urlinfo,'title':titlestr,'content':renderstr})
		return json.dumps({'status':'0','msg':'response ok','response':results_list})
	
	#标题关键词飘红
	def rendertitle(self,string,querywords):
		for word in querywords:
			keywords = ["color",'style','span']
			#keywords中的关键词不进行飘红，否则重复飘红
			flag = 1
			for keyword in keywords:
				if keyword.find(word) >= 0:
					flag = 0
					continue
			if flag == 1:
				comp = re.compile(r'(?P<word>' + word + ')',re.I)
				res = comp.search(string)
				if res == None:
					continue
				match = res.group('word')
				
				#查找第一个匹配的单词位置
				#string = re.sub(comp,'<span style="color:red">' + word + '</span>',string)
				string = string.replace(match,'<span style="color:red">' + match + '</span>')
		return string

	#内容页关键词飘红，内容切分，保证飘红单词在块中
	def rendertext(self,string,querywords):
		string = string.replace('\r\n',' ').replace('\r',' ').replace('\n',' ').\
				replace('\t',' ')
		string_array = string.split(' ') 
		new_string_array = []
		first_location = -1
		cur_pos = 0
		for string_node in string_array:
			if len(string_node) == 0 or string_node == '' or \
					string_node == ' ':
				continue
			cur_pos += 1
			for queryword in querywords:
				if string_node.lower() == queryword:
					string_node = '<span style="color:red">' \
							+ string_node + '</span>'
					if first_location == -1:
						first_location = cur_pos
			new_string_array.append(string_node)
		#有可能是文章标题匹配，而正文没有匹配结果 
		if first_location == -1:
			res_block = 0
		elif len(new_string_array)<self.block:
			res_block = 0
		else:
			res_block = int(first_location/self.block)
		if len(new_string_array) > self.block:
			sub_array = new_string_array[(res_block*self.block):(res_block + 1)*self.block]
			sub_array.append('......')
		else:
			sub_array = new_string_array
		ret_str = ""
		for sub_node in sub_array:	
			ret_str += sub_node + ' '
		return ret_str

	#@deprecated
	#内容页关键词飘红，内容切分，保证飘红单词在块中
	def rendertxt(self,string,querywords):
		location = -1
		for word in querywords:
			keywords = ["color",'style','span']
			#keywords中的关键词不进行飘红，否则重复飘红
			flag = 1
			for keyword in keywords:
				if keyword.find(word) >= 0:
					flag = 0
					continue
			if flag == 1:
				#查找第一个匹配的单词位置
				if location < 0:
					location = string.strip().find(word)
				comp = re.compile(r'(?P<word>' + word + ')',re.I)
				res = comp.findall(string)
				if res == None:
					continue
				for i in range(len(res)):
					string = string.replace(res[i],'<span style="color:red">' + res[i] + '</span>')
		
		stripstr = string.strip()
		pos = location / self.block
		if len(stripstr) > 0:
			if self.block < len(stripstr):
				#title中存在关键词，内容中不存在
				if pos == -1:
					return stripstr[0:self.block] + '......'
				#内容中存在关键词
				else:
					return stripstr[(int(pos) * self.block):((int(pos) + 1) * self.block)] + '......'
			else:
				return stripstr
		else:
			return None

if __name__ == '__main__':
	buildobj = builder('link1')
	results = buildobj.build()
	print results
