#! /bin/bash

cd ../log
for f_log in *
do
    lines=`wc -l $f_log | awk -F' ' '{print $1}'`
    l=5001
    line=`expr $l - $lines`
    echo $lines' '$line
    file=`echo ${f_log:0:2}`
    tail -$line ../data/src_data_all/$file > ../data/src_data/$file
done
