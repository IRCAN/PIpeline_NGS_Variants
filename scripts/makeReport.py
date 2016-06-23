#!/usr/bin/python
# coding: utf-8 

"""Script creant un rapport complet au format xls puis en pdf.
Ludovic KOSTHOWA (Debut : 06/04/16)
Info: Creation en cours, script peut etre modifie a tout moment.
"""

from openpyxl import *
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font


def pyxl(i, REPERTORYVCF):
	wb = Workbook()
	ws = wb.active
	ws.column_dimensions["A"].width = 20.0
	ws.column_dimensions["B"].width = 17.0		
	ws.column_dimensions["C"].width = 17.0
	ws.column_dimensions["D"].width = 22.0		
	ws.column_dimensions["E"].width = 22.0		
	ws.column_dimensions["F"].width = 17.0
	ws.column_dimensions["G"].width = 15.0
	ws.column_dimensions["H"].width = 15.0
	ws.column_dimensions["I"].width = 15.0
	ws.column_dimensions["J"].width = 25.0
	ws.column_dimensions["K"].width = 22.0
	ws.column_dimensions["L"].width = 30.0
	ws.title = "New Title"
	fichier2 = open("../Report_"+i+".txt","r")
	content = fichier2.readlines()
	border_thin = Border(left=Side(style='thin',color='FF000000'),right=Side(style='thin',color='FF000000'),top=Side(style='thin',color='FF000000'),bottom=Side(style='thin',color='FF000000'))
	alpahabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","AA","AB","AC","AD","AE","AF","AG","AH","AI","AJ","AK","AL","AM","AN","AO","AP","AQ","AR","AS","AT","AU","AV","AW","AX","AY","AZ","BA","BB","BC","BD","BE","BF","BG","BH","BI","BJ","BK","BL","BM","BN","BO","BP","BQ","BR","BS","BT","BU","BV","BW","BX","BY","BZ"]
	for row in range(len(content)):
		contentrowsplit = content[row].split("\t")
		# Met en gras les legendes
		if contentrowsplit[0] == "Gene":
			font = Font(name='Cal­ibri',size=11, bold=True)
		else:
			font = Font(name='Cal­ibri',size=11, bold=False)
		if len(contentrowsplit) == 1:
			cell = "A"+str(row+1)
			ws[cell] = content[row]
		else:
			for col in range(len(contentrowsplit)):
				cell = alpahabet[col]+str(row+1)
				ws[cell] = contentrowsplit[col]
				ws[cell].font = font
				ws[cell].border = border_thin
				ws[cell].alignment = Alignment(horizontal="center")
	wb.save("../Results/"+REPERTORYVCF+"/Rapport_Final_"+i+".xlsx")

#worksheet.column_dimensions["C"].width = 60.0