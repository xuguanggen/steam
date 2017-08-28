#! /bin/bash

for file in ../data/src_data/*
do
{
    out_file=`echo $file | cut -d \/ -f 4`
    log='../log/'$out_file'_log'
    ./run.sh $file > $log
    echo $out_file' completed'
    #ps -ef | grep run.sh | awk -F' ' '{print $2}' | xargs kill -9
    #ps -ef | grep node | awk -F' ' '{print $2}' | xargs kill -9
}&
done
wait
echo 'all fucked...'
