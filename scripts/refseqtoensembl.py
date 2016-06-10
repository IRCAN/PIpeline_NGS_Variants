import re

"""
Script qui idEnsembleFind les equivalences entre identifiants RefSeq et identifiants Ensembl puis compare
les identifiants Ensembl à ceux de Cosmic afin d'obtenir diverses informations.

Ludovic KOSTHOWA (Debut : 06/04/16)
Info: Creation en cours, script peut etre modifie a tout moment.
"""

class RefseqToEnsembl:
	def __init__(self):
		self.cosmicDict = {}
		self.gene2ensemblFinalDic = {}
		self.dicoPanel = {}
		self.parse_gene2ensembl()
		self.parse_cosmic_lite()

	def make_file_for_filter(self,file,REPERTORYVCF):
		"""Parse le file de sortie de VEP et cree un nouveau file avec les lignes qui match avec les ID ensembl."""
		File = "../Resultats/"+REPERTORYVCF+"/VEP/VEP_"+file
		with open(File,'r') as vepFile0:
			vepFile = vepFile0.readlines()
		tempList = []
		vcfFileFinalList = []
		vcfFileFinalList.append("gene\tgene Id\tRefSeq id\tTranscript\tHGVSc\tHGVSp\tcosmic ID\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
		idNotFindList = []
		mutationsFile = self.parse_mutations_file(file,REPERTORYVCF)
		####
		#Recherche si correspondance entre ID refseq de gene2ensembl avec ID refseq du file VEP
		####
		File = "../System/Cosmic/Cosmic_lite.txt"
		with open(File,'r') as cosmic0:
			cosmic=cosmic0.readlines()
		self.create_dico_panel()
		"""Verifie si id refseq de vep est dans le panel de genes.
		si il y est, on le met dans une liste temporaire."""
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

		"""liste temporaire qui ne contient que les lignes dont id refseq sont dans le panel.
		Pour chaque ligne, on recupere les informations puis on cree un file qui servira a filtrer les variants."""
		for ligne in tempList:
			ligneSplit = ligne.split("\t")
			idRefseq = ligneSplit[4]
			chromPos = ligneSplit[1].split(":")
			chrom = "chr" + chromPos[0]
			pos = chromPos[1]
			function = ligneSplit[6]
			ligneInfoVcf = ligneSplit[13]
			geneId = ligneSplit[14].replace("\n","")
				#Si correspondance entre les ID
			idEnsembleFind = False
			if idRefseq in self.gene2ensemblFinalDic:
				idEnsembleFind = True
			#Recuperation du HGVSc
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
			#Recuperation du HGVSp
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
			#Recuperation de la MAF
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
			#Recuperation du SIFT
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
			#Recuperation du Polyphen
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
			#Creation de la string resume
			if "-" in ligneSplit[1]:
				temp = pos.split("-")
				position = temp[0]
			else:
				position = pos
			consequence = ligneSplit[6]
			chromPosVcf = chrom + "\t" + position
			
			if idEnsembleFind:
				idEnsembl = self.gene2ensemblFinalDic[idRefseq]
				string = chromPos[0]+":"+position + "\t"+ geneId +"\t" + idRefseq + "\t" + idEnsembl + "\t" + HGVSc + "\t" + HGVSp + "\tidCosmicNotFound\tcov_not_find\tfreq_not_find\t"+ function + "\t" + MAF + "\t" + SIFT + "\t" +PolyPhen + "\t"+ "NO-NOCALL" + "\n"
			else:
				string = chromPos[0]+":"+position + "\t"+ geneId +"\t" + idRefseq + "\t" + "NA" + "\t" + HGVSc + "\t" + HGVSp + "\tidCosmicNotFound\tcov_not_find\tfreq_not_find\t"+ function + "\t" + MAF + "\t" + SIFT + "\t" +PolyPhen + "\t"+ "NO-NOCALL" + "\n"
			####
			#Comparaison avec les lignes de MUTATIONS pour récupérer les couvertures
			####
			for mutation in mutationsFile:
				if mutation[0]!="#":
					mutationSplit = mutation.split("\t")
					chromPosMutation = mutationSplit[0]+"\t"+mutationSplit[1]
					if chromPosMutation == chromPosVcf:
						alleleCov = self.get_allele_cov(mutationSplit[7])
						alleleFreq = self.get_allele_freq(mutationSplit[7])
						string = string.replace("cov_not_find",alleleCov)
						string = string.replace("freq_not_find",alleleFreq+"%")
						if mutationSplit[6] == "NOCALL":
							string = string.replace("NO-NOCALL","NO CALL")
			####
			#Recuperation identifiant COSMIC
			####
			if idEnsembleFind:
				idEnsembl = self.gene2ensemblFinalDic[idRefseq]
				infoCosmic = self.cosmicDict.get(idEnsembl)
				if infoCosmic != None:
					for i in infoCosmic:
						infoCosmicSplit = i.split("\t")
						if infoCosmicSplit[5] == HGVSc:
							string = string.replace("idCosmicNotFound",infoCosmicSplit[4])
			vcfFileFinalList.append(string)
		self.output_file("../Resultats/"+REPERTORYVCF+"/temp/resultats_"+file,vcfFileFinalList)

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
		########################################################
		#Creation dictionnaire cosmic DB (key = ENST)
		########################################################
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
################TODO: modifier les i,j et continuer traduction
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

	def parse_mutations_file(self,file,REPERTORYVCF):
		File = "../Resultats/"+REPERTORYVCF+"/VariantCaller/MUTATIONS_"+file
		with open(File,'r') as mutationsFile0:
			mutationsFile=mutationsFile0.readlines()
		return mutationsFile

	def get_allele_cov(self,string):
		match = re.search(r"(AO)=[0-9]*", string)
		resultat = match.group(0)
		#Supprime le "FAO="
		resultat = resultat[3:]
		return(resultat)

	def get_allele_freq(self,string):
	############################################
	#TODO Modifier AF par DP et récupérer le nombre total de reads pour calculer la fréquence
	############################################
		match = re.search(r"(AF)=\d*.\d*;", string)
		resultat = match.group(0)
	#Supprime le "AF="
		resultat = resultat.replace(";","")
		resultat = float(resultat[3:])
		resultat = resultat*100
		resultat = "%.1f" % resultat
		return(resultat)

	def create_dico_panel(self):
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

