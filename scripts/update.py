#!/usr/bin/python
# coding: utf-8 

"""Script qui verifie sur le web les dernieres versions des bases de donnees.
Si il y a une mise a jour, telecharge et remplace l'ancien fichier par la nouvelle version.

Ludovic KOSTHOWA (06/04/16)
Suite par Florent TESSIER (15/08/16)."""

from cosmiclite import CosmicLite
import os

class Updates:
	def __init__(self,REPERTORYVCF,RESULTDIR):
		"""verification si nouvelle version base de donnees VEP, creation Cosmic_lite si inexistante, creation repertoires contenant les resultats"""


		################################################################################
		# Etape de verification de MAJ du genome local avec la derniere version du genome sur ensembl
		################################################################################
		print("Verification version genome...")
		update = False
		old = os.path.getsize('../System/Ensembl/')
		os.system('rsync -u rsync://ftp.ensembl.org/ensembl/pub/current_variation/VEP/homo_sapiens_vep_85_GRCh37.tar.gz ../System/Ensembl/')
		new = os.path.getsize('../System/Ensembl/')
		if old != new:
			update=True
		print("Verification genome OK")
		#création base de données cosmic allégée
		if not os.path.isfile("../System/Cosmic/Cosmic_lite.txt") or update:
			CosmicLite()
		################################################################################
		# Etape de creation des repertoires
		################################################################################
	
		if os.path.isdir(RESULTDIR+"/"+REPERTORYVCF+"/VariantCaller")== False:
			os.makedirs(RESULTDIR+"/"+REPERTORYVCF+"/VariantCaller") 
		if os.path.isdir(RESULTDIR+"/"+REPERTORYVCF+"/VEP/")== False:
			os.mkdir(RESULTDIR+"/"+REPERTORYVCF+"/VEP/")
		if os.path.isdir(RESULTDIR+"/"+REPERTORYVCF+"/temp/")== False:
			os.mkdir(RESULTDIR+"/"+REPERTORYVCF+"/temp/")  

