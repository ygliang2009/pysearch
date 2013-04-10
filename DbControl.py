#!/bin/python
#encoding=utf-8
#@author:liangyunge@baidu.com
#@version:1.0
#@date:2012-11-21
#@desc:数据库操作程序


import MySQLdb
from Logger import logger

class dbcontrol:
	def __init__(self,user,pswd,addr='localhost',dbname='search'):
		self.conn = MySQLdb.connect(host=addr,user=user,passwd=pswd,db=dbname)
		if self.conn == None:
			logger.warning({'msg':'database connect error','host':addr,'user':user,'passwd':pswd,'dbname':dbname})
			return None	
	def select(self,tbname,query_str):
		cursor = self.conn.cursor()
		try:
			if query_str == '*':
				cursor.execute('select * from ' + tbname)
			else:
				cursor.execute('select * from ' + tbname + ' where ' + query_str)
			data = cursor.fetchall()
			cursor.close()
		except:
			cursor.close()
			return None
		return data

	def inserturl(self,url,title):
		#url表的最大长度为255
		if len(url) > 255:
			return False
		cursor = self.conn.cursor()
		insertstr = '(\'' + url + '\',\'' + title +'\')'
		insertstr = 'insert into urllist(url,title) values ' + insertstr
		try:
			cursor.execute(insertstr)
			cursor.close()
		except:
			cursor.close()
			return False
		return True
	
	def insertword(self,value,keytype=0):
		#word表的长度为20
		if len(value) > 20:
			return False
		cursor = self.conn.cursor()
		insertstr = '(\'' + value + '\',' + str(keytype) + ')'
		insertstr = 'insert into wordlist(word,type) values ' + insertstr
		try:
			cursor.execute(insertstr)
			cursor.close()
		except:
			cursor.close()
			return False
		return True
	
	def insertlink(self,worddict):
		if worddict['fromid'] == None or worddict['toid'] == None:
			#to be added log module
			pass
		else:
			cursor = self.conn.cursor()
			insertstr = 'insert into link(fromid,toid) values ('
			insertstr += str(worddict['fromid']) + ','
			insertstr += str(worddict['toid']) + ')'
			try:
				cursor.execute(insertstr)
				cursor.close()
			except:
				cursor.close()
				return False
			return True

	def insertlinkwords(self,relatedict):
		if relatedict['linkid'] == None or relatedict['wordid'] == None:
			#to be added log module
			return False
		else:
			cursor = self.conn.cursor()
			insertstr = 'insert into linkwords(wordid,linkid) values ('
			insertstr += str(relatedict['wordid']) + ','
			insertstr += str(relatedict['linkid']) + ')'
			try:
				cursor.execute(insertstr)
				cursor.close()
			except:
				cursor.close()
				return False
			return True

	#wordlocation表结构:
	#column id int   column urlid int  column wordid int  column location int
	def insertlocation(self,worddict):
		if worddict['urlid'] == None or worddict['wordid'] == None or \
				worddict['location'] == None:
			#to be added log module
			return False
		else:
			cursor = self.conn.cursor()
			insertstr = 'insert into wordlocation(urlid,wordid,location) values ('
			insertstr += str(worddict['urlid']) + ','
			insertstr += str(worddict['wordid']) + ','
			insertstr += str(worddict['location']) + ')'
			try:	
				cursor.execute(insertstr)
				cursor.close()
			except:
				cursor.close()
				return False
			return True

	#insert 根据单词名称url名称插入两者的映射关系到location表中
	#to be added 去重函数
	def insertrelation(self,worddict,wdtype = 0):
		if worddict['url'] == None or worddict['word'] == None or \
				worddict['location'] == None:
			#to be added log module
			return False
		else:
			cursor = self.conn.cursor()
			insertstr = 'insert into wordlocation(urlid,wordid,location) values ('
			urlid = '(select id from urllist where url = \'' + worddict['url']  + '\' limit 1)'
			wordid = '(select id from wordlist where type = ' + str(wdtype) + ' and word = \'' + worddict['word']  + '\' limit 1)'
			insertstr += urlid + ','
			insertstr += wordid + ','
			insertstr += str(worddict['location']) + ')'
			try:
				cursor.execute(insertstr)
				cursor.close()
			except:
				cursor.close()
				return False
			return True

	def unique_urlinsert(self,url,title):
		if len(self.select('urllist','url = \'' + url + '\'')) == 0:
			return self.inserturl(url,title)
		else:
			return False

	def unique_titleinsert(self,value):
		if len(value) > 50:
			value = value[0:50]
		#相应的标题和文字都不存在
		if len(self.select('wordlist','word = \'' + value + '\' and type = 1')) == 0:
			return self.insertword(value,1)
		else:
			#即使单词存在，也应该继续插入单词和新增URL的链接关系
			return True

	def unique_wordinsert(self,value):
		if len(value) > 50:
			value = value[0:50]
		if len(self.select('wordlist','word = \'' + value + '\' and type = 0')) == 0:
			return self.insertword(value,0)
		else:
			return True

	def unique_locationinsert(self,valuedict):
		if len(self.select('wordlocation','urlid = ' + str(valuedict['urlid']) + \
			' and wordid = ' + str(valuedict['wordid']) + ' and location = ' + \
				str(valuedict['location'])))  == 0:
			return self.insertlocation(valuedict)
		else:
			return True

	def unique_linkinsert(self,linkdict):
		if len(self.select('link','fromid = ' + str(linkdict['fromid']) + \
			' and toid = ' + str(linkdict['toid']))) == 0:
			return self.insertlink(linkdict)
		else:
			return False

	def unique_linkwordsinsert(self,linkwords_dict):
		if len(self.select('linkwords','wordid = ' + str(linkwords_dict['wordid']) + \
			' and linkid = ' + str(linkwords_dict['linkid']))) == 0:
			return self.insertlinkwords(linkwords_dict)
		else:
			return False
	
	def queryword(self,word):
		if word == None:
			return
		cursor = self.conn.cursor()
		#由于备份数据是以urlid为名称存储的，所以这里需要将urlid取出
		querystr = 'select urllist.id as urlid,urllist.title as title,wordlist.word as word,wordlist.type as wdtype,wordlocation.location as location,urllist.url as url from wordlist,wordlocation,urllist where wordlist.word = \'' + word + '\' and wordlocation.wordid = wordlist.id and wordlocation.urlid = urllist.id'
		cursor.execute(querystr)
		data = cursor.fetchall()
		datalist = []
		for one in data:
			datadict = {'urlid':one[0],'title':one[1],'word':one[2],'type':one[3],'location':one[4],'url':one[5]}
			datalist.append(datadict)
		cursor.close()
		logger.notice({'msg':'database query info','queryword':word,'queryresult':datalist})
		if len(datalist) == 0:
			return None
		return datalist
	
	def close(self):
		self.conn.close()


if __name__ == '__main__':
	dbobj = dbcontrol('root','public')
	data = dbobj.select('linkwords','*')
	#dictory = {'word':'testword','url':'testurl','location':3}
	#dbobj.insertrelation(dictory)
	res = dbobj.queryword('link2')
	#print data
	print res
