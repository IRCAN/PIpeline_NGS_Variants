#!/usr/bin/python
# coding: utf-8 

"""Script qui trouve si un hotspot est present dans le fichier de correlation refseq et cosmic.

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

def main_compare_hs(fichier):
	hotspots = parse_hs_file()
	#Modifier fichier de input pour comparer les variants trouves dans l'input au fichier de HS de reference de Tibo
	File = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/RefSeqToEnsembl_"+fichier
	sample = open(File,'r')
	sample = read_file(sample)
	del sample[0]
	outputFile = open("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/HSm_"+fichier, 'w')
	outputFile.write("gene\texon\ttranscript\tcoding\tprotein\tcosmic\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
	for hsLigne in hotspots:
		hsLigneSplit = hsLigne.split("\t")
		for sampleLigne in sample:
			sampleLigne = sampleLigne.replace("\n","")
			sampleLigneSplit = sampleLigne.split("\t")
			cosm_id = sampleLigneSplit[5][4:]
			hgvsp = sampleLigneSplit[7]
			if hsLigneSplit[0] == sampleLigneSplit[0] and int(hsLigneSplit[1]) <= int(sampleLigneSplit[1])<= int(hsLigneSplit[2]) and hsLigneSplit[3] == sampleLigneSplit[2] and cosm_id in hsLigneSplit[6] and sampleLigneSplit[6] in hsLigneSplit[7]:
				HSm = sampleLigneSplit[2]+"\t"+hsLigneSplit[4]+"\t"+sampleLigneSplit[4]+"\t"+sampleLigneSplit[6]+"\t"+hgvsp+"\t"+"COSM"+cosm_id+"\t"+sampleLigneSplit[11]+"\t"+sampleLigneSplit[12]+"\t"+sampleLigneSplit[8]+"\t"+"rien"+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\n"
				outputFile.write(HSm)

#TODO// verifier si allele_cov ou allele freq dans les filtres pour determiner si polymorphisme ou autre
#comparer avec fichier MUTATIONS
def parse_mutations_file(fichier):
	File = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VariantCaller/MUTATIONS_"+fichier
	mutationsFile = open(File,'r')
	mutationsFile = read_file(mutationsFile)
	del mutationsFile[0:71]
	return mutationsFile