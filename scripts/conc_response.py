#! /usr/bin/python

__author__="Andrew"
__date__ ="$Jun 16, 2010 10:23:48 AM$"

from qmat import Q_mat

def Conc_occup(N_s,rate_dict):
    """
    calculate equilibrium occup at range of concentrations
    return occupancies as dictionary (conc:occup pairs)
    """
    drugs = {1:0} 
    agonist = 1
    no_MR_rate={'MR_option':'Ignore'}
    print_out = []
    occup = {}
    for conc_step in range (19):

        # calculate relaxation at a range of concs
        # range from 1 uM to 100 mM
        conc = 1e-7* 10 ** ( float(conc_step)/3. )
        drugs[agonist] = conc

        Q = Q_mat(N_s)

        

        Q.build_Q(rate_dict)
        #Substitute dict for parameter dictionary
        Q.arrange_MR_on_Q(rate_dict, no_MR_rate)
        Q.apply_MR_on_Q(rate_dict)
    
        Q.add_agonist_dependence_to_Q(rate_dict, drugs)
        
        Q.p_infinity()
        occup [conc] =  Q.pinf[0]

        
        points = str(conc)+'\t'
        for P_elem in occup[conc]:
            points += str(P_elem)+'\t'
        points += '\n'
        print_out.append(points)



    return occup, print_out

def occup_with_rate(N_s,rate_dict,rate_to_vary):

    no_MR_rate={'MR_option':'Ignore'}
    print_out = []
    occup = {}
    x = rate_dict[rate_to_vary]
    rates = [x[1][0] * 10**(float(i)/4-3) for i in range(19)]

    print rates
    for rate in rates:

        Q = Q_mat(N_s)
        rate_dict[rate_to_vary][1][0] = rate
        Q.build_Q(rate_dict)
        #Substitute dict for parameter dictionary
        #Q.update_rate(rate_to_vary, rate)
        Q.arrange_MR_on_Q(rate_dict, no_MR_rate)
        #print Q.show()
        #make diagonal correct
        Q.do_diag()
        print Q.show()
        #Q.add_agonist_dependence_to_Q(rate_dict, drugs)

        Q.p_infinity()
        occup [rate] =  Q.pinf[0]

        points = str(rate)+'\t'
        for P_elem in occup[rate]:
            points += str(P_elem)+'\t'
        points += '\n'
        print_out.append(points)

    return occup, print_out

def main():

    #simple linear models for CysPro 25.3.11
    #  R - AR - AF - AFF - AFF*
    rates = {
    'alpha' :  [0, 1, 2500, 0] ,
    'beta'  :  [1, 0, 10000, 0] ,
    'ff+'   :  [2, 1, 3000, 0] ,
    'ff-'   :  [1, 2, 1000, 0] ,
    'f+'    :  [3, 2, 1000, 0] ,
    'f-'    :  [2, 3, 2000, 0] ,
    'k_min' :  [3, 4, 5000, 0] ,
    'k_pl'  :  [4, 3, 1e7, 1 ] 
    }
    #  R - AR - AF -  AF*
    rates2 = {
    'alpha' :  [0, 1, 2500, 0] ,
    'beta'  :  [1, 0, 10000, 0] ,
    'f+'    :  [2, 1, 1000, 0] ,
    'f-'    :  [1, 2, 2000, 0] ,
    'k_min' :  [2, 3, 5000, 0] ,
    'k_pl'  :  [3, 2, 1e7, 1 ]
    }


    #  R - AR - A2R- A2F -  A2F*
    rates_1 = {
    'alpha' :  [0, 1, 2500, 0] ,
    'beta'  :  [1, 0, 10000, 0] ,
    'f+'    :  [2, 1, 3000, 0] ,
    'f-'    :  [1, 2, 1000, 0] ,
    'k_min' :  [3, 4, 5000, 0] ,
    '2k_pl' :  [4, 3, 2e7, 1 ] ,
    'k_pl'  :  [3, 2, 1e7, 1 ] ,
    '2k_min':  [2, 3, 10000,0 ]
    }

    #from daniels submission JNS 10.12 
    #
    #              0AF*
    #    Glu>       |
    #  4R - 3AR  - 1AF 
    #               |
    #              2AD
    #
    #
     
    rates_9c_small = {
    (0, 1)  :  ['alpha',[2000, 0]]   ,
    (1, 0)  :  ['beta', [6000, 0]]   ,
    (1, 2)  :  ['d+',   [4000, 0]]   ,
    (2, 1)  :  ['d-',   [0.1, 0 ]]   ,
    (3, 4)  :  ['k_min',[300, 0 ]]   ,
    (4, 3)  :  ['k_pl', [1e7, 1 ]]   ,
    (3, 1)  :  ['f+',   [2.5e3, 0 ]] ,
    (1, 3)  :  ['f-',   [3e6,0  ]]
    }
    
    #carbone stg 2013

    #        0O - 1O+stg
    #         |     |
    #        2D - 3D+stg
    #

    rates_carb = {
    (0, 1)  :  ['kst_o+',[1200, 0]]   ,
    (1, 0)  :  ['kst_o-', [500, 0]]   ,
    #(1, 3)  :  ['d_stg+',   [4000, 0]]   ,
    #(3, 1)  :  ['d_stg-',   [0.1, 0 ]]   ,
    #(3, 2)  :  ['kst_d-',  [300, 0 ]]   ,
    #(2, 3)  :  ['kst_d+', [1e7, 0 ]]   ,
    (2, 0)  :  ['d_op-',   [100, 0 ]] ,
    (0, 2)  :  ['d_op+',   [1000,0  ]]
    }
    
    N_states = 3
    rates = rates_carb
    occupancy_by_rate , results = occup_with_rate(N_states, rates,(2,0))
   

    f=open('output.xls', 'w')
    for each_line in results:
            print each_line
            f.write(each_line)

    f.close()

if __name__ == "__main__":

    main()
