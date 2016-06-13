#!/usr/bin/python
# coding: utf-8 

"""
Script principal du pipeline qui traite le fichier .vcf de chaque patients d'un run
afin d'obtenir un compte rendu de mutations.

Ludovic KOSTHOWA (Debut : 06/04/16)
Info: Creation en cours, script peut etre modifie a tout moment.
"""

import os,re,time,glob
from main_varan import MainVaran 
from update import Updates
from globalinformations import GlobalInformations
from argparse import ArgumentParser

if __name__=='__main__':
	start_time = time.time()  
	#TODO: better description	
	description = ("A partir d'un fichier VCF, ......")
	parser = ArgumentParser(description=description)
	parser.add_argument('run',  action='store' ,help="path to run repertory")
	parser.add_argument('-lh','--listHotspot', default=False, nargs='+', help="fournir une liste de hotspots")
	parser.add_argument('-gi','--globalinformations', action='store_true', help="need result of plugin CoverageAnalysis")
	parser.add_argument('-NoUp','--NoUpdates', action='store_false', help="pas de mise à jour des bdd")
	args = parser.parse_args()
	pathREPERTORYVCF=args.run
	if pathREPERTORYVCF[-1]=="/":
		pathREPERTORYVCF=pathREPERTORYVCF[:-1]
	splitPathREPERTORYVCF=pathREPERTORYVCF.split("/")
	REPERTORYVCF=splitPathREPERTORYVCF[-1]
	if args.NoUpdates==False:
		print("....")
	else:
		Updates(REPERTORYVCF)
	if args.globalinformations:
		GlobalInformations(REPERTORYVCF)
	################################################################################
	# Lancement du fichier principal
	################################################################################
	if args.listHotspot:
		MainVaran(pathREPERTORYVCF,REPERTORYVCF,ALL_HS_FILE=args.listHotspot)
	else:
		MainVaran(pathREPERTORYVCF,REPERTORYVCF)

	print("######################\n Fin du script!\n######################")
	interval = time.time() - start_time
	interval_in_min = interval/60
	print('Total time in seconds:', interval) 
	print('Total time in min:', interval_in_min) 
