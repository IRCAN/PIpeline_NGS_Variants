#!/usr/bin/python3
# coding: utf-8 
import os

"""
Script qui, pour chaque mutations, la filtre dans differentes categories:
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
	File = "../Resultats/Auto_user_INS-92-SG_19-5-16_159_208/VariantCaller/MUTATIONS_"+fichier
	mutationsFile = open(File,'r')
	mutationsFile = read_file(mutationsFile)
	del mutationsFile[0:71]
	return mutationsFile

def compare_hs(File,sample,fichier):
	"""Compare les mutations de l'echantillon au fichier des hotspots d'interet."""
	hotspots = parse_hs_file()
	#Modifier fichier de input pour comparer les variants trouves dans l'input au fichier de HS de reference de Tibo
	outputFile = open("../Resultats/Auto_user_INS-92-SG_19-5-16_159_208/temp/HSm_"+fichier, 'w')
	outputFile.write("gene\texon\tRefSeq id\tTranscript\tHGVSc\tHGVSp\tcosmic ID\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
	suppList = []
	# If 0 = file is empty, if 1 file is not empty
	fileNotEmpty = 0
	for hsLigne in hotspots:
		hsLigneSplit = hsLigne.split("\t")
		for sampleLigne in sample:
			sampleLigneReplace = sampleLigne.replace("\n","")
			sampleLigneSplit = sampleLigneReplace.split("\t")
			temp = sampleLigneSplit[0].split(":")
			chrNumber = "chr"+temp[0]
			position = temp[1]
			cosmNumber = sampleLigneSplit[6].replace("COSM","")
			hgvsp = sampleLigneSplit[5]
			if hsLigneSplit[0] == chrNumber and int(hsLigneSplit[1]) <= int(position) <= int(hsLigneSplit[2]) and hsLigneSplit[3] == sampleLigneSplit[1] and cosmNumber in hsLigneSplit[6] and sampleLigneSplit[4] in hsLigneSplit[7]:
				HSm = sampleLigneSplit[1]+"\t"+hsLigneSplit[4]+"\t"+sampleLigneSplit[2]+"\t"+sampleLigneSplit[3]+"\t"+sampleLigneSplit[4]+"\t"+hgvsp+"\t"+"COSM"+cosmNumber+"\t"+sampleLigneSplit[7]+"\t"+sampleLigneSplit[8]+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\t"+sampleLigneSplit[11]+"\t"+sampleLigneSplit[12]+"\n"
				fileNotEmpty = 1
				outputFile.write(HSm)
				suppList.append(sampleLigne)
	if fileNotEmpty == 0:
		os.remove("../Resultats/Auto_user_INS-92-SG_19-5-16_159_208/temp/HSm_"+fichier)
	for supp in suppList:
		sample.remove(supp)

def find_mutation_douteuse(File,sample,fichier):
	"""Recherche parmis les mutations si elle est douteuse, cad si frequence allelique < 1 et couverture < 25."""
	outputFile = open("../Resultats/Auto_user_INS-92-SG_19-5-16_159_208/temp/Mutations_douteuse_"+fichier, 'w')
	outputFile.write("gene\tposition\tRefSeq id\tTranscript\tHGVSc\tHGVSp\tcosmic ID\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
	suppList = []
	# If 0 = file is empty, if 1 file is not empty
	fileNotEmpty = 0
	for sampleLigne in sample:
		sampleLigneReplace = sampleLigne.replace("\n","")
		sampleLigneSplit = sampleLigneReplace.split("\t")
		alleleCov = sampleLigneSplit[7]
		alleleFreq = sampleLigneSplit[8].replace("%","")
		if alleleCov != "cov_not_find":
			#Filtres pour determiner si mutation douteuse:
			# allele_cov < 25 et allele_freq < 1
			if int(alleleCov) <= 25 and float(alleleFreq) < 1:
				string = sampleLigneSplit[1]+"\t"+sampleLigneSplit[0]+"\t"+sampleLigneSplit[2]+"\t"+sampleLigneSplit[3]+"\t"+sampleLigneSplit[4]+"\t"+sampleLigneSplit[5]+"\t"+sampleLigneSplit[6]+"\t"+sampleLigneSplit[7]+"\t"+sampleLigneSplit[8]+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\t"+sampleLigneSplit[11]+"\t"+sampleLigneSplit[12]+"\n"
				outputFile.write(string)
				suppList.append(sampleLigne)
				fileNotEmpty = 1
	if fileNotEmpty == 0:
		os.remove("../Resultats/Auto_user_INS-92-SG_19-5-16_159_208/temp/Mutations_douteuse_"+fichier)
	for supp in suppList:
		sample.remove(supp)

def find_polymorphism(File,sample,fichier):
	"""Recherche parmis les mutations si c'est un polymorphisme, cad si la minor allele frequency > 0.01."""
	outputFile = open("../Resultats/Auto_user_INS-92-SG_19-5-16_159_208/temp/Polymorphism_"+fichier, 'w')
	outputFile.write("gene\tposition\tRefSeq id\tTranscript\tHGVSc\tHGVSp\tcosmic ID\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
	# If 0 = file is empty, if 1 file is not empty
	fileNotEmpty = 0
	suppList = []
	for sampleLigne in sample:
		sampleLigneReplace = sampleLigne.replace("\n","")
		sampleLigneSplit = sampleLigneReplace.split("\t")
		maf = sampleLigneSplit[10]
		if maf != "NA":
			mafSplit = maf.split(":")
			mafValue = mafSplit[1]
			mafValue = float(mafValue)
			mafValue = "%.2f" % mafValue
			if float(mafValue) > 0.01:
				fileNotEmpty = 1
				string = sampleLigneSplit[1]+"\t"+sampleLigneSplit[0]+"\t"+sampleLigneSplit[2]+"\t"+sampleLigneSplit[3]+"\t"+sampleLigneSplit[4]+"\t"+sampleLigneSplit[5]+"\t"+sampleLigneSplit[6]+"\t"+sampleLigneSplit[7]+"\t"+sampleLigneSplit[8]+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\t"+sampleLigneSplit[11]+"\t"+sampleLigneSplit[12]+"\n"
				outputFile.write(string)
				suppList.append(sampleLigne)
	if fileNotEmpty == 0:
		os.remove("../Resultats/Auto_user_INS-92-SG_19-5-16_159_208/temp/Polymorphism_"+fichier)
	for supp in suppList:
		sample.remove(supp)

def mutationSignification(File,sample,fichier):
	"""Cree un fichier contenant toutes les mutations qui ne sont pas categorisees."""
	outputFile = open("../Resultats/Auto_user_INS-92-SG_19-5-16_159_208/temp/signification_"+fichier, 'w')
	outputFile.write("gene\tposition\tRefSeq id\tTranscript\tHGVSc\tHGVSp\tcosmic ID\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
	if len(sample) != 0:
		for sampleLigne in sample:
			sampleLigneReplace = sampleLigne.replace("\n","")
			sampleLigneSplit = sampleLigneReplace.split("\t")
			string = sampleLigneSplit[1]+"\t"+sampleLigneSplit[0]+"\t"+sampleLigneSplit[2]+"\t"+sampleLigneSplit[3]+"\t"+sampleLigneSplit[4]+"\t"+sampleLigneSplit[5]+"\t"+sampleLigneSplit[6]+"\t"+sampleLigneSplit[7]+"\t"+sampleLigneSplit[8]+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\t"+sampleLigneSplit[11]+"\t"+sampleLigneSplit[12]+"\n"
			outputFile.write(string)
	else:
		os.remove("../Resultats/Auto_user_INS-92-SG_19-5-16_159_208/temp/signification_"+fichier)


def main_filtre(fichier):
	File = "../Resultats/Auto_user_INS-92-SG_19-5-16_159_208/temp/resultats_"+fichier
	sample = open(File,'r')
	sample = read_file(sample)
	del sample[0]
	compare_hs(File,sample,fichier)
	find_mutation_douteuse(File,sample,fichier)
	find_polymorphism(File,sample,fichier)
	mutationSignification(File,sample,fichier)