#!/bin/python

import os,sys

import multiprocessing 

def runjob(masspoint):
    newconfigfile="config/HZZllvv_%s.config"%(masspoint)
    command_cp="cp config/HZZllvv_template.config %s"%(newconfigfile)
    change_title="sed -i 's/HZZllvv/HZZllvv_%s/g' %s"%(masspoint, newconfigfile)
    change_input="sed -i 's/ggH300/ggH%s/g' %s"%(masspoint, newconfigfile)

    command_addcommonSys="cat ./config/highmass_MCstat/Conf_common.txt >> %s"%(newconfigfile)
    command_adddummySys="cat ./config/highmass_MCstat/Conf_dummy.txt >> %s"%(newconfigfile)
    command_addBkgMCstat="cat ./config/highmass_MCstat/Conf_bkg.txt >> %s"%(newconfigfile)
    command_addSignalMCstat="cat ./config/highmass_MCstat/Conf_ggH%s.txt >> %s"%(masspoint, newconfigfile)
    
    print command_cp
    print change_title
    print change_input
    print command_addcommonSys
    print command_addBkgMCstat
    print command_addSignalMCstat 

    os.system(command_cp)
    os.system(change_title)
    os.system(change_input)
#    os.system(command_adddummySys)
    os.system(command_addcommonSys)
    os.system(command_addBkgMCstat)
    os.system(command_addSignalMCstat)
    
    command_runjob="./myFit.exe hwf %s"%(newconfigfile)
   # command_runjob="./myFit.exe f %s"%(newconfigfile)
    print command_runjob
    os.system(command_runjob)

def runjob_ee(masspoint):
    newconfigfile="config/HZZllvv_%s_ee.config"%(masspoint)
    command_cp="cp config/HZZllvv_template_ee.config %s"%(newconfigfile)
    change_title="sed -i 's/HZZllvv/HZZllvv_%s/g' %s"%(masspoint, newconfigfile)
    change_input="sed -i 's/ggH300/ggH%s/g' %s"%(masspoint, newconfigfile)

    command_addcommonSys="cat ./config/highmass_MCstat/Conf_common.txt >> %s"%(newconfigfile)
    command_addBkgMCstat="cat ./config/highmass_MCstat/Conf_bkg_ee.txt >> %s"%(newconfigfile)
    command_addSignalMCstat="cat ./config/highmass_MCstat/Conf_ggH%s_ee.txt >> %s"%(masspoint, newconfigfile)
    command_adddummySys="cat ./config/highmass_MCstat/Conf_dummy.txt >> %s"%(newconfigfile)
    
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
#    os.system(command_adddummySys)
    
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
    command_adddummySys="cat ./config/highmass_MCstat/Conf_dummy.txt >> %s"%(newconfigfile)
    
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
#    os.system(command_adddummySys)
    
    command_runjob="./myFit.exe hwfldp %s"%(newconfigfile)
    print command_runjob
    os.system(command_runjob)





masspoints=["300","400","500","600","700", "750","800","900","1000"]
#masspoints=["300", "600", "1000"]


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
