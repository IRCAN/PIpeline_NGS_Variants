import os
import re

#creation d'une liste vide de 12 elements par echantillon
liste_echantillon=[]
#creation d'une liste contenant tout les barcodes du run
liste_barcode=[]
#creation d'une liste qui contiendra chaque liste_echantillon
liste_finale=[['Sample','Barcode','Kit','Run date','Chip','Mapped Reads','ID','Reads On-Target','Reads On-SampleID','Mean Read Depth','Base at 1x Coverage','Base at 20x Coverage','Base at 100x Coverage']]

def GetListBarcode(fileContent):
	#supprime la legende
	del fileContent[0]
	for elements in fileContent:
		#recupere le nom du barcode
		elements = elements[0:13]
		liste_barcode.append(elements)

def ReadFile(File):
	# lit le fichier
	fileContent = File.readlines()
	# fermeture du fichier
	File.close() 
	return fileContent

def GetSample(fileContent):
	sample = fileContent[0]
	##TODO// A ameliorer par recherche expression reguliere
	sample = sample.replace('Sample Name: ','')
	sample = sample.replace('\n','')
	liste_echantillon[0] = sample

def GetBarcode(barecode):
	liste_echantillon[1] = barecode

def GetKit(fileContent):
	if 'LungColon_CPv2' in fileContent[0]:
		kit = 'LungColon_CPv2' 
	elif 'CCrenal' in fileContent[0]:
		kit = 'CCrenal'
	return kit

def GetRunDate():
	listdir = []
	listdir = os.listdir("../Data/Run_test/")
	for i in listdir:
		m =re.search('\d.-\d.-\d.', i)
		if m is not None:
			match = m.group()
	liste_echantillon[3] = match


def GetChip(fileContent):
	for indice in fileContent:
		if 'ChipType' in indice:
			chip = indice
	if '318C' in chip:
		chip = 'Ion 318 Chip V2'
	return chip

def GetMappedReads(fileContent):
	mappedReads = fileContent[2]
	##TODO// A ameliorer par recherche expression reguliere
	mappedReads = mappedReads.replace('Number of mapped reads:    ','')
	mappedReads = mappedReads.replace('\n','')
	liste_echantillon[5] = int(mappedReads)

def GetID(fileContent):
	ID = fileContent[1]
	##TODO// A ameliorer par recherche expression reguliere
	ID = ID.replace('Sample ID:   ','')
	ID = ID.replace('\n','')
	liste_echantillon[6] = ID

def GetReadsOnTarget():
	readsOnTarget
	##//TODO
	pass
	liste_echantillon[7] = readsOnTarget

def GetReadsOnSampleID(fileContent):
	readsOnSampleID = fileContent[4]
	##TODO// A ameliorer par recherche expression reguliere
	readsOnSampleID = readsOnSampleID.replace('Percent reads in sample ID regions:   ','')
	readsOnSampleID = readsOnSampleID.replace('\n','')
	liste_echantillon[8] = readsOnSampleID

def GetMeanReadDepth(fileContent):
	meanReadDepth = fileContent[1]
	##TODO// A ameliorer par recherche expression reguliere
	meanReadDepth = meanReadDepth.replace('Average base coverage depth: ','')
	meanReadDepth = meanReadDepth.replace('\n','')
	liste_echantillon[9] = float(meanReadDepth)

def GetCoverage1x(fileContent):
	coverage1x = fileContent[3]
	##TODO// A ameliorer par recherche expression reguliere
	coverage1x = coverage1x.replace('Coverage at 1x:   ','')
	coverage1x = coverage1x.replace('\n','')
	liste_echantillon[10] = coverage1x

def GetCoverage20x(fileContent):
	coverage20x = fileContent[4]
	##TODO// A ameliorer par recherche expression reguliere
	coverage20x = coverage20x.replace('Coverage at 20x:  ','')
	coverage20x = coverage20x.replace('\n','')
	liste_echantillon[11] = coverage20x

def GetCoverage100x(fileContent):
	coverage100x = fileContent[5]
	##TODO// A ameliorer par recherche expression reguliere
	coverage100x = coverage100x.replace('Coverage at 100x: ','')
	coverage100x = coverage100x.replace('\n','')
	liste_echantillon[12] = coverage100x

def OutputFile(FileName, liste_finale):
	NomFichier = FileName
	# création et ouverture du File
	with open(NomFichier,"w") as fout:
	# écriture dans le File
		for i in liste_finale:
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
fileContent = ReadFile(Fichier)
GetListBarcode(fileContent)
Fichier.close()

"""
Ouverture et Analyse du fichier explog_final.txt
"""
NomFichier = "../Data/Run_test/Auto_user_INS-81-SG_02-03-16_152/explog_final.txt"
Fichier = open(NomFichier,"r")
fileContent = ReadFile(Fichier)
kit = GetKit(fileContent)
chip = GetChip(fileContent)
Fichier.close()

for barecode in liste_barcode:

	liste_echantillon=['NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA']

	"""
	Ouverture et Analyse du fichier read_stats.txt
	"""

	NomFichier = "../Data/Run_test/Auto_user_INS-81-SG_02-03-16_152/Root/plugin_out/sampleID_out.415/"+barecode+"/read_stats.txt"
	Fichier = open(NomFichier,"r")
	fileContent = ReadFile(Fichier)
	GetSample(fileContent)
	GetBarcode(barecode)
	GetID(fileContent)
	GetMappedReads(fileContent)
	GetReadsOnSampleID(fileContent)
	Fichier.close()
	liste_echantillon[2] = kit
	GetRunDate()
	liste_echantillon[4] = chip

	"""
	Ouverture et Analyse du fichier on_target_stats.txt
	"""

	NomFichier = "../Data/Run_test/Auto_user_INS-81-SG_02-03-16_152/Root/plugin_out/sampleID_out.415/"+barecode+"/on_target_stats.txt"
	Fichier = open(NomFichier,"r")
	fileContent = ReadFile(Fichier)
	GetMeanReadDepth(fileContent)
	GetCoverage1x(fileContent)
	GetCoverage20x(fileContent)
	GetCoverage100x(fileContent)



	liste_finale.append(liste_echantillon)



"""
Creation du fichier final summary.txt
"""
#TODO// recuperer nom de l'echantillon +_summary.txt
FileName = '../Resultats/Auto_user_INS-81-SG_02-03-16_152_summary.txt'
OutputFile(FileName, liste_finale)






