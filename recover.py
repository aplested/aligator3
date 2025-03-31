#recovery classes from original relaxes.py
from relaxes import ExperimentSetup, Relaxation
from common.core_utils import convert_ms, generate_Q, convert, r_tuple_from_r_name 
import numpy

class Recovery:
    #moved from relaxes.py
    """
    Two pulse protocols
    simulate relaxations of response to second pulse following a long conditioning pulse
    collect peaks to build recovery curve
    """
    
    def __init__(self, param, N_states, open_states, rates, P_init='hi', t_range=10000, normalise=False):
        
        self.intervals = convert_ms(t_range)
        self.norm = normalise
        #print self.intervals
        self.np2 = len(self.intervals)
        self.open_states = open_states
        
        #lo_rates = copy.deepcopy(rates)
        #hi_rates = copy.deepcopy(rates)
        print("make Qlo, conc: "+str(param.zero_conc) )
        self.Qlo, self.P_init_lo = generate_Q(N_states, {1: param.zero_conc}, 
                                            rates, param.MR_rate, param.MR_avoid)
        
        print("make Qhi, conc: "+str(param.high_conc) )
        self.Qhi, self.P_init_hi = generate_Q(N_states, {1: param.high_conc}, 
                                            rates, param.MR_rate, param.MR_avoid)
        
        #build data container
        self.rec_curve = numpy.zeros((self.np2, 2))
        
        #can specify initial occupancy, by default take P_inf_hi-conc 
        if P_init == 'hi':
            self.P_init = self.P_init_hi
        else:
            self.P_init = P_init
            
    def build_curve(self):
        
        _brief_jump = 100 #in ms
        _t_steps = convert(_brief_jump)
        # wait to make the second pulse trace container until we know _t_steps
        self.second_pulses = numpy.zeros((0, len(_t_steps)))
        
        for n, interval in enumerate(self.intervals):
            rr = Relaxation(self.Qlo, self.P_init)
            #send list of a single interval
            rr.assemble([interval], self.open_states)
            self.P = rr.P_final 
            
            rj = Relaxation(self.Qhi, rr.P_final)
            rj.assemble(_t_steps, self.open_states)
            
            #take max of hi-conc jump
            response  = numpy.max(rj.relax_sum)
            index_max = numpy.argmax(rj.relax_sum)
            t_exact_max = interval + _t_steps[index_max]
            
            #store profiles of test jumps
            #print self.second_pulses
            
            self.second_pulses = numpy.append(self.second_pulses, 
                                        numpy.atleast_2d(_t_steps + interval),axis=0)
            
            self.second_pulses = numpy.append(self.second_pulses, 
                                        numpy.atleast_2d(rj.relax_sum), axis=0)
            
            #store max against exact interval
            self.rec_curve[n, :] = (t_exact_max, response)
            
            #print (self.rec_curve)
        
        #normalise responses of recovery curve against limiting value
        if self.norm:
            self.rec_curve[:, 1] = self.rec_curve[:, 1] / self.rec_curve [-1, 1]
        
        print (self.rec_curve)
 
    def get_keff(self, take_final=False):
        """ Optionally called after generating the recovery curve with build_curve
        to very crudely obtain the half time

        simple modification from threshold.py
                    
        simple linear interpolation between bracketing points if no direct hit
        """
        
        # find max in rec (or final value, don't force as default)
        if take_final:
            _rec_max = self.rec_curve[-1, 1]
        else:
            _rec_max = numpy.max(self.rec_curve[:, 1])
            
        _rec_min = self.rec_curve[0, 1]  
        #Bit of a cheat - take the first point. Will be wrong in the case of 
        #very fast recovery compared to 1st interval. But in this case, _rec_min and _rec_max 
        #should be similar and caught below
        
        if _rec_min > 0.95 * _rec_max:
            print ("No recovery because too little desensitization (fast limit)")
            print ("Setting k_eff = 1000")
            self.k_eff = 1000        #We could certainly not measure a rate this fast
        
        else:
            _half_rec_amp = _rec_max - 0.5 * (_rec_max - _rec_min)
            _near_idx = (numpy.abs(self.rec_curve[:, 1] - _half_rec_amp)).argmin()
            _near_value = self.rec_curve [_near_idx, 1]

            #interpolate
            #must be a smarter way to combine the two possibilities?
            if _near_value > _half_rec_amp:
                #true half time was before our nearest neighbor
                _left = self.rec_curve[_near_idx - 1, 1]
                _right = self.rec_curve[_near_idx, 1]
                _tl = self.rec_curve[_near_idx - 1, 0]
                _tr = self.rec_curve[_near_idx, 0]
                #inverse of time difference scaled by normalized (point-threshold distance)
                self.k_eff = 1 / (_tr - (_tr - _tl) * float(_right - _half_rec_amp)/(_right - _left))

            elif _near_value < _half_rec_amp:
                #true half time was after our nearest neighbor
                _left = self.rec_curve[_near_idx, 1]
                _right = self.rec_curve[_near_idx + 1, 1]
                _tl = self.rec_curve[_near_idx, 0]
                _tr = self.rec_curve[_near_idx + 1, 0]
                #as above rearranged to approach from below.
                self.k_eff = 1 / (_tl + (_tr - _tl) * float(_half_rec_amp - _left)/(_right - _left))

            elif _near_value == _half_rec_amp:

                self.k_eff = 1 / self.rec_curve[near_hi_idx, 0]


    def make_printable(self):
        
        #self.printout = "states sum:" + "\n" + str(self.states_sum) + "\n"
        
        self.printout = 'P_init' + "\n" + str(self.P_init) + "\n"
        #self.printout += 'P_final' + "\n" + str(self.P_final) + "\n"

        self.printout += "\n\nrec_curve\n"
        for line in self.rec_curve.tolist():
            for elem in line:
                self.printout += str(elem) + "\t"  
            
            self.printout += "\n"

        self.printout += "\n\nsecond pulses\n"
        for line in self.second_pulses.tolist():
            for elem in line:
                self.printout += str(elem) + "\t"  
            
            self.printout += "\n"
 
class Recovery_Qmade(Recovery):
    #moved from relaxes.py
    """subclass to initialise recovery simply when Q mats are already made"""
    def __init__(self, param, N_states, open_states, Q_lo, Q_hi, P_init_hi, t_range=10000, normalise=False):
        
        self.intervals = convert_ms(t_range)
        self.np2 = len(self.intervals)
        self.open_states = open_states
        self.Qlo = Q_lo
        self.Qhi = Q_hi
        self.P_init = P_init_hi
        self.rec_curve = numpy.zeros((self.np2, 2))
        self.norm = normalise


class RecoveryExpt(ExperimentSetup):   
    #moved from relaxes.py
    """Recovery expt with multiple values of one rate in a mechanism"""
    
    def run(self, P_init='hi', t_range=100000, normalise=True):
        """P_init : occupancy to use at the start of the zero-relaxation
            t_range : maximum interval to check recovery
            normalise : Normalise the recovery curves to their final value"""
            
        print ("Recovery Experiment with {0} ms time range.".format(t_range))
        self.curve_set = []

        for r in self.rs.rates_set:
            _ra = r[1]  

            rec = Recovery(self.param, self.N_states, self.open_states, _ra, P_init, t_range, normalise)

            rec.build_curve()
            rec.get_keff()
            rec.make_printable()

            sp_t = rec.second_pulses.transpose()

            self.curve_set.append(rec.rec_curve)
            self.trace_set.append(sp_t)             #p2 responses go to trace_set

            for _rtc in self.param.rate_to_change:
                print (str(_rtc))
                _rate_changed = _ra[r_tuple_from_r_name(_ra, _rtc)][1][0] 

                self.table += str(r[0]) + '\t' + str(_rate_changed) + '\t' + str(rec.k_eff) + '\n' 
                print (rec.printout)
                #self.overall_printout += rec.printout 

        self.curve_save(self.curve_set, mod='_curves')
        self.curve_save(self.trace_set, mod='_traces')
        self.text_out()

