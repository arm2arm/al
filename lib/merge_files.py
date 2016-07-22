#!/usr/bin/python
# Some test case to generate ta file in parallel 
# Assuming we have N splits for final tar
# The merge algorithm is following:
# 1) merge neighbor pairs then select them as linear jobs
# 2) if no pairs exit if some pairs go to 1)
#example:
#   

import networkx as nx
import matplotlib.pyplot as plt
import sys

tarlist=[]
for line in sys.stdin:
   tarlist.append(line.rstrip()) 



path='/lnew/BACKUP/temp/cache/splcache/000/new/splitted_'
fname='tar -b 2048 --concatenate --file=%s  %s &'

col=[ "#00FFFF",  "#0000FF", "#FF00FF", "#008000", "#00FF00", "#800000", "#000080", "#808000", "#800080", "#FF0000", "#C0C0C0", "#008080", "#000000", "#FFFF00"]
slist = []
nsplits = len(tarlist) 

G=nx.DiGraph()

for i in range(0,nsplits):
    slist.append(i)
#print "#some linear jobs:"+slist

G.add_nodes_from(slist)

pas=0
while True:
    slist2=[]
    leftover=[]
    pas+=1
    while len(slist) > 1:
       a=slist.pop()
       b=slist.pop()
       slist2.append([b,a])
       G.add_edge(a,b,weight=pas,label=pas,color=col[pas])
    if len(slist)==1:
       leftover=slist
       #print("left over job",leftover)
    if len(slist2):
       #print("Iteration:",pas)
       #print("Merging tasks:",slist2)
       for i in slist2:
           print fname%(tarlist[i[0]],tarlist[i[1]]),
       print "wait"
#       print "#########"
    nojob=len(slist2)
    slist=leftover
    for i in slist2:
        slist.append(i[0])
    if nojob<1 :
       break 

print '#everything is merged to '+path+'%0.6d.tar'%(leftover[0])

pos=nx.spectral_layout(G) # positions for all nodes
nx.draw_networkx_edges(G,pos,width=1)
nx.draw_networkx_nodes(G,pos,node_size=700)
nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
plt.axis('off')
plt.savefig("path.png")
nx.write_dot(G,'file.dot')
