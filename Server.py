#!/usr/bin/python
#encoding=utf-8
#@author:liangyunge@baidu.com
#@version:1.0
#@desc:页面整合渲染模块
#@date:2012-11-25

from ConfParser import confparser
import socket,select,json
from Builder import builder
from Logger import logger
import os

class server:
	def __init__(self):
		#加载服务器信息
		os.chdir(os.getcwd())
		servermap = confparser.confdictory('server')
		if servermap == None or len(servermap) == 0:
			logger.warning("config file load error")
			return None
		if servermap.has_key('address'):
			self.addr = servermap['address']
		else:
			self.addr = 'localhost'
		if servermap.has_key('port'):
			self.port = int(servermap['port'])
		else:
			self.port = 9898
		if servermap.has_key('listennum'):
			self.listennum = int(servermap['listennum'])
		else:
			self.listennum = 10
		if servermap.has_key('timeout'):
			self.timeout = int(servermap['timeout'])
		else:
			self.timeout = 2
		if servermap.has_key('pidpath'):
			self.pidpath = servermap['pidpath']
		else:
			self.pidpath = "tmp"
		if servermap.has_key('pidfile'):
			self.pidfile = servermap['pidfile']
		else:
			self.pidfile = "server.pid"
		if servermap.has_key('recvlen'):
			self.recvlen = int(servermap['recvlen'])
		else:
			self.recvlen = 1024
		if servermap.has_key('recvbuf'):
			self.recvbuf = int(servermap['recvbuf'])
		else:
			self.recvbuf = 4096
		if servermap.has_key('sendbuf'):
			self.sendbuf = int(servermap['sendbuf'])
		else:
			self.sendbuf = 8192

		self.__setpid()
	
	def __setpid(self):
		if not os.path.isdir(self.pidpath):
			os.mkdir(self.pidpath)
		handler = open(self.pidpath + '/' + self.pidfile,'w')
		pid = str(os.getpid())
		handler.write(pid)
		handler.close()
	def start(self):
		#传输格式为JSON格式
		serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		#地址重用机制，必须放在bind之前
		serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)	
		serversocket.bind((self.addr,self.port))
		
		serversocket.listen(self.listennum)
		#非阻塞模式
		serversocket.setblocking(0)
		#No Delay模式
		serversocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		#发送接收缓冲区设置
		serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.recvbuf)
		serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.sendbuf)
		
		epoll = select.epoll()
		epoll.register(serversocket.fileno(), select.EPOLLIN)
		try:
			connections = {}; requests = {}; responses = {}
			while True:
				#超时时间
				events = epoll.poll(self.timeout)
				for fileno, event in events:
					if fileno == serversocket.fileno():
						connection, address = serversocket.accept()
						connection.setblocking(0)
						epoll.register(connection.fileno(), select.EPOLLIN)
						connections[connection.fileno()] = connection
						requests[connection.fileno()] = b''
						responses[connection.fileno()] = ''
					#监听接口可读
					elif event & select.EPOLLIN:
						requests[fileno] += connections[fileno].recv(self.recvlen)
						logger.notice({'msg':'server accept success','request':requests[fileno]})
						buildobj = builder(requests[fileno])
						epoll.modify(fileno, select.EPOLLOUT)
						response_data = buildobj.build()
						#错误处理，并不退出，需要给Server提示
						if  response_data == None:
							Logger.warning('builder return failed')
							response_data = json.dumps({'status':'2','desc':'server work error'})
						responses[fileno] = response_data
					elif event & select.EPOLLOUT:
						byteswritten = connections[fileno].send(responses[fileno])
						logger.notice({'msg':'server response ok','query':requests[fileno],'writelen':byteswritten,'result':responses[fileno][0:byteswritten]})
						responses[fileno] = responses[fileno][byteswritten:]
						if len(responses[fileno]) == 0:
							epoll.modify(fileno, 0)
							try:
								connections[fileno].shutdown(socket.SHUT_RDWR)
							except:
								pass
					
					elif event & select.EPOLLHUP:
						epoll.unregister(fileno)
						connections[fileno].close()
						del connections[fileno]
		finally:
			epoll.unregister(serversocket.fileno())
			epoll.close()
			serversocket.close()

if __name__ == '__main__':
	server = server()
	server.start()
