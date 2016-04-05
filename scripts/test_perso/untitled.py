file_input = "../../Data/Thibault/VariantsNGS.tsv"

file = open(file_input, "r")
content = file.readlines()
file.close()
ENS_id_Variants = []
print(content)
for i in content:
	s = i.split("\t")
	temp = s[1].replace("\n","")
	print(temp)
	ENS_id_Variants.append(temp)
listedecorrespondances = []
output= 'result.txt'
f = open(output, "r")
X = 1
while X:
	
	X = f.readline()
	if not "ENS" in X : continue
	
	s = X.split("\t")[1]
	if s in ENS_id_Variants :
		print(X)
		listedecorrespondances.append(X)

f.close()

#print(listedecorrespondances)
f_out = "result2.txt"
f  = open(f_out, "w")

for l in listedecorrespondances :

	
	f.write(l)
		
f.close()

print  ("Finish !")