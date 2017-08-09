var argvs=process.argv.slice(2)
var argvs_info=argvs.slice(0).toString().split(",")
var url=argvs_info[0]
var outhtml=argvs_info[1]



const request = require('superagent');
const fs = require('fs');

request
  .get(url)
  .set('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4')
  .end(function(err, res){
     fs.writeFile(outhtml , res.text, {
        encoding: 'utf8'
    }, () => {

    })
  });
