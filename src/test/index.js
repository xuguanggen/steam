const Promise = this.Promise || require('promise');
const request = require('superagent-promise')(require('superagent'), Promise);
const fs = require('fs');
const cheerio = require('cheerio');
const CircularJSON = require('circular-json-es6')
const url = process.argv[2];
const out_file = process.argv[3];
request
    .get(url)
    .set('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4')
    .end()
    .then((res) => {
        const $ = cheerio.load(res.text);
        // 姓名
        const userInfo = {};
        //console.log($('.actual_persona_name').text());
        userInfo.name = $('.actual_persona_name').text();
        userInfo.profile = $('.profile_summary').text().replace(/[\'\"\\\/\b\f\n\r\t]/g, '');
        const badgeUrl = $('.profile_header_badgeinfo_badge_area').children('a').attr('href');
        const groupsUrl = $('.profile_group_links').children('.ellipsis').children('a').attr('href');
        const friendsUrl = $('.profile_friend_links').children('.ellipsis').children('a').attr('href');
        const gamesUrl = $('.profile_item_links').children('.ellipsis').children('a').attr('href');

        const badgeP = request.get(badgeUrl).set('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4').end();
        const groupsP = request.get(groupsUrl).set('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4').end();
        const friendsP = request.get(friendsUrl).set('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4').end();
        const gamesP = request.get(gamesUrl).set('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4').end();
        Promise.all([badgeP, groupsP, friendsP, gamesP]).then((res) => {
          const badgeP$ = cheerio.load(res[0].text);
          const groupsP$ = cheerio.load(res[1].text);
          const friendsP$ = cheerio.load(res[2].text);
          const gamesP$ = cheerio.load(res[3].text);
          userInfo.level = badgeP$('.friendPlayerLevelNum').text();
          userInfo.xp = badgeP$('.profile_xp_block_xp').text().split(" ")[0];
          userInfo.next_level = badgeP$('.profile_xp_block_remaining').text().split(" ")[1]
          userInfo.remain_experience = badgeP$('.profile_xp_block_remaining').text().split(" ")[3]
          userInfo.badge = [];
          userInfo.groups = [];
          userInfo.friends = [];
          badgeP$('.badge_row.is_link').each((index, item) => {
            // console.log($(item).children('.badge_row_inner').children('.badge_title_row').children('.badge_title').text());
            // console.log($(item).children('.badge_row_inner').children('.badge_content').children('.badge_current').children('.badge_info').children('.badge_info_description').children('div').eq(1).text());
            const data = {
              name: $(item).children('.badge_row_inner').children('.badge_title_row').children('.badge_title').text().replace(/[\'\"\\\/\b\f\n\r\t]/g, '').replace('查看详情',''),
              xp: $(item).children('.badge_row_inner').children('.badge_content').children('.badge_current').children('.badge_info').children('.badge_info_description').children('div').eq(1).text().replace(/[\'\"\\\/\b\f\n\r\t]/g, '').replace('级','').replace(' 点经验值','')
            }
            userInfo.badge.push(data);
          })
          groupsP$('.groupBlock').each((index, item) => {
            const data = {
              url: $(item).children('p').children('.linkTitle').attr('href'),
              name: $(item).children('p').children('.linkTitle').text()
            }
            userInfo.groups.push(data);
          })
          friendsP$('.friendBlock').each((index, item) => {
            const data = {
              name: $(item).children('.friendBlockContent').text().split('\n')[1].replace(/[\'\"\\\/\b\f\n\r\t]/g, ''),
              url: $(item).children('.friendBlockLinkOverlay').attr('href')
            }
            userInfo.friends.push(data);
          })
          gamesP$('script').each((index, item) => {
            if(index == 12) {
              const match = $(item).html().match(/.*var rgGames = (.*)/);
              const tmp_games = eval(match[1]);
              var data_arry = new Array(tmp_games.length);
              for(var i=0; i<tmp_games.length; i++){
                var appid = tmp_games[i]['appid'];
                var name = tmp_games[i]['name'];
                var hours_forever = -1;
                if ('hours_forever' in tmp_games[i]){
                  hours_forever = tmp_games[i]['hours_forever']
                }
                const data = {
                  id: appid,
                  name: name,
                  hours_forever: hours_forever
                }
                data_arry[i] = data;
                //console.log(appid);
                //console.log(name);
                //console.log(hours_forever);
              }
              userInfo.games = data_arry;
              //console.log(userInfo.games.length);
            }
          })
          // console.log(userInfo);
          let data = CircularJSON.stringify(userInfo);
          data += '\r\n';
          fs.writeFile(out_file, data, {
            encoding: 'utf-8',
            flag: 'a+'
          }, (err, res) => {
            if(err) {
              console.log('写文件出错');
            }
          })
          // return userInfo;
          // process.stdout.write(userInfo);
        }, err => {
          console.log(err, 'promise');
        })
    }, err => {
      console.log(err, 'request');
    })
