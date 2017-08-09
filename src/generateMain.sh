#! /bin/bash

for file in ../data/src_data/*
do
    out_file=`echo $file | cut -d \/ -f 4`
    log='../log/'$out_file'_log'
    echo './run.sh '$file' >'$log
    echo 'cd ..'
    echo 'rm -rf pages'
    echo 'mkdir pages'
    echo 'cd -'

    echo 'echo "'$out_file' completed "'
done
