#!/usr/bin/python
# coding: utf-8 
"""Script principal du pipeline qui traite le fichier .vcf de chaque patients d'un run
afin d'obtenir un compte rendu de mutations.
Ludovic KOSTHOWA (Debut : 06/04/16)
Info: Creation en cours, script peut etre modifie a tout moment."""

import re,glob,os,shutil
from separationvariants import SeparationVariants
from hotspot import HotspotProcess
from variantfilter import VariantFilter
from refseqtoensembl import RefseqToEnsembl
from makeReport import *

class MainVaran(RefseqToEnsembl):

	def __init__(self,pathREPERTORYVCF, REPERTORYVCF, ALL_HS_FILE=""):
		RefseqToEnsembl.__init__(self)
		if ALL_HS_FILE != "":
			ALL_HS_FILE,hotspots=self.concatenate_hs(ALL_HS_FILE)
			self.run_VEP(pathREPERTORYVCF,REPERTORYVCF, hotspots, ALL_HS_FILE)
		else:
			self.run_VEP(pathREPERTORYVCF,REPERTORYVCF)

	def concatenate_hs(self,ALL_HS_FILE):
			""" TODO : Commentaires"""
			tempFile = open("liste_hotspot_temp.txt", "w")
			for element in ALL_HS_FILE:
				f = open(element, 'r+')
				sample = f.readlines()
				a = sample[-1]
				if a[-1] != "\n":		
					f.write("\n")	
				shutil.copyfileobj(open(element, 'r'), tempFile)
			tempFile.close()
			ALL_HS_FILE = tempFile
			hotspotsTemp=open("liste_hotspot_temp.txt", 'r')
			hotspots = self.file_to_list(hotspotsTemp)
			return (ALL_HS_FILE,hotspots)

	def run_VEP(self,pathREPERTORYVCF,REPERTORYVCF, hotspot="", ALL_HS_FILE=""):
		"""Lance le logiciel VEP sur les mutations présentes dans chaque échantillons pour les annoter."""
		######################
		######################
		#A modifier pour chemin
		######################
		######################
		pathBarecode=glob.glob(pathREPERTORYVCF+"/plugin_out/variantCaller_out*/IonXpress_[0-9]*")
		if not pathBarecode:
			path1=False
			pathBarecode=glob.glob(pathREPERTORYVCF+"/Variants/*")
		else:
			path1=True
		barecode=[]
		for element in pathBarecode:
			a=element.split('/')
			barecode.append(a[-1])
		print(barecode)
		for i in barecode:
			if path1:
				file = i+'.vcf'
				TSVC_variants = glob.glob(pathREPERTORYVCF+"/plugin_out/variantCaller_out*/"+i+"/TSVC_variants_"+file)
				print('Traitement du file: \n',TSVC_variants[0],'\n')
				print(i)
			else:
				file = i+'.vcf'
				TSVC_variants = glob.glob(pathREPERTORYVCF+"/Variants/"+i+"/"+file)
				print('Traitement du file: \n',TSVC_variants[0],'\n')
		######################
		######################
		#A modifier pour chemin
		######################
		######################
			with open(TSVC_variants[0],'r') as contentFile:
				TSVC_variants=contentFile.readlines()
			#Cree une liste avec chaque elements correspondant a une ligne du file
			listOfList = self.file_to_list(TSVC_variants)
			#Supprime les informations inutiles du file VCF
			legendCount=self.legende_counter(TSVC_variants)
			legendList = listOfList[0:legendCount]
			legendList[legendCount-1] = "\t".join(legendList[legendCount-1])
			del listOfList[0:legendCount]
			del TSVC_variants[0:legendCount]
			#Appel de la fonction qui separe les transcripts presents sur la meme ligne
			sep = SeparationVariants(TSVC_variants)
			#Traitement de la liste et ecriture dans file VCF: recupere les lignes avec 1 seul ID
			# dans listOfList et les autres dans ListdeNewLines + ajf_oute seulement les mutations
			listOfTranscripts = self.check_if_multiple_id(listOfList,sep.listNewLines)
			#//TODO A modifier lorsque arborescence finale connue
			f_out = "../Results/"+REPERTORYVCF+"/VariantCaller/SEP_LIGNES_"+file
			#creation du file de sortie: file VCF avec un transcript par ligne
			self.output_file(f_out,listOfTranscripts,legendList)
			print('Creation de ',f_out,'\n')
			################################################################################
			# Etape de recherche de Hotspots non mutes
			################################################################################
			#Etape de recherche de Hotspots non mutes
			if hotspot != "":
				resumeHotspot= HotspotProcess(REPERTORYVCF,hotspot,listOfTranscripts,file)
			################################################################################
			#Etape de creation du file ne contenant que les mutations
			################################################################################
			mutationsList = []
			for indice in range(len(listOfTranscripts)):
				transcript = listOfTranscripts[indice].split('\t')
				if "FAO=0;" not in transcript[7]:
					mutationsList.append(listOfTranscripts[indice])
			f_out2 = "../Results/"+REPERTORYVCF+"/VariantCaller/MUTATIONS_"+file
			print('Creation de ',f_out2,'\n')
			self.output_file(f_out2,mutationsList,legendList)
			################################################################################
			#Etape de lancement de VEP avec en input le file de mutations
			################################################################################
			inputfile = "../Results/"+REPERTORYVCF+"/VariantCaller/MUTATIONS_"+file
			outputFile2 = "../Results/"+REPERTORYVCF+"/VEP/VEP_"+file
			commandVEP = "perl ../System/Ensembl/ensembl-tools-release-84/scripts/variant_effect_predictor/variant_effect_predictor.pl -cache --force --no_stats --refseq --gmaf --hgvs --sift b --polyphen b --port 3337 --input_file "+inputfile+ " --output_file "+outputFile2
			os.system(commandVEP)
			################################################################################
			#Filtrage des variants
			################################################################################
			self.make_file_for_filter(file,REPERTORYVCF)
			if hotspot != "":
				filtre = VariantFilter(REPERTORYVCF,file)

			######
			#Ecriture rapport
			######
			
			report = open("../Report_"+i+".txt", "w")
			report.write("Report of "+i+".\n\n")
			if os.path.exists("../Results/"+REPERTORYVCF+"/temp/HSm_"+i+".vcf") == True:
				report.write("Hotspots mutés:\n")
				report.write("\n")
				File = "../Results/"+REPERTORYVCF+"/temp/HSm_"+i+".vcf"
				with open(File,'r') as file:
					file = file.readlines()
					for element in file:
						report.write(element)
					report.write("\n")
			if os.path.exists("../Results/"+REPERTORYVCF+"/temp/HSm_questionable_"+i+".vcf") == True:
				report.write("Hotspots mutés douteux:\n")
				report.write("\n")
				File = "../Results/"+REPERTORYVCF+"/temp/HSm_questionable_"+i+".vcf"
				with open(File,'r') as file:
					file = file.readlines()
					for element in file:
						report.write(element)
					report.write("\n")
			if os.path.exists("../Results/"+REPERTORYVCF+"/temp/nonMutatedHS_"+i+".vcf")== True:
				report.write("Hotspots non mutés:\n")
				report.write("\n")
				File = "../Results/"+REPERTORYVCF+"/temp/nonMutatedHS_"+i+".vcf"
				with open(File,'r') as file:
					file = file.readlines()
					for element in file:
						report.write(element)
					report.write("\n")
			if os.path.exists("../Results/"+REPERTORYVCF+"/temp/uncertain_mutation_"+i+".vcf")== True:
				report.write("Uncertain mutation (mutation douteuse):\n")
				report.write("\n")
				File = "../Results/"+REPERTORYVCF+"/temp/uncertain_mutation_"+i+".vcf"
				with open(File,'r') as file:
					file = file.readlines()
					for element in file:
						report.write(element)
					report.write("\n")
			if os.path.exists("../Results/"+REPERTORYVCF+"/temp/Polymorphism_"+i+".vcf")== True:
				report.write("Polymorphism:\n")
				report.write("\n")
				File = "../Results/"+REPERTORYVCF+"/temp/Polymorphism_"+i+".vcf"
				with open(File,'r') as file:
					file = file.readlines()
					for element in file:
						report.write(element)
					report.write("\n")
			if os.path.exists("../Results/"+REPERTORYVCF+"/temp/no_contributory_"+i+".vcf")== True:
				report.write("No contributory mutations (non contributif):\n")
				report.write("\n")
				File = "../Results/"+REPERTORYVCF+"/temp/no_contributory_"+i+".vcf"
				with open(File,'r') as file:
					file = file.readlines()
					for element in file:
						report.write(element)
					report.write("\n")
			if os.path.exists("../Results/"+REPERTORYVCF+"/temp/uncaracterized_mutations_"+i+".vcf")== True:
				report.write("Uncaracterized mutations (non filtrées):\n")
				report.write("\n")
				File = "../Results/"+REPERTORYVCF+"/temp/uncaracterized_mutations_"+i+".vcf"
				with open(File,'r') as file:
					file = file.readlines()
					for element in file:
						report.write(element)
					report.write("\n")
			report.close()
			fichier2 = open("../Report_"+i+".txt","r")
			content = fichier2.readlines()
			pyxl(i,REPERTORYVCF)

			
	def file_to_list(self,contentFile):
		"""Cree une liste contenant toutes les lignes du file .vcf.
		Chaque ligne est une liste composee d'elements (chrom,ID,position,etc)."""
		liste = []
		for ligne in contentFile:
			liste.append(ligne)
		liste2liste=[]
		for ligne in liste:
			lignesplit = ligne.split('\t')
			liste2liste.append(lignesplit)
		return liste2liste

	def legende_counter(self,contentFile):
		"""Count the number of legends in VCF file."""
		count=0
		for ligne in contentFile:
			if ligne[0]=="#":
				count += 1
			else:
				break
		return count

	def check_if_multiple_id(self,listOfList,ListdeNewLines):
		"""Regarde sur file original si plusieurs ID cosmic sur meme ligne
		si plusieurs ID, recupere les lignes separees dans ListdeNewLignes.
		Verifie en meme temps si la ligne correspond a une mutation et ajoute
		cette ligne dans une liste si c'est le cas. """
		contentNewVFC = []
		cmpt = 0
		for element in listOfList:
			ligne = element[4].split(",")
			if len(ligne) == 1:
				element = "\t".join(element)
				contentNewVFC.append(element)
			else:
				temp = []
				for element1 in ListdeNewLines[cmpt]:
					element1 = "\t".join(element1)
					contentNewVFC.append(element1)	
				cmpt += 1	
		return contentNewVFC
