#!/usr/bin/python
#encoding=utf-8
#@author:liangyunge@baidu.com
#@version:1.0
#@desc:日志模块
#@date:2012-11-23

from ConfParser import confparser
from sys import _getframe
from time import strftime
import os

#支持debug,notice,warning三个日志级别
class logger:
	def __init__(self):
		pass

	@staticmethod
	def warning(loginfo={}):
		try:
			confdictory = confparser.confdictory('log')
		except:
			#默认log配置
			confdictory = {'logpath':'log','logfile':'se.log','loglevel':'debug'}
		logpath = ''
		noticelog = ''
		warninglog = ''
		loginfo = loginfo
		nowstr = strftime('%Y%m%d%H')
		noticefile = ''
		warningpath = ''
		if confdictory.has_key('logpath'):
			logpath = confdictory['logpath']
		if confdictory.has_key('logfile'):
			noticefile = confdictory['logfile']
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
			confdictory = confparser.confdictory('log')
		except:
			#默认log配置
			confdictory = {'logpath':'log','logfile':'se.log','loglevel':'debug'}
		logpath = ''
		noticelog = ''
		loginfo = loginfo
		nowstr = strftime('%Y%m%d%H')
		confpath = ''
		noticepath = ''
		if confdictory.has_key('logpath'):
			logpath = confdictory['logpath']
		if confdictory.has_key('logfile'):
			confpath = confdictory['logfile']
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

	@staticmethod
	def debug(loginfo={}):
		try:
			confdictory = confparser.confdictory('log')
		except:
			#默认log配置
			confdictory = {'logpath':'log/','logfile':'se.log','loglevel':'debug'}
		logpath = ''
		debuglog = ''
		loginfo = loginfo
		nowstr = strftime('%Y%m%d%H')
		if confdictory.has_key('logpath'):
			logpath = confdictory['logpath']
		if confdictory.has_key('logfile'):
			confpath = confdictory['logfile']
			debugpath = confpath + '.' + str(nowstr) + '.dbg'
		debugfile = logpath + '/' + debugpath
		try:
			frame = _getframe(1)
		except:
			frame = _getframe()
		curfile = frame.f_code.co_filename
		linenum = frame.f_lineno
		now = strftime('%Y-%m-%d %H:%M:%S')
		logstr = '[level] debug [time] ' + str(now) + ' [fileinfo] ' + os.path.abspath(curfile) + ':' + str(linenum)
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
		if debugfile != None:
			f_handler = open(debugfile,'a+')
			f_handler.write(logstr)
			f_handler.close()

if __name__ == '__main__':
	frame = _getframe()
	curfile = frame.f_code.co_filename
	linenum = frame.f_lineno
	now = strftime('%Y-%m-%d %H:%M:%S')
	logger.warning({'aa':'bb','aa1':{'ss':'tt'},'aa2':[1,2,3,4]})
