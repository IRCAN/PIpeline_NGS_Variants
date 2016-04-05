import os
import re

#creation d'une liste vide de 12 elements par echantillon
sampleList=[]
#creation d'une liste contenant tout les barcodes du run
barcodeList=[]
#creation d'une liste qui contiendra chaque sampleList
finalList=[['Sample','Barcode','Kit','Run date','Chip','Mapped Reads','ID','Reads On-Target','Reads On-SampleID','Mean Read Depth','Base at 1x Coverage','Base at 20x Coverage','Base at 100x Coverage']]

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
	sample = fileContent[0]
	##TODO// A ameliorer par recherche expression reguliere
	sample = sample.replace('Sample Name: ','')
	sample = sample.replace('\n','')
	sampleList[0] = sample
def get_barcode(barecode):
	sampleList[1] = barecode
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
	sampleList[3] = match
def get_chip(fileContent):
	for indice in fileContent:
		if 'ChipType' in indice:
			chip = indice
	if '318C' in chip:
		chip = 'Ion 318 Chip V2'
	return chip
def get_mapped_reads(fileContent):
	mappedReads = fileContent[2]
	##TODO// A ameliorer par recherche expression reguliere
	mappedReads = mappedReads.replace('Number of mapped reads:    ','')
	mappedReads = mappedReads.replace('\n','')
	sampleList[5] = int(mappedReads)
def get_id(fileContent):
	ID = fileContent[1]
	##TODO// A ameliorer par recherche expression reguliere
	ID = ID.replace('Sample ID:   ','')
	ID = ID.replace('\n','')
	sampleList[6] = ID
def get_reads_on_target():
	readsOnTarget
	##//TODO
	pass
	sampleList[7] = readsOnTarget
def get_reads_on_sample_ID(fileContent):
	readsOnSampleID = fileContent[4]
	##TODO// A ameliorer par recherche expression reguliere
	readsOnSampleID = readsOnSampleID.replace('Percent reads in sample ID regions:   ','')
	readsOnSampleID = readsOnSampleID.replace('\n','')
	sampleList[8] = readsOnSampleID
def get_mean_read_depth(fileContent):
	meanReadDepth = fileContent[1]
	##TODO// A ameliorer par recherche expression reguliere
	meanReadDepth = meanReadDepth.replace('Average base coverage depth: ','')
	meanReadDepth = meanReadDepth.replace('\n','')
	sampleList[9] = float(meanReadDepth)
def get_coverage_1x(fileContent):
	coverage1x = fileContent[3]
	##TODO// A ameliorer par recherche expression reguliere
	coverage1x = coverage1x.replace('Coverage at 1x:   ','')
	coverage1x = coverage1x.replace('\n','')
	sampleList[10] = coverage1x
def get_coverage_20x(fileContent):
	coverage20x = fileContent[4]
	##TODO// A ameliorer par recherche expression reguliere
	coverage20x = coverage20x.replace('Coverage at 20x:  ','')
	coverage20x = coverage20x.replace('\n','')
	sampleList[11] = coverage20x
def get_coverage_100x(fileContent):
	coverage100x = fileContent[5]
	##TODO// A ameliorer par recherche expression reguliere
	coverage100x = coverage100x.replace('Coverage at 100x: ','')
	coverage100x = coverage100x.replace('\n','')
	sampleList[12] = coverage100x
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

##############################################################
########					MAIN					  ########
##############################################################

############## TODO lorsque acces au serveur OK ##############
#TODO// recuperer liste des echantillon du run et boucler sur cette liste
#TODO// recuperer read on target
"""
Ouverture et Analyse du fichier *summary.xls
"""
Fichier = open("../Data/Run_test/Auto_user_INS-81-SG_02-03-16_152/Root/plugin_out/sampleID_out.415/R_2014_07_31_06_44_53_user_INS-81-SG_02-03-16_Auto_user_INS-81-SG_02-03-16_152.bc_summary.xls","r")
fileContent = read_file(Fichier)
get_list_barcode(fileContent)
Fichier.close()

"""
Ouverture et Analyse du fichier explog_final.txt
"""
NomFichier = "../Data/Run_test/Auto_user_INS-81-SG_02-03-16_152/explog_final.txt"
Fichier = open(NomFichier,"r")
fileContent = read_file(Fichier)
kit = get_kit(fileContent)
chip = get_chip(fileContent)
Fichier.close()

for barecode in barcodeList:

	sampleList=['NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA']

	"""
	Ouverture et Analyse du fichier read_stats.txt
	"""

	NomFichier = "../Data/Run_test/Auto_user_INS-81-SG_02-03-16_152/Root/plugin_out/sampleID_out.415/"+barecode+"/read_stats.txt"
	Fichier = open(NomFichier,"r")
	fileContent = read_file(Fichier)
	get_sample(fileContent)
	get_barcode(barecode)
	get_id(fileContent)
	get_mapped_reads(fileContent)
	get_reads_on_sample_ID(fileContent)
	Fichier.close()
	sampleList[2] = kit
	get_run_date()
	sampleList[4] = chip

	"""
	Ouverture et Analyse du fichier on_target_stats.txt
	"""

	NomFichier = "../Data/Run_test/Auto_user_INS-81-SG_02-03-16_152/Root/plugin_out/sampleID_out.415/"+barecode+"/on_target_stats.txt"
	Fichier = open(NomFichier,"r")
	fileContent = read_file(Fichier)
	get_mean_read_depth(fileContent)
	get_coverage_1x(fileContent)
	get_coverage_20x(fileContent)
	get_coverage_100x(fileContent)
	finalList.append(sampleList)
"""
Creation du fichier final summary.txt
"""
#TODO// recuperer nom de l'echantillon +_summary.txt
FileName = '../Resultats/Auto_user_INS-81-SG_02-03-16_152_summary.txt'
output_file(FileName, finalList)






