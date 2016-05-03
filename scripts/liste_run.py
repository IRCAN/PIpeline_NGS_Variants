#!/usr/bin/python
# coding: utf-8 

"""
script pour recuperer liste des runs presents sur le serveur du pgm ou le serveur professorx, et contenant les fichiers du plugin coverageAnalysis necessaires pour le script permettant de fiare un fichier resumé

Soit on se connecte au pgm, soit à professorx
"""

import pxssh
import getpass

class RechercheRun():

	def __init__(self, arg1):
		
		self.location = arg1
		
	def connection_ssh(self):
		print "Connection ssh sur " + self.location + "\n"
		if self.location== "pgm":
			try:                                                            
				s = pxssh.pxssh()
				hostname = "134.59.51.82" #raw_input('hostname: ')
				username = "ftessier" #raw_input('username: ')
				password = "ircan" #getpass.getpass('password: ')
				s.login (hostname, username, password)
				s.sendline ('cd /home/ionguest/results/analysis/output/Home')
				s.prompt()     
				print "Liste des runs \n"
				s.sendline ('ls')
				s.readline()
				s.prompt()
				print s.before
				print "Liste des runs avec CoverageAnalysis \n" 
				s.sendline('for file in *;do if test -d $file/plugin_out/coverageAnalysis_out; then echo $file; fi; done')
				s.readline()
				
				s.prompt()            
				print s.before
				s.logout()
			
			except pxssh.ExceptionPxssh, e:
				print "pxssh failed on login."
				print str(e)

		else:
		
			try:                                                            
				s = pxssh.pxssh()
				hostname = "134.59.51.200" #raw_input('hostname: ')
				username = raw_input('username: ')
				password = getpass.getpass('password: ')
				s.login (hostname, username, password)
				s.sendline ('cd /home/PGM/archivedReports')
				s.prompt()
				print "Liste des runs \n"
				s.sendline ('ls')
				s.readline()
				s.prompt()
				print s.before
				print "Liste des runs avec CoverageAnalysis \n"
				s.sendline('for file in *;do if test -d $file/plugin_out/coverageAnalysis_out; then echo $file; fi; done')
				s.readline()
				s.prompt()         
				print s.before
				s.logout()
			
			except pxssh.ExceptionPxssh, e:
				print "pxssh failed on login."
				print str(e)


if __name__=='__main__':

	choice = raw_input('Enter pgm or professorx :')
	#if choice=="pgm" or choice=="professorx":
	if choice=="pgm" or choice=="professorx":
		test=RechercheRun(choice)
		test.connection_ssh()
	else:
	    print 'I didn\'t understand your choice.'

