#this script generates file names first then copy this in parallel
#usage:
#1) copy-dir-in-parallel.sh /lustre/arm2arm backup241:/lustre
#1) copy-dir-in-parallel.sh /lustre/arm2arm backup241:/lustre lfs
lustre=lfs
lustre=$3
mode=$4
procs=$5
src=$1
dst=$2
name=$(echo "$src" | tr / -)
dname=$(echo "$dst" | tr / -| tr : -)
time=$(date +"%Y%m%d-%H%M")
logdir=/work1/tmp/var/logs/copy-dir-in-parallel
logfile=$logdir/${time}${name}-${dname}.log
folder=$(basename $src)

workdir=/work1/tmp/psync/parallel-sync-${time}-$folder
jobqueuefile=/work1/tmp/var/log/jobqueue.parallel.$folder
mkdir -p $logdir
mkdir -p $workdir

touch  $logfile

cd $workdir

dirs=$workdir/dirs.log
files=$workdir/files.log

#rsync --log-file=${logfile} -au /glu/$1 /lustre

cd $src && $lustre find . -type d > ${dirs} 
cd $src && $lustre find . -type f > ${files}
nfiles=$(wc -l ${files}| cut -d ' ' -f1 )
ndirs=$(wc -l ${dirs}  | cut -d ' ' -f1)

echo "Found files:$nfiles in $ndirs folders."
cd $workdir
split -l 8 -d -a 6 ${files} files_
truncate -s 0 $jobqueuefile

for i in files_??????
do
truncate -s 0 ${workdir}/${i}.log 
echo "rsync  -aH --no-l  -e 'ssh -c arcfour '  --files-from=$workdir/${i} --log-file=${workdir}/${i}.log $src $dst/${folder}/ && bzip2 ${workdir}/${i}.log" >> $jobqueuefile 
done 

pwd 
echo '#queue is ready, please run, you cah edit line for remote servers as well:  parallel -P4 -Slei1,lei2,lei3'
echo "cat $jobqueuefile | parallel -P4 --progress "
cat $jobqueuefile | parallel   -P8  

echo rsync -a --delete $src $dst
