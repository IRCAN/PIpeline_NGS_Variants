#!/usr/bin/python
# coding: utf-8 
import os,re
import glob
from argparse import ArgumentParser

"""
Script creant un fichier resume et qualite pour chaque echantillon du run.

Ludovic KOSTHOWA (Debut : 06/04/16)
"""
class CreationResume():

	def __init__(self):
		
	#creation d'une liste vide de x elements par echantillon
		self.sampleList=[None]*14
	#creation d'une liste contenant tout les barcodes du run
		self.barcodeList=[]
	#creation d'une liste contenant tout les reads on target du run
		self.list_reads_on_target = []
	#creation d'une liste contenant les noms des echantillons
		self.sampleNameList = []
	#creation d'une liste contenant les reads "mappés"
		self.mappedReadsList = []
	#creation d'une liste qui contiendra chaque sampleList
		self.finalList=[['Sample','Barcode','Kit','Run date','Chip','Mapped Reads','ID','Reads On-Target','Reads On-SampleID','Mean Read Depth','Base at 1x Coverage','Base at 20x Coverage','Base at 100x Coverage','Base at 500x Coverage']]
		

	def read_file(self,File):
		# lit le fichier
		fileContent = File.readlines()
		# fermeture du fichier
		File.close() 
		return fileContent

	def get_list_barcode(self,fileContent):
		#supprime la legende
		del fileContent[0]
		for elements in fileContent:
			#recupere le nom du barcode
			elements = elements[0:13]
			self.barcodeList.append(elements)


	def get_sample(self,fileContent):
		for elements in fileContent:
			elements = elements.split('\t')
			self.sampleNameList.append(elements[1])

	def get_kit(self,fileContent):
		if 'LungColon_CPv2' in fileContent[0]:
			kit = 'LungColon_CPv2' 
		elif 'CCrenal' in fileContent[0]:
			kit = 'CCrenal'
		return kit

	def get_run_date(self):
		listdir = []
		listdir = os.listdir("../Data/Run_test/")
		for i in listdir:
			m =re.search('\d.-\d.-\d.', i)
			if m is not None:
				match = m.group()
		return match

	def get_chip(self,fileContent):
		for indice in fileContent:
			if 'ChipType' in indice:
				chip = indice
		if '318C' in chip:
			chip = 'Ion 318 Chip V2'
		return chip

	def get_mapped_reads(self,fileContent):
		for elements in fileContent:
			elements = elements.split('\t')
			self.mappedReadsList.append(elements[2])

	def get_id(self,fileContent):
		ID = fileContent[1]
	
		ID = ID.replace('Sample ID:   ','')
		ID = ID.replace('\n','')
		return ID
		#sampleList[6] = ID

	def get_list_reads_on_target(self,fileContent):
		for elements in fileContent:
			reads = elements.split('\t')
			reads = reads[3]
			self.list_reads_on_target.append(reads)

	def get_reads_on_sample_ID(self,fileContent):
		readsOnSampleID = fileContent[4]
		readsOnSampleID = readsOnSampleID.replace('Percent reads in sample ID regions:   ','')
		readsOnSampleID = readsOnSampleID.replace('\n','')
		return readsOnSampleID
		#sampleList[8] = readsOnSampleID

	def get_mean_read_depth(self,fileContent):
		meanReadDepth = fileContent[26]
		meanReadDepth = meanReadDepth.replace('Average base coverage depth: ','')
		meanReadDepth = meanReadDepth.replace('\n','')
		return float(meanReadDepth)
		

	def get_coverage_1x(self,fileContent):
		coverage1x = fileContent[28]
		coverage1x = coverage1x.replace('Target base coverage at 1x:   ','')
		coverage1x = coverage1x.replace('\n','')
		return coverage1x

	def get_coverage_20x(self,fileContent):
		coverage20x = fileContent[29]
		coverage20x = coverage20x.replace('Target base coverage at 20x:  ','')
		coverage20x = coverage20x.replace('\n','')
		return coverage20x

	def get_coverage_100x(self,fileContent):
		coverage100x = fileContent[30]
		coverage100x = coverage100x.replace('Target base coverage at 100x: ','')
		coverage100x = coverage100x.replace('\n','')
		return coverage100x

	def get_coverage_500x(self,fileContent):
		coverage500x = fileContent[31]
		coverage500x = coverage500x.replace('Target base coverage at 500x: ','')
		coverage500x = coverage500x.replace('\n','')
		return coverage500x

	def output_file(self,FileName, finalList):
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

"""
if __name__=='__main__':

		
	description = ("Script creant un fichier resume et qualite pour chaque echantillon du run.")
		 
	parser = ArgumentParser(description=description)
	parser.add_argument("--run", required=True, help="run repertory")
	#parser.add_argument("--summary", required=True, help="summary.xls")
	#parser.add_argument("--expl", required=True, help="explog_final.txt")
	args = parser.parse_args()
	repertoryVCF=args.run
"""	
def main(repertoryVCF):
	"""
	Ouverture et Analyse du fichier *summary.xls
	"""


	fileSummary =glob.glob("../Data/Run_test/"+repertoryVCF+"/plugin_out/coverageAnalysis_out.*/*.bc_summary.xls")
	resume = CreationResume()
	
	
	resume.file1=open(fileSummary[0],"r")
	
	resume.fileContent = resume.read_file(resume.file1)
	resume.get_list_barcode(resume.fileContent)
	resume.get_list_reads_on_target(resume.fileContent)
	resume.get_sample(resume.fileContent)
	resume.get_mapped_reads(resume.fileContent)
	"""
	Ouverture et Analyse du fichier explog_final.txt
	"""
	fileExplogFinal="../Data/Run_test/"+repertoryVCF+"/explog_final.txt"
	resume.file2=open(fileExplogFinal, 'r')  # "../Data/Run_test/Auto_user_INS-80-TF_23-02-16_151_198/explog_final.txt"
	resume.fileContent = resume.read_file(resume.file2)
	kit = resume.get_kit(resume.fileContent)
	chip = resume.get_chip(resume.fileContent)

	curentBarecodeNumber =0
	for barecode in resume.barcodeList:
			
		sampleList=['NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA']
		"""Creation de la ligne pour chaque echantillons"""
		sampleList[0] = resume.sampleNameList[curentBarecodeNumber]
		sampleList[1] = barecode
		sampleList[2] = kit
		sampleList[3] = resume.get_run_date()
		sampleList[4] = chip
		sampleList[5] = resume.mappedReadsList[curentBarecodeNumber]
		sampleList[7] = resume.list_reads_on_target[curentBarecodeNumber]
		"""
		Ouverture et Analyse du fichier read_stats.txt
		"""
		NomFichier =glob.glob("../Data/Run_test/"+repertoryVCF+"/plugin_out/sampleID_out.*/"+barecode+"/read_stats.txt")
		for fichier in NomFichier:
			Fichier = open(fichier,"r")
		fileContent = resume.read_file(Fichier)
		sampleList[6] = resume.get_id(fileContent)
		sampleList[8] = resume.get_reads_on_sample_ID(fileContent)
		Fichier.close()
		"""
		Ouverture et Analyse du fichier .stats.cov.txt
		"""
		NomFichier=glob.glob("../Data/Run_test/"+repertoryVCF+"/plugin_out/coverageAnalysis_out.*/"+barecode+"/"+barecode+"*.stats.cov.txt")
		
		#NomFichier = "../Data/Run_test/Auto_user_INS-80-TF_23-02-16_151_198/plugin_out/coverageAnalysis_out."+*+"/"+barecode+"/"+barecode+"_R_2014_07_31_04_21_49_user_INS-80-TF_23-02-16_Auto_user_INS-80-TF_23-02-16_151.stats.cov.txt"
		for fichier in NomFichier:
			Fichier = open(fichier,"r")
		fileContent = resume.read_file(Fichier)
		sampleList[9]=resume.get_mean_read_depth(fileContent)
		sampleList[10]=resume.get_coverage_1x(fileContent)
		sampleList[11]=resume.get_coverage_20x(fileContent)
		sampleList[12]=resume.get_coverage_100x(fileContent)
		sampleList[13]=resume.get_coverage_500x(fileContent)
		resume.finalList.append(sampleList)
		
		curentBarecodeNumber += 1
	"""
	Creation du fichier final summary.txt
	"""
	#TODO// recuperer nom de l'echantillon +_summary.txt
	if os.path.isdir('../Resultats/'+repertoryVCF) == False:
		#print("creation du repertoire")
		os.mkdir('../Resultats/'+repertoryVCF) 
	FileName = '../Resultats/'+repertoryVCF+'/'+repertoryVCF+'_summary.txt'
	resume.output_file(FileName, resume.finalList)


