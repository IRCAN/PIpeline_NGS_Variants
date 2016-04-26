#!/usr/bin/python
# coding: utf-8 

def read_file(File):
	"""Ouvre et lit le fichier .vcf de chaque patients."""
	contentFile = File.readlines()
	File.close() 
	return contentFile

hs = "../Data/Thibault/liste_hotspots_TF.tsv"
hotspots_file = open(hs,'r')
hotspots = read_file(hotspots_file)
del hotspots[0]
#print(hotspots)
#hotspots = file_to_list(hotspots_temp)

File = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/resultats_correlation_refseq_vs_cosmic.txt"
sample = open(File,'r')
sample = read_file(sample)
del sample[0]

output_file = open("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/HSm.txt", 'w')
output_file.write("gene\texon\ttranscript\tcoding\tprotein\tcosmic\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")

for ligne_hs in hotspots:
	ligne_hs_split = ligne_hs.split("\t")
	#ligne_hs_info_split = ligne_hs_split[5].split(";")
	for ligne_sample in sample:
		ligne_sample_split = ligne_sample.split("\t")
		cosm_id = ligne_sample_split[5][4:]
		if ligne_hs_split[0] == ligne_sample_split[0] and int(ligne_hs_split[1]) <= int(ligne_sample_split[1])<= int(ligne_hs_split[2]) and ligne_hs_split[3] == ligne_sample_split[2] and cosm_id in ligne_hs_split[6] and ligne_sample_split[6] in ligne_hs_split[7]:
			HSm = ligne_hs_split[0]+"\t"+ligne_hs_split[4]+"\t"+ligne_sample_split[4]+"\t"+ligne_sample_split[6]+"\t"+ligne_sample_split[5]+"\n"
			output_file.write(HSm)
			print(HSm)

