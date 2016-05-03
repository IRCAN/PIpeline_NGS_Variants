#!/usr/bin/python
# coding: utf-8 
import os,re
from argparse import ArgumentParser

"""
Script creant un fichier resume et qualite pour chaque echantillon du run.

Ludovic KOSTHOWA (Debut : 06/04/16)
"""

#creation d'une liste vide de x elements par echantillon
sampleList=[]
#creation d'une liste contenant tout les barcodes du run
barcodeList=[]
#creation d'une liste contenant tout les reads on target du run
list_reads_on_target = []
#creation d'une liste contenant les noms des echantillons
sampleNameList = []
#creation d'une liste contenant les reads "mappés"
mappedReadsList = []
#creation d'une liste qui contiendra chaque sampleList
finalList=[['Sample','Barcode','Kit','Run date','Chip','Mapped Reads','ID','Reads On-Target','Reads On-SampleID','Mean Read Depth','Base at 1x Coverage','Base at 20x Coverage','Base at 100x Coverage','Base at 500x Coverage']]

def get_list_barcode(fileContent):
	#supprime la legende
	del fileContent[0]
	for elements in fileContent:
		#recupere le nom du barcode
		elements = elements[0:13]
		barcodeList.append(elements)

def read_file(File):
	# lit le fichier
	fileContent = File.readlines()
	# fermeture du fichier
	File.close() 
	return fileContent

def get_sample(fileContent):
	for elements in fileContent:
		elements = elements.split('\t')
		sampleNameList.append(elements[1])

def get_kit(fileContent):
	if 'LungColon_CPv2' in fileContent[0]:
		kit = 'LungColon_CPv2' 
	elif 'CCrenal' in fileContent[0]:
		kit = 'CCrenal'
	return kit

def get_run_date():
	listdir = []
	listdir = os.listdir("../Data/Run_test/")
	for i in listdir:
		m =re.search('\d.-\d.-\d.', i)
		if m is not None:
			match = m.group()
	return match

def get_chip(fileContent):
	for indice in fileContent:
		if 'ChipType' in indice:
			chip = indice
	if '318C' in chip:
		chip = 'Ion 318 Chip V2'
	return chip

def get_mapped_reads(fileContent):
	for elements in fileContent:
		elements = elements.split('\t')
		mappedReadsList.append(elements[2])

def get_id(fileContent):
	ID = fileContent[1]
	
	ID = ID.replace('Sample ID:   ','')
	ID = ID.replace('\n','')
	return ID
	#sampleList[6] = ID

def get_list_reads_on_target(fileContent):
	for elements in fileContent:
		reads = elements.split('\t')
		reads = reads[3]
		list_reads_on_target.append(reads)

def get_reads_on_sample_ID(fileContent):
	readsOnSampleID = fileContent[4]
	
	readsOnSampleID = readsOnSampleID.replace('Percent reads in sample ID regions:   ','')
	readsOnSampleID = readsOnSampleID.replace('\n','')
	return readsOnSampleID
	#sampleList[8] = readsOnSampleID

def get_mean_read_depth(fileContent):
	meanReadDepth = fileContent[26]
	
	meanReadDepth = meanReadDepth.replace('Average base coverage depth: ','')
	meanReadDepth = meanReadDepth.replace('\n','')
	sampleList[9] = float(meanReadDepth)

def get_coverage_1x(fileContent):
	coverage1x = fileContent[28]
	
	coverage1x = coverage1x.replace('Target base coverage at 1x:   ','')
	coverage1x = coverage1x.replace('\n','')
	sampleList[10] = coverage1x

def get_coverage_20x(fileContent):
	coverage20x = fileContent[29]
	
	coverage20x = coverage20x.replace('Target base coverage at 20x:  ','')
	coverage20x = coverage20x.replace('\n','')
	sampleList[11] = coverage20x

def get_coverage_100x(fileContent):
	coverage100x = fileContent[30]
	
	coverage100x = coverage100x.replace('Target base coverage at 100x: ','')
	coverage100x = coverage100x.replace('\n','')
	sampleList[12] = coverage100x

def get_coverage_500x(fileContent):
	coverage500x = fileContent[31]
	coverage500x = coverage500x.replace('Target base coverage at 500x: ','')
	coverage500x = coverage500x.replace('\n','')
	sampleList[13] = coverage500x

def output_file(FileName, finalList):
	NomFichier = FileName
	# création et ouverture du File
	with open(NomFichier,"w") as fout:
	# écriture dans le File
		for i in finalList:
			i = str(i).replace("'","")
			i = str(i).replace("[","")
			i = str(i).replace("]","")
			fout.write(str(i))
			fout.write('\n')


############## TODO lorsque acces au serveur OK ##############
#TODO// recuperer liste des echantillon du run et boucler sur cette liste
#TODO// recuperer read on target


if __name__=='__main__':
	
	description = ("Script creant un fichier resume et qualite pour chaque echantillon du run.")
		 
	parser = ArgumentParser(description=description)
	parser.add_argument("--summary", required=True, help="summary.xls")
	parser.add_argument("--expl", required=True, help="explog_final.txt")
	args = parser.parse_args()

	"""
	Ouverture et Analyse du fichier *summary.xls
	"""
	with open(args.summary, 'r') as Fichier:
	#Fichier = open("../Data/Run_test/Auto_user_INS-80-TF_23-02-16_151_198/plugin_out/coverageAnalysis_out.410/R_2014_07_31_04_21_49_user_INS-80-TF_23-02-16_Auto_user_INS-80-TF_23-02-16_151.bc_summary.xls","r")
		fileContent = read_file(Fichier)
		get_list_barcode(fileContent)
		get_list_reads_on_target(fileContent)
		get_sample(fileContent)
		get_mapped_reads(fileContent)
		Fichier.close()

	"""
	Ouverture et Analyse du fichier explog_final.txt
	"""
	#NomFichier = "../Data/Run_test/Auto_user_INS-80-TF_23-02-16_151_198/explog_final.txt"
	with open(args.expl, 'r') as Fichier:
	#Fichier = open(NomFichier,"r")
		fileContent = read_file(Fichier)
		kit = get_kit(fileContent)
		chip = get_chip(fileContent)
		Fichier.close()
	curentBarecodeNumber =0
	for barecode in barcodeList:
			
		sampleList=['NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA']
		"""Creation de la ligne pour chaque echantillons"""
		sampleList[0] = sampleNameList[curentBarecodeNumber]
		sampleList[1] = barecode
		sampleList[2] = kit
		sampleList[3] = get_run_date()
		sampleList[4] = chip
		sampleList[5] = mappedReadsList[curentBarecodeNumber]
		sampleList[7] = list_reads_on_target[curentBarecodeNumber]
		"""
		Ouverture et Analyse du fichier read_stats.txt
		"""
		NomFichier = "../Data/Run_test/Auto_user_INS-80-TF_23-02-16_151_198/plugin_out/sampleID_out.412/"+barecode+"/read_stats.txt"
		Fichier = open(NomFichier,"r")
		fileContent = read_file(Fichier)
		sampleList[6] = get_id(fileContent)
		sampleList[8] = get_reads_on_sample_ID(fileContent)
		Fichier.close()
		"""
		Ouverture et Analyse du fichier .stats.cov.txt
		"""
		NomFichier = "../Data/Run_test/Auto_user_INS-80-TF_23-02-16_151_198/plugin_out/coverageAnalysis_out.410/"+barecode+"/"+barecode+"_R_2014_07_31_04_21_49_user_INS-80-TF_23-02-16_Auto_user_INS-80-TF_23-02-16_151.stats.cov.txt"
		Fichier = open(NomFichier,"r")
		fileContent = read_file(Fichier)
		get_mean_read_depth(fileContent)
		get_coverage_1x(fileContent)
		get_coverage_20x(fileContent)
		get_coverage_100x(fileContent)
		get_coverage_500x(fileContent)
		finalList.append(sampleList)

		curentBarecodeNumber += 1
	"""
	Creation du fichier final summary.txt
	"""
	#TODO// recuperer nom de l'echantillon +_summary.txt
	if os.path.isdir('../Resultats/Auto_user_INS-80-TF_23-02-16_151_198') == False:
		print("creation du repertoire")
		os.mkdir('../Resultats/Auto_user_INS-80-TF_23-02-16_151_198') 
	FileName = '../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/Auto_user_INS-80-TF_23-02-16_151_198_summary.txt'
	output_file(FileName, finalList)

