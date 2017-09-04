#! /bin/bash

input_file=$1
out_file='../game_info/'`echo $input_file | cut -d \/ -f 4`
#echo $input_file
#echo $out_file

url_head='https://steamcommunity.com'

for line in `cat $input_file`
do
    python3 ./tool.py $line
    if [ $? == 0 ];then
        echo $line
    else
        
        name=`echo $line | cut -d \/ -f 2`
        url=$url_head'/'$line
        game_url=$url'/games/?tab=all'

        game_html='../gamespages/'$name'_game.html'

        #echo $name
        node ./getPagehtml.js $game_url $game_html
        
        #sub_out_file='../tmp/'$name
        #python3 utils_v2.py $url $badge_html $game_html $group_html $friend_html $out_file
        python3 ./game.py $url $game_html $out_file

        rm $game_html
    fi
done
#wait
#cat ../tmp/* > $out_file
#rm ../tmp/*
echo $input_file' fuck'
