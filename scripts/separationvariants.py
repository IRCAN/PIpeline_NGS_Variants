import re

"""
Script pour separer une ligne du fichier VCF composee de plusieurs transcripts en plusieurs
lignes: une ligne par transcript.

Ludovic KOSTHOWA (06/04/16)
Info: Creation en cours, script peut etre modifie a tout moment.
"""

class SeparationVariants:

	def __init__(self,contentFile):

		"""Traite les lignes composees de plusieurs ID cosmic
		et cree de nouvelles lignes pour chaque identifiant.
		Retourne la liste des nouvelles lignes.

		@param	contentFile : contenu du fichier VCF
		@return listNewLines : liste des lignes ( un ID par ligne)."""

		self.LEGENDES = ['AF=','AO=','DP=','FAO=','FDP=','FR=','FRO=','FSAF=','FSAR=','FSRF=','FSRR=','FWDB=','FXX=','HRUN=','LEN=','MLLD=','OALT=','OID=','OMAPLAT=','OPOS=','OREF=','QD=','RBI=','REFB=','REVB=','RO=','SAF=','SAR=','SRF=','SRR=','SSEN=','SSEP=','SSSB=','STB=','STBP=','TYPE=','VARB=','']
		self.listNewLines = []
		self.contentFileCleaned = self.check_if_multiple_ID(contentFile)
		self.listLigneTemp = self.create_list_of_list(self.contentFileCleaned)
	
		for i in self.listLigneTemp:
			self.sort_informations(i)
			self.newLines = self.check_if_same_length(i)
			self.listNewLines.append(self.newLines)

	def check_if_multiple_ID(self,contentFile):
		"""Cree une liste composee seulement des lignes possedants plusieurs
		mutations. """
		contentFileList=[]
		for ligne in contentFile:
			contentFileList.append(ligne)
		listOflist=[]
		for ligne in contentFileList:
			lignesplit = ligne.split('\t')
			listOflist.append(lignesplit)
		count = 0
		multipleIDList = []
		for i in listOflist:
			ligne = i[4].split(",")
			#Si il y a plus (+) que une seule mutations, je cree une liste de ces ID.	
			if len(ligne) != 1:
				multipleIDList.append(contentFile[count])
			count += 1
		return multipleIDList

	def create_list_of_list(self,contentFile):
		"""Cree pour chaque ligne une liste de toutes les informations des
		differents identifiants cosmics. Cette liste est ajoutee dans une liste globale.
		Cette fonction permet de separer tout les elements necessaires a la
		separation des lignes composees de plusirs ID cosmics."""
		listContentFile = [] #liste du contenu du fichier
		#separation de contentFile par les tabulations
		listFinale =[]
		for element in contentFile:
			contentFile = element.split('\t')
			listContentFile.append(contentFile)
		for ligneChromosome in listContentFile:
			listLigneTemp = [] #liste temporaire correspondant a une ligne (1 transcript)
			listInfoTemp = []	#liste de la cellule INFO du fichier VCF
			listLigneInfoSort = []	#liste finale correspondant aux informations triees pour chaque transcript
			for element in ligneChromosome:
				#separation de contentFile par les ";"
				if ";" in element:
					temp = element.split(";")
					listInfoTemp.append(temp)
				#separation de contentFile par les ","
				elif "," in element:
					temp = element.split(",")
					listInfoTemp.append(temp)
				else:
					listInfoTemp.append(element)
			#traitement et separations des informations de la cellule INFO
			listInfoTemp[7][5] = listInfoTemp[7][5].replace(",","")
			for element in listInfoTemp[7]:
				listLigneTempElement7 = element.split(",")
				listLigneInfoSort.append(listLigneTempElement7)
			for element in listInfoTemp:
				if type(element) != list:
					listLigneTemp.append(element)
				elif type(element) == list:
					if element == listInfoTemp[7]:
						listLigneInfoSort = []
						for element in listInfoTemp[7]:
							listLigneTempElement7 = element.split(",")
							listLigneInfoSort.append(listLigneTempElement7)
						listLigneTemp.append(listLigneInfoSort)	
					else:
						listLigneTemp.append(element)
			#verification pour eviter saut de ligne dans fichier VCF
			if "\n" in listLigneTemp[-1]:
				listLigneTemp[-1] = listLigneTemp[-1].replace("\n","")
				listFinale.append(listLigneTemp)
			else:
				listFinale.append(listLigneTemp)
		return listFinale

	def sort_informations(self,listLigneTemp):
		"""Suppression des legendes (FAO,AF,AO,...) 
		par recherche d'une expression reguliere."""
		for i in listLigneTemp[7]:
			temp = str(i[0])
			temp = re.sub(r"([A-Z])+=","",temp)
			i[0] = temp

	def check_if_same_length(self,listLigneTemp):
		"""Verifie si la ligne possede le meme nombre d'ID cosmic
		que de mutations."""
		#nombre d'elements de la cellule INFO
		cmpt = len(listLigneTemp[7])
		newLines = []
		countID= 0
		#Pour chaque ligne , je cree une liste que je mets dans newLines
		#Verification si meme nombre ID cosmic que nombre de mutations
		if len(listLigneTemp[2]) == len(listLigneTemp[4]):
			loopNb = 4
			self.create_line(listLigneTemp,cmpt,countID,newLines,loopNb)
		else:
		#boucle sur le plus petit element
			#boucle sur ID cosmic
			if len(listLigneTemp[2]) < len(listLigneTemp[4]):
				loopNb = 2
				self.create_line(listLigneTemp,cmpt,countID,newLines,loopNb)
			#boucle sur le nombre de mutations (/!\ Possible perte du dernier ID cosmic)
			else:
				loopNb = 4
				self.create_line(listLigneTemp,cmpt,countID,newLines,loopNb)
		return newLines

	def create_line(self,listLigneTemp,cmpt,countID,newLines,a):
		"""Recupere les informations correspondants a chaque ID cosmic
		et cree une nouvelle ligne avec ces informations."""
		#pour chaque elements de la liste, recuperation des informations
		for i in range(len(listLigneTemp[a])):
			ligneTemp = []
			for element in listLigneTemp:
				# Si c'est une string, on ajoute dans listLigneTemp.
				if type(element) == str:
					ligneTemp.append(element)
				# Si c'est une liste, on on traite chaque elements de la liste
				if type(element) == list:
					if type(element[countID]) == str:
						ligneTemp.append(element[countID])
					else:
						#boucle sur la longueur de la cellule info pour extraire chaque donnees
						for number in range(cmpt):
							if len(element[number]) == 1:
								#uniformisation du contenu de la liste
								temp = str(element[number])
								temp = temp.replace("[","")
								temp = temp.replace("]","")
								temp = temp.replace("'","")
								temp = self.LEGENDES[number]+temp
								ligneTemp.append(temp)
							else:
								temp = self.LEGENDES[number]+element[number][countID]
								ligneTemp.append(temp)
			#mise en forme comme VCF				
			listVCF = ligneTemp[:]
			del listVCF[7:]
			del ligneTemp[0:7]
			listTemptoString = ";".join(ligneTemp)
			listTemptoString += "\n"
			listVCF.append(listTemptoString)
			newLines.append(listVCF)
			#incrementation pour passer a un nouveau transcript de la meme ligne
			countID +=1
		return newLines





