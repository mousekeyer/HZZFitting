#!/bin/python

import os,sys

import multiprocessing 

def runjob(masspoint, systag):
    newconfigfile="config/%s_Fit.config"%(masspoint)
    command_cp="cp config/LowMassFit.config %s"%(newconfigfile)
    change_title="sed -i 's/LowMassFit/%s_Fit/g' %s"%(masspoint, newconfigfile)
    change_input="sed -i 's/ZHinv/%s/g' %s"%(masspoint, newconfigfile)

    command_addcommonSys=""
    if systag!="bkg" and systag!="signal" and systag!="WZunc" and systag!="ZZunc" and systag!="signalZH" :
        command_addcommonSys="cat ./config/lowmass_MCstat/Conf_%s.txt >> %s"%(systag, newconfigfile)
    elif systag=="bkg":
        command_addcommonSys="cat ./config/lowmass_MCstat/Conf_bkgMCStat.txt >> %s"%(newconfigfile)
    elif systag=="signal":
        command_addcommonSys="cat ./config/lowmass_MCstat/Conf_%s.txt >> %s"%(masspoint, newconfigfile)
    elif systag=="signalZH":
        command_addcommonSys="cat ./config/lowmass_MCstat/Conf_signalZH.txt >> %s"%(newconfigfile)
    elif  systag=="WZunc" or systag=="ZZunc":
        command_addcommonSys="cat ./config/lowmass_MCstat/Conf_%s.txt >> %s"%(systag, newconfigfile)
 
        
    
    print command_cp
    print change_title
    print change_input
    print command_addcommonSys

    os.system(command_cp)
    os.system(change_title)
    os.system(change_input)
    os.system(command_addcommonSys)
    
    command_runjob="./myFit.exe hwfl %s"%(newconfigfile)
    print command_runjob
    os.system(command_runjob)

##  copy limit file to ./impact/ directory
    
    command_cp_limit="cp ./%s_Fit/Limits/%s_Fit.root ./impact/%s_Fit_%s.root"%(masspoint, masspoint, masspoint, systag)
    print command_cp_limit
    os.system(command_cp_limit)

def runjobCombined(masspoint, systag_list):
    newconfigfile="config/%s_Fit.config"%(masspoint)
    command_cp="cp config/LowMassFit.config %s"%(newconfigfile)
    change_title="sed -i 's/LowMassFit/%s_Fit/g' %s"%(masspoint, newconfigfile)
    change_input="sed -i 's/ZHinv/%s/g' %s"%(masspoint, newconfigfile)


        
    
#    print command_cp
#    print change_title
#    print change_input
#    print command_addcommonSys

    os.system(command_cp)
    os.system(change_title)
    os.system(change_input)


    for systag in systag_list:
        command_addcommonSys=""
        if systag!="bkg" and systag!="signal" and systag!="WZunc" and systag!="ZZunc" and systag!="signalZH" :
            command_addcommonSys="cat ./config/lowmass_MCstat/Conf_%s.txt >> %s"%(systag, newconfigfile)
        elif systag=="bkg":
            command_addcommonSys="cat ./config/lowmass_MCstat/Conf_bkgMCStat.txt >> %s"%(newconfigfile)
        elif systag=="signal":
            command_addcommonSys="cat ./config/lowmass_MCstat/Conf_%s.txt >> %s"%(masspoint, newconfigfile)
        elif systag=="signalZH":
            command_addcommonSys="cat ./config/lowmass_MCstat/Conf_signalZH.txt >> %s"%(newconfigfile)
        elif  systag=="WZunc" or systag=="ZZunc":
            command_addcommonSys="cat ./config/lowmass_MCstat/Conf_%s.txt >> %s"%(systag, newconfigfile)
     
        os.system(command_addcommonSys)
        
    command_runjob="./myFit.exe hwfldp %s"%(newconfigfile)
    print command_runjob
    os.system(command_runjob)

    systag_txt="_".join(systag_list)
##  copy limit file to ./impact/ directory
    
    command_cp_limit="cp ./%s_Fit/Limits/%s_Fit.root ./impact/%s_Fit_%s.root"%(masspoint, masspoint, masspoint, systag_txt)
    command_cp_scan="cp ./%s_Fit/Limits/OutCLscan_Asym_CLs_grid_ts3.root ./impact/%s_Fit_CLscan_%s.root"%(masspoint,  masspoint, systag_txt)
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



#tags=["el", "mu", "jet", "met", "lumi", "pileup", "WZunc", "ZZunc", "Zjet", "bkg", "signal", "ggZZunc", "dummy", "signalZH"]
tags=["el", "mu", "jet", "met", "lumi", "pileup", "WZunc", "ZZunc", "Zjet", "bkg", "signal", "ggZZunc", "signalZH"]

tags_sys1=["el", "mu", "jet", "met", "lumi", "pileup", "WZunc"]#, "ZZunc", "Zjet", "bkg", "signal", "ggZZunc", "dummy", "signalZH"]
tags_sys2=["ZZunc", "Zjet", "bkg", "signal", "ggZZunc", "signalZH"]
tags_sys3=["el", "mu"]
#tags=["el", "mu", "jet", "met", "lumi", "pileup", "WZunc", "ZZunc", "Zjet"]
#tags=["WZunc", "ZZunc"]

#masspoints=["300","400","500","600","700","800","900","1000"]
#masspoints=["300","400","500","600","700","800","900","1000"]
masspoints=["ZHinv"]

#runjob("600","signal")

#runjobCombined("ZHinv", tags_sys1)
#runjobCombined("ZHinv", tags_sys2)
runjobCombined("ZHinv", tags)
#runjobCombined("ZHinv", tags_sys3)
#runjob("ZHinv", "dummy")

#for tagi in tags:
#    pool=multiprocessing.Pool(processes=int(16))
#    for massi in masspoints:
#        pool.apply_async(runjob,(massi,tagi))
##    pool.apply_async(runjob_mm,(massi,))
##    pool.apply_async(runjob_ee,(massi,))
#    pool.close()
#    pool.join()
#

##    pool.apply_async(runjob,(massi, inputwsfile, "AsimovDataMu0"))
#runjob("400")
#
