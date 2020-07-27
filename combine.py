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


def gen_combined_notes(topic):
    with open("meta.json",'r') as fp:
        meta = json.load(fp)
    tDir = meta[topic]['name']
    with open("topics/"+tDir.replace('_','-')+".json",'r') as fp:
        dic = json.load(fp)
    probs = sorted(dic['problems'],key= lambda i:i['problem_score'])

    if not os.path.exists("combined"):
        os.system("mkdir combined")
    if not os.path.exists(os.path.join("combined",tDir)):
        os.system("mkdir -p combined/"+tDir)
    
    di = os.listdir("problems/"+tDir)
    for i in di:
        if not os.path.isfile("problems/"+tDir+"/"+i):
            dn = "problems/"+tDir+"/"+i
            tdn = "combined/"+tDir+"/"+i
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
        with open("problems/"+tDir+"/"+pFile+".json",'r') as fp:
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
    
    with open("combined/"+tDir+"/"+tDir+".md",'w') as fp:
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
    topic=sys.argv[1]
    # prob=sys.argv[2]
    # sol_file=sys.argv[3]
    # store_notes(topic,prob,sol_file)
    gen_combined_notes(topic)