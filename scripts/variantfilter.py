#!/usr/bin/python
# coding: utf-8 

"""Script qui filtre les variants trouves lors du sequençage. Differents filtres sont proposes
et peuvent etre modifies.

Ludovic KOSTHOWA (06/04/16)
Suite par Florent TESSIER (15/08/16)."""

import re,os

class VariantFilter:
	def __init__(self,REPERTORYVCF,file,RESULTDIR):
		self.REPERTORYVCF = REPERTORYVCF
		with open(RESULTDIR+"/"+self.REPERTORYVCF+"/temp/Results_"+file,'r') as File:
			self.sample = File.readlines()
		del self.sample[0]


	"""def parse_hs_file(self,hotspots):
		Parse la liste des hotspots fournie en entree.
		with open("liste_hotspot_temp.txt",'r') as hotspotsFile:
			hotspots = hotspotsFile.readlines()
		count = 0
		for ligne in hotspots:
			h = ligne.split("\t")
			if h[1] == "start":
				del hotspots[count]
			count += 1
		return hotspots"""

	def compare_hs(self,sample,file,RESULTDIR,hotspots):
		"""Compare les mutations de l'echantillon au fichier des hotspots d'interet."""
		#hotspots = self.parse_hs_file()
		outputFile = open(RESULTDIR+"/"+self.REPERTORYVCF+"/temp/HSm_"+file, 'w')
		outputFile.write("Gene\tposition\tExon-Intron\tRefSeq id\tHGVSc\tHGVSp\tcosmic ID\ttotal_cov\tvariant_cov\tallele_freq\tfunction\tsift\tpolyphen\tmaf\t\n")
		o_f_uncertain = open(RESULTDIR+"/"+self.REPERTORYVCF+"/temp/HSm_questionable_"+file, 'w')
		o_f_uncertain.write("Gene\tposition\tExon-Intron\tRefSeq id\tHGVSc\tHGVSp\tcosmic ID\ttotal_cov\tvariant_cov\tallele_freq\tfunction\tsift\tpolyphen\tmaf\t\n")
		suppList = []
		# If 0 = file is empty, if 1 file is not empty
		fileEmpty1 =True
		fileEmpty2=True
		for hsLine in hotspots:
			hsLineSplit = hsLine.split("\t")
			for sampleLigne in sample:
				sampleLigneReplace = sampleLigne.replace("\n","")
				sampleLigneReplace = sampleLigneReplace.replace("idCosmicNotFound"," ")
				sampleLigneReplace = sampleLigneReplace.replace("NA"," ")
				sampleLigneSplit = sampleLigneReplace.split("\t")
				temp = sampleLigneSplit[0].split(":")
				chrNumber = "chr" + temp[0]
				position = temp[1]
				cosmicNumber = sampleLigneSplit[6]
				hgvsp = sampleLigneSplit[5]
				if hsLineSplit[0] == chrNumber and int(hsLineSplit[1]) <= int(position) <= int(hsLineSplit[2]) and hsLineSplit[3] == sampleLigneSplit[1]: # and cosmicNumber in hsLineSplit[6] and sampleLigneSplit[4] in hsLineSplit[7]:
					HSm = sampleLigneSplit[1]+"\t"+sampleLigneSplit[0]+"\t"+sampleLigneSplit[14]+"\t"+sampleLigneSplit[2]+"\t"+sampleLigneSplit[4]+"\t"+sampleLigneSplit[5]+"\t"+sampleLigneSplit[6]+"\t"+sampleLigneSplit[7]+"\t"+sampleLigneSplit[8]+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\t"+sampleLigneSplit[12]+"\t"+sampleLigneSplit[13]+"\t"+sampleLigneSplit[11]+"\t\n"
					##HS douteux si nocall ou <25reads: 
					if sampleLigneSplit[7] != "DP_not_find":
						if sampleLigneSplit[15] == "NO CALL" or int(sampleLigneSplit[7]) < 25:
							if int(sampleLigneSplit[8]) !=0:
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
			os.remove(RESULTDIR+"/"+self.REPERTORYVCF+"/temp/HSm_"+file)
		if fileEmpty2:
			os.remove(RESULTDIR+"/"+self.REPERTORYVCF+"/temp/HSm_questionable_"+file)
		for supp in suppList:
			sample.remove(supp)

	def no_contributory(self,sample,file,RESULTDIR):
		"""Recherche parmis les mutations si elle est douteuse, cad si frequence allelique < 1 et couverture < 25 ou NOCALL."""
		outputFile = open(RESULTDIR+"/"+self.REPERTORYVCF+"/temp/no_contributory_"+file, 'w')
		outputFile.write("Gene\tposition\tExon-Intron\tRefSeq id\tHGVSc\tHGVSp\tcosmic ID\ttotal_cov\tvariant_cov\tallele_freq\tfunction\tsift\tpolyphen\tmaf\t\n")
		suppList = []
		# If 0 = file is empty, if 1 file is not empty
		fileEmpty = True
		for sampleLigne in sample:
			sampleLigneReplace = sampleLigne.replace("\n","")
			sampleLigneReplace = sampleLigneReplace.replace("idCosmicNotFound"," ")
			sampleLigneReplace = sampleLigneReplace.replace("NA"," ")
			sampleLigneSplit = sampleLigneReplace.split("\t")
			alleleCov = sampleLigneSplit[7]
			alleleFreq = sampleLigneSplit[9].replace("%","")
			if alleleCov != "DP_not_find":
				#Filtres pour determiner si mutation douteuse:
				# DP < 25 et allele_freq < 1
				if int(alleleCov) <= 25 and float(alleleFreq) < 1 or sampleLigneSplit[14] == "NO CALL":
					if int(sampleLigneSplit[8]) !=0:
						string = sampleLigneSplit[1]+"\t"+sampleLigneSplit[0]+"\t"+sampleLigneSplit[14]+"\t"+sampleLigneSplit[2]+"\t"+sampleLigneSplit[4]+"\t"+sampleLigneSplit[5]+"\t"+sampleLigneSplit[6]+"\t"+sampleLigneSplit[7]+"\t"+sampleLigneSplit[8]+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\t"+sampleLigneSplit[12]+"\t"+sampleLigneSplit[13]+"\t"+sampleLigneSplit[11]+"\t\n"
						outputFile.write(string)
						fileEmpty = False
					suppList.append(sampleLigne)
		if fileEmpty:
			os.remove(RESULTDIR+"/"+self.REPERTORYVCF+"/temp/no_contributory_"+file)
		for supp in suppList:
			sample.remove(supp)

	def find_polymorphism(self,sample,file,RESULTDIR):
		"""Recherche parmis les mutations si c'est un polymorphisme, cad si la minor allele frequency > 0.01."""
		outputFile = open(RESULTDIR+"/"+self.REPERTORYVCF+"/temp/Polymorphism_"+file, 'w')
		outputFile.write("Gene\tposition\tExon-Intron\tRefSeq id\tHGVSc\tHGVSp\tcosmic ID\ttotal_cov\tvariant_cov\tallele_freq\tfunction\tsift\tpolyphen\tmaf\t\n")
		# If 0 = file is empty, if 1 file is not empty
		fileEmpty = True
		suppList = []
		for sampleLigne in sample:
			sampleLigneReplace = sampleLigne.replace("\n","")
			sampleLigneReplace = sampleLigneReplace.replace("idCosmicNotFound"," ")
			sampleLigneReplace = sampleLigneReplace.replace("NA"," ")
			sampleLigneSplit = sampleLigneReplace.split("\t")
			maf = sampleLigneSplit[11]
			if maf != "NA":
				mafSplit = maf.split(":")
				mafValue = mafSplit[1]
				mafValue = float(mafValue)
				mafValue = "%.2f" % mafValue
				if float(mafValue) > 0.01:
					fileEmpty = False
					string = sampleLigneSplit[1]+"\t"+sampleLigneSplit[0]+"\t"+sampleLigneSplit[14]+"\t"+sampleLigneSplit[2]+"\t"+sampleLigneSplit[4]+"\t"+sampleLigneSplit[5]+"\t"+sampleLigneSplit[6]+"\t"+sampleLigneSplit[7]+"\t"+sampleLigneSplit[8]+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\t"+sampleLigneSplit[12]+"\t"+sampleLigneSplit[13]+"\t"+sampleLigneSplit[11]+"\t\n"
					outputFile.write(string)
					suppList.append(sampleLigne)
		if fileEmpty:
			os.remove(RESULTDIR+"/"+self.REPERTORYVCF+"/temp/Polymorphism_"+file)
		for supp in suppList:
			sample.remove(supp)


	def uncertain_mutation(self,sample,file,RESULTDIR):
		"""Mutations avec 25< couv < 300."""
		outputFile = open(RESULTDIR+"/"+self.REPERTORYVCF+"/temp/uncertain_mutation_"+file, 'w')
		outputFile.write("Gene\tposition\tExon-Intron\tRefSeq id\tHGVSc\tHGVSp\tcosmic ID\ttotal_cov\tvariant_cov\tallele_freq\tfunction\tsift\tpolyphen\tmaf\t\n")
		fileEmpty = True
		suppList = []
		for sampleLigne in sample:
			sampleLigneReplace = sampleLigne.replace("\n","")
			sampleLigneReplace = sampleLigneReplace.replace("idCosmicNotFound"," ")
			sampleLigneReplace = sampleLigneReplace.replace("NA"," ")
			sampleLigneSplit = sampleLigneReplace.split("\t")
			if sampleLigneSplit[7] != "DP_not_find" and int(sampleLigneSplit[8]) < 25:
				fileEmpty = False
				string = sampleLigneSplit[1]+"\t"+sampleLigneSplit[0]+"\t"+sampleLigneSplit[14]+"\t"+sampleLigneSplit[2]+"\t"+sampleLigneSplit[4]+"\t"+sampleLigneSplit[5]+"\t"+sampleLigneSplit[6]+"\t"+sampleLigneSplit[7]+"\t"+sampleLigneSplit[8]+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\t"+sampleLigneSplit[12]+"\t"+sampleLigneSplit[13]+"\t"+sampleLigneSplit[11]+"\t\n"
				outputFile.write(string)
				suppList.append(sampleLigne)
		if fileEmpty:
			os.remove(RESULTDIR+"/"+self.REPERTORYVCF+"/temp/uncertain_mutation_"+file)
		for supp in suppList:
			sample.remove(supp)

	def mutations(self,sample,file,RESULTDIR):
		"""Cree un fichier contenant toutes les mutations qui ne sont pas filtrees."""
		outputFile = open(RESULTDIR+"/"+self.REPERTORYVCF+"/temp/mutations_"+file, 'w')
		outputFile.write("Gene\tposition\tExon-Intron\tRefSeq id\tHGVSc\tHGVSp\tcosmic ID\ttotal_cov\tvariant_cov\tallele_freq\tfunction\tsift\tpolyphen\tmaf\t\n")
		if len(sample) != 0:
			for sampleLigne in sample:
				sampleLigneReplace = sampleLigne.replace("\n","")
				sampleLigneReplace = sampleLigneReplace.replace("idCosmicNotFound"," ")
				sampleLigneReplace = sampleLigneReplace.replace("NA"," ")
				sampleLigneSplit = sampleLigneReplace.split("\t")
				string = sampleLigneSplit[1]+"\t"+sampleLigneSplit[0]+"\t"+sampleLigneSplit[14]+"\t"+sampleLigneSplit[2]+"\t"+sampleLigneSplit[4]+"\t"+sampleLigneSplit[5]+"\t"+sampleLigneSplit[6]+"\t"+sampleLigneSplit[7]+"\t"+sampleLigneSplit[8]+"\t"+sampleLigneSplit[9]+"\t"+sampleLigneSplit[10]+"\t"+sampleLigneSplit[12]+"\t"+sampleLigneSplit[13]+"\t"+sampleLigneSplit[11]+"\t\n"
				outputFile.write(string)
		else:
			os.remove(RESULTDIR+"/"+self.REPERTORYVCF+"/temp/mutations_"+file)
