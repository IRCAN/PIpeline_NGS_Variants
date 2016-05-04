def read_file(File):
	"""Ouvre et lit le fichier .vcf de chaque patients."""
	contentFile = File.readlines()
	File.close() 
	return contentFile


File = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/RefSeqToEnsembl_TSVC_variants_IonXpress_002.vcf"

VcfFile = open(File,'r')
contentFile = read_file(VcfFile)
print(contentFile)

listeString = []
listeFinaleTriee = []
for i in contentFile:
	lignesplit = i.split("\t")
	print(lignesplit)
	string = lignesplit[0]+"-"+lignesplit[3]
	if string not in listeString:
		listeString.append(string)
		listeFinaleTriee.append(i)
	else : continue

print(len(contentFile))
print(len(listeString))

def output_file(FileName, Final_List):
	"""Cree un fichier resultat et ecrit dans ce fichier."""
	NomFile = FileName
	File = open(NomFile,'w')
	for i in Final_List:
		File.write(str(i))
	File.close()


fileOutRefSeqToEnsembl = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/temp/FINAL_TSVC_variants_IonXpress_002.vcf"
output_file(fileOutRefSeqToEnsembl,listeFinaleTriee)