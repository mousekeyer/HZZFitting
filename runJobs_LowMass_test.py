#!/bin/python

import os,sys

import multiprocessing 

def runjob(masspoint):
    newconfigfile="config/%s_Fit.config"%(masspoint)
    command_cp="cp config/LowMassFit.config %s"%(newconfigfile)
    change_title="sed -i 's/LowMassFit/%s_Fit/g' %s"%(masspoint, newconfigfile)
    change_input="sed -i 's/ZHinv/%s/g' %s"%(masspoint, newconfigfile)

#    command_addcommonSys="cat ./config/lowmass_MCstat/Conf_common.txt >> %s"%(newconfigfile)
#    command_addBkgMCstat="cat ./config/lowmass_MCstat/Conf_bkg.txt >> %s"%(newconfigfile)
#    command_addSignalMCstat="cat ./config/lowmass_MCstat/Conf_%s.txt >> %s"%(masspoint, newconfigfile)
    
    command_addcommonSys="cat ./config/lowmass_MCstat_second_bin/Conf_common.txt >> %s"%(newconfigfile)
    command_addBkgMCstat="cat ./config/lowmass_MCstat_second_bin/Conf_bkg.txt >> %s"%(newconfigfile)
    command_addSignalMCstat="cat ./config/lowmass_MCstat_second_bin/Conf_%s.txt >> %s"%(masspoint, newconfigfile)
 

    print command_cp
    print change_title
    print change_input
    print command_addcommonSys
    print command_addBkgMCstat
    print command_addSignalMCstat 

    os.system(command_cp)
    os.system(change_title)
#    os.system(change_input)
    os.system(command_addcommonSys)
    os.system(command_addBkgMCstat)
    os.system(command_addSignalMCstat)
    
    command_runjob="./myFit.exe hwfl %s"%(newconfigfile)
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
masspoints=["ZHinv_test"]


pool=multiprocessing.Pool(processes=int(16))

for massi in masspoints:
    pool.apply_async(runjob,(massi,))
#    pool.apply_async(runjob_mm,(massi,))
#    pool.apply_async(runjob_ee,(massi,))

##    pool.apply_async(runjob,(massi, inputwsfile, "AsimovDataMu0"))
#runjob("400")
pool.close()
pool.join()
#
