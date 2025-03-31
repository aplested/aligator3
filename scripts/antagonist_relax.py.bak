__author__="Andrew"
__date__ ="$Dec 15, 2011 10:59:51 PM$"


#NOTES
### calculate Pinf (antag_conc = x)
### jump to x antag, y agonist
### Get peak following jump
### calculate P inf (antag + agonist)
### equilibrate against a range of concs of B


import numpy
import Q_input as QIP
import qmat
import simple_relax as CRS

# list of calculations

class sim:

    def __init__(self):
        pass
    def eqbm (self):
        pass
    def peak (self):
        pass


def generate_Q (N_states, drugs, rates):#, MR_rate, MR_av):
    """
    NOT VALID: MR_rate can be single or list of rates
    """
    #print "MR_rate", MR_rate,"MR_Avoid", MR_av
    MR_parameters = {'MR_option':'Ignore'}#, 'MR_use': [MR_rate], 'MR_avoid': [MR_av]}
    # initialize Q matrix
    Q = qmat.Q_mat(N_states)

    Q.build_Q(rates)
    #Substitute dict for parameter dictionary
    Q.arrange_MR_on_Q(rates, MR_parameters)
    Q.apply_MR_on_Q(rates)
    Q.add_agonist_dependence_to_Q(rates, drugs)

    Q.p_infinity()
    P_init = Q.pinf[0]

    return Q, P_init

def model_rates (Tarp='Stg', antagonist='CNQX', TARP_boost=4):
    #from Maclean and Bowie but including mixed gating
    """
    Tweaks mechanism on basis of TARP / antagonist combination
    Returns:    rates -- rate dictionary
                conduct -- open state conductance dictionary
    """
    conduct =   {2 : 1}
    antag_E =   0
    mixed_E =   0
    ka_on   =   3.6e7
    ka_off  =   15000
    kb_on   =   0
    kb_off  =   0

    if antagonist == 'CNQX':
        kb_on = 3.6e7
        kb_off = 2.3

    elif antagonist == 'NBQX':
        kb_on = 3.6e7
        kb_off = 0.2

    #it would be a good idea to allow conductances for follow variable ratio
    if antagonist == 'CNQX' and Tarp =='Stg':
        antag_E = 1
        mixed_E = 1
        conduct [0] = 0.02
        conduct [1] = 0.15      #mixed antagonist/agonist

    if antagonist == 'NBQX' and Tarp =='Stg':
        ## do we expect some mixed action with NBQX and stg?
        mixed_E = 1
        conduct [1] = 0.03
        
    #+TARP
    if Tarp == 'Stg':
        boost = TARP_boost
        
    elif Tarp == 'None':
        boost = 1

    #model 1
    rates = {
    (8, 0) :  ['betab2', [300 * antag_E, 0]],
    (6, 1) :  ['betaba', [3000 * mixed_E, 0]],
    (3, 2) :  ['beta2a' , [20000 * boost, 0]],
    (0, 8) :  ['alphab2', [5000, 0]],
    (1, 6) :  ['alphaba', [2000, 0]],
    (2, 3) :  ['alpha2a', [1600 / boost, 0]],
    (3, 4) :  ['ad_pl', [8000, 0]],
    (4, 3) :  ['ad_min', [10 * boost, 0]],
    (8, 9) :  ['bd_pl', [100, 0]],
    (9, 8) :  ['bd_min', [100, 0]],
    (7, 8) :  ['k+b', [kb_on, 2]] ,
    (8, 7)  : ['k-b', [2*kb_off, 0]],
    (10, 7) : ['k+b', [2*kb_on, 2]] ,
    (7, 10) : ['k-b', [kb_off,0]],
    (5, 6)  : ['k+b', [kb_on, 2]],
    (6, 5) :  ['k-b', [kb_off,0]],
    (3, 5) :  ['k_min', [2*ka_off, 0]],
    (5, 3) :  ['k_pl' , [ka_on, 1]],
    (5, 10) : ['k_min', [ka_off, 0]],
    (10, 5) : ['k_pl', [2*ka_on, 1]],
    (6, 7) :  ['k_min', [ka_off, 0]],
    (7, 6) :  ['k_pl', [ka_on, 1]]
    }

    return rates, conduct

def sim(Tarp, Antagonist):
    """simulate responses for a given Tarp and antagonist combination"""
    
    print_out = []
    #    pr_out = []

    print_out.append("\nGlu Concentration Response with TARP:", Tarp)

    rates, conductance_dict = model_rates(Tarp, Antagonist)
    
    N_states = QIP.number_of_states(rates)

    #Clear the concentrations
    drug_dict = {1: 0, 2: 0}

    Qzero_conc, P_init_zero = generate_Q(N_states, drug_dict, rates)

    CR_data, CR_summary, CR_results = CRS.CR_curve(N_states, P_init_zero, rates, \
    'None', 'None', drugs=drug_dict, agonist_to_use=1, conductances=conductance_dict)

    for item in sorted(CR_data):
        peak = CR_data[item][0]
        eqbm = CR_data[item][1]
        print_out.append ("{0:7.4g}\t{1:7.4g}\t{2:7.4g}".format(item, peak, eqbm))



    open_relax = {}
    inhibition_curve = {}

    #range of antagonist concentrations
    for cb in numpy.logspace (1,9) * 1e-12:

        #first calculate equilibrium
        drug_dict[2] = cb
        drug_dict[1] = 250e-6       #equilibrium with 250 muM A

        Q_AB, Pinf_AB = generate_Q (N_states, drug_dict, rates)
        # by state - would be more convenient and faster to do matrix algebra for real here
        equilibrium = 0             #reinitialize equilibrium level
        for open_state in conductance_dict.keys():
            equilibrium += Pinf_AB [open_state] * conductance_dict [open_state]

        #now relaxation to [A] without B, after preincubation in [B]
        #preincubation in cb
        drug_dict[1] = 0
        Q_B, Pinf_B = generate_Q (N_states, drug_dict, rates)

        drug_dict[1] = 1e-2
        drug_dict[2] = 0
        Q_A, Pinf_A = generate_Q (N_states, drug_dict, rates)

        Q_A.relax(Pinf_B)
        jump_A, pr_out_A = CRS.relax_open_group(Q_A.w, Q_A.eigenval, conductance_dict)
        peak = max(jump_A.values())                  #find peak in relax dictionary

        #store p&e and relaxation
        inhibition_curve[cb] = (peak, equilibrium)
        open_relax[cb] = jump_A
        
        print_out.append('\nopen states & current relaxation at 10 mM Glu following equilibration with antagonist {0}\n-------\n'.\
                    format(cb) )
                    
        print_out.append(pr_out_A)

    #should split out printing and formatting to another function


    print ("Open state peak response following incubation with TARP:{0} and B:{1}".format(Tarp, Antagonist))

    header ='cb (Molar)'
    
    for key in sorted(open_relax):
        header += "\t{0:7.4g}".format(key)
        s = key
    header += '\n'
    
    print header
    
    #get time series from last relaxation
    for t in sorted(open_relax[s]):
        l = "{0:7.4g}".format(t)
        for key in sorted(open_relax):
            l += "\t{0:7.4g}".format(open_relax[key][t])
        
        print_out.append(l)
    
    return inhibition_curve, print_out
       
def main():
    
    #Make curves to match Maclean and Bowie 11.04.2012
    #
    #DATA
    #Figure 2 : GluA1 alone and GluA1 + Stg following equilibration with CNQX or NBQX
    #
    #Figure 3 : Activation of GluA1 + Stg by CNQX alone (but not NBQX). 
    #           with and without CTZ. Activation should be less potent than inhibition (low E?)
    #
    #THEIR SIMS
    #Figure 4 : B - equilibrium Glu CR curve +/- Stg (should steepen from 30 muM nh = 1.3 ?? to 4.4 muM nh = 2 ??)
    #               are more binding sites required to get nh up?
    #           C - Simulated eqbm CNQX inhibition curves with 250 muM Glu 
    #               +/- Stg
    #           D - Simulated Peak CNQX inhibition Right shift not found by M&B sim
    #
    #           remaining questions: Why does NBQX potency shift? Because gating of mixed complexes gets stronger?
    #
    #           would be useful to know conductance of mixed gating complexes -
    #           triple barrel noise? Can look slightly after peak
    
    
    curves = {}
    pr_out = []

    for tarp in ['Stg', 'None']:
        for antagonist in ['NBQX', 'CNQX']:
            # get peak and equilibrium inhibition curves as dict of tuples
            # would be good idea to record peak in specified part of record, or in entire record

            inhib_curves, print_out = sim(tarp, antagonist)
            curves[tarp + ':' + antagonist] = inhib_curves
            pr_out.append(print_out)

    print 'Peak vs Equib-Inhibition responses'
    header = '[Antag]'+'\t'
    for condition in sorted(curves):
            header += str(condition)+'\tPk; Eqbm\t'
            
    print header
    
    #use last version of returned peak dict to get concs.
    if inhib_curves != None:
    
        for conc in sorted(inhib_curves):
            l = str(conc) + '\t'
            for condition in sorted(curves):
                l += str(curves[condition][conc][0]) + '\t' + str(curves[condition][conc][1]) + '\t'

            print l
        
if __name__ == "__main__":
    main()
