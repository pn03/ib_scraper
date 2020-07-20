import json
import os

def sol_skel(topicsPath):
    with open(topicsPath,'r') as fp:
        d = json.load(fp)
    d = d['topics']
    if not os.path.exists("solutions"):
        os.system("mkdir solutions")
    for i in d:
        tn = i.split("/")[-2]
        name = i.split("/")[-2].replace("-","_")
        if not os.path.exists("solutions/"+name):
            os.system("mkdir solutions/"+name)
        with open("topics/"+tn+".json",'r') as fp:
            pr = json.load(fp)
        for p in pr["problems"]:
            pDir = p["problem_link"].split("/")[-2].replace("-","_")
            pPath = "solutions/"+name+"/"+pDir
            if not os.path.exists(pPath):
                os.system("mkdir "+pPath)
            # os.system(cmd+"/s_"+pDir+".md")
            # os.system("touch "+pPath+"/n_"+pDir+".md")

sol_skel("topics.json")