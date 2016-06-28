#!/usr/bin/python
# coding: utf-8 

"""Script creant un fichier resume et qualite pour chaque echantillon du run.
Ludovic KOSTHOWA (Debut : 06/04/16)
Info: Creation en cours, script peut etre modifie a tout moment.
"""

import os,re
import glob
from argparse import ArgumentParser

class GlobalInformations():
	def __init__(self,REPERTORYVCF):
		#liste vide de x elements par echantillon
			self.sampleList = [None]*14
		#liste contenant tout les barcodes du run
			self.barcodeList = []
		#liste contenant tout les reads on target du run
			self.listReadsOnTarget = []
		#liste contenant les noms des echantillons
			self.sampleNameList = []
		#liste contenant les reads "mappes"
			self.mappedReadsList = []
		#liste qui contiendra chaque sampleList
			self.finalList = [['Sample','Barcode','Kit','Run date','Chip','Mapped Reads','ID','Reads On-Target','Reads On-SampleID','Mean Read Depth','Base at 1x Coverage','20x','100x','500x',' ']]
		#############################
		#############################
		# Attention chemins
		#############################
		#############################
			fileSummary = glob.glob("../Run_test/"+REPERTORYVCF+"/plugin_out/coverageAnalysis_out.*/*.bc_summary.xls")
		
			self.file1 = open(fileSummary[0],"r")
			self.fileContent = self.read_file(self.file1)
			self.get_list_barcode(self.fileContent)
			self.get_list_reads_on_target(self.fileContent)
			self.get_sample(self.fileContent)
			self.get_mapped_reads(self.fileContent)

		#############################
		#############################
		# Attention chemins
		#############################
		#############################

			################################################################################
			# Ouverture et Analyse du fichier explog_final.txt
			################################################################################
			fileExplogFinal="../Run_test/"+REPERTORYVCF+"/explog_final.txt"
			self.file2=open(fileExplogFinal, 'r')  # "../Data/Run_test/Auto_user_INS-80-TF_23-02-16_151_198/explog_final.txt"
			self.fileContent = self.read_file(self.file2)
			kit = self.get_kit(self.fileContent)
			chip = self.get_chip(self.fileContent)

			curentBarecodeNumber =0
			for barecode in self.barcodeList:
			
				sampleList=['NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA']
				"""Creation de la ligne pour chaque echantillons"""
				sampleList[0] = self.sampleNameList[curentBarecodeNumber]
				sampleList[1] = barecode
				sampleList[2] = kit
				sampleList[3] = self.get_run_date()
				sampleList[4] = chip
				sampleList[5] = self.mappedReadsList[curentBarecodeNumber]
				sampleList[7] = self.listReadsOnTarget[curentBarecodeNumber]
				################################################################################
				# Ouverture et Analyse du fichier read_stats.txt
				################################################################################
				fileName =glob.glob("../Run_test/"+REPERTORYVCF+"/plugin_out/sampleID_out.*/"+barecode+"/read_stats.txt")
				fichier = open(fileName[0],"r")
				fileContent = self.read_file(fichier)
		
				sampleList[6] = self.get_id(fileContent)
				sampleList[8] = self.get_reads_on_sample_ID(fileContent)
				fichier.close()
				################################################################################
				# Ouverture et Analyse du fichier .stats.cov.txt
				################################################################################
				fileName=glob.glob("../Run_test/"+REPERTORYVCF+"/plugin_out/coverageAnalysis_out.*/"+barecode+"/"+barecode+"*.stats.cov.txt")
				fichier = open(fileName[0],"r")
				fileContent = self.read_file(fichier)
				sampleList[9]=self.get_mean_read_depth(fileContent)
				sampleList[10]=self.get_coverage_1x(fileContent)
				sampleList[11]=self.get_coverage_20x(fileContent)
				sampleList[12]=self.get_coverage_100x(fileContent)
				sampleList[13]=self.get_coverage_500x(fileContent)
				sampleList[14]=" "
				self.finalList.append(sampleList)
				curentBarecodeNumber += 1

			################################################################################
			# Creation du fichier final globalInformations.txt
			################################################################################
			if os.path.isdir('../Results/'+REPERTORYVCF) == False:
				#print("creation du repertoire")
				os.mkdir('../Results/'+REPERTORYVCF) 
			FileName = '../Results/'+REPERTORYVCF+'/'+REPERTORYVCF+'_globalInformations.txt'
			self.output_file(FileName, self.finalList)
			print("\nCreation fichier informations OK \n")

	def read_file(self,File):
		"""Lit le fichier d'entree."""
		fileContent = File.readlines()
		File.close() 
		return fileContent

	def get_list_barcode(self,fileContent):
		"""Recupere la liste des barecodes pour un run."""
		#supprime la legende
		del fileContent[0]
		for elements in fileContent:
			#recupere le nom du barcode
			elements = elements[0:13]
			self.barcodeList.append(elements)

	def get_sample(self,fileContent):
		"""Recupere les identifiants des echantillons."""
		for elements in fileContent:
			elements = elements.split('\t')
			self.sampleNameList.append(elements[1])

	def get_kit(self,fileContent):
		"""Recupere le nom du kit utilise pour le run."""
		if 'LungColon_CPv2' in fileContent[0]:
			kit = 'LungColon_CPv2' 
		elif 'CCrenal' in fileContent[0]:
			kit = 'CCrenal'
		else:
			kit = "not define"
		return kit

	def get_run_date(self):
		"""Recupere la date d'execution du run."""
		listdir = []
		#############################
		#############################
		# Attention chemins
		#############################
		#############################
		listdir = os.listdir("../Run_test/")
		for i in listdir:
			m = re.search('\d.-\d.-\d.', i)
			if m is not None:
				match = m.group()
		return match

	def get_chip(self,fileContent):
		"""Recupere le type du chip utilise."""
		for indice in fileContent:
			if 'ChipType' in indice:
				chip = indice
		if '318C' in chip:
			chip = 'Ion 318 Chip V2'
		else:
			chip = "chip non define"
		return chip

	def get_mapped_reads(self,fileContent):
		"""Recupere le nombre de mapped reads pour chaque echantillons."""
		for elements in fileContent:
			elements = elements.split('\t')
			self.mappedReadsList.append(elements[2])

	def get_id(self,fileContent):
		"""Recupere l'identifiant de chaque echantillon."""
		ID = fileContent[1]
		ID = ID.replace('Sample ID:   ','')
		ID = ID.replace('\n','')
		return ID

	def get_list_reads_on_target(self,fileContent):
		"""Recuper la liste des reads on target."""
		for elements in fileContent:
			reads = elements.split('\t')
			reads = reads[3]
			self.listReadsOnTarget.append(reads)

	def get_reads_on_sample_ID(self,fileContent):
		"""Recupere le nombre de reads sur le SampleID."""
		readsOnSampleID = fileContent[4]
		readsOnSampleID = readsOnSampleID.replace('Percent reads in sample ID regions:   ','')
		readsOnSampleID = readsOnSampleID.replace('\n','')
		return readsOnSampleID

	def get_mean_read_depth(self,fileContent):
		"""Recupere la profondeur moyenne des reads d'un echantillon."""
		meanReadDepth = fileContent[26]
		meanReadDepth = meanReadDepth.replace('Average base coverage depth: ','')
		meanReadDepth = meanReadDepth.replace('\n','')
		return float(meanReadDepth)

	def get_coverage_1x(self,fileContent):
		"""Recupere la couverture à 1x."""
		coverage1x = fileContent[28]
		coverage1x = coverage1x.replace('Target base coverage at 1x:   ','')
		coverage1x = coverage1x.replace('\n','')
		return coverage1x

	def get_coverage_20x(self,fileContent):
		"""Recupere la couverture à 20x."""		
		coverage20x = fileContent[29]
		coverage20x = coverage20x.replace('Target base coverage at 20x:  ','')
		coverage20x = coverage20x.replace('\n','')
		return coverage20x

	def get_coverage_100x(self,fileContent):
		"""Recupere la couverture à 100x."""
		coverage100x = fileContent[30]
		coverage100x = coverage100x.replace('Target base coverage at 100x: ','')
		coverage100x = coverage100x.replace('\n','')
		return coverage100x

	def get_coverage_500x(self,fileContent):
		"""Recupere la couverture à 500x."""
		coverage500x = fileContent[31]
		coverage500x = coverage500x.replace('Target base coverage at 500x: ','')
		coverage500x = coverage500x.replace('\n','')
		return coverage500x

	def output_file(self,FileName, finalList):
		"""Cree le fichier output de global informations."""
		fileName = FileName
		# creation et ouverture du File
		with open(fileName,"w") as fout:
		# ecriture dans le File
			for i in finalList:
				i = str(i).replace("'","")
				i = str(i).replace("[","")
				i = str(i).replace("]","")
				fout.write(str(i))
				fout.write('\n')



