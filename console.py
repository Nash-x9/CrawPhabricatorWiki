# -*- coding: utf-8 -*-

import sys,getopt
from RequestLimeWiki import RequestLimeWiki

def usage():
	print 
	print 'python console.py --server=<ServerHost> --user=<username> --pass=<password> --CommandLine'
	print 
	print 'Accept CommandLine:'
	print 
	print ' --login: Login Phriction.It will return loginDatas'
	print 
	print ' --getPage="http://what.you.want.to.craw">: get a requests type object from url'	

def main(argv):
	host = 'http://192.168.1.1'
	username = ''
	password = ''
	url = ''
	if argv[1:] == []:
		usage()
		sys.exit()
	try:
		opts, args = getopt.getopt(sys.argv[1:],"h",["server=","user=","pass=","url=","help","login","getPage="])
	except getopt.GetoptError:
		usage()
		sys.exit()
	
	for opt,arg in opts:
		if opt == '--help':
			usage()
			sys.exit()
		elif opt == '--server':
			host = arg
			RLW = RequestLimeWiki(host)
		elif opt == '--user':
			username = arg
		elif opt == '--pass':
			password = arg
		elif opt == '--server':
			host = arg
		elif opt == '--login':
			if username != '' and password != '' and host != '':
				return RLW.login(username,password)
			else:
				print '\n You Miss One of the Options:[username,password,host]'
		elif opt == '--getPage':
			url = arg
			if url != '':
				loginData = RLW.login(username,password)
				if loginData != None and loginData['cookie'] != None:
					r = RLW.getPage(dict(loginData['cookie']),url)
					print RLW.parseHtml(r.text)
			else:
				print '\nYou should add option --url="http://You.want.to.Craw.com"'
				sys.exit()
		else:
			usage()
			sys.exit()
			
	
	
if __name__ == '__main__':
	main(sys.argv)