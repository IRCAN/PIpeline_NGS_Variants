#!/usr/bin/python
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
gene2ensemblFinalList = []

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
		gene2ensemblFinalList.append(ligne)
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
	File = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VariantCaller/MUTATIONS_"+fichier
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

def main_refseq_ensembl(fichier):
	"""Parse le fichier de sortie de VEP et cree un nouveau fichier avec les lignes qui match avec les ID ensembl."""

	File = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VEP/VEP_"+fichier
	VcfFile = open(File,'r')
	VcfFile = read_file(VcfFile)
	# supprime les lignes d'information du VCF.
	del VcfFile[0:70]
	VcfFileFinalList = []
	VcfFileFinalList.append("chrom-pos\tRefSeq id\tensembl id\tHGVSc\tHGVSp\tfunction\tsift\tpolyphen\tallele_cov\tallele_freq\n")
	idNotFindList = []
	for ligne in VcfFile:
		#Supprime le retour a la ligne
		ligne = ligne[0:len(ligne)-1]
		ligneSplit = ligne.split("\t")
		idRefseqSample = ligneSplit[4]
		# valeur = 0 si l'id de matche pas , valur = 1 si l'id matche
		idSampleNotInGene2ensembl = 0
		#temp = None
		for gene2ensemblLigne in gene2ensemblFinalList:
			idRefseqFromGene2ensembl = gene2ensemblLigne[3]
			if idRefseqSample == idRefseqFromGene2ensembl:
				idSampleNotInGene2ensembl = 1
				ligneInfoVcf = ligneSplit[13]
				#Recuperation du HGVSc
				regex = "HGVSc="+idRefseqSample+":(.*);"
				match = re.search(regex, ligneInfoVcf)
				if match == None: HGVSc = "NA"
				else: 
					HGVSc = match.group(1)
				#Recuperation du HGVSp
				regex2 = "HGVSp=(.*)"
				match2 = re.search(regex2, ligneInfoVcf)
				if match2 == None: HGVSp = "NA"
				else: 
					HGVSp = match2.group(1)
				#Recuperation du SIFT
				###Pas robuste car recherche par le P de Polyphen
				regex3 = "SIFT=(.*);P"
				match3 = re.search(regex3, ligneInfoVcf)
				if match3 == None: SIFT = "NA"
				else: 
					SIFT = match3.group(1)
				#Recuperation du SIFT
				###Pas robuste car recherche par le E de Exon
				regex4 = "PolyPhen=(.*);E"
				match4 = re.search(regex4, ligneInfoVcf)
				if match4 == None: PolyPhen = "NA"
				else: 
					PolyPhen = match4.group(1)
				#Creation de la string resume
				position = ligneSplit[1]
				consequence = ligneSplit[6]
				temp = position + "\t" + idRefseqSample + "\t" + str(gene2ensemblLigne[4]) + "\t" + HGVSc + "\t" + HGVSp + "\t" + consequence + "\t"+ SIFT + "\t" +PolyPhen + "\tcov_not_find\tfreq_not_find\n"

				mutationsFile = parse_mutations_file(fichier)
				for mutation in mutationsFile:
					mutationSplit = mutation.split("\t")
					chromPos = mutationSplit[0].replace("chr","")+":"+mutationSplit[1]
					#print(chromPos)
					mut = mutationSplit[3]+">"+mutationSplit[4]
					#print(mut)
					if chromPos in temp:
						if mut in temp:
							alleleCov = get_allele_cov(mutationSplit[7])
							alleleFreq = get_allele_freq(mutationSplit[7])
							temp = temp.replace("cov_not_find",alleleCov)
							temp = temp.replace("freq_not_find",alleleFreq+"%")
							#temp = temp.replace("\n","\t")
							#temp = temp+alleleCov+"\t"+alleleFreq+"%"+"\n"
						
				#//TODO a modifier car probleme car NA pas sur toutes les lignes		
				#temp = temp.replace("\n","\t")
				#temp = temp + "NA\tNA\n"
				VcfFileFinalList.append(temp)
		#si identifiant refseq n'est pas trouve:
		###//TODO voir difference XN, NM XR et voir si on peut les supprimer		
		if idSampleNotInGene2ensembl == 0:
			idNotFindList.append(ligne+"\n")
	#print("###############################\n",VcfFileFinalList,"\n########################\n")
	fileOutRefSeqToEnsembl = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/RefSeqToEnsembl_"+fichier
	output_file(fileOutRefSeqToEnsembl,VcfFileFinalList)
	print('Création de RefseqtoEnsembl_',fichier)
	fileOutIdNotFind = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/ID_not_find_"+fichier
	output_file(fileOutIdNotFind,idNotFindList)
	print('Création de ID_not_find_',fichier)
	########################################################
	#Comparaison dico COSMIC avec resultats de VEP (.vcf)
	########################################################
	resultsCorrelationList = ['chr\tpos\tgene\tensembl ID\tRefSeq ID\t Cosmic ID\t HGVSc\tHGVSp\tfunction\tsift\tpolyphen\tallele_cov\tallele_freq\n']
	#print("###############################\n",VcfFileFinalList,"\n########################\n")
	for ligne in VcfFileFinalList:
		ligneSplitVcf = ligne.split("\t")
		#print("######################\n",ligneSplitVcf)
		idEnsemblVcf = ligneSplitVcf[2]
		if idEnsemblVcf in CosmicDict:
			listes_interet = CosmicDict.get(idEnsemblVcf)
			#permet de recupérer au premier tour de boucle le premier element.
			indice = -1
			for variant in listes_interet:
				indice +=1
				variantsplit = variant.split("\t")
				geneId = variantsplit[0]
				idEnsemblVariant = variantsplit[1]
				########################################################
				# Suppression des Gene_ENST
				########################################################
				regex = "(.*)_ENST"
				match = re.search(regex, variant)
				#Si pas de match
				if match is None:
					infoChromPosition = ligneSplitVcf[0].split(":")
					id_refseq = ligneSplitVcf[1]
					id_cosmic = variantsplit[16]
					id_HGVSc = variantsplit[17]
					id_HGVSp = variantsplit[18]
					polyphen = ligneSplitVcf[7].replace("\n","")
					alleleFreq = ligneSplitVcf[9].replace("\n","")
					#print(ligneSplitVcf[7])
					#Verifie si la position est un intervalle ou pas
					if "-" in infoChromPosition[1]:
						position = infoChromPosition[1].split("-")
						string ="chr"+infoChromPosition[0] + "\t" + position[0] + "\t" + geneId+"\t"+idEnsemblVariant+"\t"+id_refseq+"\t"+id_cosmic+"\t"+id_HGVSc+"\t"+id_HGVSp+ligneSplitVcf[5]+"\t"+ligneSplitVcf[6]+"\t"+polyphen+"\t"+ligneSplitVcf[8]+"\t"+alleleFreq+"\n"
					else:
						string ="chr"+infoChromPosition[0] + "\t" + infoChromPosition[1] + "\t" + geneId+"\t"+idEnsemblVariant+"\t"+id_refseq+"\t"+id_cosmic+"\t"+id_HGVSc+"\t"+id_HGVSp+"\t"+ligneSplitVcf[5]+"\t"+ligneSplitVcf[6]+"\t"+polyphen+"\t"+ligneSplitVcf[8]+"\t"+alleleFreq+"\n"
					if string in resultsCorrelationList: continue
					else:
						resultsCorrelationList.append(string)
	###Attention, manque les transcripts sans ID cosmic
	output_file("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/resultats_correlation_refseq_vs_cosmic_"+fichier,resultsCorrelationList)
	print('Fichier de correlation pour '+fichier+' créé !!!')



#Code de test a supprimer lorsque programme OK
"""
barecode = ['IonXpress_001']#,'IonXpress_002']
#,'IonXpress_003','IonXpress_004','IonXpress_005','IonXpress_006','IonXpress_007','IonXpress_008','IonXpress_009','IonXpress_011','IonXpress_012','IonXpress_013','IonXpress_015','IonXpress_016']

parse_gene2ensembl()
parse_cosmic_lite()
for i in barecode:
	fichier = 'TSVC_variants_'+i+'.vcf' 
	main_refseq_ensembl(fichier)

for ligne in VcfFile:
		#Supprime le retour a la ligne
		ligne = ligne[0:len(ligne)-1]
		ligneSplit = ligne.split("\t")
		idRefseqSample = ligneSplit[4]
		# valeur = 0 si l'id de matche pas , valur = 1 si l'id matche
		idSampleNotInGene2ensembl = 0
		for gene2ensemblLigne in gene2ensemblFinalList:
			idRefseqFromGene2ensembl = gene2ensemblLigne[3]
			if idRefseqSample == idRefseqFromGene2ensembl:
				idSampleNotInGene2ensembl = 1
				ligneInfoVcf = ligneSplit[13]
				#Recuperation du HGVSc
				regex = "HGVSc="+idRefseqSample+":(.*);"
				match = re.search(regex, ligneInfoVcf)
				if match == None: HGVSc = "NA"
				else: 
					HGVSc = match.group(1)
				#Recuperation du HGVSp
				regex2 = "HGVSp=(.*)"
				match2 = re.search(regex2, ligneInfoVcf)
				if match2 == None: HGVSp = "NA"
				else: 
					HGVSp = match2.group(1)
				#Recuperation du SIFT
				###Pas robuste car recherche par le P de Polyphen
				regex3 = "SIFT=(.*);P"
				match3 = re.search(regex3, ligneInfoVcf)
				if match3 == None: SIFT = "NA"
				else: 
					SIFT = match3.group(1)
				#Recuperation du SIFT
				###Pas robuste car recherche par le E de Exon
				regex4 = "PolyPhen=(.*);E"
				match4 = re.search(regex4, ligneInfoVcf)
				if match4 == None: PolyPhen = "NA"
				else: 
					PolyPhen = match4.group(1)
				#Creation de la string resume
				position = ligneSplit[1]
				consequence = ligneSplit[6]
				temp = position + "\t" + idRefseqSample + "\t" + str(gene2ensemblLigne[4]) + "\t" + HGVSc + "\t" + HGVSp + "\t" + consequence + "\t"+ SIFT + "\t" +PolyPhen+ "\n"
				VcfFileFinalList.append(temp)


"""