#!/usr/bin/python
# coding: utf-8 

"""Script qui verifie sur le web les dernieres versions des bases de donnees.
Si il y a une mise a jour, telecharge et remplace l'ancien fichier par la nouvelle version.

Ludovic KOSTHOWA (06/04/16)
Info: Creation en cours, script peut etre modifie a tout moment."""

from cosmiclite import CosmicLite
import os

class Updates:
	def __init__(self,REPERTORYVCF):
		############################
		############################
		############################
		# TODO :Commentaire sur la fonction
		############################
		############################
		############################


		################################################################################
		# Etape de verification de MAJ du genome local avec la derniere version du genome sur ensembl
		################################################################################
		print("Verification version genome...")
		update = False
		old = os.path.getsize('../System/Ensembl/')
		os.system('rsync -u rsync://ftp.ensembl.org/ensembl/pub/current_variation/VEP/homo_sapiens_vep_84_GRCh37.tar.gz ../System/Ensembl/')
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
	
		if os.path.isdir("../Results/"+REPERTORYVCF+"/VariantCaller")== False:
			os.makedirs("../Results/"+REPERTORYVCF+"/VariantCaller") 
		if os.path.isdir("../Results/"+REPERTORYVCF+"/VEP/")== False:
			os.mkdir("../Results/"+REPERTORYVCF+"/VEP/")
		if os.path.isdir("../Results/"+REPERTORYVCF+"/temp/")== False:
			os.mkdir("../Results/"+REPERTORYVCF+"/temp/")  

