
__author__="Andrew"
__date__ ="$Aug 26, 2013 4:03:07 PM$"

import relaxes as re
import IO_utils as iou
import time
import mechanisms
#import pprint
import numpy
from logging import Logger
from IO_utils import curve_save

def announce ():
    print("\
    PCF simulator : \n\
    v. 0.1\
    Andrew Plested FMP-Berlin 2014\
    ")

def random_F_dict(N):
    # N is the number of states
    # returns a dictionary of state : F - intensity pairs
    v = {}
    for state in range(N):
        v[state] = numpy.random.random_sample()
        
    #print v
    return v    

def generate_F_dict_set(N):
    F_set = []
    # make a large set of F-vectors
    for i in range(10 * N**2):
        F_set.append(random_F_dict(N))
        
    return F_set

def baseline_normalise(trace):
    nbt = numpy.copy(trace)
    
    nbt -= nbt[0] # baseline against first element
    
    maxt = abs(nbt.max())
    mint = abs(nbt.min())
    
    if maxt == mint:
        #no change during trace?
        return numpy.zeros(len(trace))       #null
    
    if mint > maxt:
        nbt = -nbt
    
    nbt /= nbt.max()
    
    if nbt.max() != 1: print nbt.max()
    return nbt

def states_dict_2_vector(N, s):
    
    vec = numpy.zeros((N))
    for key in s:
        vec[key] = s[key]
    return vec
    
    
if __name__ == "__main__":
    
    #pick directory
    working_directory = "/users/andrew/desktop/projects/fluorescence/PCF trials"
    
    #modify filename with project
    mod = "_CC"
    traces = []
    normbs_tr = []
    F_vectors = []
    F_traces = []
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

    param.MR_rate = [(3,2)] # (4,6) is the rate between flipped states in flipF
                            # (3,2) is the rate between des in GG1
    param.MR_avoid = [None]
    param.high_conc = 1e-4

    pulse_n = 1
    pulse_l = 2000
    freq = .25
    rise = 200
    
    rd, N_states, open_states, F_states = mechanisms.mechanism("GG5")

    # not sure if open_states is needed here
    Sim = re.RCJ_Train(pulse_n, pulse_l, freq, rise, param, N_states, open_states, rd, sample=1000)
    Sim.build()
    Sim.rcj_calc_2()
    


    ##########need to convert dicts into vectors of open states
    osv = states_dict_2_vector (N_states, open_states)
    Sim.construct_trace(osv)
    
    #store the time signal, the stimulus and the "current" trace
    traces.append(Sim.t)
    Sim.stim += 2.2     #offset for graph
    traces.append(Sim.stim)
    traces.append(Sim.trace)
    traces_header = "time(ms)\tstim\tcurrent"
    
    NormBsTrace = - baseline_normalise(Sim.trace) - 1 #offset and invert for display purposes.
    normbs_tr.append(NormBsTrace)       #store the normalised current trace
    NB_header = "Norm-I\t"
    
    F_dict_set = generate_F_dict_set(N_states) #monte carlo generation of F vector
    
    counter = 0
    F_v_header = ""
    F_header = ""
    
    for F_state_vector in F_dict_set:
        
        fsv = states_dict_2_vector (N_states, F_state_vector)
        Sim.construct_trace(fsv)    #weight states according to F_vector
        NormBsTrace = - baseline_normalise(Sim.trace)   # switch sign to match display of GABA data
        
        F_traces.append(Sim.trace)    #store raw F-trace 
        F_header += "F{0}\t".format(counter)
        
        normbs_tr.append(NormBsTrace)   #store normalised and baselined F trace
        NB_header += "NBF{0}\t".format(counter)
        
        F_vectors.append(fsv)       #store F-vector
        F_v_header += "Fv{0}\t".format(counter)
        
        counter += 1 #update the trace counter for header elements
        
    #traces.append(Sim.occupancy_t)
    #print traces
    curve_save(traces, timestr+"I&S", traces_header) 
    curve_save(F_vectors, timestr+"Fvectors", F_v_header )
    curve_save(normbs_tr, timestr+"NormBsI+F", NB_header)
    curve_save(Sim.occupancy_t, timestr+"Occup")
    curve_save(F_traces, timestr+"F", F_header)
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
