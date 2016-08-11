#!/usr/bin/python
# coding: utf-8 

"""
Script qui idEnsembleFind les equivalences entre identifiants RefSeq et identifiants Ensembl puis compare
les identifiants Ensembl à ceux de Cosmic afin d'obtenir diverses informations.
Ludovic KOSTHOWA (Debut : 06/04/16)
Suite par Florent TESSIER (15/08/16).
"""

###############
##TODO: Modfier la creation du dictionnaire du panel
###############

import re

class RefseqToEnsembl:
	def __init__(self):
		"""initiation des dictionnaires, parsing des bdd"""
		self.cosmicDict = {}
		self.gene2ensemblFinalDic = {}
		self.dicoPanel = {}
		self.parse_gene2ensembl()
		self.parse_cosmic_lite()

	def make_file_for_filter(self,file,REPERTORYVCF, RESULTDIR):
		"""Parse le file de sortie de VEP et cree un nouveau file avec les lignes qui match avec les ID ensembl."""
		File =  RESULTDIR+"/"+REPERTORYVCF+"/VEP/VEP_"+file
		with open(File,'r') as vepFile0:
			vepFile = vepFile0.readlines()
		tempList = []
		vcfFileFinalList = []
		vcfFileFinalList.append("gene\tgene Id\tRefSeq id\tTranscript\tHGVSc\tHGVSp\tcosmic ID\tDP\tFAO\tallele_freq\tfunction\tmaf\tsift\tpolyphen\texon ou intron\n")
		idNotFindList = []
		mutationsFile = self.parse_mutations_file(file,REPERTORYVCF, RESULTDIR)
		################################################################################
		#Recherche si correspondance entre ID refseq de gene2ensembl avec ID refseq du fichier VEP
		################################################################################
		File = "../System/Cosmic/Cosmic_lite.txt"
		with open(File,'r') as cosmic0:
			cosmic=cosmic0.readlines()
		self.create_dico_panel()
		#Verifie si id refseq de vep est dans le panel de genes si il y est, on le met dans une liste temporaire.
		for ligne in vepFile:
			if ligne[0]!="#":
				#Supprime le retour a la ligne
				ligne = ligne[0:len(ligne)-1]
				ligneSplit = ligne.split("\t")
				idRefseqSample = ligneSplit[4]
				match = re.search(r"[A-Z]*_[0-9]*.", idRefseqSample)
				if match != None:
					#enleve . pour correpsondre avec dico
					idRefseqSample = match.group(0)[:-1]
				for key in self.dicoPanel.keys():
					keyWithoutPoint = key
					if "." in key:
						keyWithoutPoint = key.split(".")
						keyWithoutPoint = keyWithoutPoint[0]
					if idRefseqSample == keyWithoutPoint:
						temp = self.dicoPanel[key].split("\t")
						tempList.append(ligne+"\t"+temp[0]+"\n")

		#liste temporaire qui ne contient que les lignes dont id refseq sont dans le panel. Pour chaque ligne, on recupere les informations puis on cree un file qui servira a filtrer les variants.
		for ligne in tempList:
			ligneSplit = ligne.split("\t")
			idRefseq = ligneSplit[4]
			chromPos = ligneSplit[1].split(":")
			chrom = "chr" + chromPos[0]
			pos = chromPos[1]
			function = ligneSplit[6]
			ligneInfoVcf = ligneSplit[13]
			geneId = ligneSplit[14].replace("\n","")
			idEnsembleFind = False
			if idRefseq in self.gene2ensemblFinalDic:
				idEnsembleFind = True
			################################################################################
			#Recuperation du HGVSc
			################################################################################
			regexHGVSc = "HGVSc=" + idRefseq + ":(.*)"
			matchHGVSc = re.search(regexHGVSc, ligneInfoVcf)
			if matchHGVSc == None: 
				HGVSc = "NA"
			else: 
				temp = matchHGVSc.group(0)
				tempSplit = temp.split(";")
				tempSplit = tempSplit[0]
				tempSplit = tempSplit.split(":")
				HGVSc = tempSplit[1]
			################################################################################
			#Recuperation du HGVSp
			################################################################################
			regexHGVSp = "HGVSp=(.*)"
			matchHGVSp = re.search(regexHGVSp, ligneInfoVcf)
			if matchHGVSp == None: 
				HGVSp = "NA"
			else: 
				HGVSpTemp = matchHGVSp.group(0)
				HGVSpTemp = HGVSpTemp.split(";")
				HGVSpTemp = HGVSpTemp[0]
				HGVSpTemp = HGVSpTemp.split(":")
				HGVSp = HGVSpTemp[1]
			################################################################################
			#Recuperation de la MAF
			################################################################################
			regexMAF = "GMAF=.*"
			matchMAF = re.search(regexMAF, ligneInfoVcf)
			if matchMAF == None :
				MAF = "NA"
			else:
				MAFTemp = matchMAF.group(0)
				if ";" in MAFTemp:
					MAFTemp = MAFTemp.split(";")
					MAFTemp = MAFTemp[0]
					MAFTemp = MAFTemp.split("=")
					MAF = MAFTemp[1]
				else:
					MAFTemp = MAFTemp.split("=")
					MAF = MAFTemp[1]
			################################################################################
			#Recuperation du SIFT
			################################################################################
			regexSift = "SIFT=(.*);"
			matchSift = re.search(regexSift, ligneInfoVcf)
			if matchSift == None: SIFT = "NA"
			else: 
				SIFTTemp = matchSift.group(0)
				if ";" in SIFTTemp:
					SIFTTemp = SIFTTemp.split(";")
					SIFTTemp = SIFTTemp[0]
					SIFTTemp = SIFTTemp.split("=")
					SIFT = SIFTTemp[1]
				else:
					SIFTTemp = SIFTTemp.split("=")
					SIFT = SIFTTemp[1]
			################################################################################
			#Recuperation du Polyphen
			################################################################################
			regexPolyphen = "PolyPhen=(.*);"
			matchPolyphen = re.search(regexPolyphen, ligneInfoVcf)
			if matchPolyphen == None: PolyPhen = "NA"
			else: 
				PolyPhenTemp = matchPolyphen.group(0)
				if ";" in PolyPhenTemp:
					PolyPhenTemp = PolyPhenTemp.split(";")
					PolyPhenTemp = PolyPhenTemp[0]
					PolyPhenTemp = PolyPhenTemp.split("=")
					PolyPhen = PolyPhenTemp[1]
				else:
					PolyPhenTemp = PolyPhenTemp.split("=")
					PolyPhen = PolyPhenTemp[1]
			################################################################################
			#Recuperation du EXON
			################################################################################
			regexExon = "EXON=[0-9]*\/[0-9]*;"
			matchExon = re.search(regexExon, ligneInfoVcf)
			if matchExon == None:
				regexIntron = "INTRON=[0-9]*\/[0-9]*;"
				matchIntron = re.search(regexIntron, ligneInfoVcf)
				if matchIntron == None: 
					Exon = "NA"
				else: 
					temp = matchIntron.group(0)
					tempSplit = temp.split(";")
					tempSplit = tempSplit[0]
					Exon = tempSplit
			else: 
				temp = matchExon.group(0)
				tempSplit = temp.split(";")
				tempSplit = tempSplit[0]
				Exon = tempSplit
			################################################################################
			#Creation de la string resume
			################################################################################
			if "-" in ligneSplit[1]:
				temp = pos.split("-")
				position = temp[0]
			else:
				position = pos
			consequence = ligneSplit[6]
			chromPosVcf = chrom + "\t" + position
			if idEnsembleFind:
				idEnsembl = self.gene2ensemblFinalDic[idRefseq]
				string = chromPos[0]+":"+position + "\t"+ geneId +"\t" + idRefseq + "\t" + idEnsembl + "\t" + HGVSc + "\t" + HGVSp + "\tidCosmicNotFound\tDP_not_find\tFAO_not_find\tfreq_not_find\t"+ function + "\t" + MAF + "\t" + SIFT + "\t" +PolyPhen + "\t"+ Exon +"\t"+ "NO-NOCALL" + "\n"
			else:
				string = chromPos[0]+":"+position + "\t"+ geneId +"\t" + idRefseq + "\t" + "NA" + "\t" + HGVSc + "\t" + HGVSp + "\tidCosmicNotFound\tDP_not_find\tFAO_not_find\tfreq_not_find\t"+ function + "\t" + MAF + "\t" + SIFT + "\t" +PolyPhen + "\t"+ Exon +"\t"+ "NO-NOCALL" + "\n"
			################################################################################
			#Comparaison avec les lignes de MUTATIONS pour récupérer les couvertures
			################################################################################
			Continue=True
			for mutation in mutationsFile:
				if mutation[0]!="#":
					mutationSplit = mutation.split("\t")
					recalculPosition=0
					#calcul des positions si del
					if "del" in HGVSc:
						HGV=HGVSc.split("del")
						if "ins" in HGV[1]:
							recupLen=HGV[1].split("ins")
							recalculPosition=len(recupLen[-2]) -len(recupLen[-1])
						else:
							recalculPosition=len(HGV[-1])
					chromPosMutation = mutationSplit[0]+"\t"+mutationSplit[1]

					chromPosMutationSplit=chromPosMutation.split()
					chromPosVcfSplit=chromPosVcf.split()
					if (chromPosMutationSplit[0] == chromPosVcfSplit[0]) and (int(chromPosMutationSplit[1]) == (int(chromPosVcfSplit[1]) - int(recalculPosition))) and Continue:
						#DP = self.get_DP(mutationSplit[7])
						FRO= self.get_FRO(mutationSplit[7])
						FAO = self.get_FAO(mutationSplit[7])
						DP=int(FAO)+int(FRO)
						alleleFreq=int(FAO)/(int(FAO)+int(FRO))
						alleleFreq = alleleFreq * 100
						alleleFreq = "%.2f" % alleleFreq
						#alleleFreq = self.get_allele_freq(mutationSplit[7])
						string = string.replace("DP_not_find",str(DP))
						string = string.replace("FAO_not_find",str(FAO))
						string = string.replace("freq_not_find",str(alleleFreq)+"%")
						if mutationSplit[6] == "NOCALL":
							string = string.replace("NO-NOCALL","NO CALL")
						Continue=False

					elif (chromPosMutationSplit[0] == chromPosVcfSplit[0]) and (int(chromPosMutationSplit[1]) == (int(chromPosVcfSplit[1])-1)) and Continue:
						#DP = self.get_DP(mutationSplit[7])
						FRO= self.get_FRO(mutationSplit[7])
						FAO = self.get_FAO(mutationSplit[7])
						alleleFreq=int(FAO)/(int(FAO)+int(FRO))
						alleleFreq=int(FAO)/(int(FAO)+int(FRO))
						alleleFreq = alleleFreq * 100
						alleleFreq = "%.2f" % alleleFreq
						#alleleFreq = self.get_allele_freq(mutationSplit[7])
						string = string.replace("DP_not_find",str(DP))
						string = string.replace("FAO_not_find",str(FAO))
						string = string.replace("freq_not_find",str(alleleFreq)+"%")
						if mutationSplit[6] == "NOCALL":
							string = string.replace("NO-NOCALL","NO CALL")

			if "del" in HGVSc:
				newPosition = int(position)
				newPosition = newPosition-1
				string = string.replace(position,str(newPosition))			
			################################################################################
			#Recuperation identifiant COSMIC
			################################################################################
			if idEnsembleFind:
				idEnsembl = self.gene2ensemblFinalDic[idRefseq]
				infoCosmic = self.cosmicDict.get(idEnsembl)
				if infoCosmic != None:
					for i in infoCosmic:
						infoCosmicSplit = i.split("\t")
						if infoCosmicSplit[5] == HGVSc:
							string = string.replace("idCosmicNotFound",infoCosmicSplit[4])
			vcfFileFinalList.append(string)
		self.output_file( RESULTDIR+"/"+REPERTORYVCF+"/temp/Results_"+file,vcfFileFinalList)

	def parse_gene2ensembl(self):
		"""Parse le file de correlation RefSeq vers Ensembl."""
		File = "../System/Ensembl/gene2ensembl.txt"
		with open(File,'r') as gene2ensembl0:
			gene2ensembl = gene2ensembl0.readlines()
		print('Parsing de la table de correlation Refseq to Ensembl en cours...')
		for line in gene2ensembl:
			line = line.replace(",","\t")
			ligne = line.split()	
			self.gene2ensemblFinalDic[ligne[3]] = ligne[4]
		print('Parsing OK')

	def parse_cosmic_lite(self):
		"""Parse le file DB Cosmic_lite et cree un dictionnaire:
		key = ID_ensembl
		valeur = contenu de la (ou les) ligne(s) correspondant(s) à la key."""
		print('Parsing de la DB Cosmic lite en cours...')
		File = "../System/Cosmic/Cosmic_lite.txt"
		with open(File,'r') as cosmic0:
			cosmic = cosmic0.readlines()
		idEnsemblFromCosmic = ""
		################################################################################
		#Creation dictionnaire cosmic DB (key = ENST)
		################################################################################
		for cosmicLigne in cosmic:
			cosmicLigne = cosmicLigne.replace("\n","")
			cosmicLigneSplit = cosmicLigne.split("\t")
			idEnsemblFromCosmic = cosmicLigneSplit[1]
			#Si la key n'est pas dans le dictionnaire je la cree
			if idEnsemblFromCosmic not in self.cosmicDict:
				self.cosmicDict[idEnsemblFromCosmic] = []
				self.cosmicDict[idEnsemblFromCosmic].append(cosmicLigne)
			#sinon j'ajoute la ligne dans la liste de la key
			else:
				self.cosmicDict[idEnsemblFromCosmic].append(cosmicLigne)
		print('Parsing OK')

	def output_file(self,FileName, finalList,legendList=""):
		"""Cree un file resultat et ecrit dans ce file."""
		fileName = FileName
		File = open(fileName,'w')	# creation et ouverture du File
		for legende in legendList:		#ecriture de la legende
			legende = "".join(legende)
			File.write(str(legende))
		for line in finalList:	#ecriture des donnees
			File.write(str(line))
		File.close()

	def parse_mutations_file(self,file,REPERTORYVCF,RESULTDIR):
		"""Parse le fichier contenant toutes les mutations présentes dans l'echantillon."""
		File =  RESULTDIR+"/"+REPERTORYVCF+"/VariantCaller/MUTATIONS_"+file
		with open(File,'r') as mutationsFile0:
			mutationsFile=mutationsFile0.readlines()
		return mutationsFile

	def get_DP(self,string):
		"""Recupere la profondeur totale pour chaque mutations."""
		match = re.search(r"(DP)=[0-9]*", string)
		resultat = match.group(0)
		#Supprime le "FAO="
		resultat = resultat[3:]
		return(resultat)

	def get_FRO(self,string):
		"""Recupere la profondeur totale pour chaque mutations."""
		match = re.search(r"(FRO)=[0-9]*", string)
		resultat = match.group(0)
		#Supprime le "FAO="
		resultat = resultat[4:]
		return(resultat)

	def get_FAO(self,string):
		"""Recupere le nombre d'allèles mutés pour chaque mutations."""
		match = re.search(r"(FAO)=[0-9]*", string)
		resultat = match.group(0)
		#Supprime le "FAO="
		resultat = resultat[4:]
		return(resultat)



	def get_allele_freq(self,string):
		"""Recupere la frequence allelique pour chaque mutations de l'echantillon."""

		matchFAO = re.search(r"FAO=\d*;", string)
		matchDP = re.search(r"DP=\d*;", string)
		alleleObservation = matchFAO.group(0)
		alleleObservation = alleleObservation.replace(";","")
		alleleObservation = alleleObservation.split("=")
		alleleObservation = alleleObservation[1]
		alleleObservation = int(alleleObservation)
		totalReads = matchDP.group(0)
		totalReads = totalReads.replace(";","")
		totalReads = totalReads.split("=")
		totalReads = totalReads[1]
		totalReads = int(totalReads)
		alleleFreq = alleleObservation / totalReads
		alleleFreq = alleleFreq * 100
		alleleFreq = "%.2f" % alleleFreq
		return(alleleFreq)


	def create_dico_panel(self):
		"""Cree un dictionnaire contenant tout les identifiants RefSeq su panel."""
		#############################
		#############################
		#CHEMIN A MODIFIER
		#############################
		#############################
		File = "../Personal_Data/Panel/liste transcrit panel CHP2-CLv2 25-5-16-2.csv"
		with open(File,'r') as panel0:
			panel=panel0.readlines()
		for i in panel:
			panelSplit = i.split("\t")
			if "_ENST" not in panelSplit[0]:
				idRefseqPanel = panelSplit[1]
				if "NM_" in idRefseqPanel:
					idRefseqPanel = str(idRefseqPanel)
					self.dicoPanel[idRefseqPanel] = i

