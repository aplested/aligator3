#top level wrapper for relaxes module
 
__author__="Andrew"
__date__ ="$Aug 26, 2013 4:03:07 PM$"

from recover import RecoveryExpt
from concentration import CrExpt 
from compare import TwoMechSetup, Pack_m, PairExpt, PairMechComparison
from trains import TrainExpt, JFExpt
import relaxes_w as re
import common.IO_utils as iou
import time
import mechanisms_UAA as mechanisms
import pprint
import sys          #this is needed!!!
import config
import os
from common.simple_log import Logger
from scripts.conductance_change import ConductMat as CM

#special version for doing multiple conductance experiments


def announce ():
    print("\
    ALiGaTOR-MC : Analysis of Ligand Gating: Trains and Other Relaxations\n\
    for multiple conductances \n\
    v. 0.4\
    Andrew Plested FMP-Berlin 2018 (Poulsen et al paper)\
    ")

def package(expt_list=["train", "rec", "relax", "cr"], mech_list=["3"], rate="alpha", power=[1], v_range=1, g_mat=None, N_trials=10):
    """
    run multiple experiments on multiple mechanisms
    
    expt_list should contain keyword strings to launch particular experiments
    mech_list : mechanism keyword strings
    power = list of power with which exponents are varied
    range = +ve and -ve limit of exponents over which to vary rate
    """
    expt_call_table = {   
                "train"     : TrainExpt, 
                "rec"       : RecoveryExpt, 
                #"fixrec"    : re.FixedRecExpt,
                "relax"     : re.RelaxExpt, 
                "cr"        : CrExpt, 
                "jumpfamily": JFExpt,
                      }

    for mech in mech_list:

        for expt_type in expt_list:

            param = re.Parameters() # set defaults and then modify below
            
            # these are the default attributes of param that are loaded
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
            #param.hi_exp    = v_range
            #param.lo_exp    = 0
            param.var_power = power
            param.N_trials  = N_trials

            #edit rate to use specified //doesn't work for a series of names
            param.rate_to_change = rate

            #to force d1min to be used to compensate beta - ref question from poulsen et al
            param.MR_rate = [(3, 5), (3, 4)]
            param.open_state_matrix = g_mat

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
    
    ###conductance matrix is a special parameter
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
        v_range = c.v_range
        pair_expt = c.pair_expt
        
        config_imported = True
        config_file_used = config_file
        
    except:
        print ("Failed to import default config (default.txt)")
        config_imported = False
    
    # Override imported params here
    # moved up to allow manual override of "mod" or "working_directory"
    # alter mechanims.py to put a new mechanism in. 
    N_trials = 10
    expt_list = ['jumpfamily'] 
    mech_list = ['3']
    mod = '_UAA'
    
    #opening rate expt - 
    rate = ['beta']
    power = [1]
    
    #towards resting expt
    #rate=['alpha', 'd2op_min', "d2_min"]
    #power = [1, 1, 1]

    # d2 lifetime experiment
    #rate=['d2_min', 'd2op_min']
    #power=[1, 1]
    #alternatively, run comparison experiment
    
    rd, N_states, open_states = mechanisms.mechanism(mech_list[0])
    # cycle through 10 different conductance levels (to match number of trials)
    g_mat = CM(N_trials, N_states)
    g_mat.add_constant_g_vec(0, 1)  #main open state
    #g_mat.add_range_g_vec(2,.2)      #range from g = 0 to .2 for state #2 , to 1 was too much
    
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
    
    
    print ("\nParameters and settings used\nwd: {0}\nmod: {1}\nm_l: {2}\ne_l: {3}\nrate: {4}\npower: {5}\nv_range: {6}\nN_trials: {7}\n".format(working_directory, mod, mech_list, expt_list, rate, power, v_range, N_trials))
    
    if pair_expt:
        a = re.PairExpt()
        a.run()
    
    else:
        package(expt_list, mech_list, rate, power, v_range, g_mat, N_trials)
    
    del Log


    f = open(timestr+'_mechs.txt', "w")
    f.write("Hint: these mechanisms can be copied to a rate dictionary and reused [omit open state matrix]\n")
    
    for m in mech_list:
        r, n, o = mechanisms.mechanism(m)
        o = g_mat.g_mat
        f.write("rate mechanism " + str(m) + "\n")
        f.write(pprint.pformat(r)) 
        f.write("\n**********\n")
        f.write("\nOpen states\n" + str(o))
        f.write("\n**********\n\n\n")
    f.close()

