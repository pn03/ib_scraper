const puppeteer = require('puppeteer');
const iPadProLandscape = puppeteer.devices['iPad Pro landscape'];
const fs = require('fs');
const fse = require('fs-extra');
const {exec} = require("child_process");
const cheerio = require('cheerio');
const axios = require('axios');

let programming_url = "https://www.interviewbit.com/courses/programming";

const problemDict = {
  container:'#problem-content',
  titleContainer:'.css-v3d350',
  suffix:'',
  hintSelector:'div.css-isal7m',
  topicSelector:'.topic-tag__1jni',
  imgSelector:'#problem-content > img',
}

async function downloadImage (url,path) {  
  const writer = fs.createWriteStream(path)
  const response = await axios({
    url,
    method: 'GET',
    responseType: 'stream'
  })
  response.data.pipe(writer)
  return new Promise((resolve, reject) => {
    writer.on('finish', resolve)
    writer.on('error', reject)
  })
}

function getProblemLinks (url) {
  return new Promise(async (resolve, reject) => {
      try {
          const browser = await puppeteer.launch();
          const page = await browser.newPage();
          await page.emulate(iPadProLandscape);
          console.log(url);
          await page.goto(url,{waitUntil:'load'});
          await page.waitFor(5000);
          // await page.screenshot({path: 'screenshot.png'});
          let result = await page.evaluate(() => {
            let pr = document.querySelectorAll("tr[id*='problem'");
            let ret = {};
            ret['problems'] = []
            pr.forEach(element => {
              let tmp={};
              tmp['problem_id']=Number.parseInt(element.attributes.id.value.split("_")[1]);
              tmp['problem_name']=element.children[0].innerText;
              tmp['problem_link']=element.children[0].querySelector("a").href;
              tmp['problem_score']=Number.parseInt(element.children[1].innerText);
              tmp['time_to_solve']=element.children[3].innerText;
              ret['problems'].push(tmp);
            });
            return ret;
          })
          
          await page.waitFor(5000);
          await browser.close();
          return resolve(result);
      } catch (e) {
          return reject(e);
      }
  })
}
function getTopics(url){
  return new Promise(async (resolve, reject) => {
    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.emulate(iPadProLandscape);
        console.log(url);
        await page.goto(url,{waitUntil:'load'});
        await page.waitFor(5000);
        let result = await page.evaluate(() => {
          let pr = document.querySelectorAll('a[href*="programming/topics/"]');
          let ret = {};
          ret['topics'] = []
          pr.forEach(element => {
            ret['topics'].push(element.href);
          });
          return ret;
        })
        
        await page.waitFor(5000);
        await browser.close();
        return resolve(result);
    } catch (e) {
        return reject(e);
    }
  })
}
function getProblem (topic_name,problem_dict,url) {
  return new Promise(async (resolve, reject) => {
      try {
          const browser = await puppeteer.launch();
          const page = await browser.newPage();
          
          await page.emulate(iPadProLandscape);
          console.log(url);
          await page.goto(url,{waitUntil:'load'});
          await page.waitFor(5000);
          // await page.screenshot({path: 'screenshot.png'});
          let result = await page.evaluate((pbDict,problem_dict) => {
            let hasImages = false
            let ret={}
            let contentElement = document.querySelector(pbDict.container)
            // let titleElement = document.querySelector(pbDict.titleContainer)
            let imgElements = contentElement.getElementsByTagName('img')
            // let hintElements = document.querySelectorAll(pbDict.hintSelector)
            // ret['hints'] = []
            // ret['topic'] = hintElements[1].childNodes[1].childNodes[0].childNodes[0].innerHTML;
            // for(let i=2;i<hintElements.length;i++){
            //     ret.hints.push(hintElements[i].childNodes[1].innerHTML)
            // }
            let con = contentElement.innerHTML
            con=con.replace(/\n/g,"<br>")
            if(imgElements.length!==0){
                hasImages = true;
                ret['imgUrls'] = []
                for( im of imgElements){
                  ret['imgUrls'].push(im.src)
                }
            }
            ret['hasImages'] = hasImages;
            ret['contentHTML'] = '<h4>'+problem_dict['problem_name']+'</h4>'+'<div><strong>Time: '+problem_dict['time_to_solve']+'</strong><br><strong>Score: '+problem_dict['problem_score']+'</strong></div>' +'<br>'+ con;
            return ret;
          },problemDict,problem_dict)
          
          if(result['hasImages']){
            let imgUrls = result['imgUrls']
            // for(ie of result['imgUrls']){
            result['imgNames'] = []
            //   imgUrls.push(ie)
            // }
            // console.log(allImgResponses.length)
            console.log('Oh! Found images in problem description!')
            console.log(result.imgUrls)
            let imageCount  = 0;
            let temp = url.split('/')
            let problem_slug = temp[temp.length-2]
            problem_slug = problem_slug.replace(/-/g,'_')
            for (const imgURL of imgUrls) {
                imageCount = imageCount + 1
                let arr = imgURL.split('/')
                let oldName = arr[arr.length-1]
                let newName = 'Q_'+problem_slug+'_'+imageCount+oldName.substring(oldName.indexOf('.'),oldName.length)
                result.imgNames.push(oldName)
                result.imgNames.push(newName)
                let fileLocation = "problems/"+topic_name+"/"+topic_name+'_assets/'+ newName;
                let dnldImg = await downloadImage(imgURL,fileLocation)
                console.log(dnldImg)
            }
          }
          console.log(result['imgNames'])
          await page.waitFor(5000);
          await browser.close();
          return resolve(result);
      } catch (e) {
          return reject(e);
      }
  })
}
function clearLinks(topic_name,doc){
  try{
    let contentHTML = doc['contentHTML'];
    let imgs = doc['imgNames'];
    const $ = cheerio.load(contentHTML);
    let asset = topic_name+"_assets"
    $('img').each(function() {
      for(let i=0;i<imgs.length;i+=2){
        let name = $(this)[0].attribs.src.split('/')
        name = name[name.length-1]
        if(name == imgs[i]){
          $(this).attr('src',asset+"/"+imgs[i+1])
        }
      }
    })
    return $.html();
  }catch(e){
    console.log(e)
    return "";
  }
}

async function main(){
    // let rawdata = fs.readFileSync('topics.json');
    // let topics = JSON.parse(rawdata)['topics'];
    // for(let i=0;i<topics.length;i++){
      // let tn = topics[i].split("/")[6];
      let tn = process.argv[2]
      let topic_name = tn.replace(/-/g,"_")
      await exec("mkdir -p problems/"+topic_name)
      await exec("mkdir -p problems/"+topic_name+"/"+topic_name+"_assets")
      // let x = await getProblemLinks(topics[i]);
      let raw = fs.readFileSync("topics/"+tn+'.json');
      let problems = JSON.parse(raw)['problems'];
      console.log(topic_name+": "+problems.length)
      for(let j=0;j<problems.length;j++){
        let x = await getProblem(topic_name,problems[j],problems[j]['problem_link']);
        let html = clearLinks(topic_name,x)
        x['contentHTML']=html;
        x['problem_id']=problems[j]['problem_id']
        x['problem_name']=problems[j]['problem_name']
        x['problem_link']=problems[j]['problem_link']
        x['problem_score']=problems[j]['problem_score']
        x['time_to_solve']=problems[j]['time_to_solve']
        let pbName = problems[j]['problem_link'].split("/")[4];
        fs.writeFileSync("problems/"+topic_name+"/"+pbName+".json",JSON.stringify(x,null,2))
        // fs.writeFileSync("problems/"+topic_name+"/"+".html",JSON.stringify(html,null,2))
        console.log(pbName+" "+(j+1))
      }
    // }
    
}

main();
