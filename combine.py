import sys
import os
import textwrap
from datetime import datetime
import json
import pypandoc

def combine_md(f1,f2):
    with open(f1,'r') as fp:
        k1 = fp.read()
    with open(f2,'r') as fp:
        k2 = fp.read()
    k2 = textwrap.indent(k2,"\t")
    sol_banner = "??? Solution\n"
    ks = k1+ sol_banner +k2
    # print(ks)
    with open("tmp.md",'w') as fp:
        fp.write(ks)

def append_notes_md(f1,f2,sol_name):
    with open(f1,'r') as fp:
        k1 = fp.read()
    with open(f2,'r') as fp:
        k2 = fp.read()
    k2 = textwrap.indent(k2,"\t")
    # perma_link_name = "\n\n#### "+sol_name+"\n"
    now = datetime.now()
    date_time = now.strftime("%d %B %Y, %H:%M:%S")
    sol_banner = "\n\n??? Notes\n" + "\n\t**Time**: "+date_time+"\n\n"
    ks = ""
    # ks += perma_link_name
    ks += sol_banner +k2
    # print(ks)
    with open("tmp2.md",'a') as fp:
        fp.write(ks)


def gen_combined_notes(basePath,targetPath,sortKey="score"):
    with open("meta.json",'r') as fp:
        meta = json.load(fp)
    # tDir = meta[topic]['name']
    if not os.path.exists(basePath):
        print("problems dir does not exist")
        sys.exit(2)
    if not os.path.exists(targetPath):
        os.system("mkdir "+targetPath)

    topics = os.listdir(basePath)
    for t in topics:
        with open("topics/"+t.replace('_','-')+".json",'r') as fp:
            dic = json.load(fp)
    # with open("topics/"+tDir.replace('_','-')+".json",'r') as fp:
    #     dic = json.load(fp)
        tDir = t
        for i in range(len(dic['problems'])):
            ti = dic['problems'][i]['time_to_solve']
            mi,sec = ti.split(":")
            tim = int(mi)*60 + int(sec)
            dic['problems'][i]['time_sec']=tim
        # probs = sorted(dic['problems'],key= lambda i:i['problem_score'])
        if sortKey == "score":
            probs = sorted(dic['problems'],key= lambda i:i['problem_score'])
        elif sortKey == "time":
            probs = sorted(dic['problems'],key= lambda i:(i['time_sec'],i['problem_score']))
        else:
            probs = sorted(dic['problems'],key= lambda i:i['problem_score'])
        if not os.path.exists(targetPath):
            os.system("mkdir "+targetPath)
        targetTopic = meta[tDir]
        if not os.path.exists(os.path.join(targetPath,targetTopic)):
            os.system("mkdir -p "+targetPath+"/"+targetTopic)
        problemsPath = os.path.join(basePath,tDir)
        di = os.listdir(problemsPath)
        for i in di:
            if not os.path.isfile(os.path.join(problemsPath,i)):
                dn = problemsPath+"/"+i
                targetTopic=meta[tDir]
                tdn = targetPath+"/"+targetTopic+"/"+i
                ld = os.listdir(dn)
                for j in ld:
                    if not os.path.exists(tdn):
                        os.system("mkdir "+tdn)
                    with open(os.path.join(dn,j),'rb') as fp:
                        data = fp.read()
                    with open(os.path.join(tdn,j),'wb') as fp2:
                        fp2.write(data)
        combined = ""
        for p in probs:
            # get problem md
            pFile = p['problem_link'].split("/")[-2]
            if not os.path.exists(problemsPath+"/"+pFile+".json"):
                continue
            with open(problemsPath+"/"+pFile+".json",'r') as fp:
                k = json.load(fp)
            pContent = k['contentHTML']
            p_md = pypandoc.convert_text(pContent,'markdown_strict',format='html')
            if len(combined)!=0:
                combined+= "\n---\n"
            combined += p_md
            sol_md=""
            # check if notes or sol exists
            nFile = pFile.replace("-","_")
            nPath = "solutions/"+tDir+"/"+nFile+"/n_"+nFile+".md"
            if os.path.exists(nPath):
                with open(nPath,'r') as fp:
                    k2 = fp.read()
                k2 = textwrap.indent(k2,"\t")
                # perma_link_name = "\n\n#### "+sol_name+"\n"
                now = datetime.now()
                date_time = now.strftime("%d %B %Y, %H:%M:%S")
                sol_banner = "\n\n??? Notes\n" + "\n\t**Time**: "+date_time+"\n\n"
                ks = ""
                # ks += perma_link_name
                ks += sol_banner +k2
                combined += ks
        targetTopic=meta[tDir]
        with open(targetPath+"/"+targetTopic+"/"+targetTopic+".md",'w') as fp:
            fp.write(combined)



def store_notes(topic,problem,sol_file):
    pName = problem.replace("-","_")
    with open(sol_file,'r') as fp:
        data = fp.read()
    with open("meta.json",'r') as fp:
        meta = json.load(fp)
    tDir = meta[topic]['name']
    if not os.path.exists("sol/"+tDir):
        os.system("mkdir -p sol/"+tDir)
    ibHome="https://www.interviewbit.com/problems/"
    banner = "**Problem: ["+problem+"]("+ibHome+problem+")**\n\n"
    dic = {}
    dic['notes'] = banner+data
    dic['solution'] = ""
    with open("sol/"+tDir+"/n_"+pName+".json",'w') as fp:
        json.dump(dic,fp)

if __name__=="__main__":
    # f1 = sys.argv[1]
    # f2 = sys.argv[2]
    # f3 = sys.argv[3]
    # combine_md(f1,f2)
    # append_sol_md(f1,f2,f3)
    base=sys.argv[1]
    tar=sys.argv[2]
    sortKey=sys.argv[3]
    # store_notes(topic,prob,sol_file)
    gen_combined_notes(base,tar)