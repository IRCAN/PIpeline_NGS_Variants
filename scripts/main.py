from Separation_transcripts import main_separation_transcripts
import os

# je veux recuperer pour chaque patients le fichier .VCF
# et le traiter par Separation_transcripts.py pour creer un nouveau fichier plus lisible.
def read_file(File):
	contentFile = File.readlines()
	File.close() 
	return contentFile

def file_to_list(contentFile):
	# change le contentFile du File en liste de liste
	liste=[]
	for k in contentFile:
		liste.append(k)
	liste2liste=[]
	for k in liste:
		lignesplit = k.split('\t')
		liste2liste.append(lignesplit)
	return liste2liste

def output_file(FileName, Final_List):
	NomFile = FileName
	# creation et ouverture du File
	File = open(NomFile,'w')
	# ecriture dans le File
	for j in listeLegendes:
		j = "".join(j)
		File.write(str(j))
	for i in Final_List:
		File.write(str(i))
	# fermeture du File
	File.close()

def check_if_multiple_id(listOfList):
	contentNewVFC = []
	cmpt = 0
	for i in listOfList:
		ligne = i[2].split(";")
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



#//TODO A modifier lorsque arborescence finale connue
fichiers = ['TSVC_variants_IonXpress_001.vcf','TSVC_variants_IonXpress_002.vcf','TSVC_variants_IonXpress_005.vcf','TSVC_variants_IonXpress_006.vcf','TSVC_variants_IonXpress_007.vcf','TSVC_variants_IonXpress_008.vcf','TSVC_variants_IonXpress_009.vcf','TSVC_variants_IonXpress_012.vcf','TSVC_variants_IonXpress_013.vcf','TSVC_variants_IonXpress_016.vcf']

for i in fichiers:
	#//TODO A modifier lorsque arborescence finale connue
	j = "../Data/VariantCaller/"+i
	print('Traitement du fichier: ',j)
	File = open(j,'r')
	contentFile = read_file(File)
	#Cree une liste avec chaque elements correspondant a une ligne du fichier
	listOfList = file_to_list(contentFile)
	#Supprime les informations inutiles du fichier VCF
	listeLegendes = listOfList[0:71]
	listeLegendes[70] = "\t".join(listeLegendes[70])
	del listOfList[0:71]
	del contentFile[0:71]
	#Appel de la fonction qui separe les transcripts presents sur la meme ligne
	ListdeNewLines = main_separation_transcripts(contentFile,listOfList)
	#Traitement de la liste et ecriture dans fichier VCF
	newContentFile = check_if_multiple_id(listOfList)
	#//TODO A modifier lorsque arborescence finale connue
	out = "../Resultats/VariantCaller/RESULTAT_"+i+".vcf"
	#creation du fichier de sortie: fichier VCF avec un transcript par ligne
	output_file(out,newContentFile)
print("Fichier triee crees !")


os.system('rsync -u rsync://ftp.ensembl.org/ensembl/pub/current_variation/VEP/homo_sapiens_vep_84_GRCh38.tar.gz ../Data/Ensembl/')
for i in fichiers:
	#//TODO faire la fonction dans script VEP + comparer resultats fichier debut et fichier fin
	inputfile = "../Resultats/VariantCaller/RESULTAT_"+i+".vcf"
	output_file = "../Resultats/VEP/VEP_GAEL_"+i
	output_file1 = "../Resultats/VEP/VEP_LUDO_"+i
	output_file2 = "../Resultats/VEP/VEP_NOUVELLE_CMD_"+i
	#gael = mieux que script perso , + d'informations
	#command = "perl ../Logiciels/ensembl-tools-release-84/scripts/variant_effect_predictor/variant_effect_predictor.pl  -cache --no_stats --pick --refseq --symbol --hgvs --gmaf --sift b --polyphen b --canonical --regulatory --numbers --filter_common --filter coding_change,splice,regulatory --input_file "+inputfile+ " --output_file "+output_file
	#perso
	#command2 = "perl ../Logiciels/ensembl-tools-release-84/scripts/variant_effect_predictor/variant_effect_predictor.pl --appris --biotype --check_existing --gmaf --maf_1kg --maf_esp --maf_exac --polyphen both --pubmed --regulatory --sift both --species homo_sapiens --symbol --tsl --cache --input_file "+inputfile+ " --output_file "+output_file1
	#test mix comamnde
	command3 = "perl ../Logiciels/ensembl-tools-release-84/scripts/variant_effect_predictor/variant_effect_predictor.pl -cache --no_stats --symbol --sift b --hgvs --gmaf --polyphen b --regulatory --filter_common --biotype --pubmed --input_file "+inputfile+ " --output_file "+output_file2
	
	#os.system(command)
	#os.system(command2)
	os.system(command3)
print("Creation fichiers traites par VEP OK")