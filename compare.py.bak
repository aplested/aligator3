#classes to perform comparisons between two different mechanisms, taken from original relaxes_w.py
class TwoMechSetup:
        """ base class for comparison experiments on a two mechanisms
        
        subclass of ExperimentSetup with new __init__ method"""
        
        def __init__(self, mech1=None, param1=None, mech2=None, param2=None):
                    #get mechanism
            
            ##setup dummy containers and then replace
            ## these calls to ExperimentSetup choose the defaults if
            self.m1 = ExperimentSetup(mech1, param1)
            self.m2 = ExperimentSetup(mech2, param2)
            
            if mech1 == None:
                self.m1.name = "3"
                self.m1.rates, self.m1.N_states, self.m1.open_states = mechanism(self.m1.name)
                print ("No mech1 given, using default #3 [TwoMechSetup]")
 
            #set parameters
            if param1 == None:
                self.m1.param = Parameters()        #set default parameters        
                self.m1.param.MR_rate_clean(self.m1.rates)
                print ("No parameters given, using default [TwoMechSetup]")

            if mech2 == None:
                self.m2.name = "4"
                self.m2.rates, self.m2.N_states, self.m2.open_states = mechanism(self.m2.name)  
                print ("No mech2 given, using default #4 [TwoMechSetup]")

            if param2 == None:
                self.m2.param = Parameters()        #set default parameters        
                self.m2.param.MR_rate_clean(self.m2.rates)
                print ("No parameters given, using default [TwoMechSetup]")

            #output specification - NOT FINALISED
            self.table = "Trial #"+ '\t'+ self.m1.name + '\t'+ self.m2.name + '\n'
            self.trace_set = [] #??
            
class Pack_m:
    def __init__(self, mechname="3"):
        
        self.rates, self.N_states, self.open_states = mechanism(mechname)

class PairExpt:
    """Run function for pairwise comparisons"""
    
    def __init__(self, pairmech1 = "3", pairmech2 = "4", 
                        common_rate = "d2op_min", Verbose=False):
        
        self.Verbose = Verbose
        #data = 
        self.m1 = Pack_m(pairmech1)
        self.m2 = Pack_m(pairmech2)
        #call mechanism and pack into single object
        self.p1 = Parameters()
        self.p2 = Parameters()
    
        #adjust default parameters to be useful; could also alter
        ##  'N_trials'       = 10   
        ##  'hi_exp'         = 1.5
        ##  'lo_exp'         = -1.5
        ##  'MR_rate'        = [(1,7), (0,5), (7,8), (5,6)]
        ##  'MR_avoid'       = [(0,2)]
        ##  'zero_conc'      = 0 
        ##  'high_conc'      = 1e-2
        ## 'MR_avoid_preserve' = True
    
        self.p1.rate_to_change = common_rate
        self.p2.rate_to_change = common_rate
        
        self.p1.MR_rate_clean(self.m1.rates)
        self.p2.MR_rate_clean(self.m2.rates)
        #tidying up - a rate to be avoided for MR should not be in the "use" list
        #at the moment, the Auto MR will find another way
        #adjust MR_rate list in order to hard code?
        #This following is method "MR_rate_clean" in Parameters class
        """
        print ("p1.MR_avoid:" + str(p1.MR_avoid))
        
        m1_avoid = r_tuple_from_r_name(m1.rates, common_rate, Verbose=True)
        print ("p2.MR_avoid:" + str(p2.MR_avoid))
    
        m2_avoid = r_tuple_from_r_name(m2.rates, common_rate, Verbose=True)
    
        p1.MR_avoid = [m1_avoid]
        p2.MR_avoid = [m1_avoid]

        if m1_avoid in p1.MR_rate:
            p1.MR_rate.remove(m1_avoid)
    
        if m2_avoid in p2.MR_rate:
            p2.MR_rate.remove(m2_avoid)
    
        print ("p1.MR_avoid:" + str(p1.MR_avoid))
        print ("p2.MR_avoid:" + str(p2.MR_avoid))
        """
    
        self.p1.sim_name = "Comp_m" + pairmech1 + "_m" + pairmech2 +"_"+ common_rate
        self.p2.sim_name = "Comp_m" + pairmech1 + "_m" + pairmech2 +"_"+ common_rate 
    
        self.printout = ""
        
    def run(self):
        
        #parameters determine how rate set is constructed
        self.rs1 = RateGenerator(self.m1.rates, self.p1)   
        self.rs1.make()                              #rates_set attribute now has sets
        self.rs2 = RateGenerator(self.m2.rates, self.p2) 
        self.rs2.make()                              #rates_set attribute now has sets

        #during loop, mshell1 and 2 will be updated with the new rates 
        #but the other attributes stay constant
        #including bundled parameters

        self.mshell1 = copy.deepcopy(self.m1)
        self.mshell2 = copy.deepcopy(self.m2)
        self.mshell1.param = self.p1
        self.mshell2.param = self.p2

        if self.Verbose:
            print ("\nMech "+ pairmech1 + ", rs1.rates_set: \n" + str(self.rs1.rates_set))
            print ("\nMech "+ pairmech2 + ", rs2.rates_set: \n" + str(self.rs2.rates_set))

        for _ms1, _ms2 in zip(self.rs1.rates_set, self.rs2.rates_set):

            self.mshell1.rates = _ms1[1]      #to grab right part
            self.mshell2.rates = _ms2[1]

            _PMC = PairMechComparison (self.mshell1, self.mshell2)
            _PMC.gather_pk_ss()
            _PMC.gather_krec()
            _rtc_tuple = r_tuple_from_r_name(self.mshell1.rates, self.p1.rate_to_change)
            _PMC.make_printable(self.p1.rate_to_change, 
                                    self.mshell1.rates[_rtc_tuple][1][0])
                
            self.printout += _PMC.table_line
        
        #only need the final copies of header and key
        self.printout = "\nExperiment name: " + self.p1.sim_name + "\n" + \
                _PMC.global_head + "\n" + _PMC.key_line + "\n" + self.printout
        
        print (self.printout)

class PairMechComparison: 
    """Compare pk/ss vs recovery for two individual mechanisms 
        Methods:
        __init__        : takes or generates mechanisms and parameters
        gather_pk_ss    : gather and process peak and steady states for two mechs
        gather_k_rec    : gather and process recovery data for two mechs
        make_printable  : string to describe data generated
        
        Output: 

    """
    #cycle against rates in mechanism

    # first write comparison of two mechanisms (can be any pair, rates already fixed, Qmat etc defined)
    # Iss/Ipeak and krec
    # then serve up mechanisms pairwise, across orchestrated rate changes, rate changing etc 
    # make condition of same rate names or require mechanism-wise rate pairs
    
    def __init__(self, m1=None, m2=None):
        """m1 and m2 are preformed mechanism objects, containing the attributes
        rates       : the rate dictionary 
        params      : parameter dictionary
        open_states : dictionary of state-wise conductances (can be normalised)
        N_states    : The number of states in the mechanism
        ---Normalization of open_states dictionary must be consistent across objects
        ---Preparing these four objects from two rate dictionaries
        could probably be a method of this class
        
        """
        if m1 == None and m2 == None:
            
            TMS = TwoMechSetup()
            self.m1 = TMS.m1
            self.m2 = TMS.m2
            
        else:
            #takes this path if called from PairExpt
            self.m1 = m1
            self.m2 = m2
        """    
        self.m1.rates = m1.rates
        self.m2.rates = m2.rates
        self.m1.open_states = m1.open_states
        self.m2.open_states = m2.open_states
        self.m1.N_states = m1.N_states
        self.m2.N_states = m2.N_states
        self.m1.param = m1.param
        self.m2.param = m2.param
        """
        
        #Initialize hi and lo Qmats here
        
        self.m1.Qlo, self.m1.P_init_lo = generate_Q(
            self.m1.N_states, {1: self.m1.param.zero_conc}, self.m1.rates, 
            self.m1.param.MR_rate, self.m1.param.MR_avoid)
        
        self.m1.Qhi, self.m1.P_init_hi = generate_Q(
            self.m1.N_states, {1: self.m1.param.high_conc}, self.m1.rates, 
            self.m1.param.MR_rate, self.m1.param.MR_avoid)
        
        self.m2.Qlo, self.m2.P_init_lo = generate_Q(
            self.m2.N_states, {1: self.m2.param.zero_conc}, self.m2.rates, 
            self.m2.param.MR_rate, self.m2.param.MR_avoid)
        
        self.m2.Qhi, self.m2.P_init_hi = generate_Q(
            self.m2.N_states, {1: self.m2.param.high_conc}, self.m2.rates, 
            self.m2.param.MR_rate, self.m2.param.MR_avoid)
        

    def gather_pk_ss(self):
        """Make a relaxation for each mechanism and take Iss / Ipeak ratio, 
        and calculate fold-change"""
        # only works if peak is bigger than ss (otherwise will go to 1)
        
        _t_step = numpy.arange (1, 9, .2)
        _log_t_step = 1e-7 * 10 ** (_t_step) 
        
        # take max 10mM relax mech 1
        r1 = Relaxation(self.m1.Qhi, self.m1.P_init_lo)
        r1.assemble(_log_t_step, self.m1.open_states)
            
        #take max of hi-conc jump
        self.peak1  = numpy.max(r1.relax_sum)
        # calc Iss mech 1
        self.eqbm1 = r1.relax_sum[-1]       #steady state at 100 sec.
        
        # take max 10mM relax mech 2
        r2 = Relaxation(self.m2.Qhi, self.m2.P_init_lo)
        r2.assemble(_log_t_step, self.m2.open_states)
            
        #take max of hi-conc jump
        self.peak2  = numpy.max(r2.relax_sum)
        # calc Iss mech 2
        self.eqbm2 = r2.relax_sum[-1]
        
        self.fold_change = (self.eqbm1 * self.peak2) / (self.eqbm2 * self.peak1)
        
    def gather_krec(self):
        """get krec for the two mechanisms"""
        
        #getting Qlo and Qhi the wrong way round here gives perfect flat s.s. recovery
        rec1 = Recovery_Qmade(self.m1.param, self.m1.N_states, 
            self.m1.open_states, self.m1.Qlo, self.m1.Qhi, self.m1.P_init_hi, t_range=1e4)

        rec1.build_curve()
        rec1.get_keff()
        
        rec2 = Recovery_Qmade(self.m2.param, self.m2.N_states, 
            self.m2.open_states, self.m2.Qlo, self.m2.Qhi, self.m2.P_init_hi, t_range=1e4)

        rec2.build_curve()
        rec2.get_keff()
        
        self.k_eff1 = rec1.k_eff
        self.k_eff2 = rec2.k_eff
        
        self.mean_keff = (rec1.k_eff + rec2.k_eff ) / 2

    def make_printable(self, _d_rate=None, _d_value=None):
       ###not final - adjusted now to be useful?
        self.d_rate = _d_value
        self.global_head = "Pairwise comparison of two mechanisms\n"
        self.global_head += "Mech 1 open states: " + str(self.m1.open_states) + "\n"
        self.global_head += "M1 P_init_hi_concentration: \n" + str(self.m1.P_init_hi) + "\n"
        self.global_head += "Mech 2 open states: " + str(self.m2.open_states) + "\n"
        self.global_head += "M2 P_init_hi_concentration: \n" + str(self.m2.P_init_hi) + "\n"
        
        _data = [ "eqbm1", "peak1", "eqbm2", "peak2", "fold_change", "k_eff1", "k_eff2"]
        # add changing rate information to table
        self.key_line = "{:>12}".format(_d_rate) + "\t".join("{:>12}".format(d) for d in _data) + "\n"
        
        _data.insert(0, "d_rate")
        
        self.table_line = "\t".join("{:12.5g}".format(self.__dict__[_key]) \
                        for _key in _data) + "\n"
