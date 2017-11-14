#!/home/kmm5/anaconda2/bin/python
##############################################################################################
### Revised on 10/02/13 ######################################################################
### re-Revised on 05/07/15 - made it to an executable - ######################################
### Edited on 03/29/17 (line 94): It now outputs DI as the third column.
##############################################################################################

import linecache

#take the name of files
align = raw_input("Alignment file name: ")
ranked = raw_input("Ranked DI file name: ")

#get information from manual alignment file
domain = linecache.getline(align, 1)
protein_id = linecache.getline(align, 6)[:4]

print '\nDomain:\t'+domain+'\nProtein ID:\t'+protein_id+'\n'
print 'generating matched alignment...\n'

d_init = int(linecache.getline(align, 2))
d_end = int(linecache.getline(align, 4))
p_init = int(linecache.getline(align, 7))
p_end = int(linecache.getline(align, 9))

#domain sequence string
l1 = linecache.getline(align, 3)
#protein sequence string
l2 = linecache.getline(align, 8)

x1 = len(l1)
x2 = len(l2)

output1 = open(align+"_reference.txt", "w")
output1.write('Domain \t n \t Protein \t n\n')

#get the difference between initial positions
delta = max(x1,x2)
#delta = max(d_end-d_init,p_end-p_init)

#domain code and respective number
d = []
dn = []
#protein code and respective number
p = []
pn = []

#fill d and p arrays with domain and protein sequences
for i in range(0,delta-1):
	d.append(l1[i])
	p.append(l2[i])

#compute the original positions in the system

j1=-1
j2=-1
for i in range(0,len(d)):
	if d[i]!='.':
		j1+=1
		dn.append(str(d_init+j1))
	if d[i]=='.':
		dn.append('')
	if p[i]!='-':
		j2+=1
		pn.append(str(p_init+j2))
	if p[i]=='-':
		pn.append('')
	output1.write(d[i]+'\t'+str(dn[i])+'\t'+p[i]+'\t'+str(pn[i])+'\n')


output1.close()

## Matching

output2 = open(align + "_mapped.fn", "w")

#open the ID file with ranking pairs
f=open(ranked,'r')

dic = {}

for i in range(0,len(dn)):
	if d[i]!='.' and p[i]!='-':
		dic[dn[i]]=pn[i]

#outer loop runs along all DCA pairs

for i in range(1,len(f.readlines())):
	pair = linecache.getline(ranked, i)
	pair1 = pair.split()[0]
	pair2 = pair.split()[1]
	try:
		if pair1 and pair2 in dic:
			output2.write(dic[pair1]+'\t'+dic[pair2]+'\t'+pair.split()[2]+'\n')
			# output2.write(dic[pair1]+'\t'+dic[pair2]+'\n')
	except KeyError:
		pass

output2.close()
print "\nFile saved as: "+align+"_mapped.fn\n\n"
