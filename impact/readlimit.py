#!/bin/env python

from ROOT import TFile, TH1F


tags=["el", "mu", "jet", "met", "lumi", "pileup", "WZunc", "ZZunc", "Zjet"]

masspoints=["300","600", "1000"]

def getlimit(inputfile):
    rootfile=TFile(inputfile)
    limithist=rootfile.Get("limit")
    Obslimit=limithist.GetBinContent(1) 
    Explimit=limithist.GetBinContent(2) 
    limits_list=[Obslimit, Explimit] 
    return limits_list

exp_dic={
        "300":[],
        "600":[],
        "1000":[]
        }

obs_dic={
        "300":[],
        "600":[],
        "1000":[]
        }

for tag in tags:
    for massi in masspoints:
        inputfile="./HZZllvv_%s_%s.root"%(massi, tag)
        inputfile_nominal="./HZZllvv_%s_dummy.root"%(massi)
        limits=getlimit(inputfile)
        limits_nominal=getlimit(inputfile_nominal)
        exp_dic[massi].append("%.2f"%(100*(limits[1]-limits_nominal[1])/limits_nominal[1]))
        obs_dic[massi].append("%.2f"%(100*(limits[0]-limits_nominal[0])/limits_nominal[0]))
        
print exp_dic
print obs_dic
