#! /bin/bash

input_file='../data/url_uniq.txt'

url_head='https://steamcommunity.com/'
url_tail='/games/?tab=all'

for line in `cat $input_file`
do
    url=$url_head$line$url_tail
    name=`echo $line | cut -d \/ -f 2`
    node ./getPagehtml.js  $url  ../gamespages/$name'.html'
    python3 ./user_game.py $url_head$line ../gamespages/$name'.html'
    rm ../gamespages/$name'.html'
    sleep 5
done
