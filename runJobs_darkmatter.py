#!/bin/python

import os,sys

import multiprocessing 

def runjob(masspoint):
    newconfigfile="config/%s_Fit.config"%(masspoint)
    command_cp="cp config/MonoZFit.config %s"%(newconfigfile)
    change_title="sed -i 's/MonoZFit/%s_Fit/g' %s"%(masspoint, newconfigfile)
    change_input="sed -i 's/ZHinv/%s/g' %s"%(masspoint, newconfigfile)

    command_addcommonSys="cat ./config/darkmatter_MCstat/Conf_common.txt >> %s"%(newconfigfile)
    command_addBkgMCstat="cat ./config/darkmatter_MCstat/Conf_bkg.txt >> %s"%(newconfigfile)
    command_addSignalMCstat="cat ./config/darkmatter_MCstat/Conf_%s.txt >> %s"%(masspoint, newconfigfile)
    
#    command_addcommonSys="cat ./config/lowmass_MCstat_second_bin/Conf_common.txt >> %s"%(newconfigfile)
#    command_addBkgMCstat="cat ./config/lowmass_MCstat_second_bin/Conf_bkg.txt >> %s"%(newconfigfile)
#    command_addSignalMCstat="cat ./config/lowmass_MCstat_second_bin/Conf_%s.txt >> %s"%(masspoint, newconfigfile)
 

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
    
    command_runjob="./myFit.exe hwfs %s"%(newconfigfile)
    print command_runjob
    os.system(command_runjob)

def runjob_ee(masspoint):
    newconfigfile="config/%s_Fit_ee.config"%(masspoint)
    command_cp="cp config/LowMassFit_ee.config %s"%(newconfigfile)
    change_title="sed -i 's/LowMassFit_ee/%s_Fit_ee/g' %s"%(masspoint, newconfigfile)
    change_input="sed -i 's/ZHinv/%s/g' %s"%(masspoint, newconfigfile)

    command_addcommonSys="cat ./config/lowmass_MCstat/Conf_common.txt >> %s"%(newconfigfile)
    command_addBkgMCstat="cat ./config/lowmass_MCstat/Conf_bkg_ee.txt >> %s"%(newconfigfile)
    command_addSignalMCstat="cat ./config/lowmass_MCstat/Conf_%s_ee.txt >> %s"%(masspoint, newconfigfile)
    
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
    newconfigfile="config/%s_Fit_mm.config"%(masspoint)
    command_cp="cp config/LowMassFit_mm.config %s"%(newconfigfile)
    change_title="sed -i 's/LowMassFit_mm/%s_Fit_mm/g' %s"%(masspoint, newconfigfile)
    change_input="sed -i 's/ZHinv/%s/g' %s"%(masspoint, newconfigfile)

    command_addcommonSys="cat ./config/lowmass_MCstat/Conf_common.txt >> %s"%(newconfigfile)
    command_addBkgMCstat="cat ./config/lowmass_MCstat/Conf_bkg_mm.txt >> %s"%(newconfigfile)
    command_addSignalMCstat="cat ./config/lowmass_MCstat/Conf_%s_mm.txt >> %s"%(masspoint, newconfigfile)
    
    print command_cp
    print change_title
    print change_input
#    print command_addcommonSys
#    print command_addBkgMCstat
#    print command_addSignalMCstat 

    os.system(command_cp)
    os.system(change_title)
    os.system(change_input)
    os.system(command_addcommonSys)
    os.system(command_addBkgMCstat)
    os.system(command_addSignalMCstat)
    
    command_runjob="./myFit.exe hwfldp %s"%(newconfigfile)
    print command_runjob
    os.system(command_runjob)




#masspoints=["ZHinv", "dmVDM1MM10", "dmVDM50MM300"]
#masspoints=[ "dmVDM1MM10", "dmVDM50MM300"]
#masspoints=["ZHinv"]
masspoints=[
"DM1000_MM10",
"DM1000_MM1000",
"DM1000_MM1995",
"DM100_MM100",
"DM100_MM300",
"DM100_MM500",
"DM100_MM700",
"DM10_MM10",
"DM10_MM100",
"DM10_MM10000",
"DM10_MM300",
"DM10_MM500",
"DM150_MM10",
"DM150_MM1000",
"DM150_MM295",
"DM1_MM10",
"DM1_MM100",
"DM1_MM2000",
"DM1_MM300",
"DM1_MM500",
"DM1_MM700",
"DM30_MM10",
"DM30_MM100",
"DM30_MM300",
"DM30_MM500",
"DM30_MM700",
"DM500_MM10",
"DM500_MM10000",
"DM500_MM2000",
"DM500_MM995",
"DM50_MM10",
"DM50_MM300",
"DM50_MM500",
"DM50_MM700",
"DM50_MM95"
]

pool=multiprocessing.Pool(processes=int(20))

for massi in masspoints:
    pool.apply_async(runjob,(massi,))
#    pool.apply_async(runjob_mm,(massi,))
#    pool.apply_async(runjob_ee,(massi,))

##    pool.apply_async(runjob,(massi, inputwsfile, "AsimovDataMu0"))
#runjob("400")
pool.close()
pool.join()
#
