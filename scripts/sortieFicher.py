from xlwt import Workbook
 
# création 
book = Workbook()
 
# création de la feuille 1
feuil1 = book.add_sheet('feuille 1')
 
# ajout des en-têtes
feuil1.write(0,0,'id')
feuil1.write(0,1,'x')
feuil1.write(0,2,'y')
feuil1.write(0,3,'test')
 
# ajout des valeurs dans la ligne suivante
ligne1 = feuil1.row(1)
ligne1.write(0,'1')
ligne1.write(1,'235.0')
ligne1.write(2,'424.0')
ligne1.write(3,'a')

 
# ajustement éventuel de la largeur d'une colonne
feuil1.col(0).width = 10000
 
# éventuellement ajout d'une autre feuille 2
feuil2 = book.add_sheet('feuille 2')

 
 
# création matérielle du fichier résultant
book.save('monsimple.xls')
