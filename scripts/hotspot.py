#!/usr/bin/python
# coding: utf-8 

"""
A COMMENTER EN MODE "comentaire de fichier"..
TODO : Si une liste de hotspot est fournie par l'utilisateur, HotspotProcess va regarder les si les differentes mutations sont presentes dans ces Hotposts.
Cela permettra de ressortir une liste des hotspots non mutes, avec la profondeur pour chacun de ces HSnm.
preciser HSnm et HSm"""

import re
import os

class HotspotProcess:

	def __init__(self,REPERTORYVCF,hotspot,list_of_transcripts,fichier):
		self.dicoHS = self.create_dico_HS(hotspot)
		#ajout dans le dictionnaire des profondeurs des variants
		self.find_depth_HSnm(list_of_transcripts,hotspot,self.dicoHS)
		#calcul et ajout de la profondeur mean et minimale de chaque hotspot 
		self.globalInfoHSnm = self.get_depth(self.dicoHS)
		#creation fichier de sortie du tableau Hotspots non mutes
		self.output_nmHS(fichier,self.globalInfoHSnm,REPERTORYVCF)

	def create_dico_HS(self, hotspots):
		"""Creation d'un dictionnaire a partir de la liste de hotspots avec:
		key = nomGene-numeroExon
		value = liste vide. """
		dicoHS = {}
		for hs in hotspots:
			key = hs[3]+'-'+hs[4]
			dicoHS[key] = []
		#Supprime la legende du tableau liste_hotspots
		del dicoHS["gene-exon"]
		return dicoHS

	def find_depth_HSnm(self,lignes,hotspots,dicoHS):
		"""Compare les variants non mutes (FAO = 0) du fichier avec le fichier liste_hotspots
		et ressort dans un dictionnaire les profondeurs des hotspots non mutes.
		key = nomGene-numeroExon
		value = profondeurDuVariant"""
		for l in lignes:
			ligne = l.split("\t")
			for hs in hotspots:
				if ligne[0] == hs[0] and int(hs[1]) <= int(ligne[1]) <= int(hs[2]):
					geneExon = hs[3]+'-'+hs[4]
					#recherche de la profondeur du variant par expression reguliere
					match = re.search(r"(FDP)=[0-9]*", ligne[7])
					result = match.group(0)
					result = int(result[4:])
					#ajout pour chaque variants du HS la profondeur.
					dicoHS[geneExon].append(result)				
		return dicoHS

	def get_depth(self,dicoHS):
		"""Calcul de la profondeur mean et minimale pour chaque HS."""
		for key,value in dicoHS.items():
			if not value : 
				dicoHS[key] = "N/A\tN/A\tN/A"
			else:
				#calcul de la profondeur mean pour le hotspot et arrondi de la value
				mean = round(sum(value) / len(value),2)
				#calcul de la profondeur minimale pour le hotspot
				minDepthHSnm = min(value)
				maxDepthHSnm = max(value)
				value = str(mean) + "\t" + str(minDepthHSnm)+ "\t" + str(maxDepthHSnm)
				dicoHS[key] = value
		return dicoHS

	def output_nmHS(self,nomFichier,globalInfoHSnm,REPERTORYVCF):
		"""Traitement du dictionnaire contenant les HS et leurs profondeurs puis ecriture dans un fichier tabule (utile pour le rapport final)."""
		HSnmGlobalList = []
		for key, value in globalInfoHSnm.items():
			hsLine = []
			#Separation du gene et de l'exon
			key = key.split("-")
			key = "\t".join(key)
			hsLine.append(key)
			hsLine.append(value)
			hsLine = "\t".join(hsLine)
			hsLine = hsLine+"\t"
			HSnmGlobalList.append(hsLine)
		#Trie de la liste de genes par ordre alphabetique pour meilleure lisibilite.
		HSnmGlobalList = sorted(HSnmGlobalList)
		HSnmGlobalList = "\n".join(HSnmGlobalList)
		f_out = "../Results/"+REPERTORYVCF+"/temp/nonMutatedHS_"+nomFichier
		File = open(f_out,'w')	# creation et ouverture du File
		File.write("Gene\texon\tMean Depth\tMinimal Depth\tMaximal Depth\t\n")	#Ecriture de la legende.
		for i in HSnmGlobalList:	#ecriture des donnees
			File.write(i)
		File.close()
		print('Creation de ',f_out,'\n')






