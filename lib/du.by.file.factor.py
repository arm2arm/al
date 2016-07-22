#!/usr/bin/python

import os
import io
import sys

blocksize=512*512

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
    if os.path.isfile(filename):
	   s=os.stat(filename).st_size
           if s<blocksize:
              s=blocksize
 	   ssum+=s
	   nfiles+=1

filename= os.path.basename(lstfile)
print filename,':Nfiles - ',nfiles, ' - ',ssum/1024/1024/1024,' GB'
