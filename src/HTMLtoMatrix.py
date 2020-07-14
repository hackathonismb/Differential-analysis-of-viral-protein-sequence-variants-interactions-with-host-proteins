import sys
filename=sys.argv[1]
def tableHTMLtoMatrix(filename):
 file=open(filename,"r")
 for i in range (2):
  file.readline()
 all_lines=file.readline().split("</td></tr></tbody></table></td></tr></thead>")
 entries=all_lines[1].split('<tr align="center">')
 dict,Enodes={},[]
 for entry in entries[1:]:
  entry=entry.strip('<th>').split('Highlight')[:-1]
  for sets in entry:
   sets=sets.split('nowrap')[1:]
   A,E=sets[0].split("id=")[1:],sets[1].split("id=")[1:-1]
   classA=A[0].split()[0][1:-2] #E should have the same class
   resA=A[1].split('"> ')[1].split(' <span style="background-color:')[0].split()
   Elist=E[1].split('<td align="center">')[:-1]
   resE=Elist[0].split('"> ')[1].split(' <span style="background-color:')[0].split()
   resA,resE=resA[0]+resA[1].split(":")[-1],resE[0]+resE[1].split(":")[-1]
   resA,resE=resA.split("@"),resE.split("@")
   if resE[0] not in Enodes:
    Enodes.append(resE[0])
   Elist=[s.replace('</td>', '') for s in Elist[1:]]
   Elist.append(resA[1]+"-"+resE[1])
   if len(Elist) < 4:
    bond=classA.split("_")[1][:-1]
    Elist.append(bond)
   if resA[0] not in dict:
    dict[resA[0]]={resE[0]:[Elist]}
   else:
    if resE[0] not in dict[resA[0]]:
     dict[resA[0]][resE[0]]=[Elist]
    else:
     dict[resA[0]][resE[0]].append(Elist)
 struct=filename.split("-")[0]
 ofile1=open(struct+"_NumContact.csv","w")
 ofile2=open(struct+"_MinDistance.csv","w")
 ofile3=open(struct+"_C-alphaDistance.csv","w")
 ofile1.write(","+','.join(Enodes)+ '\r\n')
 ofile2.write(","+','.join(Enodes)+ '\r\n')
 ofile3.write(","+','.join(Enodes)+ '\r\n')
 for A in dict:
  row1,row2,row3=A,A,A
  for E in Enodes:
   if E not in dict[A]:
    row1+=",0"
    row2+=",0"
    row3+=",0"
   else:
    if len(dict[A][E]) == 1 and len(dict[A][E][0]) == 4:
     row1+=","+dict[A][E][0][0]
     row2+=","+dict[A][E][0][1]
     row3+=","+dict[A][E][0][2]
    elif len(dict[A][E]) ==  1 and len(dict[A][E][0]) < 4:
     row1+=",0"
     row2+=","+dict[A][E][0][0]
     row3+=",0"
    elif len(dict[A][E]) > 1:
     for grp in dict[A][E]:
      if len(grp) == 4:
       row1+=","+grp[0]
       row2+=","+grp[1]
       row3+=","+grp[2]
  ofile1.write(row1+"\r\n")
  ofile2.write(row2+"\r\n")
  ofile3.write(row3+"\r\n")
 ofile1.close()
 ofile2.close()
 ofile3.close()

tableHTMLtoMatrix(filename)

def linegraphtoMatrix(filename):
 file=open(filename,"r")
 for i in range (2):
  file.readline()
 all_lines=file.readline().split("<title>")
 colors=all_lines[0].split("<span")
 interactions={'#888':'contact'}
 for color in colors[1:]:
  if color.startswith(" style") and "Grey" not in color:
   color=color.split("</div>")[0].split('; font-weight:bold">')
   fullcode=color[0].split("color:")[-1]
   codeused=fullcode[:2]+fullcode[4]+fullcode[6] 
   interaction=color[-1].split(":")[-1].strip().strip(";")
   interactions[codeused]=interaction
 dict,Enodes={},{}
 for ln in all_lines[1:]:
  struct=ln.split("resid")[-1].split("_")[0].split('="')[1]
  if struct not in dict:
   dict[struct]={}
   Enodes[struct]=[]
  if not ln.startswith("Interaction"):  
   ln=ln.split("fill=")
   node=ln[0].split("</title>")[0]
   struct=node.split(".")[-1]
   color=ln[1].split()[0].strip('"')  ##color for conservation info
   if node.split(".")[1] == "E":
    Enodes[struct].append(node)
  else:
   ln=ln.split('stroke="')
   color=ln[1].split('"')[0]
   interaction=interactions[color]
   ln=ln[0].split("residue")
   resid1=ln[1].split("with")[0].strip().split("_")[0]
   resid2=ln[2].split("</title>")[0].strip().split("_")[0]
   struct=resid1.split(".")[-1]
   if resid1 not in dict[struct]:
    dict[struct][resid1]={resid2:[interaction]}
   else:
    if resid2 not in dict[struct][resid1]:
     dict[struct][resid1][resid2]=[interaction]
    elif resid2 in dict[struct][resid1]:
     dict[struct][resid1][resid2].append(interaction)

 for struct in dict:
  outfile=open(struct+"_matrix.csv","w")
  outfile.write(","+','.join(Enodes[struct])+ '\r\n')
  for A in dict[struct]:
   row=A
   for i in Enodes[struct]:
    if i not in dict[struct][A]:
     row+=",0"
    else:
     interaction=""
     for j in dict[struct][A][i]:
      interaction+=j+"_"
     row+=","+interaction.strip("_")
   outfile.write(row+"\r\n")
  outfile.close()

#linegraphtoMatrix(filename) #using 6M0J-2AJF-linegraph.html from Link 10
