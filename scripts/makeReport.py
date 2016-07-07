#!/usr/bin/python
# coding: utf-8 

"""Script creant un rapport complet au format xls puis en pdf.
Ludovic KOSTHOWA (Debut : 06/04/16)
Info: Creation en cours, script peut etre modifie a tout moment.
"""

from openpyxl import *
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from pdfrw import PdfWriter
import os

class MakeReport:
	def __init__(self,REPERTORYVCF,i):
		self.report_body(REPERTORYVCF,i)



	def report_body(self,REPERTORYVCF,i):
		report = open("../Results/"+REPERTORYVCF+"/temp/Report_"+i+".txt", "w")
		report.write("Report of "+i+"  from  "+REPERTORYVCF+"\n\n")
		if os.path.exists("../Results/"+REPERTORYVCF+"/"+REPERTORYVCF+"_globalInformations.txt") == True:
			report.write("Informations:")
			report.write("\n")
			File = "../Results/"+REPERTORYVCF+"/"+REPERTORYVCF+"_globalInformations.txt"
			with open(File,'r') as file:
				file = file.readlines()
				legendes = str(file[0])
				legendesReplace = legendes.replace(", ","\t")
				legendesReplace = legendesReplace.replace("\n","")
				report.write(legendesReplace)
				report.write("\n")
				for element in file:
					element = element.replace(", ","\t")
				if i in element:
					report.write(element)
			report.write("\n")
		notAlreadyDone=True
		if os.path.exists("../Results/"+REPERTORYVCF+"/temp/HSm_"+i+".vcf") == True:
			notAlreadyDone=False
			report.write("Inside Hotspots Panel:")
			report.write("\n")
			report.write("Mutated Hotspots:")
			report.write("\n")
			File = "../Results/"+REPERTORYVCF+"/temp/HSm_"+i+".vcf"
			with open(File,'r') as file:
				file = file.readlines()
				for element in file:
					report.write(element)
			report.write("\n")
		if os.path.exists("../Results/"+REPERTORYVCF+"/temp/HSm_questionable_"+i+".vcf") == True:
			if notAlreadyDone:
				report.write("Inside Hotspots Panel:")
				report.write("\n")
			report.write("No significant mutations:")
			report.write("\n")
			File = "../Results/"+REPERTORYVCF+"/temp/HSm_questionable_"+i+".vcf"
			with open(File,'r') as file:
				file = file.readlines()
				for element in file:
					report.write(element)
			report.write("\n")
		if os.path.exists("../Results/"+REPERTORYVCF+"/temp/nonMutatedHS_"+i+".vcf")== True:
			report.write("Couverture Hotspots:")
			report.write("\n")
			File = "../Results/"+REPERTORYVCF+"/temp/nonMutatedHS_"+i+".vcf"
			with open(File,'r') as file:
				file = file.readlines()
				for element in file:
					report.write(element)
			report.write("\n")
			report.write("\n")
		report.write("Outside Hotspots Panel:")
		report.write("\n")
		if os.path.exists("../Results/"+REPERTORYVCF+"/temp/mutations_"+i+".vcf")== True:
			report.write("Mutations:")
			report.write("\n")
			File = "../Results/"+REPERTORYVCF+"/temp/mutations_"+i+".vcf"
			with open(File,'r') as file:
				file = file.readlines()
				for element in file:
					report.write(element)
			report.write("\n")
		if os.path.exists("../Results/"+REPERTORYVCF+"/temp/uncertain_mutation_"+i+".vcf")== True:
			report.write("Uncertain mutation: (cov < 300)")
			report.write("\n")
			File = "../Results/"+REPERTORYVCF+"/temp/uncertain_mutation_"+i+".vcf"
			with open(File,'r') as file:
				file = file.readlines()
				for element in file:
					report.write(element)
			report.write("\n")
		"""if os.path.exists("../Results/"+REPERTORYVCF+"/temp/Polymorphism_"+i+".vcf")== True:
			report.write("Polymorphism:")
			report.write("\n")
			File = "../Results/"+REPERTORYVCF+"/temp/Polymorphism_"+i+".vcf"
			with open(File,'r') as file:
				file = file.readlines()
				for element in file:
					report.write(element)
		report.write("\n")"""
		if os.path.exists("../Results/"+REPERTORYVCF+"/temp/no_contributory_"+i+".vcf")== True:
			report.write("No contributory mutations: (NOCALL or allele_freq < 1%  or < 25 reads)")
			report.write("\n")
			File = "../Results/"+REPERTORYVCF+"/temp/no_contributory_"+i+".vcf"
			with open(File,'r') as file:
				file = file.readlines()
				for element in file:
					report.write(element)
			report.write("\n")

		
		report.close()




	def pyxl(self,i, REPERTORYVCF):
		wb = Workbook()
		ws = wb.active
		ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
		ws.page_setup.paperSize = ws.PAPERSIZE_TABLOID
		#####
		# Largeur des colonnes
		#####
		ws.column_dimensions["A"].width = 10.0
		ws.column_dimensions["B"].width = 10.0		
		ws.column_dimensions["C"].width = 10.0
		ws.column_dimensions["D"].width = 12.0		
		ws.column_dimensions["E"].width = 12.0		
		ws.column_dimensions["F"].width = 10.0
		ws.column_dimensions["G"].width = 10.0
		ws.column_dimensions["H"].width = 10.0
		ws.column_dimensions["I"].width = 12.0
		ws.column_dimensions["J"].width = 12.0
		ws.column_dimensions["K"].width = 12.0
		ws.column_dimensions["L"].width = 14.0
		ws.column_dimensions["M"].width = 6.0
		ws.column_dimensions["N"].width = 6.0
		#Titre du fichier
		ws.title = i
		fichier2 = open("../Results/"+REPERTORYVCF+"/temp/Report_"+i+".txt","r")
		content = fichier2.readlines()
		border_thin = Border(left=Side(style='thin',color='FF000000'),right=Side(style='thin',color='FF000000'),top=Side(style='thin',color='FF000000'),bottom=Side(style='thin',color='FF000000'))
		alpahabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","AA","AB","AC","AD","AE","AF","AG","AH","AI","AJ","AK","AL","AM","AN","AO","AP","AQ","AR","AS","AT","AU","AV","AW","AX","AY","AZ","BA","BB","BC","BD","BE","BF","BG","BH","BI","BJ","BK","BL","BM","BN","BO","BP","BQ","BR","BS","BT","BU","BV","BW","BX","BY","BZ"]
		for row in range(len(content)):
			contentrowsplit = content[row].split("\t")
			# Met en gras les legendes
			if contentrowsplit[0] == "Gene" or contentrowsplit[0] == "Sample":
				font = Font(name='Arial',size=8, bold=True)
			else:
				font = Font(name='Arial',size=8, bold=False)
			if len(contentrowsplit) == 1:
				font = Font(name='Arial',size=10, bold=True, underline='single')
				cell = "A"+str(row+1)
				ws[cell] = content[row]
				ws[cell].font = font
			else:
				for col in range(len(contentrowsplit)):
					if col == len(contentrowsplit)-1:
						cell = alpahabet[col]+str(row+1)
						ws[cell] = contentrowsplit[col]
						ws[cell].font = font
						ws[cell].alignment = Alignment(horizontal="center",vertical="center")
					else:
						cell = alpahabet[col]+str(row+1)
						ws[cell] = contentrowsplit[col]
						ws[cell].font = font
						ws[cell].border = border_thin
						ws[cell].alignment = Alignment(horizontal="center",vertical="center")
		wb.save("../Results/"+REPERTORYVCF+"/Report_"+i+".xlsx")
		a = "libreoffice --headless --invisible --convert-to pdf --outdir ../Results/"+REPERTORYVCF+" ../Results/"+REPERTORYVCF+"/Report_"+i+".xlsx"
		os.system(a)
		os.chdir("../Results/"+REPERTORYVCF+"/")
		c = "tar cf Report_"+i+".tar Report_"+i+".xlsx Report_"+i+".pdf"
		os.system(c)
		os.remove("Report_"+i+".xlsx")
		os.remove("Report_"+i+".pdf")
		os.chdir("../../scripts")





