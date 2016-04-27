#!/usr/bin/python
# coding: utf-8 

"""
Script qui reduit la taille de la database cosmic en supprimant tout les doublons par rapport aux identifiants cosmic.

Ludovic KOSTHOWA (Debut : 06/04/16)
Info: Creation en cours, script peut etre modifie a tout moment.
"""

File = "../Data/Cosmic/CosmicCompleteExport.tsv"
contentFile = open(File,"r")
cosmic =  contentFile.readlines()
cosmicIdList = set()
cosmicDbLite = []
f_out = "../Data/Cosmic/Cosmic_lite.txt"
File_out = open(f_out,'w')
print("Lecture de la base de données COSMIC...")
print("Création de Cosmic_lite: merci de patienter...")
for cosmicLigne in cosmic:
	cosmicLigneSplit = cosmicLigne.split("\t")
	if cosmicLigneSplit[16] not in cosmicIdList:
		cosmicIdList.add(cosmicLigneSplit[16])
		File_out.write(cosmicLigne)
print("Création terminée !")
