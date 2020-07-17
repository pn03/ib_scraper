'''
Python script to create md files for all the problem descriptions in problems directory
@author:prabhath
'''
import os
import json
import sys

def main(basePath,targetPath):
  topics = os.listdir(basePath)
  for t in topics:
    problemsPath = os.path.join(basePath,t)
    problems = os.listdir(problemsPath)
    tPath = os.path.join(targetPath,t)
    if not os.path.exists(tPath):
      os.mkdir(tPath)
    # print(tPath)
    for p in problems:
      if os.path.isfile(os.path.join(problemsPath,p)):
        with open(os.path.join(problemsPath,p),'r') as fp:
          dic = json.load(fp)
        with open("tmp.html",'w') as fp:
          fp.write(dic['contentHTML'])
        pName = p[:-5]
        mdName = pName+".md"
        ofile = os.path.join(tPath,mdName)
        # print(ofile)
        command = "pandoc tmp.html -f html -t markdown_strict -s -o "+ofile
        os.system(command)
      else:
        imgPath = os.path.join(tPath,p)
        os.mkdir(imgPath)
        imgDir = os.path.join(problemsPath,p)
        imgs = os.listdir(imgDir)
        for img in imgs:
          with open(os.path.join(imgDir,img),'rb') as fp:
            data = fp.read()
          with open(os.path.join(imgPath,img),'wb') as fp2:
            fp2.write(data)
    print(t,"done")
  pass

if __name__=="__main__":
  arg1 = sys.argv[1]
  arg2 = sys.argv[2]
  if not os.path.exists(arg2):
    print("target dir doesn't exist!")
    sys.exit(0)
  main(arg1,arg2)
