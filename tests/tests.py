__author__="Andrew"
__date__ ="$Aug 26, 2013 11:25:41 AM$"

import relaxes
from mechanisms import mechanism
import numpy

def recovery_test():   
    """test recovery class"""

    rates, N_states, open_states = mechanism("4")
    param = relaxes.Parameters()   
    
    rec = relaxes.Recovery(param, N_states, open_states, rates, P_init='hi', t_range=3000)
 
    rec.build_curve()
    print rec.second_pulses.shape
    sp_t = rec.second_pulses.transpose()
    
    print rec.second_pulses.shape
    print sp_t.shape
    numpy.savetxt(sim_name+"_traces.txt", sp_t, delimiter='\t') 
    numpy.savetxt(sim_name+"_curve.txt", rec.rec_curve, delimiter='\t') 
 
def cr_test():
    """test cr class"""
    
    rates, N_states, open_states = mechanism("3")
    param = relaxes.Parameters()
    
    min_conc = 1e-6
    max_conc = 1e-1
    
    cr = relaxes.ConcResponse(param, N_states, open_states, rates, min_conc, max_conc, steps=19)
    cr.build_curve()
    numpy.savetxt(param.sim_name+"_curve.txt", cr.curve, delimiter='\t') 
    
    
def train_response():
    """create response to a train of pulses"""
    #test function
    
    rates, N_states, open_states = mechanism("4")
    param = relaxes.Parameters()  
    
    #Train params
    n = 1
    pwidth = 50     #in ms
    pfreq = 2      #in hz

    
    t = relaxes.Train(n, pwidth, pfreq, param, N_states, open_states, rates)
    t.build()
    t.construct_train()
    print t.printout



def relax_test():   
    """test relaxation class"""
    
    rates, N_states, open_states = mechanism("3")
    param = relaxes.Parameters()
    
    #Qzero and P_init_hi are not used
    Qzero,  P_init_zero = relaxes.generate_Q(N_states, {1: param.zero_conc}, rates, param.MR_rate, param.MR_avoid)
    Qhi,    P_init_hi   = relaxes.generate_Q(N_states, {1: param.high_conc}, rates, param.MR_rate, param.MR_avoid)
    
    t_step = numpy.arange (1,9,.2)
    log_t_step = 1e-7 * 10 ** (t_step)           
    #open_state = 0

    r = relaxes.Relaxation(Qhi, P_init_zero)
    r.assemble(log_t_step, open_states)
    
    f=open(param.sim_name + '.xls', 'w')
    for each_line in r.printout.split("\n"):
        print each_line
        f.write(each_line + "\n")

    f.close()



def pdict_test():
        
    experimental_parameters = {

    'rate_to_change': 's_op_plus', 
    'sim_name'      : "trial",
    'N_trials'      : 10   ,
    'MR_rate'       : [(1,7),(0,5),(7,8),(5,6)],
    'MR_avoid'      : [(2,0)],
    'zero_conc'     : 0, 
    'high_conc'     : 1e-2
    
    }

    print experimental_parameters.keys()

    re = relaxes.Parameters(experimental_parameters)
    
    print re.keys()
    print "sim_name:", re.sim_name
    
    
    


def main():
    #pdict_test()
    #recovery_test()
    #train_response()
    relax_test()
    #cr_test()

if __name__ == "__main__":
    main()
