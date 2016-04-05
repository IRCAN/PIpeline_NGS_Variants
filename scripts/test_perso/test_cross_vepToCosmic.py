
f_vep = '../../Resultats/VEP/VEP_NOUVELLE_CMD_TSVC_variants_IonXpress_001.vcf'
f = open(f_vep, "r")
L = f.readlines()
f.close()
del L[0:42]
#print(L)
ENS_id = []
ENS_id_ok = []
X_id_ok = []

print ("\n=> Cross IDs from VEP file with Cosmic data")
print ("Waiting...")

for l in L:
	
	s = l.split("\t")[4]
	print(s)
	if "ENST"  in s :
		ENS_id.append(s)
		
#print(ENS_id)

f_cosmic = '../../../Data/Original/CosmicCompleteExport.tsv'
f = open(f_cosmic, "r")

#########

X = 1
j=0
while X:
	
	X = f.readline()
	
	if not "ENST" in X : continue
	
	s = X.split("\t")[1]
	
	#print s
	#print ENS_id
	
	if s in ENS_id :
		ENS_id_ok.append(s)
		X_id_ok.append(X)
		print(X)
		
	j+=1
	
	#if j >50000 : break

f.close()

#print ENS_id_ok
print(len(ENS_id))
print(len(ENS_id_ok))
ENS_id_ok = list(set(ENS_id_ok))
#print(ENS_id_ok)
#print len(ENS_id_ok)

f_out = "result.txt"
f  = open(f_out, "w")

for l in X_id_ok :
	f.write(l)
		
f.close()

print  ("Finish !")

sys.exit()