#!/usr/bin/python
# coding: utf-8 
from Separation_variants import main_separation_variants
import os,re

"""
Script principal du pipeline qui traite le fichier .vcf de chaque patients d'un run
afin d'obtenir un compte rendu de mutations.

Ludovic KOSTHOWA (Debut : 06/04/16)
Info: Creation en cours, script peut etre modifie a tout moment.
"""

def read_file(File):
	"""Ouvre et lit le fichier .vcf de chaque patients."""
	contentFile = File.readlines()
	File.close() 
	return contentFile

def file_to_list(contentFile):
	"""Cree une liste contenant toutes les lignes du fichier .vcf.
	Chaque ligne est une liste composee d'elements (chrom,ID,position,etc)."""
	liste=[]
	for k in contentFile:
		liste.append(k)
	liste2liste=[]
	for k in liste:
		lignesplit = k.split('\t')
		liste2liste.append(lignesplit)
	return liste2liste

def output_file(FileName, Final_List):
	"""Cree un fichier resultat et ecrit dans ce fichier."""
	NomFile = FileName
	File = open(NomFile,'w')	# creation et ouverture du File
	for j in listeLegendes:		#ecriture de la legende
		j = "".join(j)
		File.write(str(j))
	for i in Final_List:	#ecriture des donnees
		File.write(str(i))
	File.close()

def check_if_multiple_id(listOfList):
	"""Regarde sur fichier original si plusieurs ID cosmic sur meme ligne
	si plusieurs ID, recupere les lignes separees dans ListdeNewLignes.
	Verifie en meme temps si la ligne correspond a une mutation et ajoute
	cette ligne dans une liste si c'est le cas. """
	contentNewVFC = []
	cmpt = 0
	for i in listOfList:
		ligne = i[4].split(",")
		if len(ligne) == 1:
			i="\t".join(i)
			contentNewVFC.append(i)
		else:
			temp = []
			for j in ListdeNewLines[cmpt]:
				j="\t".join(j)
				contentNewVFC.append(j)		
			cmpt+=1
	return contentNewVFC	

def creation_dico_HS():
	"""Creation d'un dictionnaire a partir de la liste de hotspots avec:
	cle = nomGene-numeroExon
	valeur = liste vide. """
	dico = {}
	for hs in hotspots:
		cle = hs[3]+'-'+hs[4]
		dico[cle] = []
	#Supprime la legende du tableau liste_hotspots
	del dico["gene-exon"]
	return dico

def find_depth_HSnm(lignes,hotspots):
	"""Compare les variants non mutes (FAO = 0) du fichier avec le fichier liste_hotspots
	et ressort dans un dictionnaire les profondeurs des hotspots non mutes.
	cle = nomGene-numeroExon
	Valeur = profondeurDuVariant"""
	for l in lignes:
		if "FAO=0;" in l:
			l = l.split("\t")
			for hs in hotspots:
				if l[0] == hs[0] and int(hs[1]) <= int(l[1]) <= int(hs[2]):
					geneExon = hs[3]+'-'+hs[4]
					#recherche de la profondeur du variant par expression reguliere
					match = re.search(r"(FDP)=[0-9]*", l[7])
					resultat = match.group(0)
					resultat = int(resultat[4:])
					#ajout pour chaque variants du HS la profondeur.
					dico[geneExon].append(resultat)				
	return dico

def get_depth(dico):
	"""Calcul de la profondeur moyenne et minimale pour chaque HS."""
	for cle,valeur in dico.items():
		if not valeur : 
			dico[cle] = "N/A"
		else:
			#calcul de la profondeur moyenne pour le hotspot et arrondi de la valeur
			moyenne = round(sum(valeur) / len(valeur),2)
			#calcul de la profondeur minimale pour le hotspot
			minDepthHSnm = min(valeur)
			valeur = str(moyenne)+"\t"+str(minDepthHSnm)
			dico[cle] = valeur
	return dico

def output_nmHS(nomFichier):
	"""Traitement du dictionnaire contenant les HS et leurs profondeurs puis ecriture dans un fichier tabulé (utile pour le rapport final)."""
	HSnmGlobalList = []
	for cle, valeur in globalInfoHSnm.items():
		HSLigne = []
		#Separation du gene et de l'exon
		cle = cle.split("-")
		cle = "\t".join(cle)
		HSLigne.append(cle)
		HSLigne.append(valeur)
		HSLigne = "\t".join(HSLigne)
		HSnmGlobalList.append(HSLigne)
	#Trie de la liste de genes par ordre alphabetique pour meilleure lisibilite.
	HSnmGlobalList = sorted(HSnmGlobalList)
	HSnmGlobalList = "\n".join(HSnmGlobalList)
	f_out = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/HSnonmuté_"+nomFichier
	File = open(f_out,'w')	# creation et ouverture du File
	File.write("Gene\texon\tMean Depth\tMinimal Depth\n")	#Ecriture de la legende.
	for i in HSnmGlobalList:	#ecriture des donnees
		File.write(i)
	File.close()
	print('Création de ',f_out,'\n')


########################################
####Pour verification, a supprimer plus tard
def find_HSnm(lignes,hotspots):
	"""Compare les transcripts du fichier avec le fichier liste_hotspots
	et ressort les hs non mutes"""
	#je recupere tout les FAO = 0
	nonMuteHs = []
	for l in lignes:
		if "FAO=0;" in l:
			l = l.split("\t")
			for hs in hotspots:
				if l[0] == hs[0] and int(hs[1]) <= int(l[1]) <= int(hs[2]):
					listTemp=[]
					listTemp.append(hs[3])
					listTemp.append(hs[4])
					if listTemp in nonMuteHs : 
						continue
					else:
						nonMuteHs.append(l)
						#verifie si element n'est pas dans la liste globale (si non ajout a
						# chaque tour de boule des memes listeTemp...)
						if listTemp not in listeNonMuteHs:
							listeNonMuteHs.append(listTemp)				
	return nonMuteHs

def profondeur_moyenne_HSnm():
	"""Donne la profondeur moyenne des hotspots non mutés."""
	listeProfondeur = []
	for hs in HSNONMUTE:
		match = re.search(r"(FDP)=[0-9]*", hs[7])
		resultat = match.group(0)
		resultat = int(resultat[4:])
		listeProfondeur.append(resultat)
	depthHSnm = sum(listeProfondeur) / len(listeProfondeur)
	return depthHSnm

def profondeur_min_HSnm():
	"""Donne la profondeur minimale des hotspots non mutés."""
	listeProfondeur = []
	for hs in HSNONMUTE:
		match = re.search(r"(FDP)=[0-9]*", hs[7])
		resultat = match.group(0)
		resultat = int(resultat[4:])
		listeProfondeur.append(resultat)
	minDepthHSnm = min(listeProfondeur)
	return minDepthHSnm
####FIN DE Pour verification, a supprimer plus tard
########################################



##############################################################
########					MAIN					  ########
##############################################################
#//TODO a supprimer pour final
listeNonMuteHs = []

#Ouverture fichier liste_HS
hs = "../Data/Thibault/liste_hotspots_TF.tsv"
hotspots_file = open(hs,'r')
hotspots_temp = read_file(hotspots_file)
hotspots = file_to_list(hotspots_temp)

#//TODO A modifier lorsque arborescence finale connue
barecode = ['IonXpress_001']
#,'IonXpress_002','IonXpress_003','IonXpress_004','IonXpress_005','IonXpress_006','IonXpress_007','IonXpress_008','IonXpress_009','IonXpress_011','IonXpress_012','IonXpress_013','IonXpress_015','IonXpress_016',]

#//TODO FINAL: recuperer liste des  fichiers VCF du run en cours et boucler dessus

################################################################################
# Etape de verification de MAJ du genome local avec la derniere version du genome sur ensembl
################################################################################

print("Vérification version génome...")
os.system('rsync -u rsync://ftp.ensembl.org/ensembl/pub/current_variation/VEP/homo_sapiens_vep_84_GRCh37.tar.gz ../Data/Ensembl/')
print("Vérification génome OK")

################################################################################
# Etape de creation des repertoires
################################################################################

#Verification si repertoires existent deja (necessaire si script lance sur 1 run ?)
if os.path.isdir("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VariantCaller") == False:
	os.mkdir("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VariantCaller") 
if os.path.isdir("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VEP/") == False:
	os.mkdir("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VEP/")
if os.path.isdir("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/") == False:
	os.mkdir("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/")  

################################################################################
# Etape de separation des lignes de variants
################################################################################

for i in barecode:

	fichier = 'TSVC_variants_'+i+'.vcf'
	#//TODO A modifier lorsque arborescence finale connue
	j = "../Data/Run_test/Auto_user_INS-80-TF_23-02-16_151_198/plugin_out/variantCaller_out.411/"+i+'/'+fichier
	print('Traitement du fichier: \n',j,'\n')
	"""File = open(j,'r')
	contentFile = read_file(File)
	#Cree une liste avec chaque elements correspondant a une ligne du fichier
	listOfList = file_to_list(contentFile)
	#Supprime les informations inutiles du fichier VCF
	listeLegendes = listOfList[0:71]
	listeLegendes[70] = "\t".join(listeLegendes[70])
	del listOfList[0:71]
	del contentFile[0:71]
	#Appel de la fonction qui separe les transcripts presents sur la meme ligne
	ListdeNewLines = main_separation_variants(contentFile)
	#Traitement de la liste et ecriture dans fichier VCF: recupere les lignes avec 1 seul ID
	# dans listOfList et les autres dans ListdeNewLines + ajf_oute seulement les mutations
	list_of_transcripts = check_if_multiple_id(listOfList)"""
	#//TODO A modifier lorsque arborescence finale connue
	"""f_out = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VariantCaller/SEP_LIGNES_"+fichier
	#creation du fichier de sortie: fichier VCF avec un transcript par ligne
	output_file(f_out,list_of_transcripts)
	print('Création de ',f_out,'\n')"""

	################################################################################
	# Etape de recherche de Hotspots non mutes
	################################################################################
	#creation d'un dictionnaire avec cle = gene-exon et valeurs vide.
	"""dico = creation_dico_HS()
	#ajout dans le dictionnaire des profondeurs des variants
	depthHotspotnm = find_depth_HSnm(list_of_transcripts,hotspots)
	#calcul et ajout de la profondeur moyenne et minimale de chaque hotspot 
	globalInfoHSnm = get_depth(dico)
	#creation fichier de sortie du tableau Hotspots non mutés
	output_nmHS(fichier)
	#//TODO a supprimer pour final
	HSNONMUTE = find_HSnm(list_of_transcripts,hotspots)
	#print("Hotspots non mutés: (Gene , exon): \n",listeNonMuteHs,"\n")"""
	
	################################################################################
	#Etape de creation du fichier ne contenant que les mutations
	################################################################################
	"""
	list_of_mutations = []
	for l in range(len(list_of_transcripts)):
		a = list_of_transcripts[l].split('\t')
		if "FAO=0;" not in a[7]:
			list_of_mutations.append(list_of_transcripts[l])
	f_out2 = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VariantCaller/MUTATIONS_"+fichier
	output_file(f_out2,list_of_mutations)
	print('Création de ',f_out2,'\n')
	"""
	#//TODO
	#Pour chaque FAO != 0:
	#regarde dans HS si il en fait parti ????
	#lancer vep
	#recup id cosmic et comparer à HS et variants NGS

	################################################################################
	#Etape de lancement de VEP avec en input le fichier de mutations
	################################################################################

	inputfile = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VariantCaller/MUTATIONS_"+fichier
	output_file2 = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VEP/VEP_REFSEQ_CANONICAL_PROTEIN_"+fichier
	command3 = "perl ../Logiciels/ensembl-tools-release-84/scripts/variant_effect_predictor/variant_effect_predictor.pl -cache --refseq --no_stats --symbol --sift b --hgvs --gmaf --polyphen b --regulatory --filter_common --biotype --pubmed --canonical --input_file "+inputfile+ " --output_file "+output_file2
	os.system(command3)
print("######################\n Fin du script!\n######################")
#//TODO prendre chaque FAO = 0 et comparer si ds HS













################################################################################
################################################################################
#A supprimer plus tard, je le conserve maintenant par securite.
"""
#verifie si le genome en local correspond a la derniere version du genome sur ensembl
print("Vérification version génome...")
os.system('rsync -u rsync://ftp.ensembl.org/ensembl/pub/current_variation/VEP/homo_sapiens_vep_84_GRCh37.tar.gz ../Data/Ensembl/')
print("Vérification génome OK")
for i in barecode:
	fichier = 'TSVC_variants_'+i+'.vcf'
	#//TODO faire la fonction dans script VEP + comparer resultats fichier debut et fichier fin
	inputfile = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VariantCaller/MUTATIONS_"+fichier
	output_file = "../Resultats/VEP/VEP_GAEL_"+fichier
	output_file1 = "../Resultats/VEP/VEP_LUDO_"+fichier
	output_file2 = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VEP/VEP_"+fichier
	#gael = mieux que script perso , + d'informations
	command = "perl ../Logiciels/ensembl-tools-release-84/scripts/variant_effect_predictor/variant_effect_predictor.pl  -cache --no_stats --pick --refseq --symbol --hgvs --gmaf --sift b --polyphen b --canonical --regulatory --numbers --filter_common --filter coding_change,splice,regulatory --input_file "+inputfile+ " --output_file "+output_file
	#perso
	command2 = "perl ../Logiciels/ensembl-tools-release-84/scripts/variant_effect_predictor/variant_effect_predictor.pl --appris --biotype --no_stats --check_existing --gmaf --maf_1kg --maf_esp --maf_exac --polyphen both --pubmed --regulatory --sift both --species homo_sapiens --symbol --tsl --cache --input_file "+inputfile+ " --output_file "+output_file1
	#test mix commande
	command3 = "perl ../Logiciels/ensembl-tools-release-84/scripts/variant_effect_predictor/variant_effect_predictor.pl -cache --no_stats --symbol --sift b --hgvs --gmaf --polyphen b --regulatory --filter_common --biotype --pubmed --input_file "+inputfile+ " --output_file "+output_file2
	#os.system(command)
	#os.system(command2)
	os.system(command3)
print("Creation fichiers par VEP OK")

##//TODO realiser intersection avec fichiers tibo"""