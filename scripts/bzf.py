__author__="Andrew"
__date__ ="$30-Oct-2013 19:41:59$"
#from core_utils import generate_Q
from relaxes import Relaxation
from qmat import Q_mat
import numpy

def mech1(conductance=15):
    #irreversible apparent crosslinking rates, per episode
    
    #    /-OI-\
    #   OO    II
    #    \_IO_/
    
    rd = {
    (0, 1) :  ['oo-oi', [0.03, 0]] ,
    (1, 3) :  ['oi-ii'  , [0.03, 0]] ,
    (0, 2) :  ['oo-io' , [0.03, 0]] ,
    (2, 3) :  ['io-ii' , [0.03, 0]] ,
        }
        
    N_states = 4
    open_states = {0:30, 1: conductance, 2: conductance }   #values are conductances

    return rd, N_states, open_states

def mech2(conductance=15):
    #irreversible apparent crosslinking rates, per episode
    # compacted version of mech1
    #   
    #   OO    II
    #    \_IO_/
    
    rd = {
    (0, 1) :  ['oo-oi', [0.1, 0]] ,
    (1, 2) :  ['oi-ii'  , [0.05, 0]] 
        }
        
    N_states = 3
    open_states = {0:30, 1: conductance , 2: conductance }   #values are conductances

    return rd, N_states, open_states

def mech4(conductance=15):
    #   
    #   OOOO-OOOI-OOII-OIII-IIII
    
    rd = {
    (0, 1) :  ['oooo-oooi', [0.08, 0]] ,
    (1, 2) :  ['oooi-ooii' , [0.06, 0]] ,
    (2, 3) :  ['ooii-oiii' , [0.04, 0]] ,
    (3, 4) :  ['oiii-iiii' , [0.02, 0]] ,
        }
        
    N_states = 5
    open_states = {0:30}
    
    return rd, N_states, open_states
     
            
            
if __name__ == "__main__":
    #dictionary of dictionaries of conductances
    
    
    #HOMOMER
    open_set = {
            "AMPA4": {0:30, 1:15, 2:3},
            "AMPA4_flat": {0:30, 1:22, 2:15, 3:7, 4:0},
            "sigmoid4": {0:30, 1:25, 2:15, 3:0},
            "waiting4": {0:30, 1:30}
    }
    n_trace = len(open_set)
    
    trials = range (n_trace)
    #gammas = range (0, 30, 5)
    #print (trials, gammas)
    points = 100
    episodes = range(points)
    traces = numpy.zeros((points, n_trace + 1))
    
    traces [:,-1] = episodes
    
    p_init = numpy.array([1, 0, 0, 0, 0]) #Begin in state 0
    header =""
    rates, N_states, open_states = mech4()
    Q = Q_mat(N_states)

    Q.build_Q(rates)  
    Q.do_diag()             #otherwise you will get singular matrix complaint
    rel = Relaxation(Q, p_init, True)
    
    for o_key,trial in zip(open_set.keys(), trials):
        
        open_states = open_set[o_key]
        rel.assemble(episodes, open_states)
        traces [:,trial] = rel.relax_sum
        header += o_key +"\t"
        
    print header, traces
    numpy.savetxt("//users/andrew/bzf-homo2.txt", traces, delimiter='\t') 
    

    #HETEROMER or DIMER
    open_set = {
            "AMPA2": {0:30, 1:15, 2:3},
            "AMPA2_flat": {0:30, 1:15, 2:0},
            "heteromer_hi": {0:30, 1:25, 2:20},
            "heteromer_lo": {0:30, 1:20, 2:12}
    }
    n_trace = len(open_set)
    
    trials = range (n_trace)
    #gammas = range (0, 30, 5)
    #print (trials, gammas)
    points = 100
    episodes = range(points)
    traces = numpy.zeros((points, n_trace + 1))
    
    traces [:,-1] = episodes
    
    p_init = numpy.array([1, 0, 0]) #Begin in state 0
    header =""
    rates, N_states, open_states = mech2()
    Q = Q_mat(N_states)

    Q.build_Q(rates)  
    Q.do_diag()             #otherwise you will get singular matrix complaint
    rel = Relaxation(Q, p_init, True)
    
    for o_key,trial in zip(open_set.keys(), trials):
        
        open_states = open_set[o_key]
        rel.assemble(episodes, open_states)
        traces [:,trial] = rel.relax_sum
        header += o_key +"\t"
        
    print header, traces
    numpy.savetxt("//users/andrew/bzf-Het2.txt", traces, delimiter='\t') 
    
