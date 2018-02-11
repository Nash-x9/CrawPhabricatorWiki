# -*- coding: utf-8 -*-

import requests
import bs4  
import sys 
import time
import re
reload(sys) 
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup  

class RequestLimeWiki():
	
	def __init__(self,host):
		self.name = host
		self.host = host
		
		self.url_array = {
		'loginPage': self.host+'/auth/loggedout/',
		'loginPost': self.host+'/auth/login/password:self/',
		'crawPage':  self.host+'/w/'
		}

	
		self.postHeaders = {
			'Upgrade-Insecure-Requests': '1',
			'Origin': 'null',
			'Content-Type': 'application/x-www-form-urlencoded',
			'User-Agent': 'User-Agent:Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9'
		}
	
		self.userdata = {
			'__form__': '1',
			'__dialog__': '1'
		}

	def login(self,username,password):
		prev = self.getPrev()
		self.userdata['username'] = username
		self.userdata['password'] = password
		self.userdata['__csrf__'] = prev['_csrf']
		
		R = requests.post(
			self.url_array['loginPost'],
			headers=self.postHeaders,
			params = self.userdata,
			cookies= dict(prev['cookie']),
			allow_redirects=False
		)
		validate = self.getPage(dict(R.cookies),self.url_array['crawPage'])
		if('Recent Activity' in validate.text):
			print '================================'
			print 'Login Success'
			print '================================'
			print 
			return {'cookie': R.cookies}
		#done 2018年2月6日 16:27:40 函数功能已完成。
		
		
	def getPrev(self):
		try:
			r = requests.get(self.url_array['loginPage'],timeout=3)
		except requests.exceptions.ConnectTimeout:
			print('Connect TimeOut!')
			sys.exit();
		r.encoding = 'UTF-8'
		soup = BeautifulSoup(r.text,'lxml')
		#print(soup.prettify())
		#print(soup.find('input'))
		_csrf = soup.select('input[name="__csrf__"]')[0]['value']
		return {
			'cookie': r.cookies,
			'_csrf': _csrf
		}
		#done 2018年2月6日 16:27:38 函数功能已完成。
		
		
	def getPage(self,cookie,url):
		r = requests.get(
			url,
			cookies = cookie,
			headers=self.postHeaders
		)
		r.encoding = 'UTF-8'
		return r
		
	def parseHtml(self,html):
		soup = BeautifulSoup(html,'lxml')
		if 'Document Hierarchy' in html:#这是一个目录 GET FOLDER
			list = soup.find_all(attrs={"class": "remarkup-list"})
			list = list[0]
			count = 0
			link = []
			for li in list:
				#Parent
				obj = re.search(r'a href="(.*)">(.*)</a>',li.next_element.encode("utf-8"))
				count+=1
				link.append({
					'title': obj.group(2),#目录标题
					'url'  : self.host + obj.group(1)#目录链接
				})	
			return link #返回目录以及对应链接  Back Folders and Link
		else:
			return html  #返回文章内容html Back HTML
	