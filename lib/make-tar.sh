#!/bin/bash
# usage: /work1/backup/al/lib/make-tar.sh /srv/zaip/cache/cosmdata2016/a 6 archcosmdata
path=$1
split=$2
bname=$3

nr=`ls $path/splitted_* |wc -l`

echo $nr

s=1
p=" "

for (( i=0; i<$nr; i+=1 )); do
n=$((i%$split))
if [ $n -eq 0 ] &&  [ $((i+split-nr)) -lt $((split-1))  ]; then

 if [ ! $i -eq 0 ]; then 
  echo "####"
  unlink  ${path}/splcache/${bname}${s}
  echo  "tapedev    lto6ultr"       | tee -a ${path}/splcache/${bname}${s}
  echo  "tapemach   alma018"        | tee -a ${path}/splcache/${bname}${s}
  echo  "machine    alma018"        | tee -a ${path}/splcache/${bname}${s}
  echo  "name    ${bname}${s}"       | tee -a ${path}/splcache/${bname}${s}
  echo  "path=$p"                   | tee -a ${path}/splcache/${bname}${s}
  s=$((s+1))
 fi

 p=" "
fi
printf -v j "%03d" $i

printf -v p " %s %s  " $p ${path}/splcache/$j 
echo  "cat ${path}/splcache/$j/paralleljobs.queue| parallel "|tee -a  ${path}/splcache/mktar-${s}.sh

done

echo "path=$p"

unlink  ${path}/splcache/${bname}${s}
echo  "tapedev    lto6ultr"       | tee -a ${path}/splcache/${bname}${s}
echo  "tapemach   alma018"        | tee -a ${path}/splcache/${bname}${s}
echo  "machine    alma018"        | tee -a ${path}/splcache/${bname}${s}
echo  "name    ${bname}${s}"       | tee -a ${path}/splcache/${bname}${s}
echo  "path=$p"                   | tee -a ${path}/splcache/${bname}${s}

