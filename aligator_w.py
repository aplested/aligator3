#top level wrapper for relaxes module

__author__="Andrew"
__date__ ="$Aug 26, 2013 4:03:07 PM$"

import relaxes_w as re
import IO_utils as iou
import time
import sys
import mechanisms_UAA as mechanisms
import pprint
import config
import os
from simple_log import Logger

#140918 new generic version, gets parameters from config.py module
#141219 added fixrec (but it disappeared?)
#170606 moved logger out

def announce ():
    print("\
    ALiGaTOR : Analysis of Ligand Gating: Trains and Other Relaxations\n\
    v. 0.3\
    Andrew Plested FMP-Berlin 2017 (work-in-progress version)\
    ")

def package(expt_list=["train", "rec", "relax", "cr"], mech_list=["3"], rate="alpha", power=[1], range = 1):
    """
    run multiple experiments on multiple mechanisms
    
    expt_list should contain keyword strings to launch particular experiments
    mech_list : mechanism keyword strings
    power = list of power with which exponents are varied
    range = +ve and -ve limit of exponents over which to vary rate
    """
    expt_call_table = {   
                "train"     : re.TrainExpt, 
                "rec"       : re.RecoveryExpt,
                #"fixrec"    : re.FixedRecExpt,
                "relax"     : re.RelaxExpt, 
                "cr"        : re.CrExpt, 
                "jumpfamily": re.JFExpt,
                      }
    ###paircomp is not going to work in this context (no run method)
    for mech in mech_list:
        
        for expt_type in expt_list:
            
            param = re.Parameters() # set defaults and then modify below
            
            ##  'sim_name'       = "trial"
        
            ##  'rate_to_change' = 'd2op_plus'
            ##  'N_trials'       = 10   
            ##  'hi_exp'         = 1.5
            ##  'lo_exp'         = -1.5
        
            ##  'MR_rate'        = [(1,7), (0,5), (7,8), (5,6)]
            ##  'MR_avoid'       = [(0,2)]
            ##  'zero_conc'      = 0 
            ##  'high_conc'      = 1e-2
            
            #edit simulation name to include mechanism used
            param.sim_name = expt_type + "_m" + mech
            
            #range of powers of ten to scan around initial rate
            param.hi_exp    =  range
            param.lo_exp    = -range
            param.var_power = power
            param.N_trials  = 20
            
            #edit rate to use specified //doesn't work for a series of names
            param.rate_to_change = rate
            #for changing binding only
            param.MR_rate = [(2, 3), (3, 4)]
            print ("\n\nExperiment name: " + param.sim_name)
            
            experiment = expt_call_table[expt_type]
            e = experiment(mech, param)
            e.run()


    
if __name__ == "__main__":
    """
    some example paramters 
    ----------------------
    
    #pick directory
    working_directory = "/users/andrew/desktop/aligator trials"
    
    #modify filename with project
    mod = "_CP_stg"
     
    #define experiments to be done here
    mech_list=['3KA', '4KA', '3','4']
    expt_list=["jumpfamily" ]
    rate=["d2_min", "d2op_min"]         #must be a list  
    power = [1, .7]
    range = 1.5
    """
    
    #import parameters from config module
    #implement more concise unpacking?, with defaults to rescue missing values
    print ("The current working directory is {0}".format(os.getcwd()))
    # read pickled config module 
    # there is a default.txt configuration
    config_file = "default.txt"
    
    #it would be ideal here to be able to specify the name of the mechanisms module
    # that should be used. At the moment, this must be specified both here (import) 
    # and also as an import in the Relaxes module. 
    
    try:
        c = config.ConfigIO(Empty=True)
        c.read_config(config_file, Verbose=True)
        
        #unpack values
        working_directory = c.working_directory
        mod = c.mod
        mech_list = c.mech_list
        expt_list = c.expt_list
        rate = c.rate
        power = c.power
        range = c.range
        pair_expt = c.pair_expt
        
        config_imported = True
        config_file_used = config_file
    except:
        print ("Failed to import default config (default.txt)")
    
    # Override imported params here
    # moved up to allow manual override of "mod" or "working_directory"
    # alter mechanims.py to put a new mechanism in. 
    expt_list=['jumpfamily'] 
    mech_list=['4']
    mod='_UAA'
    rate=['beta', 'd2op_min', "d2_min", "d1_plus"]
    power = [1, 1, 1, 1]
    #try the following 180503
    """rate=[]
    power=[]"""
    # d2 lifetime experiment
    #rate=['d2_min', 'd2op_min']
    #power=[1, 1]
    #alternatively, run comparison experiment
    
    #move to working directory
    #the variable :file_list: is returned but not used here
    file_list, wd = iou.getpath(True, working_directory)
    
    #generate time string (unique, to the second) and make a new folder with that
    #timestamp, so we can work in any directory without fear of overwriting 
    #anything
    timestr = time.strftime("%y%m%d-%H%M%S")   
    iou.make_folder(timestr + mod, wd)
    
    Log = Logger(timestr+'_log.txt')        #create logfile
    announce()                              #announce program version
    
    if config_imported: print ("\nConfiguration file "+config_file_used+" imported by config.py")
    print ('\nThis file is: '+timestr+'_log.txt')
    
    print ("\nParameters and settings used\nwd: {0}\nmod: {1}\nm_l: {2}\ne_l: {3}\nrate: {4}\npower: {5}\nrange: {6}\n".format(working_directory, mod, mech_list, expt_list, rate, power, range))
    
    if pair_expt:
        a = re.PairExpt()
        a.run()
    
    else:
        package(expt_list, mech_list, rate, power, range)
    
    del Log


    f = open(timestr+'_mechs.txt', "w")
    f.write("Hint: these mechanisms can be copied to a rate dictionary and reused\n")
    for m in mech_list:
        r, n, o = mechanisms.mechanism(m)
        
        f.write("rate mechanism " + str(m) + "\n")
        f.write(pprint.pformat(r)) 
        f.write("\n**********\n")
        f.write("\nOpen states " + str(o))
        f.write("\n**********\n\n\n")
    f.close()

