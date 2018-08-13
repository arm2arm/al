#!/usr/bin/python
import os
import io
import sys

ar=str(sys.argv)
if len(sys.argv) != 3:
   print "Wrong number of parameters."
   print "Usage: "+sys.argv[0]+" path_to_backup_dirlist  path_to_cache"
   exit(0)


dirfile=sys.argv[1]
lstfile=sys.argv[2]
lstf = open(lstfile, 'w')
s=0
ssum=0
nfiles=0

lines = [line.rstrip() for line in open(dirfile)]
for dirname in lines:
    if os.path.isdir(dirname):
       filenames = [entry for entry in os.listdir(dirname) if os.path.isfile(os.path.join(dirname,entry))]
       for filename in filenames:
           f=os.path.join(dirname,filename)
           lstf.write(f+'\n')
           s=os.stat(f).st_size
           ssum+=s
           nfiles+=1

filename= os.path.basename(lstfile)
print filename,':Nfiles - ',nfiles, ' - ',ssum/1024/1024/1024,' GB'
lstf.close();
