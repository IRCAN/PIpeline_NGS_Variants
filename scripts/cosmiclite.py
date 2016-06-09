#!/usr/bin/python
# coding: utf-8 

"""
Script qui reduit la taille de la database cosmic en supprimant tout les doublons par rapport aux identifiants cosmic.

Ludovic KOSTHOWA (Debut : 06/04/16)
Info: Creation en cours, script peut etre modifie a tout moment.
"""
class CosmicLite:
	def __init__(self):
		File = "../System/Cosmic/CosmicCompleteExport.tsv"
		contentFile = open(File,"r")
		cosmic =  contentFile.readlines()
		contentFile.close()
		cosmicIdList = set()
		f_out = "../System/Cosmic/Cosmic_lite.txt"
		File_out = open(f_out,'w')
		print("Lecture de la base de données COSMIC...")
		print("Création de Cosmic_lite: merci de patienter...")
		for cosmicLigne in cosmic:
			cosmicLigneSplit = cosmicLigne.split("\t")
			if cosmicLigneSplit[16] not in cosmicIdList:
				cosmicIdList.add(cosmicLigneSplit[16])
				mutation_AA = cosmicLigneSplit[18].replace("\n","")
				ligne = cosmicLigneSplit[0]+"\t"+cosmicLigneSplit[1]+"\t"+cosmicLigneSplit[3]+"\t"+cosmicLigneSplit[7]+"\t"+cosmicLigneSplit[16]+"\t"+cosmicLigneSplit[17]+"\t"+cosmicLigneSplit[18]+"\n"
				File_out.write(ligne)
		File_out.close()
		print("Création terminée !")


