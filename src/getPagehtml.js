var argvs=process.argv.slice(2)
var argvs_info=argvs.slice(0).toString().split(",")
var url=argvs_info[0]
var outhtml=argvs_info[1]



const request = require('superagent');
const fs = require('fs');

request
  .get(url)
  .end(function(err, res){
     fs.writeFile(outhtml , res.text, {
        encoding: 'utf8'
    }, () => {

    })
  });
