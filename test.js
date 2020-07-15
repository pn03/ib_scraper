const fs = require('fs');

function main(){
  let rawdata = fs.readFileSync('topics.json');
  let topics = JSON.parse(rawdata)['topics'];
  let count = 0;
  for(let i=0;i<topics.length;i++){
    let tn = topics[i].split("/")[6];
    let topic_name = tn.replace(/-/g,"_")
    let raw = fs.readFileSync("topics/"+tn+'.json');
    let problems = JSON.parse(raw)['problems'];
    console.log(tn+" "+problems.length)
    count = count+problems.length
  }
  console.log(count)
}

main();
