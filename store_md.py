import os
import sys
import json

def create_meta():
    meta={}
    with open("topics.json",'r') as fp:
        topics=json.load(fp)['topics']
    for t in topics:
        tn=t.split("/")[-2].replace("-","_")
        key=input(tn+" key:")
        key2=input(tn+" shortName:")
        meta[key]={}
        meta[key]['name']=tn
        meta[key]['short_name']=key2
        meta[key]['problem_count']=0
        meta[tn]=key2
    with open("meta.json",'w') as fp:
        json.dump(meta,fp,indent=2,sort_keys=True)

def store_md_notes(topic,problem,sol_file):
    pName = problem.replace("-","_")
    with open(sol_file,'r') as fp:
        data = fp.read()
    with open("meta.json",'r') as fp:
        meta = json.load(fp)
    tDir = meta[topic]['name']
    # if not os.path.exists("solutions"):
    #     os.system("mkdir solutions")
    # if not os.path.exists("solutions/"+tDir):
    #     os.system("mkdir solutions/"+tDir)
    if not os.path.exists("solutions/"+tDir+"/"+pName):
        os.system("mkdir -p solutions/"+tDir+"/"+pName)
    ibHome="https://www.interviewbit.com/problems/"
    banner = "**Problem: ["+problem+"]("+ibHome+problem+")**\n\n"
    # dic = {}
    # dic['notes'] = banner+data
    # dic['solution'] = ""
    # with open("solutions/"+tDir+"/n_"+pName+".json",'w') as fp:
    #     json.dump(dic,fp)
    with open("solutions/"+tDir+"/"+pName+"/n_"+pName+".md",'w') as fp:
        fp.write(banner)
        fp.write(data)

if __name__=="__main__":
    fun=sys.argv[1]
    if fun=='store':
        topic=sys.argv[2]
        prob=sys.argv[3]
        sol_file=sys.argv[4]
        store_md_notes(topic,prob,sol_file)
    elif fun=='meta':
        create_meta()