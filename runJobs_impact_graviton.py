#!/bin/python

import os,sys

import multiprocessing 

def runjob(masspoint, systag):
    newconfigfile="config/Graviton_%s.config"%(masspoint)
    command_cp="cp config/Graviton_template.config %s"%(newconfigfile)
    change_title="sed -i 's/Graviton/Graviton_%s/g' %s"%(masspoint, newconfigfile)
    change_input="sed -i 's/ggH300/Graviton%s/g' %s"%(masspoint, newconfigfile)

    command_addcommonSys=""
    if systag!="bkg" and systag!="signal":
        command_addcommonSys="cat ./config/highmass_MCstat/Conf_%s.txt >> %s"%(systag, newconfigfile)
    elif systag=="bkg":
        command_addcommonSys="cat ./config/highmass_MCstat/Conf_bkgMCstat.txt >> %s"%(newconfigfile)
    elif systag=="signal":
        command_addcommonSys="cat ./config/highmass_MCstat/Conf_Graviton%s.txt >> %s"%(masspoint, newconfigfile)
        
    
    print command_cp
    print change_title
    print change_input
    print command_addcommonSys

    os.system(command_cp)
    os.system(change_title)
    os.system(change_input)
    os.system(command_addcommonSys)
    
    command_runjob="./myFit.exe hwfldp %s"%(newconfigfile)
    print command_runjob
    os.system(command_runjob)

##  copy limit file to ./impact/ directory
    
    command_cp_limit="cp ./Graviton_%s/Limits/Graviton_%s.root ./impact/Graviton_%s_%s.root"%(masspoint, masspoint, masspoint, systag)
    print command_cp_limit
    os.system(command_cp_limit)

def runjob_ee(masspoint):
    newconfigfile="config/HZZllvv_%s_ee.config"%(masspoint)
    command_cp="cp config/HZZllvv_template_ee.config %s"%(newconfigfile)
    change_title="sed -i 's/HZZllvv/HZZllvv_%s/g' %s"%(masspoint, newconfigfile)
    change_input="sed -i 's/ggH300/ggH%s/g' %s"%(masspoint, newconfigfile)

    command_addcommonSys="cat ./config/highmass_MCstat/Conf_common.txt >> %s"%(newconfigfile)
    command_addBkgMCstat="cat ./config/highmass_MCstat/Conf_bkg_ee.txt >> %s"%(newconfigfile)
    command_addSignalMCstat="cat ./config/highmass_MCstat/Conf_ggH%s_ee.txt >> %s"%(masspoint, newconfigfile)
    
    print command_cp
    print change_title
    print change_input
    print command_addcommonSys
    print command_addBkgMCstat
    print command_addSignalMCstat 

    os.system(command_cp)
    os.system(change_title)
    os.system(change_input)
    os.system(command_addcommonSys)
    os.system(command_addBkgMCstat)
    os.system(command_addSignalMCstat)
    
    command_runjob="./myFit.exe hwfldp %s"%(newconfigfile)
    print command_runjob
    os.system(command_runjob)

def runjob_mm(masspoint):
    newconfigfile="config/HZZllvv_%s_mm.config"%(masspoint)
    command_cp="cp config/HZZllvv_template_mm.config %s"%(newconfigfile)
    change_title="sed -i 's/HZZllvv/HZZllvv_%s/g' %s"%(masspoint, newconfigfile)
    change_input="sed -i 's/ggH300/ggH%s/g' %s"%(masspoint, newconfigfile)

    command_addcommonSys="cat ./config/highmass_MCstat/Conf_common.txt >> %s"%(newconfigfile)
    command_addBkgMCstat="cat ./config/highmass_MCstat/Conf_bkg_mm.txt >> %s"%(newconfigfile)
    command_addSignalMCstat="cat ./config/highmass_MCstat/Conf_ggH%s_mm.txt >> %s"%(masspoint, newconfigfile)
    
    print command_cp
    print change_title
    print change_input
    print command_addcommonSys
    print command_addBkgMCstat
    print command_addSignalMCstat 

    os.system(command_cp)
    os.system(change_title)
    os.system(change_input)
    os.system(command_addcommonSys)
    os.system(command_addBkgMCstat)
    os.system(command_addSignalMCstat)
    
    command_runjob="./myFit.exe hwfldp %s"%(newconfigfile)
    print command_runjob
    os.system(command_runjob)



tags=["el", "mu", "jet", "met", "lumi", "pileup", "WZunc", "ZZunc", "Zjet", "bkg", "signal", "ggZZunc", "dummy"]
#tags=["el", "mu", "jet", "met", "lumi", "pileup", "WZunc", "ZZunc", "Zjet"]
#tags=["Zjet"]

#masspoints=["300","400","500","600","700","800","900","1000"]
#masspoints=["300","400","500","600","700","800","900","1000"]
masspoints=["600", "800", "1000", "1200"]

#runjob("600","signal")

for tagi in tags:
    pool=multiprocessing.Pool(processes=int(16))
    for massi in masspoints:
        pool.apply_async(runjob,(massi,tagi))
#    pool.apply_async(runjob_mm,(massi,))
#    pool.apply_async(runjob_ee,(massi,))
    pool.close()
    pool.join()


##    pool.apply_async(runjob,(massi, inputwsfile, "AsimovDataMu0"))
#runjob("400")
#
