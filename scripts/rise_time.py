__author__="Andrew"
__date__ ="$Aug 26, 2013 4:03:07 PM$"

import numpy
import time
from math import log as ln

from mechanisms_albert import mechanism
import relaxes as re

import common.IO_utils as iou
import common.simple_log as sl
import common.threshold as th

   
def announce ():
    print("Kinetics simulator for variable rise times \n\
    Andrew Plested FMP-Berlin 2017")

def get_rise_fall (data, low=0.1, high=0.9):
    print ("\nCalculating 10-90% rise and fall times, and equivalent tau_decay...")
    print ("Rising threshold algorithm")
    a, b, c, d, e, f = th.rise_threshold (data, low, high)

    aa, bb, cc, dd, ee, ff = th.fall_threshold (data, low, high)
     
    rise = f - e
    fall = ee - ff
        
    print ("{0} - {1}% rise time = {2:.3f} samples".format(int(low * 100), int(high * 100), rise))
    print ("{0} - {1}% fall time = {2:.3f} samples".format(int(low * 100), int(high * 100), fall))   
    
    fall_tau =  fall / ln(9)      # scaling time taken to lose 80% of amplitude 
                                    # fall = t10 - t90
                                    # ln (0.9) - ln (0.1) = ln( 0.9 / 0.1 )  or ln (9)
                                    
    print ("Equivalent exponential tau for falling phase: {0:.3f} samples".format(fall_tau))
    max = data.max()
    min = data.min()
    
    return max - min, rise, fall, fall_tau
    
def states_dict_2_vector(N, s):
    
    vec = numpy.zeros((N))
    for key in s:
        vec[key] = s[key]
    return vec
    
if __name__ == "__main__":
    
    #pick directory
    working_directory = "/users/andrew/desktop/projects/albert_rise"
    
    #modify filename with project
    mod = "_rise"
    traces = []
    rise_fall_times = []
    #move automatically to working directory
    #variable "file_list" is not used
    file_list, wd = iou.getpath(True, working_directory)
    
    #generate time string (unique to the second) and make a new folder with that
    #timestamp, so we can work in any directory without fear of overwriting 
    #anything
    timestr = time.strftime("%y%m%d-%H%M%S")   
    iou.make_folder(timestr + mod, wd)
    
    Log = sl.Logger(timestr + "_log.txt")        #create logfile
    announce()                              #announce program version

    # calculate relaxation at different rise times
    
    param = re.Parameters() 

    ### NEED TO FIX PARAMETERS HERE
    
    param.MR_rate = [(4,3), (6,5)] # (4,3) is single bound recovery, (6,5) is unbound recovery
    param.MR_avoid = [None]
    
    param.high_conc = 1e-2
    
    pulse_n = 1
    pulse_l = 0.8
    freq = 50          #gives 10 ms prepadding, and 20 postpadding
    
    traces_header = "time(ms)"
    sample_us = 5       #sample time in microseconds
    factors = [2, 1, 0.5, 0.2, 0.1, 0.05]          #factor to change the binding rates
    rise_times = [0.100, 0.200, 0.300, 0.400, 0.500, 0.800]
    mech = "R+H4" 
    
    for factor in factors:
        # get mechanism
        # not sure if open_states is needed here
        rd, N_states, open_states = mechanism(mech, factor)     
        for rise in rise_times:
            print ("\n\nRate dictionary: {0}\
            \nNumber of states: {1}\
            \nOpen states : {2}\
            \nSolution rise time : {3} ms\
            \nBinding Rate Factor : {4}\n\
            ".format(rd, N_states, open_states, rise, factor))
            
            Sim = re.RCJ_Train(pulse_n, pulse_l, freq, rise, param, N_states, open_states, rd, sample=sample_us)
            Sim.build()
            Sim.rcj_calc_2()

        ##########need to convert dicts into vectors of open states
            osv = states_dict_2_vector (N_states, open_states)
            Sim.construct_trace(osv)

        #store the time signal, the stimulus and the "current" trace
            
            stim_name = "stim {0}[{1}][{2}]".format(mech, rise, factor)
            trace_name = "current {0}[{1}][{2}]".format(mech, rise, factor)
            
            Sim.stim *= 10 #rescale
            Sim.stim += 1   #offset
            traces.append(Sim.stim)
            traces.append(Sim.trace)
            max, riset, fallt, fall_tau = get_rise_fall(Sim.trace)
            
            ##convert samples to microsecond
            
            riset *= sample_us
            fallt *= sample_us
            fall_tau *= sample_us
            
            
            traces_header += "\t{0}\t{1}".format(stim_name, trace_name) #append column names to header line
            rise_fall_times.append("{0}\t{1:.2f}\t{2:.0f}\t{3:.0f}\t{4:.0f}\n".format(trace_name, max, riset, fallt, fall_tau))
            iou.curve_save(Sim.occupancy_t, timestr+"Occup " + mech + "_" + str(rise) + "_" + str(factor))
            
    traces.insert(0, Sim.t) #we only want the timepoints once, first column
    iou.curve_save(traces, timestr+"I&S_", traces_header) 
    
    rise_fall_times.insert(0, "file\tmax\trise\tfall\tTau_fall\n") #header
    with open (timestr+"r_f_times.txt", "w") as output:
        for line in rise_fall_times:
            output.write(line)

    del Log
