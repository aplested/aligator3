#concentration response and concentration inhibition responses from original relaxes.py
from relaxes import ExperimentSetup
class CrExpt(ExperimentSetup):
    #moved from relaxes_w.py
    """construct concentration response relations (peak and ss)
    on a set of mechanisms with altered rate(s)  
    """
    
    def run(self, min_conc = 10e-8, max_conc = 10e-2):
        
        print ("Conc. Response Experiment with {0} M minimum, and {1} M maximum, concentration.".format(min_conc, max_conc))
        self.txt_curves = ''
        for r in self.rs.rates_set:
            _ra = r[1]
            cr = ConcResponse(self.param, self.N_states, self.open_states, _ra, min_conc, max_conc)
            cr.build_curve()
            
            #append one by one to get the right arrangement??
            for t in cr.responses:
                self.trace_set.append(t)

            #get rate constant
            #keys of ra are the rate tuple
            #refer to it with rate name
            for _rtc in self.param.rate_to_change:
                print (str(_rtc))
                _rate_changed = _ra[r_tuple_from_r_name(_ra, _rtc)][1][0]
            
                self.table += str(r[0]) + '\t' + str(_rate_changed) + '\n'
            
                head = '\n-\nTrial#\t' + str(r[0]) + '\t' + str(self.param.rate_to_change) + '\t' + str(_rate_changed) + '\n'
            
            print (cr.printout)
            self.txt_curves += head
            self.txt_curves += cr.printout
            
        self.curve_save(self.trace_set)
        self.text_out(self.txt_curves)          #extra data to pass to text_out
        
        

class ConcResponse:
    #moved from relaxes_w.py
    """Calculate peak and equilibrium responses over a range of concentrations
        Methods:
        __init__        : takes rates and P_init
        build_curve     : gather and process
        make_printable  : string to describe data generated
        
        Output: 
            curve as numpy array [3 x steps]: conc, peak, steady_state, 
            all relaxations and summary of curve as text
    """
    
    def __init__(self, param, N_states, open_states, rates, min_conc, max_conc, steps=19, P_init=None):
        """    Arguments:
            N_states                -- Number of states in the mechanism
            rates                   -- rate dictionary
            open_state              -- dictionary of open state : conductance pairs
            min_conc and max_conc   -- pretty self-explanatory
            steps                   -- points in the curve
            P_init                  -- the initial occupancy for each c-jump"""
    
        self.responses = []
        self.log_min_conc = log10(min_conc)
        self.log_max_conc = log10(max_conc)
        self.steps = steps
        self.rates = rates
        
        self.exponent = float(self.log_max_conc - self.log_min_conc) / self.steps
        
        self.N_states = N_states
        self.open_states = open_states
        self.curve = numpy.zeros((self.steps, 4))       #conc, peak, steady_state, 1ms
        
        self.MR_rate = param.MR_rate
        self.MR_avoid = param.MR_avoid

        if P_init == None:
            #take resting (i.e. zero concentration) equilibrium for start of jump
            Q_z, self.P_init = generate_Q(self.N_states, {1: param.zero_conc},
                                        self.rates, self.MR_rate, self.MR_avoid)
            print ("self.P_init:", self.P_init)
        else:
            self.P_init = P_init
        
    def build_curve(self, drugs = {1:0}, agonist_to_use = 1):
        """    drugs -- dict, keys must include all drugs used in rate dict.
        agonist_to_use -- specify which key in the drug dictionary to update"""
        
        _t_step = numpy.arange (1, 9, .2)
        _log_t_step = 1e-7 * 10 ** (_t_step) 
        
        #put the timebase for the jumps as first column
        self.responses.append(_log_t_step)
        
        for n in range (self.steps):

            # calculate relaxation at a range of concs
            agonist_conc = 10 ** ( self.log_min_conc + n * self.exponent )
            #Currently, MR is recalculated on each Q matrix, simple but wasteful 
            #update drug dictionary 
            drugs[agonist_to_use] = agonist_conc

            Q_conc,  P_eq = generate_Q(self.N_states, drugs, self.rates, self.MR_rate, self.MR_avoid)
            print ("Calculating relaxation with following drug concentration" + 
                    str(drugs) + ", giving Qmat:\n" + str(Q_conc.Q))
            #print 'P_init', P_init

            r = Relaxation(Q_conc, self.P_init)
            print (self.open_states)
            r.assemble(_log_t_step, self.open_states)
            
            #take max of hi-conc jump
            max_response  = numpy.max(r.relax_sum)
            self.responses.append(r.relax_sum)

            eqbm = r.relax_sum[-1]
            print ("Equilibrium P-open, only true if conductances are normalised: ", eqbm)
            onems = r.relax_sum[15]     #1ms point is normally the 15th in time series (HACK)
            #store points
            self.curve [n] = (agonist_conc, max_response, eqbm, onems)
        
        print (self.curve)
        self.make_printable()
        
    def make_printable(self):
                
        self.printout = "Concentration Response\n"
        self.printout += "open states: " + str(self.open_states) + "\n"
        self.printout += "P_init\n" + str(self.P_init) + "\n"
                
        self.printout += "\n\nconc\tpeak\tss\t1ms peak\n"
        for line in self.curve.tolist():
            for elem in line:
                self.printout += str(elem) + "\t"  
            
            self.printout += "\n"
        

class ConcInhibition:
    """ //______|
        //------|
        //^^^^^^|"""
        
    def __init__(self):
        pass
        