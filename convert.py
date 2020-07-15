'''
Python script to create md files for all the problem descriptions in problems directory
@author:prabhath
'''
import os
import json

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
    print(t,"done")
  pass

if __name__=="__main__":
  main("problems","ib_docs/docs")