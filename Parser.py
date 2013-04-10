#!/bin/python
#encoding=utf-8
#@author:liangyunge@baidu.com
#@version:1.0
#@desc:解析程序
#@date:2012-11-21

import HTMLParser,re
from Logger import logger

class parser(HTMLParser.HTMLParser):
	def __init__(self):
		self.wordlist = []
		self.linklist = []
		HTMLParser.HTMLParser.__init__(self)
	
	def handle_data(self,content):
		self.wordlist.append(content)
	
	def handle_starttag(self,tag,attr_list):
		if tag == "a":
			self.parsea(attr_list)

	#解析文档，把a标签和数据内容分别存入到linklist和wordlist中
	def handle_startendtag(self,tag,attrlist):
		pass
	
	def parsehead(self,header):
		#解析出文档的标题，没有标题的文档标记为undefined_title
		p = re.compile(r"<title>(?P<title>.+)</title>",re.I)
		m = p.search(header)
		if m == None or len(m.group('title')) == 0:
			#logger.warning({'msg':'parser get error format for the title','headinfo':header})
			#self.title = 'undefined_title'
			return False
		else:
			self.title = m.group('title')
			return True

	def parsetext(self,html):
		#把head单独提取出来，解析title信息
		content = ''
		if html.find('<head>') >= 0:
			html_split = html.split('<head>')
			spot_html = html_split[1]
			if spot_html.find('</head>') >= 0:
				head_body = spot_html.split('</head>')
				if len(head_body) != 2:
					logger.warning({'msg':'parse html file error','html':html})
					return False
				header = head_body[0]
				if len(header) > 0:
					if self.parsehead(header) == False:
						return False
				else:
					logger.warning({'msg':'parse html file error','html':html})
					return False
				content = head_body[1]
			else:
				logger.warning({'msg':'parse html file error','html':html})
				#没有header的时候，title标记为undefined
				return False
				#self.title = 'undefined_title'

		if len(content) > 0:
			self.feed(content)
		else:
			#logger.warning({'msg':'parse html file error','html':html})
			return False
		#logger.notice({'msg':'parser work done','wordlist':self.wordlist,'linklist':self.linklist})
		return True
	#解析a标签
	def parsea(self,attr_list):
		for attr in attr_list:
			#将链接存入到linklist中
			if attr[0] == "href":
				self.linklist.append(attr[1])	

if __name__ == "__main__":
	ps = parser()
	ps.parsetext("<html><head><title>Just A Test</title></head><body><div style='color:red' font='xxx'>我乐歌曲</div><a href='http://www.baidu.com'>同学们</a><input type='text' name='test'/></body></html>")
	ps.close()
	print ps.linklist
	print ps.title
