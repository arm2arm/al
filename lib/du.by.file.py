#!/usr/bin/python

import os
import io
import sys

ar=str(sys.argv)
if len(sys.argv) != 2:
   print "Wrong number of parameters."
   print "Usage: "+sys.argv[0]+" path_to_backup_list_file "
   exit(0)


lstfile=sys.argv[1]
s=0
ssum=0
nfiles=0

lines = [line.rstrip() for line in open(lstfile)]
for filename in lines:
    #print filename
    if os.path.isfile(filename):
	   s=os.stat(filename).st_size
	   ssum+=s
	   nfiles+=1
	   #print ssum

filename= os.path.basename(lstfile)
print filename,':Nfiles - ',nfiles, ' - ',ssum/1024.0/1024.0/1024.0,' GB'
