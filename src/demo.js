const request = require('superagent');
const fs = require('fs');

request
  .get('http://steamcommunity.com/id/afarnsworth/games/?tab=all&content_only=true')
  .end(function(err, res){
     fs.writeFile('2.html', res.text, {
        encoding: 'utf8'
    }, () => {

    })
  });
