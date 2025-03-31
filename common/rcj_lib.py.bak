### Library of routines for making realistic concentration jumps

__author__="Andrew Plested"
__date__ ="$Dec 20, 2010 12:07:36 PM$"

#module qmat provides Q matrix implementation and calculations
#module Q_input imports Q matrix information and allows user editing
#module IO_utils provides input and output functionality

import math
from common.qmat import Q_mat
from math import exp
import threshold as thr
import numpy

def erf(x):
    '''
    accurate, fast approximation of the error function
    from http://www.johndcook.com/blog/2009/01/19/stand-alone-error-function-erf/
    arguments -- x - a scalar
    returns -- a scalar
    '''

    # constants
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911

    # Save the sign of x
    sign = 1
    if x < 0:
        sign = -1
    x = abs(x)

    # A & S 7.1.26
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(- x * x)

    return sign * y

def erf_pulse(z, pulse_width, pulse_conc, rise_t, pulse_centre, time_step):
    '''
    constructs a "top-hat" pulse with rise and fall from error function.

    arguments --    z   - NUMPY array which will take the pulse, zeros spaced by time_step
                    pulse_width - approximate FWHM in microseconds
                    pulse_conc - ligand concentration during jump in Molar
                    rise_t - desired 10 - 90% rise time (can use 0. for square pulse)
                    centre - position of pulse in simulation trace
                    time_step - sampling interval in microseconds - removed in some calcs upon NUMPY update

    returns -- array of concentration values, spaced by dt
    '''

    ### work in sample point space, following numpy conversion
    nrt = float (rise_t) / time_step
    npc = int (float (pulse_centre) / time_step)
    npw = float(pulse_width) / time_step
               
    erf_rise = 1.8  #10-90% of erf(x)
    step_factor = float(nrt) / erf_rise

    # lock to sampling intervals
    left_fwhm  = int(npc - (float(npw) / 2))
    right_fwhm = int(npc + (float(npw) / 2))

    # fill in with true top hat at pulse_concentration - will overwrite flanks with erf
    for r in range(left_fwhm, right_fwhm):

        z [r] = pulse_conc

    # Return a perfect top hat if rise time is 0. or shorter than sampling interval
    if rise_t < time_step :
        return z

    pts =  int(nrt * 1.25)                #scale with rise time and extend
    for s in range(-pts, pts + 1):                 #symmetrical
        
        x = float(s) / step_factor              # scale x into correct intervals

        y = (erf(x) + 1.) / 2. * pulse_conc          # y-shift erf into range 0 to 1; scale by concentration

        # flatten differences under 10 pM during constant-concentration sections
        if y < 10e-11:
           y = 0.

        if y > pulse_conc - 10e-11:
            y = pulse_conc

        #inflexion points centred on left_fwhm, right_fwhm
        #160723 converted to sample space to avoid anti-aliasing
        pt_rise = left_fwhm + s
        pt_fall = right_fwhm + s
        
        # truncate rise and fall if pulse is too thin to reach max.
        if pt_rise <= npc:
            z[pt_rise] = y

        if pt_fall >= npc:
            z[pt_fall] = pulse_conc - y

    return z

def make_family():
    '''
    testing - make a family of pulses to examine properties
    alternate main()
    no arguments
    returns nothing
    '''

    center = 10000
    width = 2500. #desired 10-90% in microseconds
    family = []
    peak_conc = 30e-3
    step_size = 8
    max_length =0
    for rise_time in range(50,500,50):           

        profile = erf_pulse(width,peak_conc,rise_time,center,step_size)
        family.append(profile)

        if len(profile) > max_length:
            max_length = len (profile)

    rcj_IO.family_write(family,max_length)


def make_jump(pa):
    '''
    argument --
    pa : the parameter dictionary
    returns --
    profile : numpy array of concentration points
    '''
    #unpack parameter dictionary
    pw = pa['pulse_width']
    pc = pa['peak_conc']
    rt = pa['rise_time']
    pr = pa['pulse_rise']
    ss = pa['step_size']
    rl = pa['record_length']
    
    samples = rl / ss
    
    #very ugly- made twice in different places because of different ways to make jumps.
    t_point = numpy.arange(0, rl, ss)
    ju = numpy.zeros(samples, dtype='float')    #zero array

    if pa['shape'] != 'instant exponential':

        pce = pr + pw / 2          # move center of pulse so that rises align (for multiple widths)
        profile = erf_pulse(ju, pw, pc, rt, pce, ss)

    else:
        cb = 0
        # need to pass array of time to pulse_instexp
        profile = pulse_instexp(t_point, (pr, pc, pw, cb))

    return profile
    


def rcj_calc_nump (jux, mech_rates, paras, P=[]):
    '''
    arguments --
    jux         : concentration jump profile array
    mech_rates  : dictionary of rate name - constant pairs
    paras       : dictionary of parameters that defines pulse
    P           : optionally pass current occupancy (for chains of pulses)
    returns - relaxation and jump
    '''
    ###Not using MR_needed to avoid many recalculations
    
    Q_library = {}
    rlx = {}

    #P = []                  #current occupancy as a list NOW SET AS ARGUMENT
    dt = paras['step_size'] * 1.e-6
        #convert from microseconds to seconds

    ss = paras['step_size']
    rl = paras['record_length'] 
    
    t_point = numpy.arange(0, rl, ss)
    
    print'ok', len(t_point), len (jux)
    print jux
    for idx in range (len(jux)):

        #extract concentration.
        c = jux[idx]

        if c in Q_library:
            #retreive Q if previously calculated, Qc_w stands for "working Q(c)" also pick up A_matrices etc
            Qc_w = Q_library[c]

        else:
            #calculate Q matrix, spectral coefficients for given concentration,
            #initialise
            Qc_w = Q_mat(paras['N_states'])
            
            Qc_w.build_Q (mech_rates)
            if len(Q_library) == 0:  #if only concentration varies, MR should not change.
                
                Qc_w.arrange_MR_on_Q(paras)
                Qc_w.apply_MR_on_Q()  
                MR_saved = Qc_w.mst
            else:
                print len(Q_library)
                Qc_w.mst = MR_saved #maybe this is not needed? Belt and braces
                
            Qc_w.add_agonist_dependence_to_Q({1:c})     #c must be passed as a dict
                                                                
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
            for s in range(paras['N_states']):

                #r is a running total over contributions of all components
                r = 0
                #print Qc_w.w[:,s],Qc_w.eigenval
                for ju, k in zip(Qc_w.w[:,s],Qc_w.eigenval):
                    try:
                        r = r + ju * exp(k*dt)
                        
                    except:
                        print len(rlx), r, ju, k, Qc_w.w[:,s] 
                        print Qc_w.eigenval 
                        print Qc_w.Q
                        break
                P[s] = r                    #update P stepwise  

        else:

            #First iteration, just calculate P_infinity at initial concentration
            Qc_w.p_infinity()
            P = Qc_w.pinf[0]

        #must copy P, otherwise every value in dictionary = P (entire output has last value!)
        rlx [t_point[idx]] = P.copy()

    return rlx



    
    
def compose_rcj_out (cjump,relax_dict,o_states,offset=1.2,output_Occup=False,output_PO=True):
    '''
    write output to text file as lines of t,j,p0,p1,p2....pn,pOpen with option to omit
    arguments --
        cjump           : dictionary of agonist profile values against time
        relax_dict      : dictionary of state occupancies against time
        o_states        : list of open states for P-open calculation - should convert to dictionary
        offset          : float by which to offset the jump from the response
        output_option   : By default, do not save the occupancies of individual states
        output_PO       : By default, output only the open probability
    returns --
        lines           : A list of strings

    '''
    lines = []
    
    i = 0
    for time_key in sorted(relax_dict):
        
        if type(cjump) == type(numpy.array(())):
            line = str(time_key)+'\t'+str(cjump[i]+offset) 
            i += 1
        else:
            line = str(time_key)+'\t'+str(cjump[time_key]+offset)       #positive offset = 1.2 for jump
        
        isochrone = relax_dict[time_key]

        if output_Occup:
            #Full occupancy
            for elem in isochrone:
                line += '\t'+str(elem)

        if output_PO:
            #Open Probability - no allowance for multiple conductances
            Popen = 0.
            for o in o_states:
                Popen = Popen + isochrone[o]

            line += '\t'+str(Popen)

        lines.append(line)

    return lines

def pulse_instexp(t, (prepulse, cmax, tdec, cb)):
    """
    From Remis Lape 2011
    t is the time array
    prepulse -- interval before the pulse
    cmax    -- max concentration in molar
    tdec    -- decay time
    cb- background concentration in molar
    """

    if type(t) == type(numpy.array(())):
        print 'array'
        t1 = numpy.extract(t[:] < prepulse, t)
        t2 = numpy.extract(t[:] >= prepulse, t)
        conc2 = cmax * numpy.exp(- (t2 - prepulse) / tdec)
        conct = numpy.append(t1 * 0.0, conc2)
        conct = conct + cb

    else:
        #not clear to me that this works
        if t <= prepulse:
            conct = cb
        else:
            conct = cmax * exp(-float(t - prepulse) / tdec) + cb

    return conct 


def crossing_time_measure (trace, low=0.1, high=0.9, verbose=True):
    '''
    Take a trace and measure the rise and fall times using threshold algorithm

    arguments : trace - numpy array
                low = 0.1  default 10-90% rise time
                high = 0.9
    '''
    a, b, c, d, e, f = thr.rise_threshold (trace,low,high)

    aa, bb, cc, dd, ee, ff = thr.fall_threshold (trace,low,high)

    if verbose:
        print "%i-%i%% rise time = %f time units" %(int(low*100),int(high*100),f-e)
        print "%i-%i%% fall time = %f time units" %(int(low*100),int(high*100),ee-ff)
        print a,trace[b],c,trace[d]
        print aa,trace[bb],cc,trace[dd]

    return f-e, ee-ff


