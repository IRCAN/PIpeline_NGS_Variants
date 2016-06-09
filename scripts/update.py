import cosmiclite
import os
"""Commentaires"""

class Updates:
	def __init__(self,REPERTORYVCF):
		################################################################################
		# Etape de verification de MAJ du genome local avec la derniere version du genome sur ensembl
		################################################################################
		print("Verification version génome...")
		update = False
		old = os.path.getsize('../System/Ensembl/')
		os.system('rsync -u rsync://ftp.ensembl.org/ensembl/pub/current_variation/VEP/homo_sapiens_vep_84_GRCh37.tar.gz ../System/Ensembl/')
		new = os.path.getsize('../System/Ensembl/')
		if old != new:
			update=True
		print("Verification génome OK")
		#création base de données cosmic allégée
		if not os.path.isfile("../System/Cosmic/Cosmic_lite.txt") or update:
			CosmicLite()
		################################################################################
		# Etape de creation des repertoires
		################################################################################
	
		if os.path.isdir("../Resultats/"+REPERTORYVCF+"/VariantCaller")== False:
			os.makedirs("../Resultats/"+REPERTORYVCF+"/VariantCaller") 
		if os.path.isdir("../Resultats/"+REPERTORYVCF+"/VEP/")== False:
			os.mkdir("../Resultats/"+REPERTORYVCF+"/VEP/")
		if os.path.isdir("../Resultats/"+REPERTORYVCF+"/temp/")== False:
			os.mkdir("../Resultats/"+REPERTORYVCF+"/temp/")  

