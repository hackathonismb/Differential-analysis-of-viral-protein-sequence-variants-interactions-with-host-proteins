import sys
file=open(sys.argv[1],"r")
def HTMLtoMatrix(file):
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
    dict[struct][resid1]={resid2:interaction}
   else:
    if resid2 not in dict[struct][resid1]:
     dict[struct][resid1][resid2]=interaction
    elif resid2 in dict[struct][resid1] and interaction != "contact":
     dict[struct][resid1][resid2]=interaction

 for struct in dict:
  outfile=open(struct+"_matrix.csv","w")
  outfile.write(","+','.join(Enodes[struct])+ '\r\n')
  for A in dict[struct]:
   row=A
   for i in Enodes[struct]:
    if i not in dict[struct][A]:
     row+=",0"
    else:
     row+=","+dict[struct][A][i]
   outfile.write(row+"\r\n")
  outfile.close()

HTMLtoMatrix(file)
