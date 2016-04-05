import re

###############################################################
######## Script pour separer une ligne du fichier VCF  ########
########composee de plusieurs transcripts en plusieurs ########
########        lignes: une ligne par transcript       ########
###############################################################

########	Variable(s)	########
legendes = ['AF=','AO=','DP=','FAO=','FDP=','FR=','FRO=','FSAF=','FSAR=','FSRF=','FSRR=','FWDB=','FXX=','HRUN=','LEN=','MLLD=','OALT=','OID=','OMAPLAT=','OPOS=','OREF=','QD=','RBI=','REFB=','REVB=','RO=','SAF=','SAR=','SRF=','SRR=','SSEN=','SSEP=','SSSB=','STB=','STBP=','TYPE=','VARB=','']

########	Fonctions	########

def ReadFile(File):
	contentFile = File.readlines()
	File.close()
	return contentFile

def CheckIfMultipleID(contentFile):
	#creation d'une liste pour compter le nombre d'ID cosmic par ligne
	contentFile_list=[]
	for k in contentFile:
		contentFile_list.append(k)
	listOflist=[]
	for k in contentFile_list:
		lignesplit = k.split('\t')
		listOflist.append(lignesplit)
	cpt = -1
	multiple_ID_list = []
	for i in listOflist:
		cpt += 1
		ligne = i[2].split(";")
		#Si il y a plus que un seul ID cosmic, je cree une liste de ces ID.	
		if len(ligne) != 1:
			multiple_ID_list.append(contentFile[cpt])
	return multiple_ID_list

def CreateListOfList(contentFile):
	list_contentFile = [] #liste du contenu du fichier
	#separation de contentFile par les tabulations
	listFINALE =[]
	for element in contentFile:
		contentFile = element.split('\t')
		list_contentFile.append(contentFile)
	for ligne_chromosome in list_contentFile:
		list_ligne_temp = [] #liste temporaire correspondant a une ligne (1 transcript)
		list_INFO_temp = []	#liste de la cellule INFO du fichier VCF
		list_ligne_info_trie = []	#liste finale correspondant aux informations triees pour chaque transcript
		for element in ligne_chromosome:
			#separation de contentFile par les ";"
			if ";" in element:
				temp = element.split(";")
				list_INFO_temp.append(temp)
			#separation de contentFile par les ","
			elif "," in element:
				temp = element.split(",")
				list_INFO_temp.append(temp)
			else:
				list_INFO_temp.append(element)
		#traitement et separations des informations de la cellule INFO
		list_INFO_temp[7][5] = list_INFO_temp[7][5].replace(",","")
		for element in list_INFO_temp[7]:
			list_ligne_temp_element7 = element.split(",")
			list_ligne_info_trie.append(list_ligne_temp_element7)
		for element in list_INFO_temp:
			if type(element) != list:
				list_ligne_temp.append(element)
			elif type(element) == list:
				if element == list_INFO_temp[7]:
					list_ligne_info_trie = []
					for element in list_INFO_temp[7]:
						list_ligne_temp_element7 = element.split(",")
						list_ligne_info_trie.append(list_ligne_temp_element7)
					list_ligne_temp.append(list_ligne_info_trie)	
				else:
					list_ligne_temp.append(element)
		#verification pour eviter saut de ligne dans fichier VCF
		if "\n" in list_ligne_temp[-1]:
			list_ligne_temp[-1] = list_ligne_temp[-1].replace("\n","")
			listFINALE.append(list_ligne_temp)
		else:
			listFINALE.append(list_ligne_temp)
	return listFINALE

def TrieInformations(list_ligne_temp):
	#suppression des legendes (FAO,AF,AO,...) par recherche d'une expression reguliere
	#pour uniformiser les contentFile_lists
	for i in list_ligne_temp[7]:
		temp = str(i[0])
		temp = re.sub(r"([A-Z])+=","",temp)
		i[0] = temp

def CheckIfSameLength(list_ligne_temp):
	#nombre d'elements de la cellule INFO
	cmpt = len(list_ligne_temp[7])
	newLines = []
	compteurID= 0
	#Pour chaque lignes , je cree une liste que je mets dans newLines
	#Verification si meme nombre ID cosmic que nombre de mutations
	if len(list_ligne_temp[2]) == len(list_ligne_temp[4]):
		nbeBoucle = 4
		CreationLignes(list_ligne_temp,cmpt,compteurID,newLines,nbeBoucle)
	else:
	#boucle sur le plus petit element
		#boucle sur ID cosmic
		if len(list_ligne_temp[2]) < len(list_ligne_temp[4]):
			nbeBoucle = 2
			CreationLignes(list_ligne_temp,cmpt,compteurID,newLines,nbeBoucle)
		#boucle sur le nombre de mutations (/!\ Possible perte du dernier ID cosmic)
		else:
			nbeBoucle = 4
			CreationLignes(list_ligne_temp,cmpt,compteurID,newLines,nbeBoucle)
	return newLines

def CreationLignes(list_ligne_temp,cmpt,compteurID,newLines,a):
	#pour chaque elements de la liste, recuperation des informations
	for i in range(len(list_ligne_temp[a])):
		ligne_temp = []
		for element in list_ligne_temp:
			# Si c'est une string, on ajoute dans list_ligne_temp.
			if type(element) == str:
				ligne_temp.append(element)
			# Si c'est une liste, on on traite chaque elements de la liste
			if type(element) == list:
				if type(element[compteurID]) == str:
					ligne_temp.append(element[compteurID])
				else:
					#boucle sur la longueur de la cellule info pour extraire chaque donnees
					for number in range(cmpt):
						if len(element[number]) == 1:
							#uniformisation du contenu de la liste
							temp = str(element[number])
							temp = temp.replace("[","")
							temp = temp.replace("]","")
							temp = temp.replace("'","")
							temp = legendes[number]+temp
							ligne_temp.append(temp)
						else:
							temp = legendes[number]+element[number][compteurID]
							ligne_temp.append(temp)
		#mise en forme comme VCF				
		list_VCF = ligne_temp[:]
		del list_VCF[7:]
		del ligne_temp[0:7]
		list_temptoString = ";".join(ligne_temp)
		list_temptoString += "\n"
		list_VCF.append(list_temptoString)
		newLines.append(list_VCF)
		#incrementation pour passer a un nouveau transcript de la meme ligne
		compteurID +=1
	return newLines


##############################################################
########					MAIN					  ########
##############################################################
#Fonction qui traite les lignes composees de plusieurs ID cosmic

def main_separation_transcripts(contentFile,ListOfList):
	list_newLines = []
	contentFileCleaned = CheckIfMultipleID(contentFile)
	list_ligne_temp = CreateListOfList(contentFileCleaned)
	cmpt = 0
	for i in list_ligne_temp:
		cmpt +=1
		TrieInformations(i)
		newLines = CheckIfSameLength(i)
		list_newLines.append(newLines)
	return list_newLines


