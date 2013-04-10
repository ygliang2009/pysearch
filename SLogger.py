#!/usr/bin/python
#encoding=utf-8
#@author:liangyunge@baidu.com
#@version:1.0
#@desc:Spider日志模块
#@date:2012-11-23

from ConfParser import confparser
from sys import _getframe
from time import strftime
import os

#支持debug,notice,warning三个日志级别
class slogger:
	def __init__(self):
		pass

	@staticmethod
	def warning(loginfo={}):
		try:
			confdictory = confparser.confdictory('spider')
		except:
			#默认log配置
			confdictory = {'slogpath':'log','slogfile':'spider.log','sloglevel':'debug'}
		logpath = ''
		noticelog = ''
		warninglog = ''
		loginfo = loginfo
		nowstr = strftime('%Y%m%d%H')
		noticefile = ''
		warningpath = ''
		if confdictory.has_key('slogpath'):
			logpath = confdictory['slogpath']
		if confdictory.has_key('slogfile'):
			noticefile = confdictory['slogfile']
			warningpath = noticefile + '.' + str(nowstr) + '.wf'
		warningfile = logpath + '/' + warningpath
		
		try:
			frame = _getframe(1)
		except:
			frame = _getframe()
		curfile = frame.f_code.co_filename
		linenum = frame.f_lineno
		now = strftime('%Y-%m-%d %H:%M:%S')
		logstr = '[level] warning [time] ' + str(now) + ' [fileinfo] '  + os.path.abspath(curfile) + ':' + str(linenum)
		if isinstance(loginfo,str):
			logstr += ' [msg] ' + loginfo
		elif isinstance(loginfo,dict):
			for info in loginfo:
				if isinstance(loginfo[info],str):
					logstr += ' [' + info + '] ' + loginfo[info]
				else:
					try:
						logstr += ' [' + info + '] (' + str(loginfo[info]) + ')'
					except:
						logstr += ' [' + info + '] Error Format' 

		else:
			logstr += ' [msg] (' + str(loginfo) + ')'
		logstr += '\n'
		if warningfile != None:
			new_link = 0
			if not os.path.exists(warningfile) or not os.path.isfile(warningfile):
				new_link = 1
			f_handler = open(warningfile,'a+')
			f_handler.write(logstr)
			f_handler.close()
			warninglink = logpath + '/' + noticefile + '.wf'
			if not os.path.islink(warninglink) or new_link == 1:
				if os.path.islink(warninglink):
					os.unlink(warninglink)
				os.symlink(warningpath,warninglink)


	@staticmethod
	def notice(loginfo={}):
		try:
			confdictory = confparser.confdictory('spider')
		except:
			#默认log配置
			confdictory = {'slogpath':'log','slogfile':'spider.log','sloglevel':'debug'}
		logpath = ''
		noticelog = ''
		loginfo = loginfo
		nowstr = strftime('%Y%m%d%H')
		confpath = ''
		noticepath = ''
		if confdictory.has_key('slogpath'):
			logpath = confdictory['slogpath']
		if confdictory.has_key('slogfile'):
			confpath = confdictory['slogfile']
			noticepath = confpath + '.' + str(nowstr)
		noticefile = logpath + '/' + noticepath
		try:
			frame = _getframe(1)
		except:
			frame = _getframe()
		curfile = frame.f_code.co_filename
		linenum = frame.f_lineno
		now = strftime('%Y-%m-%d %H:%M:%S')
		logstr = '[level] notice [time] ' + str(now) + ' [fileinfo] ' + os.path.abspath(curfile) + ':' + str(linenum)
		if isinstance(loginfo,str):
			logstr += ' [msg] ' + loginfo
		elif isinstance(loginfo,dict):
			for info in loginfo:
				if isinstance(loginfo[info],str):
					logstr += ' [' + info + '] ' + loginfo[info]
				else:
					try:
						logstr += ' [' + info + '] (' + str(loginfo[info]) + ')'
					except:
						logstr += ' [' + info + '] Error Format' 
		else:
			logstr += ' [msg] (' + str(loginfo) + ')'
		logstr += '\n'
		if noticefile != None:
			new_link = 0
			#创建软链接
			if not os.path.exists(noticefile) or not os.path.isfile(noticefile):
				new_link = 1
			f_handler = open(noticefile,'a+')
			f_handler.write(logstr)
			f_handler.close()
			noticelink = logpath + '/' + confpath
			if not os.path.islink(noticelink) or new_link == 1:
				if os.path.islink(noticelink):
					os.unlink(noticelink)
				os.symlink(noticepath,noticelink)

if __name__ == '__main__':
	frame = _getframe()
	curfile = frame.f_code.co_filename
	linenum = frame.f_lineno
	now = strftime('%Y-%m-%d %H:%M:%S')
	slogger.warning({'aa':'bb','aa1':{'ss':'tt'},'aa2':[1,2,3,4]})
