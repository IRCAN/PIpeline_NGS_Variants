#!/usr/bin/python
# coding: utf-8 
import os

"""Script qui, pour chaque mutations, la filtre dans differentes categories:
Hotspots mutes, Polymorphisme ou mutation douteuse.

Ludovic KOSTHOWA (Debut : 06/04/16)
Info: Creation en cours, script peut etre modifie a tout moment.
"""

def read_file(File):
	"""Ouvre et lit le fichier .vcf de chaque patients."""
	contentFile = File.readlines()
	File.close() 
	return contentFile

def parse_hs_file():
	hs = "../Data/Thibault/liste_hotspots_TF.tsv"
	hotspotsFile = open(hs,'r')
	hotspots = read_file(hotspotsFile)
	del hotspots[0]
	return hotspots

def parse_mutations_file(fichier):
	"""Parse le fichier contenant les mutations de l'echantillon."""
	File = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VariantCaller/MUTATIONS_"+fichier
	mutationsFile = open(File,'r')
	mutationsFile = read_file(mutationsFile)
	del mutationsFile[0:71]
	return mutationsFile

def compare_hs(File,sample,fichier):
	"""Compare les mutations de l'echantillon au fichier des hotspots d'interet."""
	hotspots = parse_hs_file()
	#Modifier fichier de input pour comparer les variants trouves dans l'input au fichier de HS de reference de Tibo
	outputFile = open("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/HSm_"+fichier, 'w')
	outputFile.write("gene\texon\ttranscript\tcoding\tprotein\tcosmic\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
	# If 0 = file is empty, if 1 file is not empty
	fileNotEmpty = 0
	for hsLigne in hotspots:
		hsLigneSplit = hsLigne.split("\t")
		for sampleLigne in sample:
			sampleLigne = sampleLigne.replace("\n","")
			sampleLigneSplit = sampleLigne.split("\t")
			cosmNumber = sampleLigneSplit[5][4:]
			hgvsp = sampleLigneSplit[7]
			if hsLigneSplit[0] == sampleLigneSplit[0] and int(hsLigneSplit[1]) <= int(sampleLigneSplit[1])<= int(hsLigneSplit[2]) and hsLigneSplit[3] == sampleLigneSplit[2] and cosmNumber in hsLigneSplit[6] and sampleLigneSplit[6] in hsLigneSplit[7]:
				HSm = sampleLigneSplit[2]+"\t"+hsLigneSplit[4]+"\t"+sampleLigneSplit[4]+"\t"+sampleLigneSplit[6]+"\t"+hgvsp+"\t"+"COSM"+cosmNumber+"\t"+sampleLigneSplit[11]+"\t"+sampleLigneSplit[12]+"\t"+sampleLigneSplit[8]+"\t"+"rien"+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\n"
				fileNotEmpty = 1
				outputFile.write(HSm)
	if fileNotEmpty == 0:
		os.remove("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/HSm_"+fichier)

def find_mutation_douteuse(File,sample,fichier):
	"""Recherche parmis les mutations si elle est douteuse, cad si frequence allelique < 1 et couverture < 25."""
	outputFile = open("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/Mutations_douteuse_"+fichier, 'w')
	outputFile.write("gene\texon\ttranscript\tcoding\tprotein\tcosmic\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
	# If 0 = file is empty, if 1 file is not empty
	fileNotEmpty = 0
	for sampleLigne in sample:
		sampleLigne = sampleLigne.replace("\n","")
		sampleLigneSplit = sampleLigne.split("\t")
		alleleCov = sampleLigneSplit[8]
		alleleFreq = sampleLigneSplit[9].replace("%","")
		if alleleCov != "cov_not_find":
			#Filtres pour determiner si mutation douteuse:
			# allele_cov < 25 et allele_freq < 1
			if int(alleleCov) <= 25 and float(alleleFreq) < 1:
				outputFile.write(sampleLigne+"\n")
				fileNotEmpty = 1
	if fileNotEmpty == 0:
		os.remove("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/Mutations_douteuse_"+fichier)

def find_polymorphism(File,sample,fichier):
	"""Recherche parmis les mutations si c'est un polymorphisme, cad si la minor allele frequency < 1."""
	outputFile = open("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/Polymorphism_"+fichier, 'w')
	outputFile.write("gene\texon\ttranscript\tcoding\tprotein\tcosmic\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
	# If 0 = file is empty, if 1 file is not empty
	fileNotEmpty = 0
	for sampleLigne in sample:
		sampleLigne = sampleLigne.replace("\n","")
		sampleLigneSplit = sampleLigne.split("\t")
		maf = sampleLigneSplit[10]
		if maf != "maf_not_find":
			if int(maf) < 1:
				fileNotEmpty = 1
				outputFile.write(sampleLigne+"\n")
	if fileNotEmpty == 0:
		os.remove("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/Polymorphism_"+fichier)

def main_filtre(fichier):
	File = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/RefSeqToEnsembl_"+fichier
	sample = open(File,'r')
	sample = read_file(sample)
	del sample[0]
	compare_hs(File,sample,fichier)
	find_mutation_douteuse(File,sample,fichier)