
__author__="Andrew"
__date__ ="$Aug 26, 2013 4:03:07 PM$"

import relaxes as re
import IO_utils as iou
import time
import sys
#import copy #although this kind of work should be done in relaxes.py
#import core_utils #although this kind of work should be done in relaxes.py
import mechanisms
import pprint
import numpy
from logging import Logger
from IO_utils import curve_save

def announce ():
    print("\
    PCF simulator : \n\
    v. 0.1\
    Andrew Plested FMP-Berlin 2014\
    ")
    
if __name__ == "__main__":
    
    #pick directory
    working_directory = "/users/andrew/desktop/PCF trials"
    
    #modify filename with project
    mod = "_trials"
    traces =[]
    #move automatically to working directory
    #variablefile_list is not used
    file_list, wd = iou.getpath(True, working_directory)
    
    #generate time string (unique to the second) and make a new folder with that
    #timestamp, so we can work in any directory without fear of overwriting 
    #anything
    timestr = time.strftime("%y%m%d-%H%M%S")   
    iou.make_folder(timestr + mod, wd)
    
    Log = Logger(timestr+'_log.txt')        #create logfile
    announce()                              #announce program version
    
    #define experiments to be done here
    #
    
    #get mechanism
    # calculate relaxation
    # calculate fluorescence relaxation
    param = re.Parameters() 

    param.MR_rate = [None]
    param.MR_avoid = [None]
    param.high_conc = 1e-3

    pulse_n = 1
    pulse_l = 500
    pad = 0.01

    rd, N_states, open_states, F_states = mechanisms.mechanism("dckF2")

    I = re.Train(pulse_n, pulse_l, pad, param, N_states, open_states, rd)
    I.build()
    I.construct_train()
    traces.append(I.t)
    traces.append(I.stim)
    traces.append(I.trace)
    traces.append(I.occupancy_t)

    #three levels - no fluorescence, full fluorescence and a partially quenched level
    F_vectors = [
    {0: 1,     1: 0,    2: 1,    3: 0,     4: 0   },
    {0: 0,     1: 1,    2: 0  ,  3: 0.5,   4: 0.5 },
    {0: 0,     1: 1,    2: 1,    3: 0,     4: 1   },
    {0: 1,     1: 1,    2: 0.5,  3: 0.5,   4: 0   },
    {0: 0,     1: 0,    2: 0,    3:   1,   4: 0  },
    {0: 0,     1: 0,    2: 0.5,  3:   1,   4: 0  },
    {0: 0,     1: 0,    2: 1,    3:   1,   4: 0  },
    {0: 0,     1: 0,    2: 1,    3: 0.5,   4: 0  },
    {0: 0,     1: 0,    2: 1,    3: 0,     4: 0  }
    ]

    for F_state_vector in F_vectors:
        F = re.Train(pulse_n, pulse_l, pad, param, N_states, F_state_vector, rd)
        F.build()
        F.construct_train()
        traces.append(F.trace)
    
    print traces
    curve_save(traces, timestr+"I&F") 
   

    del Log

    """
    f = open(timestr+'_mechs.txt', "w")
    for m in mech_list:
        r, n, o = mechanisms.mechanism(m)
        
        f.write("rate mechanism " + str(m) + "\n")
        f.write(pprint.pformat(r)) 
        f.write("\n**********\n")
        f.write("\nOpen states " + str(o))
        f.write("\n**********\n\n\n")
    f.close()
    """
