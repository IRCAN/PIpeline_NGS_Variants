#!/usr/bin/python
# coding: utf-8 

"""Script qui filtre les variants trouves lors du sequençage. Differents filtres sont proposes
et peuvent etre modifies.

Ludovic KOSTHOWA (06/04/16)
Info: Creation en cours, script peut etre modifie a tout moment."""

import re,os

class VariantFilter:
	def __init__(self,REPERTORYVCF,file):
		############################
		############################
		############################
		# TODO :Commentaire sur la fonction
		############################
		############################
		############################
		self.REPERTORYVCF = REPERTORYVCF
		with open("../Results/"+self.REPERTORYVCF+"/temp/Results_"+file,'r') as File:
			sample = File.readlines()
		del sample[0]
		self.compare_hs(sample,file)
		self.uncertain_mutation(sample,file)
		self.find_polymorphism(sample,file)
		self.no_contributory(sample,file)
		self.uncaracterized_mutations(sample,file)


	def parse_hs_file(self):
		############################
		############################
		############################
		# TODO :Commentaire sur la fonction
		############################
		############################
		############################
		with open("liste_hotspot_temp.txt",'r') as hotspotsFile:
			hotspots = hotspotsFile.readlines()
		count = 0
		for ligne in hotspots:
			h = ligne.split()
			if h[1] == "start":
				del hotspots[count]
			count += 1
		return hotspots

	def compare_hs(self,sample,file):
		"""Compare les mutations de l'echantillon au fichier des hotspots d'interet."""
		hotspots = self.parse_hs_file()
		outputFile = open("../Results/"+self.REPERTORYVCF+"/temp/HSm_"+file, 'w')
		outputFile.write("gene\texon\ttranscript\tcoding\tprotein\tcosmic\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
		o_f_uncertain = open("../Results/"+self.REPERTORYVCF+"/temp/HSm_questionable_"+file, 'w')
		o_f_uncertain.write("gene\texon\tRefSeq id\tTranscript\tHGVSc\tHGVSp\tcosmic ID\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
		suppList = []
		# If 0 = file is empty, if 1 file is not empty
		fileEmpty1 =True
		fileEmpty2=True
		for hsLine in hotspots:
			hsLineSplit = hsLine.split("\t")
			for sampleLigne in sample:
				sampleLigneReplace = sampleLigne.replace("\n","")
				sampleLigneSplit = sampleLigneReplace.split("\t")
				temp = sampleLigneSplit[0].split(":")
				chrNumber = "chr" + temp[0]
				position = temp[1]
				cosmicNumber = sampleLigneSplit[6]#.replace("COSM","")
				hgvsp = sampleLigneSplit[5]
				if hsLineSplit[0] == chrNumber and int(hsLineSplit[1]) <= int(position) <= int(hsLineSplit[2]) and hsLineSplit[3] == sampleLigneSplit[1]: # and cosmicNumber in hsLineSplit[6] and sampleLigneSplit[4] in hsLineSplit[7]:
					HSm = sampleLigneSplit[1]+"\t"+hsLineSplit[4]+"\t"+sampleLigneSplit[2]+"\t"+sampleLigneSplit[3]+"\t"+sampleLigneSplit[4]+"\t"+hgvsp+"\t"+cosmicNumber+"\t"+sampleLigneSplit[7]+"\t"+sampleLigneSplit[8]+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\t"+sampleLigneSplit[11]+"\t"+sampleLigneSplit[12]+"\n"
					##HS douteux si nocall ou <25reads: 
					if sampleLigneSplit[7] != "cov_not_find":
						if sampleLigneSplit[13] == "NO CALL" or int(sampleLigneSplit[7]) < 25:
							o_f_uncertain.write(HSm)
							fileEmpty2 = False
						else:
							fileEmpty1 = False
							outputFile.write(HSm)
					else:
						o_f_uncertain.write(HSm)
						fileEmpty2 = False
					suppList.append(sampleLigne)
		if fileEmpty1:
			os.remove("../Results/"+self.REPERTORYVCF+"/temp/HSm_"+file)
		if fileEmpty2:
			os.remove("../Results/"+self.REPERTORYVCF+"/temp/HSm_questionable_"+file)
		for supp in suppList:
			sample.remove(supp)

	def uncertain_mutation(self,sample,file):
		"""Recherche parmis les mutations si elle est douteuse, cad si frequence allelique < 1 et couverture < 25."""
		outputFile = open("../Results/"+self.REPERTORYVCF+"/temp/uncertain_mutation_"+file, 'w')
		outputFile.write("gene\tposition\tRefSeq id\tTranscript\tHGVSc\tHGVSp\tcosmic ID\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
		suppList = []
		# If 0 = file is empty, if 1 file is not empty
		fileEmpty = True
		for sampleLigne in sample:
			sampleLigneReplace = sampleLigne.replace("\n","")
			sampleLigneSplit = sampleLigneReplace.split("\t")
			alleleCov = sampleLigneSplit[7]
			alleleFreq = sampleLigneSplit[8].replace("%","")
			if alleleCov != "cov_not_find":
				#Filtres pour determiner si mutation douteuse:
				# allele_cov < 25 et allele_freq < 1
				if int(alleleCov) <= 25 and float(alleleFreq) < 1 or sampleLigneSplit[13] == "NO CALL":
					string = sampleLigneSplit[1]+"\t"+sampleLigneSplit[0]+"\t"+sampleLigneSplit[2]+"\t"+sampleLigneSplit[3]+"\t"+sampleLigneSplit[4]+"\t"+sampleLigneSplit[5]+"\t"+sampleLigneSplit[6]+"\t"+sampleLigneSplit[7]+"\t"+sampleLigneSplit[8]+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\t"+sampleLigneSplit[11]+"\t"+sampleLigneSplit[12]+"\n"
					outputFile.write(string)
					suppList.append(sampleLigne)
					fileEmpty = False
		if fileEmpty:
			os.remove("../Results/"+self.REPERTORYVCF+"/temp/uncertain_mutation_"+file)
		for supp in suppList:
			sample.remove(supp)

	def find_polymorphism(self,sample,file):
		"""Recherche parmis les mutations si c'est un polymorphisme, cad si la minor allele frequency > 0.01."""
		outputFile = open("../Results/"+self.REPERTORYVCF+"/temp/Polymorphism_"+file, 'w')
		outputFile.write("gene\tposition\tRefSeq id\tTranscript\tHGVSc\tHGVSp\tcosmic ID\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
		# If 0 = file is empty, if 1 file is not empty
		fileEmpty = True
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
					fileEmpty = False
					string = sampleLigneSplit[1]+"\t"+sampleLigneSplit[0]+"\t"+sampleLigneSplit[2]+"\t"+sampleLigneSplit[3]+"\t"+sampleLigneSplit[4]+"\t"+sampleLigneSplit[5]+"\t"+sampleLigneSplit[6]+"\t"+sampleLigneSplit[7]+"\t"+sampleLigneSplit[8]+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\t"+sampleLigneSplit[11]+"\t"+sampleLigneSplit[12]+"\n"
					outputFile.write(string)
					suppList.append(sampleLigne)
		if fileEmpty:
			os.remove("../Results/"+self.REPERTORYVCF+"/temp/Polymorphism_"+file)
		for supp in suppList:
			sample.remove(supp)

	def uncaracterized_mutations(self,sample,file):
		"""Cree un fichier contenant toutes les mutations qui ne sont pas categorisees."""
		outputFile = open("../Results/"+self.REPERTORYVCF+"/temp/uncaracterized_mutations_"+file, 'w')
		outputFile.write("gene\tposition\tRefSeq id\tTranscript\tHGVSc\tHGVSp\tcosmic ID\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
		if len(sample) != 0:
			for sampleLigne in sample:
				sampleLigneReplace = sampleLigne.replace("\n","")
				sampleLigneSplit = sampleLigneReplace.split("\t")
				string = sampleLigneSplit[1]+"\t"+sampleLigneSplit[0]+"\t"+sampleLigneSplit[2]+"\t"+sampleLigneSplit[3]+"\t"+sampleLigneSplit[4]+"\t"+sampleLigneSplit[5]+"\t"+sampleLigneSplit[6]+"\t"+sampleLigneSplit[7]+"\t"+sampleLigneSplit[8]+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\t"+sampleLigneSplit[11]+"\t"+sampleLigneSplit[12]+"\n"
				outputFile.write(string)
		else:
			os.remove("../Results/"+self.REPERTORYVCF+"/temp/uncaracterized_mutations_"+file)

	def no_contributory(self,sample,file):
		"""Cree un fichier contenant toutes les mutations qui ne sont pas categorisees."""
		outputFile = open("../Results/"+self.REPERTORYVCF+"/temp/no_contributory_"+file, 'w')
		outputFile.write("gene\tposition\tRefSeq id\tTranscript\tHGVSc\tHGVSp\tcosmic ID\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
		fileEmpty = True
		suppList = []
		for sampleLigne in sample:
			sampleLigneReplace = sampleLigne.replace("\n","")
			sampleLigneSplit = sampleLigneReplace.split("\t")
			if sampleLigneSplit[7] != "cov_not_find" and int(sampleLigneSplit[7]) < 300:
				fileEmpty = False
				string = sampleLigneSplit[1]+"\t"+sampleLigneSplit[0]+"\t"+sampleLigneSplit[2]+"\t"+sampleLigneSplit[3]+"\t"+sampleLigneSplit[4]+"\t"+sampleLigneSplit[5]+"\t"+sampleLigneSplit[6]+"\t"+sampleLigneSplit[7]+"\t"+sampleLigneSplit[8]+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\t"+sampleLigneSplit[11]+"\t"+sampleLigneSplit[12]+"\n"
				outputFile.write(string)
				suppList.append(sampleLigne)
		if fileEmpty:
			os.remove("../Results/"+self.REPERTORYVCF+"/temp/no_contributory_"+file)
		for supp in suppList:
			sample.remove(supp)