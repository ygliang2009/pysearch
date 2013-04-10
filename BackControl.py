#!/bin/python
#encoding=utf-8
#@author:liangyunge@baidu.com
#@version:1.0
#@desc: 本地文件管理

import os
from Logger import logger
from ConfParser import confparser
import zipfile

class backcontrol:
	def __init__(self):
		try:
			cparser = confparser.confdictory('backinfo')
		except:
			cparser = {"backpath":"/home/chemical/workspace/python/se/backup"}
		if cparser.has_key('backpath'):
				self.backpath = cparser['backpath']
		else:
			return
	
	def backhtml(self,idx,filecontent):
		fulfilepath = self.backpath + '/' + str(idx) + '.htm'
		relatepath = str(idx) + '.htm'
		self.__writefile(fulfilepath,filecontent)
		#self.__writefile(str(idx),filecontent)
		os.chdir(self.backpath)
		self.__backzip(relatepath)
		os.remove(fulfilepath)

	def backtext(self,idx,filecontent):
		fulpath = self.backpath + '/' + str(idx) + '.file'
		relatepath = str(idx) + '.file'
		#self.__writefile(fulpath,filecontent)
		self.__writefile(fulpath,filecontent)
		os.chdir(self.backpath)
		self.__backzip(relatepath)
		os.remove(fulpath)
	
	#压缩成zip格式包
	def __backzip(self,filename):
		fulzippath = filename + '.zip'
		zfile = zipfile.ZipFile(fulzippath,'w',zipfile.ZIP_DEFLATED)
		zfile.write(filename)
		zfile.close()

	def __writefile(self,filename,filecontent):
		if os.path.exists(filename):
			logger.warning(filename + 'already exists')
			return
		f_handler = file(filename,'w+')
		f_handler.write(filecontent)
		f_handler.close()

if __name__ == '__main__':
	backobj = backcontrol()
	backobj.backtext(2,'ssss')
