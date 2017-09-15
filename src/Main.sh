#! /bin/bash

for file in ../data/src_data/*
do
{
    out_file=`echo $file | cut -d \/ -f 4`
    log='../log_new/'$out_file'_log'
    ./run.sh $file > $log
    echo $out_file' completed'
}&
done
wait
