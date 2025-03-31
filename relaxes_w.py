#! /usr/bin/python

# Classes:
#
# Parameters          - Common information required to run experiments
# RateGenerator       - build a set of rates for a rate experiment
# ExperimentSetup     - generic setup for all the rate experiments
# TwoMechSetup        - 
#
# PairMechComparison  - build kinetic comparisons between two mechanisms
# ConcResponse        - MOVED TO CONCENTRATION calculate concentration-response curve
# Relaxation          - calculate relaxation (open states...)
# Recovery            - MOVED TO RECOVERY calculate recovery curve (desensitized/shut state relaxation?)
# Recovery_Qmade      - MOVED TO RECOVERY 
# Train               - calculate response to a train of pulses
# ConcInhibition (ND) - MOVED TO CONCENTRATION calculate low concentration-inhibition relation 
# PulseInhibition (ND)- prepulse inhibition (3 barrel) experiment
# RcjTrain            - calculate train using realistic concentration jumps
#
# TrainExpt           - calculate family of trains to see effect of changing a rate
# RecoveryExpt        - MOVED TO RECOVERY calculate family of recovery curves
# CrExpt              - MOVED TO CONCENTRATION calculate family of concentration response curves
# RelaxExpt           - calculate family of relaxations
# JFExpt              - calculate families of relaxations to different single pulses subclassing TrainExpt 
#
#   August 2013: ConcResponse added
#   October 2013: building pairwise comparisons (for two mechanisms)


from __future__ import print_function
from math import exp, log10
import copy
import numpy
from mechanisms import mechanism
#from qmat import Q_mat
from common.core_utils import generate_Q, r_tuple_from_r_name, convert, convert_ms

import common.rcj_lib as rcj

__author__="Andrew"
__date__ ="$Jun 12, 2010 9:10:37 AM$"


class Parameters(dict):
    """Encapsulate some common information required to run the experiment
    allow instantiation with a default set.
    from http://stackoverflow.com/a/9550596
    Data storage by subclassing dict"""
    
    def __init__(self, parameters=None):
        if parameters == None: 
            self.set_defaults()  
        else:
            for d in parameters.keys():
                self[d] = parameters[d]

    def __getattr__(self, param):
        return self[param]

    def __setattr__(self, param, value):
        self[param] = value

    def set_defaults(self):

        self['sim_name'      ] = "trial"
        
        self['rate_to_change'] = 'd2op_plus'
        self['N_trials'      ] = 10   
        self['hi_exp'        ] = 1.5
        self['lo_exp'        ] = -1.5
        self['var_power'     ] = [1]  #default is one rate, varying with full exponent
                                    #extend this list in case multiple 
                                    #variables should be varied
                                    #with different powers
                                    
        #Pick MR_rates that are common, and check them against mechanism later
        self['MR_rate'       ] = [(1,7), (0,5), (7,8), (5,6)]
        self['MR_avoid'      ] = []     #this will be augmented according to varying rates
        self['zero_conc'     ] = 0 
        self['high_conc'     ] = 1e-2
        self['MR_avoid_preserve'] = False
        self['open_state_matrix'] = None       #usually set within mechanism, but this is the external route

    def MR_rate_clean(self, mech_rates):
        """Remove rate tuples from 'MR_rate' that are not in the mechanism"""
        for rate_tuple in self['MR_rate']:
            
            if rate_tuple not in mech_rates.keys():
                self['MR_rate'].remove(rate_tuple)
                print ("Removed " + str(rate_tuple) + " from MR_rate")
                
        #check for rate to change in MR params
        for _rtc in self['rate_to_change']:
            rtc_tuple = r_tuple_from_r_name(mech_rates, _rtc)
        
            if rtc_tuple not in self['MR_avoid'] and not self['MR_avoid_preserve']:
                #this blanket hack will remove any special info in MR_avoid
                #flag can be used to make MR_avoid invulnerable
                
                self['MR_avoid'].append(rtc_tuple)
                print ("Adding "+str(rtc_tuple)+" to MR_avoid (now: "+ str(self['MR_avoid'])+" )\n")
            
            #take the rate to change out of MR use    
            if rtc_tuple in self['MR_rate']:
                self['MR_rate'].remove(rtc_tuple)
        
class RateGenerator:
    """
    Prepare a list of rate sets within which a subset of the rate constants
    are varied. Use for generating Q-matrices for a set of experiments.
    
    Input - rate dictionary, rates to vary during experiment, 
    and the high and low exponents of 10 and number of trials
    rates to vary is a list
    var_power is a list of factors to make different rates vary with different extents
    
    Output - rates_set : a list of experiment number : rate set pairs
    """
    
    def __init__(self, rates, param):
        
        self.rates_set = []
        self.core_rate_set = rates
        self.rates_to_vary = param.rate_to_change
        self.hi_exp = param.hi_exp
        self.lo_exp = param.lo_exp
        self.N_trials = param.N_trials
        self.exp_step = float(self.hi_exp - self.lo_exp) / self.N_trials
        self.var_power = param.var_power 
        print ("Var_power..."+str(param.var_power))
        
    def make_tuple_list(self):
        #construct an ordered list of the keys in rate dictionary
        #(state from, to) tuples for the values that will be tweaked
        #these tuples are not mutated
        #in some cases, might want to vary rates in lock-step -
        #like forward binding rates
        self.tuples_to_vary = []
        for r in self.rates_to_vary:
            print (str(r))
            t = r_tuple_from_r_name(self.core_rate_set, r)
            self.tuples_to_vary.append(t)  
    
    def make_rate_vary_list(self):
        #construct an ordered list of the original rate values that will be 
        #mutated- so deepcopy needed to avoid propagation
        _b_r = []
        for r in self.tuples_to_vary:
            _b_r.append(self.core_rate_set.get(r))

        self.base_rates_to_change = copy.deepcopy(_b_r)    
        print ("Base rates to change:" + str(self.base_rates_to_change))
    
    def make(self):
        
        self.make_tuple_list()
        self.make_rate_vary_list()
        
        for trial in range(self.N_trials):
        
            exponent = self.lo_exp + trial * self.exp_step       
            
            adjusted_rate_set = copy.deepcopy(self.core_rate_set)
            
            #adjust each rate in turn 
            for base_r, tuple, power in zip(self.base_rates_to_change, self.tuples_to_vary, self.var_power):
                #_exp = float(exponent)
                _b = float(base_r[1][0])
                _adjusted_rate = _b * 10 ** (exponent * power)
                adjusted_rate_set[tuple][1][0] = _adjusted_rate
                #show calculation
                #print base_r, _exp, _b, 10**exponent, _adjusted_rate
            
            self.rates_set.append([trial, adjusted_rate_set])    

class ExperimentSetup:
    """ Generic base class for all experiments on a single mechanism
        Instantiated as mechanism container 
        Methods :   curve_save  : write arrays out to disk
                    text_out    : write tables out to disk"""
    
        
    def __init__(self, mech=None, param=None):
        """ Arguments
            mech       : kinetic mechanism in rate dictionary form
            param      : instance of experiment class containing parameters as attributes
        """
        
        #get mechanism
        if mech == None:
            # use default mechanism
            self.rates, self.N_states, self.open_states = mechanism()  
            print ("No mech given, using default [ExperimentSetup]")
        else:
            self.rates, self.N_states, self.open_states = mechanism(mech)
        
        #set parameters
        if param == None:
            self.param = Parameters()        #set default parameters        
            print ("No parameters given, using default [ExperimentSetup]")
            #Remove tuples from MR_rate that aren't in the mechanism
            #self.param.MR_rate_clean(self.rates) 
        else:
            self.param = param
        print ("SPOSM", self.param.open_state_matrix)
        print ("[ExperimentSetup] Cleaning MR parameters")
        self.param.MR_rate_clean(self.rates)
          
        
        #make rate set
        self.rs = RateGenerator(self.rates, self.param)
        self.rs.make()  #the ExperimentSetup object "rs", 
        #attribute "rates_set" is now a list of [experiment number and rates] pairs
    
        #output specification
        self.table = "Trial #\t"+ '\t'.join(n for n in self.param.rate_to_change) + "\tOpen States" +'\n'
        self.trace_set = []  
        self.header = False          #default no header for the trace output. Build in some subclasses
     
    
    def curve_save(self, curve_data, mod=""):
        #print ("shapes")
        #for elem in curve_data:
        #    print ("elem"+ str(len(elem)))
        #    for e in elem:
        #        print ("e"+ str(len(elem)))
        print (mod)
        print (self.param.sim_name)
        self.trace_coll = numpy.column_stack(curve_data)
        
        if not mod: mod = ""
        
        if self.header:
            print (self.header)
            numpy.savetxt(self.param.sim_name + mod + ".txt", self.trace_coll, delimiter='\t', header=self.header) 
        else:
            numpy.savetxt(self.param.sim_name + mod + ".txt", self.trace_coll, delimiter='\t') 

    def text_out(self, extra_data=False):

        print ("Printout generated by " + self.__class__.__name__ + "\n")
        print (self.table)
        
        self.f=open(self.param.sim_name + '.xls', 'w')
        self.f.write("Printout generated by " + self.__class__.__name__ + "\n")
        self.f.write(self.table) 
        if extra_data:
            self.f.write(extra_data)
        self.f.close()
  
  
class Relaxation:
    """
    Calculate relaxation from a Q-matrix
    can specify states to put together (as tuple, e.g. P-open - all open states)
    must supply time points to calculate over
    must supply Q-matrix
    This is a core class that is used by the other more complicated experiments

    relaxations are first made as 2-D arrays where
    columns correspond to individual state occupancies
    rows are isochrones
    
    Methods:
        __init__        : takes Q matrix and initial occupancy (P_init)
        assemble        : gather and process
        calculate       : calculate occupancies during relaxation
        calculate_sum   : sum up occupancies
        make_printable  : string to describe data generated
    """
    
    def __init__(self, Q, P, verbose=False):
       
        #???self.state_by_state_relax = {}
        self.Q = Q
        if verbose: print ("Dimension of Qmatrix (states): ", self.Q.N_states)
        
        self.P_init = P
        self.Q.relax(self.P_init)
        self.eigenvals = self.Q.eigenval
        #default state to calculate for is state 0
        #By DC's convention, this is the open state if there's only one.
        self.states_sum=(0)
        self.verbose = verbose
        if verbose: 
            print ("Q:")
            print (self.Q.show())
            print ("Q.w:")
            print (self.Q.w)
        
    def assemble(self, time_pts, states_to_sum=False):
        """put the relaxation together"""
        #need to pass time range
        #if "states to sum" (the list of state occupancies that should be summed)
        #is provided, it is not False and will be set here
        if states_to_sum:
            self.states_sum = states_to_sum
        else:
            self.states_sum = False
      
        self.pts = time_pts
        
        if self.verbose:
            print ("Assemble: Length of relaxation in points: ", len(self.pts))
            if self.states_sum:
                _ss = ""
                for x in self.states_sum:
                   _ss += str(x)+'\t'
                print ("States to sum (usu. open states): "+_ss)
        
        #Wow: using numpy.empty rather than numpy.zeros here is a disaster!
        self.relax = numpy.zeros([len(self.pts),self.Q.N_states])

        #calculate and make output.
        self.calculate()
        if self.states_sum: self.calculate_sum()
        #store final occupancy (critical for chaining together relaxations)
        self.P_final = self.relax[-1, :]
        self.make_printable()
    
    def calculate(self):
        #construct relaxation from sum of occupancy(t) over each state
        # need to take the pt-th value from the array self.pts (=time)

        #this way of updating self.relax relies on not using numpy.empty
        for s in range(self.Q.N_states):
            for pt in range(len(self.pts)):
                for a, k in zip(self.Q.w[:, s], self.eigenvals):
                    self.relax [pt, s] += a * exp (k * self.pts[pt])

    def calculate_sum(self):
        #calculate sum of occupancies (with t) for states given in states_sum
        self.relax_sum = numpy.zeros([len(self.pts)])
        
        #Sum slices, each of which is P(s)(full t range), weighted by conductance
        for s in self.states_sum.keys():
            #self.states_sum[s] is the conductance of state s
            self.relax_sum += self.relax [:,s] * self.states_sum[s]
            #print self.relax_sum
        
    def make_printable(self):
        
        self.printout = "states sum:" + "\n" + str(self.states_sum) + "\n"
        self.printout += "eigenvalues" + "\n" + str(self.eigenvals) + "\n" 
        
        self.printout += 'P_init' + "\n" + str(self.P_init) + "\n"
        self.printout += 'P_final' + "\n" + str(self.P_final) + "\n"

        self.printout += "\n\nby state\n"
        for pt in range(len(self.pts)):
            self.printout += str(self.pts[pt]) + "\t" + str(self.relax[pt, :]) +  "\n"
        
        self.printout += "\n\nsummed\n"
        for pt in range(len(self.pts)):
            self.printout += str(self.pts[pt]) +"\t" +str(self.relax_sum[pt]) + "\n"
 

class RelaxExpt(ExperimentSetup):   
    
    """generate family of relaxations with varying rate"""
    
    def run(self, start=0, end=8, steps=.2):
        """ start   : min. interval in log microsec
            end     : max. interval in log microsec
            steps   : log decade step size
        """
        #identical for each relaxation, append as first col of traces
        self.t_step = numpy.arange (start, end, steps)
        self.log_t_step = 1e-6 * 10 ** (self.t_step) 
        self.trace_set.append(self.log_t_step)
        self.header = "t_" + str(self.param.sim_name)
        for r in self.rs.rates_set:
            _ra = r[1]
            Qzero,  P_init_zero = generate_Q(self.N_states, {1: self.param.zero_conc}, _ra, self.param.MR_rate, self.param.MR_avoid)
            Qhi,    P_init_hi   = generate_Q(self.N_states, {1: self.param.high_conc}, _ra, self.param.MR_rate, self.param.MR_avoid)

            rel = Relaxation(Qhi, P_init_zero)
            rel.assemble(self.log_t_step, self.open_states)
            self.trace_set.append(rel.relax_sum)
            for _rtc in self.param.rate_to_change:
                print (str(_rtc))
                _rate_changed = _ra[r_tuple_from_r_name(_ra, _rtc)][1][0] 
                self.table += str(r[0]) + '\t' + str(_rate_changed) + '\n'
                print (rel.printout)
                self.header += '\t'+ str(self.param.sim_name) +"_{0:.2f}".format(_rate_changed)
            #self.overall_printout += rel.printout

        #trace_set.append(log_t_step)
        #trace_set.append(t.stim)

        self.curve_save(self.trace_set, mod='_traces')
        self.text_out()

