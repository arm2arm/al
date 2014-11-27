import os
import io
import sys
#import multiprocessing
class Logger(object):
    def __init__(self, filename="report.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)





ar=str(sys.argv)
path=sys.argv[1]
cachepath=sys.argv[2]
lstfile=cachepath+'/file.all.lst'
sys.stdout = Logger(cachepath+"/report.log")
print path, cachepath

exec_cmd='lfs find '+path+' -type f >  ' + lstfile


kb=1000 #roundup the kb
gb=kb*kb*kb
TSIZE=800*gb
numbertarsplits=20.0
ssize=0
thefiles=[]
thefilesize=[]


def dump_file(li,ntape,ssum,cph):

    the_filename=cph+'/splitted_'+str(ntape).zfill(6)
    thefiles.append(the_filename)
    thefilesize.append(ssum)
    with open(the_filename, 'w') as f:
        for item in li:
            f.write(item+"\n")
    print the_filename," - ",ssum,' - ',len(li),' - ',(ssum/(TSIZE*1.0))*100.0
    

os.system(exec_cmd)
f = os.popen(exec_cmd)
result = f.read()
print exec_cmd, result

def splitter(lstfile,splitsize,cph):
    tapesize=int(splitsize) #LTO6
    print tapesize
    lines = [line.rstrip() for line in open(lstfile)]
    ssum=0
    tsum=0
    ntape=0
    li=[]
    for filename in lines:
        if os.path.isfile(filename):
            s=os.path.getsize(filename)
            if s > tapesize:
                print  "single file size is bigger than tapesize\n it is not supported yet please split your file before archive"
                print tapesize,' - ',s,' ',filename
                sys.exit(0)
    
        if s+ssum>tapesize:
            if ssum==0:
                ssum=s
                li.append(filename)
            dump_file(li,ntape,ssum,cph)
            ssum=0;
            ntape+=1
            del li[:]
        
        li.append(filename)
        ssum+=s
        tsum+=s


    if len(li)>0:
        dump_file(li,ntape,ssum,cph)


    print 'Ntapes used:',ntape+1, ' - ',tsum



splitter(lstfile,TSIZE, cachepath)



#1) split thefiles 
#2) generate cache from splitted files
#3) write to tape directly splitted files

#tarcmd="/bin/tar cf "+cachepath+"/"+thefiles+".tar.cache -b 512 -T "+cachepath+"/"+thefile " --total"

#print thefiles

splcachedir="splcache"
splittedcache=cachepath+'/'+splcachedir
if not os.path.exists(splittedcache):
    os.makedirs(splittedcache)

realfiles=thefiles[:]
realsize=thefilesize[:]

i=0
for sf in realfiles:
    fs=realsize[i]/numbertarsplits
    print ">>>SPLITS-phaseII-",i," -- filesize=",fs," -- ", sf
    spli=splittedcache+"/"+str(i).zfill(3)
    if not os.path.exists(spli):
        os.makedirs(spli)
    numlines=int(os.popen("wc -l "+sf).readline().split()[0])
    thefiles=[]
    thefilesize=[]    
    splitter(sf,fs,spli)

    with open(spli+"/paralleljobs.queue", 'w') as f:
        for thef in thefiles:  
            f.write("/bin/tar cf "+thef+".tar -b 512 -T "+thef+"  --total\n")
    i+=1
     
     

