#!/usr/bin/python3
# coding: utf-8 
import re

"""
Script qui trouve les equivalences entre identifiants RefSeq et identifiants Ensembl puis compare
les identifiants Ensembl à ceux de Cosmic afin d'obtenir diverses informations.

Ludovic KOSTHOWA (Debut : 06/04/16)
Info: Creation en cours, script peut etre modifie a tout moment.
"""
#Variables
CosmicDict = {}
gene2ensemblFinalDic = {}
dicoPanel = {}

def read_file(File):
	"""Ouvre et lit le fichier .vcf de chaque patients."""
	contentFile = File.readlines()
	File.close() 
	return contentFile
def output_file(FileName, Final_List):
	"""Cree un fichier resultat et ecrit dans ce fichier."""
	NomFile = FileName
	File = open(NomFile,'w')
	for i in Final_List:
		File.write(str(i))
	File.close()
def parse_gene2ensembl():
	"""Parse le fichier de correlation RefSeq vers Ensembl."""
	File = "../Data/Ensembl/gene2ensembl.txt"
	gene2ensembl = open(File,'r')
	gene2ensembl = read_file(gene2ensembl)
	print('Parsing de la table de correlation Refseq to Ensembl en cours...')
	for ligne in gene2ensembl:
		ligne = ligne.split(",")
		gene2ensemblFinalDic[ligne[3]] = ligne[4]
		#gene2ensemblFinalDic.append(ligne)
	print('Parsing OK')
def parse_cosmic_lite():
	"""Parse le fichier DB Cosmic_lite et cree un dictionnaire:
	cle = ID_ensembl
	valeur = contenu de la (ou les) ligne(s) correspondant(s) à la cle."""
	print('Parsing de la DB Cosmic lite en cours...')
	File = "../Data/Cosmic/Cosmic_lite.txt"
	cosmic = open(File,"r")
	cosmic = read_file(cosmic)
	idEnsemblFromCosmic = ""
	########################################################
	#Creation dictionnaire cosmic DB (cle = ENST)
	########################################################
	for cosmicLigne in cosmic:
		cosmicLigne = cosmicLigne.replace("\n","")
		cosmicLigneSplit = cosmicLigne.split("\t")
		idEnsemblFromCosmic = cosmicLigneSplit[1]
		#Si la cle n'est pas dans le dictionnaire je la cree
		if idEnsemblFromCosmic not in CosmicDict:
			CosmicDict[idEnsemblFromCosmic] = []
			CosmicDict[idEnsemblFromCosmic].append(cosmicLigne)
		#sinon j'ajoute la ligne dans la liste de la cle
		else:
			CosmicDict[idEnsemblFromCosmic].append(cosmicLigne)
	print('Parsing OK')

def parse_mutations_file(fichier):
	File = "../Resultats/Auto_user_INS-92-SG_19-5-16_159_208/VariantCaller/MUTATIONS_"+fichier
	mutationsFile = open(File,'r')
	mutationsFile = read_file(mutationsFile)
	del mutationsFile[0:71]
	return mutationsFile
def get_allele_cov(string):
	match = re.search(r"(FAO)=[0-9]*", string)
	resultat = match.group(0)
	#Supprime le "FAO="
	resultat = resultat[4:]
	return(resultat)
def get_allele_freq(string):
	match = re.search(r"(AF)=\d*.\d*;", string)
	resultat = match.group(0)
	#Supprime le "AF="
	resultat = resultat.replace(";","")
	resultat = float(resultat[3:])
	resultat = resultat*100
	resultat = "%.1f" % resultat
	return(resultat)

def createDicoPanel():
	File = "../Data/Thibault/liste transcrit panel CHP2-CLv2 25-5-16-2.csv"
	panel = open(File,'r')
	panel = read_file(panel)
	for i in panel:
		panelSplit = i.split("\t")
		if "_ENST" not in panelSplit[0]:
			idRefseqPanel = panelSplit[1]
			if "NM_" in idRefseqPanel:
			### Je trie et enleve les .1
				"""if "." in idRefseqPanel:
					idRefseqPanel = str(idRefseqPanel)[:-2]
					dicoPanel[idRefseqPanel] = i
				else:"""
				idRefseqPanel = str(idRefseqPanel)
				dicoPanel[idRefseqPanel] = i
def main_refseq_ensembl(fichier):
	"""Parse le fichier de sortie de VEP et cree un nouveau fichier avec les lignes qui match avec les ID ensembl."""
	File = "../Resultats/Auto_user_INS-92-SG_19-5-16_159_208/VEP/VEP_"+fichier
	VepFile = open(File,'r')
	VepFile = read_file(VepFile)
	# supprime les lignes d'informations globales du VCF.
	del VepFile[0:31]
	VcfFileFinalList = []
	VcfFileFinalList2 = []
	VcfFileFinalList2.append("gene\tgene Id\tRefSeq id\tTranscript\tHGVSc\tHGVSp\tcosmic ID\tallele_cov\tallele_freq\tfunction\tmaf\tsift\tpolyphen\n")
	idNotFindList = []
	mutationsFile = parse_mutations_file(fichier)
	####
	#Recherche si correspondance entre ID refseq de gene2ensembl avec ID refseq du fichier VEP
	####
	File = "../Data/Cosmic/Cosmic_lite.txt"
	cosmic = open(File,"r")
	cosmic = read_file(cosmic)
	createDicoPanel()
	for ligne in VepFile:
		#Supprime le retour a la ligne
		ligne = ligne[0:len(ligne)-1]
		ligneSplit = ligne.split("\t")
		idRefseqSample = ligneSplit[4]
		match = re.search(r"[A-Z]*_[0-9]*.", idRefseqSample)
		if match != None:
			#enleve . pour correpsondre avec dico
			idRefseqSample = match.group(0)[:-1]
			#print(idRefseqSample)
		"""if idRefseqSample in dicoPanel:
			temp = dicoPanel[idRefseqSample].split("\t")
			VcfFileFinalList.append(ligne+"\t"+temp[0]+"\n")"""
		for cle in dicoPanel.keys():
			cleSansPoint = cle
			if "." in cle:
				cleSansPoint = cle.split(".")
				cleSansPoint = cleSansPoint[0]
			#print(cleSansPoint)
			if idRefseqSample == cleSansPoint:
				temp = dicoPanel[cle].split("\t")
				#print(idRefseqSample,cle)
				#print(temp)
				VcfFileFinalList.append(ligne+"\t"+temp[0]+"\n")
	output_file("../Resultats/Auto_user_INS-92-SG_19-5-16_159_208/temp/test_"+fichier,VcfFileFinalList)




	for ligne in VcfFileFinalList:
		ligneSplit = ligne.split("\t")
		#print(ligneSplit)
		idRefseq = ligneSplit[4]
		chromPos = ligneSplit[1].split(":")
		chrom = "chr"+chromPos[0]
		pos = chromPos[1]
		function = ligneSplit[6]
		ligneInfoVcf = ligneSplit[13]
		geneId = ligneSplit[14].replace("\n","")
		#for gene2ensemblLigne in gene2ensemblFinalDic:
			#idRefseqFromGene2ensembl = gene2ensemblLigne[3]
			#Si correspondance entre les ID
		Trouve = False
		if idRefseq in gene2ensemblFinalDic:
			Trouve = True
			
		idSampleNotInGene2ensembl = 1
		#Recuperation du HGVSc
		regexHGVSc = "HGVSc="+idRefseq+":(.*)"
		matchHGVSc = re.search(regexHGVSc, ligneInfoVcf)
		if matchHGVSc == None: 
			HGVSc = "NA"
		else: 
		#Dans le cas ou la regex a match avec HGVSp
			if "HGVSp=" in matchHGVSc.group(0):
				temp = matchHGVSc.group(0)
				tempSplit = temp.split(";")
				tempSplit = tempSplit[0]
				tempSplit = tempSplit.split(":")
				HGVSc = tempSplit[1]
			else:
				temp = matchHGVSc.group(0)
				tempSplit = temp.split(":")
				HGVSc = tempSplit[1]
		#Recuperation du HGVSp
		regexHGVSp = "HGVSp=(.*)"
		matchHGVSp = re.search(regexHGVSp, ligneInfoVcf)
		if matchHGVSp == None: HGVSp = "NA"
		else: 
			HGVSpTemp = matchHGVSp.group(0)
			HGVSpTemp = HGVSpTemp.split(";")
			HGVSpTemp = HGVSpTemp[0]
			HGVSpTemp = HGVSpTemp.split(":")
			HGVSp = HGVSpTemp[1]
		#Recuperation de la MAF
		regexMAF = "GMAF=.*"
		matchMAF = re.search(regexMAF, ligneInfoVcf)
		if matchMAF == None : MAF = "NA"
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

		if Trouve:
			idEnsembl = gene2ensemblFinalDic[idRefseq]
			string = chromPos[0]+":"+position + "\t"+ geneId +"\t" + idRefseq + "\t" + idEnsembl + "\t" + HGVSc + "\t" + HGVSp + "\tidCosmicNotFound\tcov_not_find\tfreq_not_find\t"+ function + "\t" + MAF + "\t" + SIFT + "\t" +PolyPhen + "\n"
		else:
			string = chromPos[0]+":"+position + "\t"+ geneId +"\t" + idRefseq + "\t" + "NA" + "\t" + HGVSc + "\t" + HGVSp + "\tidCosmicNotFound\tcov_not_find\tfreq_not_find\t"+ function + "\t" + MAF + "\t" + SIFT + "\t" +PolyPhen + "\n"
		####
		#Comparaison avec les lignes de MUTATIONS pour récupérer les couvertures
		####
		for mutation in mutationsFile:
			mutationSplit = mutation.split("\t")
			chromPosMutation = mutationSplit[0]+"\t"+mutationSplit[1]
			if chromPosMutation == chromPosVcf:
				alleleCov = get_allele_cov(mutationSplit[7])
				alleleFreq = get_allele_freq(mutationSplit[7])
				string = string.replace("cov_not_find",alleleCov)
				string = string.replace("freq_not_find",alleleFreq+"%")
		####
		#Recuperation identifiant COSMIC
		####
		if Trouve:
			idEnsembl = gene2ensemblFinalDic[idRefseq]
			infoCosmic = CosmicDict.get(idEnsembl)
			if infoCosmic != None:
				for i in infoCosmic:
					infoCosmicSplit = i.split("\t")
					if infoCosmicSplit[5] == HGVSc:
						string = string.replace("idCosmicNotFound",infoCosmicSplit[4])
		VcfFileFinalList2.append(string)
	output_file("../Resultats/Auto_user_INS-92-SG_19-5-16_159_208/temp/resultats_"+fichier,VcfFileFinalList2)