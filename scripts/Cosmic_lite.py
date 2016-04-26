#!/usr/bin/python
# coding: utf-8 

"""
Script qui reduit la taille de la database cosmic en supprimant tout les doublons par rapport aux identifiants cosmic.

Ludovic KOSTHOWA (Debut : 06/04/16)
Info: Creation en cours, script peut etre modifie a tout moment.
"""

File = "../Data/Cosmic/CosmicCompleteExport.tsv"
content_file = open(File,"r")
cosmic =  content_file.readlines()
cosmic_id_list = set()
cosmic_db_lite = []
f_out = "../Data/Cosmic/Cosmic_lite.txt"
File_out = open(f_out,'w')
print("Lecture de la base de données COSMIC...")
print("Création de Cosmic_lite: merci de patienter...")
for ligne_cosmic in cosmic:
	ligne_cosmic_split = ligne_cosmic.split("\t")
	if ligne_cosmic_split[16] not in cosmic_id_list:
		cosmic_id_list.add(ligne_cosmic_split[16])
		File_out.write(ligne_cosmic)
print("Création terminée !")
