#!/bin/python

import os,sys

import multiprocessing 

def runjob(masspoint):
    newconfigfile="config/HZZllvvVBF_%s.config"%(masspoint)
    command_cp="cp config/HZZllvvVBF_template.config %s"%(newconfigfile)
    change_title="sed -i 's/HZZllvvVBF/HZZllvvVBF_%s/g' %s"%(masspoint, newconfigfile)
    change_input="sed -i 's/VBF300/VBF%s/g' %s"%(masspoint, newconfigfile)

    command_addSignalMCstat="cat ./config/vbf_MCstat/Conf_VBF%s_combined.txt >> %s"%(masspoint, newconfigfile)
    
    print command_cp
    print change_title
    print change_input
    print command_addSignalMCstat 

    os.system(command_cp)
    os.system(change_title)
    os.system(change_input)
    os.system(command_addSignalMCstat)
    
    command_runjob="./myFit.exe hwfldp %s"%(newconfigfile)
    print command_runjob
    os.system(command_runjob)

def runjob_ee(masspoint):
    newconfigfile="config/HZZllvv_%s_ee.config"%(masspoint)
    command_cp="cp config/HZZllvv_template_ee.config %s"%(newconfigfile)
    change_title="sed -i 's/HZZllvv/HZZllvv_%s/g' %s"%(masspoint, newconfigfile)
    change_input="sed -i 's/ggH300/ggH%s/g' %s"%(masspoint, newconfigfile)

    command_addSignalMCstat="cat ./config/highmass_MCstat/Conf_ggH%s_ee.txt >> %s"%(masspoint, newconfigfile)
    
    print command_cp
    print change_title
    print change_input
    print command_addSignalMCstat 

    os.system(command_cp)
    os.system(change_title)
    os.system(change_input)
#    os.system(command_addSignalMCstat)
    
    command_runjob="./myFit.exe hwfl %s"%(newconfigfile)
    print command_runjob
    os.system(command_runjob)

def runjob_mm(masspoint):
    newconfigfile="config/HZZllvv_%s_mm.config"%(masspoint)
    command_cp="cp config/HZZllvv_template_mm.config %s"%(newconfigfile)
    change_title="sed -i 's/HZZllvv/HZZllvv_%s/g' %s"%(masspoint, newconfigfile)
    change_input="sed -i 's/ggH300/ggH%s/g' %s"%(masspoint, newconfigfile)

    command_addSignalMCstat="cat ./config/highmass_MCstat/Conf_ggH%s_mm.txt >> %s"%(masspoint, newconfigfile)
    
    print command_cp
    print change_title
    print change_input
    print command_addSignalMCstat 

    os.system(command_cp)
    os.system(change_title)
    os.system(change_input)
#    os.system(command_addSignalMCstat)
    
    command_runjob="./myFit.exe hwfldp %s"%(newconfigfile)
    print command_runjob
    os.system(command_runjob)





masspoints=["300","400","500","600","700","800","900","1000"]
#masspoints=["300"]


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
