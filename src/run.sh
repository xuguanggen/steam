#! /bin/bash

input_file=$1
out_file='../userinfo/'`echo $input_file | cut -d \/ -f 4`
echo $input_file
#echo $out_file

url_head='https://steamcommunity.com'

cat $input_file | while read line;
do
    {
        python3 ./tool.py $line
        if [ $? == 0 ];then
            echo $line
        else
            
            name=`echo $line | cut -d \/ -f 2`
            url=$url_head'/'$line
            badge_url=$url'/badges'
            game_url=$url'/games/?tab=all'
            group_url=$url'/groups'
            friend_url=$url'/friends'

            badge_html='../pages/'$name'_badge.html'
            game_html='../pages/'$name'_game.html'
            group_html='../pages/'$name'_group.html'
            friend_html='../pages/'$name'_friend.html'

            #echo $name
            node ./getPagehtml.js $badge_url $badge_html
            node ./getPagehtml.js $game_url $game_html
            node ./getPagehtml.js $group_url $group_html
            node ./getPagehtml.js $friend_url $friend_html
            
            python3 utils_v2.py $url $badge_html $game_html $group_html $friend_html $out_file
        fi
    }&
done
wait
