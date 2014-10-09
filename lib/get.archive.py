import os
import io
import sys
#import multiprocessing


lstfile='file.all.lst'
#path='/archive/arm2arm/'
ar=str(sys.argv)
path=sys.argv[1]
print path

exec_cmd='lfs find '+path+' -type f >  ' + lstfile
thefiles=[]
kb=1000 #roundup the kb
gb=kb*kb*kb
tapesize=2500*gb #LTO6
print tapesize,' ',kb


def dump_file(li,ntape):
    the_filename='splitted_'+str(ntape).zfill(6)
    thefiles.append(the_filename)
    with open(the_filename, 'w') as f:
        for item in li:
            f.write(item+"\n")
    print the_filename," - ",ssum,' - ',len(li)
    



os.system(exec_cmd)
f = os.popen(exec_cmd)
result = f.read()
print exec_cmd, result

lines = [line.rstrip() for line in open(lstfile)]
ssum=0
tsum=0
ntape=0
li=[]

for filename in lines:
    s=os.path.getsize(filename)
    if s > tapesize:
        print  "single file size is bigger than tapesize\n it is not supported yet please split your file before archive"
        print tapesize/(kb*kb*kb),' - ',s/(kb*kb*kb),' ',filename
        sys.exit(0)

    if s+ssum>tapesize:
        dump_file(li,ntape)
        ssum=0;
        ntape+=1
        del li[:]
    li.append(filename)
    ssum+=s
    tsum+=s

if len(li)>0:
    dump_file(li,ntape)

print 'Ntapes used:',ntape+1, ' - ',tsum

#1) split thefiles 
#2) generate cache from splitted files
#3) write to tape directly splitted files

#tarcmd="/bin/tar cf "+cachepath+"/"+thefiles+".tar.cache -b 512 -T "+cachepath+"/"+thefile " --total"
#print tarcmd
