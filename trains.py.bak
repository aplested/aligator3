#classes for simulating responses to trains of pulses
from relaxes import ExperimentSetup, Relaxation
from common.core_utils import generate_Q, convert, r_tuple_from_r_name
import numpy

class Train:
    #moved from relaxes.py
    """Trains of ideal square pulses"""
    
    def __init__(self, npulse, pwidth, pfreq, param, N_states, open_states, rates):
        
        #pulse sequence will be built as a list because order is important
        self.pulse_seq = []
        
        self.n = npulse
        self.width = pwidth     #in ms
        self.freq = pfreq       #in Hz
        
        self.open_states = open_states
        self.zero_conc = param.zero_conc
        self.high_conc = param.high_conc
        
        #lo_rates = copy.deepcopy(rates)
        #hi_rates = copy.deepcopy(rates)
        
        print("make Qlo, conc: "+str(self.zero_conc) )
        
        #rates is deepcopied in generate_Q so doesn't propagate 
        self.Qlo, self.P_init_lo = generate_Q(N_states, {1: self.zero_conc}, 
                                            rates, param.MR_rate, param.MR_avoid)
        
        print("make Qhi, conc: "+str(self.high_conc))
        self.Qhi, self.P_init_hi = generate_Q(N_states, {1: self.high_conc}, 
                                            rates, param.MR_rate, param.MR_avoid)

        #make trace containers
        #create zero by N matrix for appending time series of occupancies
        #http://stackoverflow.com/questions/568962/how-do-i-create-an-empty-array-matrix-in-numpy
        
        self.t = numpy.zeros((0))
        self.stim = numpy.zeros((0))
        self.trace = numpy.zeros((0))
        self.occupancy_t = numpy.zeros((0, N_states))


    def build(self, prepad=True):
        # build list of pulse steps, with values of start time, interval and Q-matrix
        
        self.ipi = 1000./self.freq
        self.off_interval = self.ipi - self.width
        
        # the running timer of each pulse start time (in ms)
        timer = 0
        
        if prepad:
            self.pulse_seq.append([timer, 100, self.Qlo, self.zero_conc])
            timer = 100
        
        for i in range(self.n):
            
            self.pulse_seq.append([timer, self.width, self.Qhi, self.high_conc])
            timer += self.width
            self.pulse_seq.append([timer, self.off_interval, self.Qlo, self.zero_conc])
            timer += self.off_interval
            
    def construct_train(self):

        _P = self.P_init_lo

        for step in self.pulse_seq:
            _pulse_start = step [0]
            _interval = step [1]
            _Q = step[2]
            _conc = step[3]
            _t_steps = convert(_interval)
            #print ("Alpha:"+ str(_Q.Q[0,5]))  a check for updating
            r = Relaxation(_Q, _P)
                  # 5 points per log decade is the default
            r.assemble(_t_steps, self.open_states)
            
            _P = r.P_final      #update _P to pass forward to the next relaxation
            
            self.t = numpy.append(self.t, _t_steps + _pulse_start / 1e3, axis=0)
            self.occupancy_t = numpy.append(self.occupancy_t, r.relax, axis=0)
            self.trace = numpy.append(self.trace, r.relax_sum, axis=0)
            self.stim = numpy.append(self.stim, numpy.ones(len(_t_steps)) + _conc)
            #effective offset of 1 M
            
            #print "sot", self.occupancy_t
            #print "r.relax", r.relax
            #print "r.relax_sum", r.relax_sum
            #print "self.trace", self.trace
        self.P = _P                 #pass on final value of occupancy 
        self.make_printable()
        
    def make_printable(self):
        
        self.printout = "train\n"
        self.printout += "open states\n" + str(self.open_states) + "\n"
        
        self.printout += "P_init\n" + str(self.P_init_lo) + "\n"
        self.printout += "P_final\n" + str(self.P) + "\n"
        
        self.printout += "\n\nsummed\n"
        for t, a, i in numpy.nditer([self.t, self.stim, self.trace]):
            self.printout += str(t) + "\t" + str(a) + "\t" + str(i) + "\n"
    
    def resample(self):
        #take unequally sampled knitted train response and sample equally
        #not done yet
        pass
        #convert train info into piecewise record

class RCJ_Train:
    #moved from relaxes.py
    """Trains of realistic concentration jumps"""
    
    def __init__(self, npulse, pwidth, pfreq, prise, param, N_states, open_states, rates, sample=8):
             
        #default sampling 8 microseconds
        
        self.n = npulse         #number of pulses
        self.width = pwidth     #width of each pulse in ms
        self.freq = pfreq       #in Hz
        self.rise = prise       #10-90% time in ms
        self.params = param
        
        self.N_states = N_states
        self.open_states = open_states
        self.rates = rates
        self.MR_needed = True   #Assume until told otherwise
        
        self.zero_conc = param.zero_conc
        self.high_conc = param.high_conc
        
        self.sample_time = sample # microseconds
        self.sample_time_ms = self.sample_time / 1e3 #milliseconds
    
        #print("make Qlo, conc: " + str(self.zero_conc) )
        
        #rates is deepcopied in generate_Q so changes don't propagate 
        #at the first run, MR_needed is True by default in generate_Q (we don't know yet)
        self.Qlo, self.P_init_lo = generate_Q(N_states, {1: self.zero_conc}, 
                                            rates, param.MR_rate, param.MR_avoid)
        
        #did the calcuation of self.Qlo reveal that there are no loops 
        #that is, was self.Qlo.MR_needed set to False?
        #if so, save the trouble of calculating it again during this jump
        if self.Qlo.MR_needed == False:
            self.MR_needed = False
        #Changed by AP 170619 to stop endless recalculation of MR
    
    def build(self, prepad=True):
        # build concentration profile 
        # prepad adds one half of the interpulse interval to the start of the record
        # lay out pulses one by one onto stimulation record
        # 160723 tested, works as expected when rcj_lib updated
        
        self.ipi = 1000./self.freq
        self.off_interval = self.ipi - self.width
        self.duration = prepad * self.ipi / 2 + self.n * self.ipi #in millseconds
        self.samples = int(self.duration / self.sample_time_ms) 
        
         #make trace containers
        #create zero by N matrix for appending time series of occupancies
        #http://stackoverflow.com/questions/568962/how-do-i-create-an-empty-array-matrix-in-numpy
        self.t = numpy.arange(0, self.duration, self.sample_time_ms)    
        self.stim = numpy.zeros((self.samples))
        self.trace = numpy.zeros((self.samples))
        self.occupancy_t = numpy.zeros((self.samples, self.N_states))
        
        
        # the running timer of each pulse start time (in ms)
        timer = 0
        
        if prepad:
            timer = self.ipi / 2
        
        for i in range(self.n):             #step through the pulses in turn
            #erf pulse input is in microseconds
            self.stim = rcj.erf_pulse(self.stim, self.width * 1e3, self.high_conc, self.rise * 1e3, timer * 1e3, self.sample_time)
            timer += self.ipi
            
    def rcj_calc_2 (self, P=[]):
        '''
        argument --
        P           : optionally pass current occupancy (for chains of pulses)
        '''

        Q_library = {}

        dt = self.sample_time * 1.e-6
            #convert from microseconds to seconds

        for idx in range (len(self.t)):

            #extract concentration.
            c = self.stim[idx]

            if c in Q_library:
                #retreive Q if previously calculated, Qc_w stands for "working Q(c)" also pick up A_matrices etc
                Qc_w = Q_library[c]

            else:
                #calculate Q matrix, spectral coefficients for given concentration
                #initialise
                #MR_needed is known from the initial calculation of Qlo in __init__
                Qc_w, P_inf = generate_Q(self.N_states, {1: c}, 
                                self.rates, self.params.MR_rate, self.params.MR_avoid, self.MR_needed)
                
                #calculate spectral coefficients
                Qc_w.spectral()

                #store Q, eigenvalues of Q, and A matrices for future use (called a hint in Python)
                Q_library[c] = Qc_w

            if P != []:
                #Not the first step or no blank input so use P from last step to calculate new occupancy

                #creates Q.w[:,:], nth row of which is p * A_sub_n
                #Note that P is not used again in the calculation, so can be updated safely
                Qc_w.coefficient_calc(P)

                #loop over states to get occupancy of each
                for s in range(self.N_states):

                    #r is a running total over contributions of all components
                    r = 0
                    #print Qc_w.w[:,s],Qc_w.eigenval
                    for ju, k in zip(Qc_w.w[:,s], Qc_w.eigenval):
                        try:
                            r = r + ju * exp(k * dt)

                        except:
                            print (len(self.t), r, ju, k, Qc_w.w[:,s])
                            print (Qc_w.eigenval)
                            print (Qc_w.Q)
                            break
                    P[s] = r                    #update P stepwise  

            else:

                #First iteration, just take P_infinity at initial concentration
                P = P_inf

            #must copy P, otherwise every value in dictionary = P (entire output has last value!)
            
            fP = P.copy()
            fP.shape = (1, self.N_states)   #column into row reshaping
            self.occupancy_t [idx] = fP         #store occupancy

    def construct_trace(self, vector):
        self.trace = numpy.dot (self.occupancy_t, vector)
        
    def make_printable(self):
        
        self.printout = "train\n"
        self.printout += "open states\n" + str(self.open_states) + "\n"
        
        self.printout += "P_init\n" + str(self.P_init_lo) + "\n"
        self.printout += "P_final\n" + str(self.P) + "\n"
        
        self.printout += "\n\nsummed\n"
        for t, a, i in numpy.nditer([self.t, self.stim, self.trace]):
            self.printout += str(t) + "\t" + str(a) + "\t" + str(i) + "\n"
    
class JFExpt():
    #moved from relaxes_w.py
    """
    Jump Family expt with multiple values of one rate in a mechanism
    wrapper for TrainExpt, using a single pulse and padding it at the back
    """
    def __init__(self, mech, params):
        #pass through of mechanism and parameters
        self.mech = mech
        self.params = params 
    
    def run(self, jumps_list = [1, 50, 125, 500, 5000]):
        """jumps_list is the length of each jump in ms"""
        
        print ("Jumps family with {0} ms jumps.".format(jumps_list))
        for j in jumps_list:
           
            #define post-pulse relaxation time
            if j < 1000:
                pfreq = 1       #if jump is shorter than a second, make it 1s
            else: 
                pfreq = float(1e3) / (10*j) # make it 10x longer than jump if > 1s
                #print ("pfreq: " +str(pfreq))
            t= TrainExpt(self.mech, self.params)
            t.run(1, j, pfreq, mod='_'+str(j))
            
            #this below is not needed??
            """
            for r in self.rs.rates_set:
                _ra = r[1]
                t = Train(1, j, pfreq, self.param, self.N_states, self.open_states, _ra)
                t.build()       #optional argument can cancel prepadding with 100 ms
                t.construct_train()

                self.trace_set.append(t.trace)

                #get rate constant
                #keys of ra are the rate tuple
                #refer with rate name
                _rate_changed = _ra[r_tuple_from_r_name(_ra, self.param.rate_to_change)][1][0] 

                self.table += str(r[0]) + '\t' + str(_rate_changed) + '\n'
                
                print ('\n-\nTrial#\t' + str(r[0]) + '\t' + str(self.param.rate_to_change) + '\t' + str(_rate_changed) + '\n')
                print (t.printout)

            self.curve_save(self.trace_set, )
        
        self.text_out()
    """
class TrainExpt(ExperimentSetup):
    #moved from relaxes_w.py
    """Construct trains on a set of mechanisms with altered rates"""

    def run(self, n=50, pwidth=1, pfreq=200, mod=False):
        """train params 
        n : consecutive pulses in train
        pwidth : pulse width in ms
        pfreq  : pulse frequency in Hz
        """
        #print ("Did trainexpt get sim_name? "+ self.param.sim_name)
        print ("Train Experiment with {0} ms pulse width, {1} Hz pulse frequency and {2} pulses in train.".format(pwidth, pfreq, n))
        if not mod: mod = ""
        self.header = ""
        
        #rates_set is a set of experiment number : rate set pairs
        for r in self.rs.rates_set:
           #usually open_states_matrix is None
           #if we are doing a conductance variation, retrieve the open states for ith iteration
            if self.param.open_state_matrix != None:
            
                #can fail spectacularly -should wrap this
                #self.param.open_states_matrix should be a ConductMat object
                self.open_states = self.param.open_state_matrix.get_open_states(r[0])
                
            _ra = r[1]
            t = Train(n, pwidth, pfreq, self.param, self.N_states, self.open_states, _ra)
            t.build()       #optional argument can cancel prepadding with 100 ms
            t.construct_train()

            self.trace_set.append(t.trace)

            #get rate constant
            #keys of ra are the rate tuple
            #refer with rate name
            self.table += str(r[0]) + '\t'
            print ('\n------\nTrial#\t' + str(r[0]))
            
            #add rates to line of table in order
            for _rtc in self.param.rate_to_change:
                #print (str(_rtc))
                _rate_changed = _ra[r_tuple_from_r_name(_ra, _rtc)][1][0]
                rtc_print = "{0}\t".format(_rate_changed)
                self.table +=  rtc_print            
                print (str(_rtc) + rtc_print)
            
            print (self.open_states)
            self.table += "{0}\n".format(self.open_states)
            
            #hack, put the last rate from rate_to_change this string each time
            self.header += str(self.param.sim_name) + "_" + mod + "_{0:.2f}".format(_rate_changed) + "\t"
            #self.overall_printout += t.printout
            
            print (t.printout)
            
        #add the time points and stimulus from the final train calc (all identical)
        self.trace_set.append(t.t)
        self.trace_set.append(t.stim)
        self.header += "t_"+str(self.param.sim_name)+"_"+mod+"\tstim_"+str(self.param.sim_name)+"_"+mod
    
        self.curve_save(self.trace_set, mod)
        self.text_out()
   

