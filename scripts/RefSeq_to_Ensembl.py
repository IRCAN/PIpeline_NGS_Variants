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
	File = "../Data/Cosmic/Cosmic_lite_2.txt"
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
	#print(resultat)
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
	mutationsFile = parse_mutations_file(fichier)
	####
	#Recherche si correspondance entre ID refseq de gene2ensembl avec ID refseq du fichier VEP
	####
	for ligne in VcfFile:
		#Supprime le retour a la ligne
		ligne = ligne[0:len(ligne)-1]
		ligneSplit = ligne.split("\t")
		idRefseqSample = ligneSplit[4]
		# valeur = 0 si l'id de matche pas , valur = 1 si l'id matche
		idSampleNotInGene2ensembl = 0
		for gene2ensemblLigne in gene2ensemblFinalList:
			idRefseqFromGene2ensembl = gene2ensemblLigne[3]
			#Si correspondance entre les ID
			if idRefseqSample == idRefseqFromGene2ensembl:
				idSampleNotInGene2ensembl = 1
				ligneInfoVcf = ligneSplit[13]
				#Recuperation du HGVSc
				regex = "HGVSc="+idRefseqSample+":(.*);"
				match = re.search(regex, ligneInfoVcf)
				if match == None: HGVSc = "NA"
				else: HGVSc = match.group(1)
				#Recuperation du HGVSp
				regex2 = "HGVSp=(.*)"
				match2 = re.search(regex2, ligneInfoVcf)
				if match2 == None: HGVSp = "NA"
				else: HGVSp = match2.group(1)
				#Recuperation du SIFT
				###Pas robuste car recherche par le P de Polyphen
				regex3 = "SIFT=(.*);P"
				match3 = re.search(regex3, ligneInfoVcf)
				if match3 == None: SIFT = "NA"
				else: SIFT = match3.group(1)
				#Recuperation du SIFT
				###Pas robuste car recherche par le E de Exon
				regex4 = "PolyPhen=(.*);E"
				match4 = re.search(regex4, ligneInfoVcf)
				if match4 == None: PolyPhen = "NA"
				else: PolyPhen = match4.group(1)
				#Creation de la string resume
				position = ligneSplit[1]
				consequence = ligneSplit[6]
				temp = position + "\t" + idRefseqSample + "\t" + str(gene2ensemblLigne[4]) + "\t" + HGVSc + "\t" + HGVSp + "\t" + consequence + "\t"+ SIFT + "\t" +PolyPhen + "\tcov_not_find\tfreq_not_find\n"
				####
				#Comparaison avec les lignes de MUTATIONS pour récupérer les couvertures
				####
				
				for mutation in mutationsFile:
					mutationSplit = mutation.split("\t")
					chromPos = mutationSplit[0].replace("chr","")+":"+mutationSplit[1]
					mut = mutationSplit[3]+">"+mutationSplit[4]
					if chromPos in temp:
						if mut in temp:
							alleleCov = get_allele_cov(mutationSplit[7])
							alleleFreq = get_allele_freq(mutationSplit[7])
							temp = temp.replace("cov_not_find",alleleCov)
							temp = temp.replace("freq_not_find",alleleFreq+"%")
							#TODO verifier que exp reguliere fonctionne car pas FAO ni AF sur toutles variants
						
				#//TODO a modifier car probleme car NA pas sur toutes les lignes
				#Verifier si ID cosmic du VEP correspond a ID COSMIC trouve dans resultat final	
				#TOTO verifier pourquoi couverture n'est pas sur tout les fichier de mutations.
				#temp = temp.replace("\n","\t")
				#temp = temp + "NA\tNA\n"
				VcfFileFinalList.append(temp)
		#si identifiant refseq n'est pas trouve:
		###//TODO voir difference XN, NM XR et voir si on peut les supprimer		
		if idSampleNotInGene2ensembl == 0:
			idNotFindList.append(ligne+"\n")

	########################################################
	#Creation fichier de HS non trouves sur table gene2ensembl
	########################################################
	fileOutIdNotFind = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/ID_not_find_"+fichier
	print('Création de ID_not_find_',fichier)
	output_file(fileOutIdNotFind,idNotFindList)
	print('OK')

	########################################################
	#Suppression des doublons chr-pos-HGVSc
	########################################################
	listeString = []
	listeFinaleTriee = []
	for ligne in VcfFileFinalList:
		ligneVcfSplit = ligne.split("\t")
		string = ligneVcfSplit[0]+"-"+ligneVcfSplit[3]
		if string not in listeString:
			listeString.append(string)
			listeFinaleTriee.append(ligne)
		else : continue

	########################################################
	#Creation fichier de correlation ID RefSeq de VEP avec ID ensembl
	########################################################
	fileOutRefSeqToEnsembl = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/RefSeqToEnsembl_"+fichier
	print('Création de RefseqtoEnsembl_',fichier)
	output_file(fileOutRefSeqToEnsembl,listeFinaleTriee)
	print('OK')

	########################################################
	#Comparaison dico COSMIC avec contenu de RefSeqToEnsembl (.vcf)
	#Si ENST de RefSeqToEnsembl est dans le dico alors j'ecrit les data correspondantes
	########################################################
	print('Creation de '+fichier)
	resultsCorrelationList = ['chr\tpos\tgene\tensembl ID\tRefSeq ID\t Cosmic ID\t HGVSc\tHGVSp\tfunction\tsift\tpolyphen\tallele_cov\tallele_freq\n']

	for ligne in listeFinaleTriee:
		ligneSplitVcf = ligne.split("\t")
		idEnsemblVcf = ligneSplitVcf[2]
		if idEnsemblVcf in CosmicDict:
			listes_interet = CosmicDict.get(idEnsemblVcf)
			#permet de recupérer au premier tour de boucle le premier element.
			indice = -1
			for variant in listes_interet:
				indice +=1
				variant = variant.replace("\t\t","\tNone\t")
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
					id_cosmic = variantsplit[4]
					id_HGVSc = variantsplit[5]
					id_HGVSp = variantsplit[6].replace("\n","")
					polyphen = ligneSplitVcf[7].replace("\n","")
					alleleFreq = ligneSplitVcf[9].replace("\n","")
					#Verifie si la position est un intervalle ou pas
					if "-" in infoChromPosition[1]:
						position = infoChromPosition[1].split("-")
						string ="chr"+infoChromPosition[0] + "\t" + position[0] + "\t" + geneId+"\t"+idEnsemblVariant+"\t"+id_refseq+"\t"+id_cosmic+"\t"+id_HGVSc+"\t"+id_HGVSp+"\t"+ligneSplitVcf[5]+"\t"+ligneSplitVcf[6]+"\t"+polyphen+"\t"+ligneSplitVcf[8]+"\t"+alleleFreq+"\n"
					else:
						string ="chr"+infoChromPosition[0] + "\t" + infoChromPosition[1] + "\t" + geneId+"\t"+idEnsemblVariant+"\t"+id_refseq+"\t"+id_cosmic+"\t"+id_HGVSc+"\t"+id_HGVSp+"\t"+ligneSplitVcf[5]+"\t"+ligneSplitVcf[6]+"\t"+polyphen+"\t"+ligneSplitVcf[8]+"\t"+alleleFreq+"\n"
					if string in resultsCorrelationList: continue
					else:
						resultsCorrelationList.append(string)
		else:
			###Attention, manque les transcripts sans ID cosmic
			###TODO// obtenir informations sur les transcrits non references sur COSMIC
			print("Pas dans le dico: "+idEnsemblVcf)
			
	output_file("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/resultats_correlation_refseq_vs_cosmic_"+fichier,resultsCorrelationList)
	print('OK')