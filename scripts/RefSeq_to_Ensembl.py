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
COSMIC_DICT = {}
GENE2ENSEMBL_FINAL_LIST = []

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
		GENE2ENSEMBL_FINAL_LIST.append(ligne)
	print('Parsing OK')
def parse_cosmic_lite():
	"""Parse le fichier DB Cosmic_lite et cree un dictionnaire:
	cle = ID_ensembl
	valeur = contenu de la (ou les) ligne(s) correspondant(s) à la cle."""
	print('Parsing de la DB Cosmic lite en cours...')
	File = "../Data/Cosmic/Cosmic_lite.txt"
	cosmic = open(File,"r")
	cosmic = read_file(cosmic)
	id_Ensembl_cosmic = ""
	########################################################
	#Creation dictionnaire cosmic DB (cle = ENST)
	########################################################
	for ligne_cosmic in cosmic:
		ligne_split_cosmic = ligne_cosmic.split("\t")
		id_Ensembl_cosmic = ligne_split_cosmic[1]
		#Si la cle n'est pas dans le dictionnaire je la cree
		if id_Ensembl_cosmic not in COSMIC_DICT:
			COSMIC_DICT[id_Ensembl_cosmic] = []
			COSMIC_DICT[id_Ensembl_cosmic].append(ligne_cosmic)
		#sinon j'ajoute la ligne dans la liste de la cle
		else:
			COSMIC_DICT[id_Ensembl_cosmic].append(ligne_cosmic)
	print('Parsing OK')
def main_refseq_ensembl(fichier):
	"""Parse le fichier de sortie de VEP et cree un nouveau fichier avec les lignes qui match avec les ID ensembl."""
	File = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VEP/VEP_"+fichier
	VCF_file = open(File,'r')
	VCF_file = read_file(VCF_file)
	# supprime les lignes d'information du VCF.
	del VCF_file[0:70]
	VCF_file_final_list = []
	ID_not_find_list = []
	for ligne in VCF_file:
		#Supprime le retour a la ligne
		ligne = ligne[0:len(ligne)-1]
		ligne_split = ligne.split("\t")
		id_RefSeq_sample = ligne_split[4]
		# valeur = 0 si l'id de matche pas , valur = 1 si l'id matche
		id_sample_not_in_gene2ensembl = 0
		for gene2ensembl_ligne in GENE2ENSEMBL_FINAL_LIST:
			id_RefSeq_gene2ensembl = gene2ensembl_ligne[3]
			if id_RefSeq_sample == id_RefSeq_gene2ensembl:
				id_sample_not_in_gene2ensembl = 1
				ligne_info_VCF = ligne_split[13]
				#Recuperation du HGVSc
				regex = "HGVSc="+id_RefSeq_sample+":(.*);"
				match = re.search(regex, ligne_info_VCF)
				if match == None: HGVSc = "NA"
				else: 
					HGVSc = match.group(1)
				#Recuperation du HGVSp
				regex2 = "HGVSp=(.*)"
				match2 = re.search(regex2, ligne_info_VCF)
				if match2 == None: HGVSp = "NA"
				else: 
					HGVSp = match2.group(1)
				#Recuperation du SIFT
				###Pas robuste car recherche par le P de Polyphen
				regex3 = "SIFT=(.*);P"
				match3 = re.search(regex3, ligne_info_VCF)
				if match3 == None: SIFT = "NA"
				else: 
					SIFT = match3.group(1)
				#Recuperation du SIFT
				###Pas robuste car recherche par le E de Exon
				regex4 = "PolyPhen=(.*);E"
				match4 = re.search(regex4, ligne_info_VCF)
				if match4 == None: PolyPhen = "NA"
				else: 
					PolyPhen = match4.group(1)
				#Creation de la string resume
				position = ligne_split[1]
				consequence = ligne_split[6]
				temp = position + "\t" + id_RefSeq_sample + "\t" + str(gene2ensembl_ligne[4]) + "\t" + HGVSc + "\t" + HGVSp + "\t" + consequence + "\t"+ SIFT + "\t" +PolyPhen+ "\n"
				VCF_file_final_list.append(temp)
		#si identifiant refseq n'est pas trouve:
		###//TODO voir difference XN, NM XR et voir si on peut les supprimer		
		if id_sample_not_in_gene2ensembl == 0:
			ID_not_find_list.append(ligne+"\n")

	f_out_RefSeqToEnsembl = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/RefSeqToEnsembl_"+fichier
	output_file(f_out_RefSeqToEnsembl,VCF_file_final_list)
	print('Création de RefseqtoEnsembl_',fichier)
	f_out_id_not_find = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/ID_not_find_"+fichier
	output_file(f_out_id_not_find,ID_not_find_list)
	print('Création de ID_not_find_',fichier)
	########################################################
	#Comparaison dico COSMIC avec resultats de VEP (.vcf)
	########################################################
	list_resultats_correlations_tables = ['chr\tpos\tgene\tensembl ID\tRefSeq ID\t Cosmic ID\t HGVSc\tHGVSp\n']
	for ligne in VCF_file_final_list:
		ligne_split_vcf = ligne.split("\t")
		id_Ensembl_VCF = ligne_split_vcf[2]
		if id_Ensembl_VCF in COSMIC_DICT:
			listes_interet = COSMIC_DICT.get(id_Ensembl_VCF)
			#permet de recupérer au premier tour de boucle le premier element.
			indice_variant = -1
			for variant in listes_interet:
				indice_variant +=1
				variant_split = variant.split("\t")
				gene_id = variant_split[0]
				id_ensembl_variant = variant_split[1]
				########################################################
				# Suppression des Gene_ENST
				########################################################
				regex = "(.*)_ENST"
				match = re.search(regex, variant)
				#Si pas de match
				if match is None:
					info_chrom_pos = ligne_split_vcf[0].split(":")
					id_refseq = ligne_split_vcf[1]
					id_cosmic = variant_split[16]
					id_HGVSc = variant_split[17]
					id_HGVSp = variant_split[18]
					#Verifie si la position est un intervalle ou pas
					if "-" in info_chrom_pos[1]:
						position = info_chrom_pos[1].split("-")
						string ="chr"+info_chrom_pos[0] + "\t" + position[0] + "\t" + gene_id+"\t"+id_ensembl_variant+"\t"+id_refseq+"\t"+id_cosmic+"\t"+id_HGVSc+"\t"+id_HGVSp+"\n"
					else:
						string ="chr"+info_chrom_pos[0] + "\t" + info_chrom_pos[1] + "\t" + gene_id+"\t"+id_ensembl_variant+"\t"+id_refseq+"\t"+id_cosmic+"\t"+id_HGVSc+"\t"+id_HGVSp+"\n"
					if string in list_resultats_correlations_tables: continue
					else:
						list_resultats_correlations_tables.append(string)

	###Attention, manque les transcripts sans ID cosmic
	output_file("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/resultats_correlation_refseq_vs_cosmic"+fichier,list_resultats_correlations_tables)
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

"""