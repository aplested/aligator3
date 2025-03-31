#This module handles the mechanism

#module is becoming huge. Need to package up mechanisms better
#in a subdirectory?

def mechanism(mech="4"):
    # rate dictionaries for the given mechanisms
    #

    if mech == "None":
        return None, None, None

    built_ins = ["1s", "4", "4_dg", "cp2", "4KA"]
    
    
    if mech not in built_ins:
        print "mechanism requested: ", mech
        try:
            i_mech = __import__(mech)
            if 'mech_definition' in dir(i_mech):
                rd, N_states, open_states = i_mech.mech_definition()
                print ("Valid mechanism method found")
                print rd
            else:
                print (mech+" is not a valid mechanism module - needs a method: mech_definition")
                print ("Reverting to built-in default (mech. #4)")
                mech = "4"
        except:
            print ("couldn't find or import mechanism, using default (mech. #4)")
            mech = "4"

    #By default, mechanisms don't include fluorescence
    F_states = None

     

    if mech == "1s":

        # GluR2ish Rates from Zhang et al 2006 BJ
        # Tweaked to give : ~20% ss with fast rec, ec50 700 muM, higher p_o
        #   d2 connected to open state.
        rd = {
        (0, 3) :  ['dop_pl', [150, 0]] ,
        (1, 0) :  ['beta'  , [10000, 0]] ,
        (0, 1) :  ['alpha' , [3000, 0]] ,
        (1, 2) :  ['d1_pl' , [600, 0]] ,
        (2, 1) :  ['d1_min', [100, 0]] ,
        (2, 3) :  ['d2_pl' , [150, 0]] ,
        (3, 2) :  ['d2_min', [2, 0] ]   ,
        (2, 4) :  ['kd_min', [1500, 0]]  ,
        (4, 2) :  ['kd_pl' , [1e7, 1]]  ,
        (5, 1) :  ['k_pl'  , [3e7, 1]]  ,
        (1, 5) :  ['k_min' , [20000, 0]],
        (5, 4) :  ['d0_pl' , [1, 0]],
        (4, 5) :  ['d0_min', [9, 0]],
        (3, 0) :  ['dop_min',[10, 0 ]]

        }
        N_states = 6
        open_states = {0 : 1}


        
    if mech == "4":
        # used in Poulsen et al
      
        ### TOPOLOGY
        #                               0 = AR*
        # 1 - 5 - 0    Rest - open      2 = AD2
        # |   |   |                     3 = AD
        # 4 - 3 - 2    des              4 = D
        #                               5 = AR
        #                               1 = R
        #
        #rates don't obey MR - will be adjusted
        #131112 synced with "3"
        rd = {

        (5, 0) : ['beta',      [ 8000, 0]] ,
        (0, 5) : ['alpha',     [ 3000, 0]] ,
        (3, 2) : ['d2_plus',   [  120, 0]] ,
        (2, 3) : ['d2_min',    [    5, 0]] ,

        (1, 4) : ['d0_plus',   [    1, 0]] ,
        (4, 1) : ['d0_min',    [    3, 0]] ,
        (5, 3) : ['d1_plus',   [  300, 0]] ,
        (3, 5) : ['d1_min',    [   25, 0]] ,
        (0, 2) : ['d2op_plus', [  120, 0]] ,
        (2, 0) : ['d2op_min',  [    2, 0]] ,

        (4, 3) : ['kd_plus',   [  5e6, 1]] ,
        (3, 4) : ['kd_min',    [  500, 0]] ,
        (1, 5) : ['k_plus',    [  5e6, 1]] ,
        (5, 1) : ['k_min',     [40000, 0]] ,

        }

        N_states = 6 # state this rather than obtain automatically.

        #states and their conductances
        open_states = {0 : 1}
    
    if mech == "4_dg":
        # mechanism 3 without Stg on open state
        # with desensitized state (d) conducting (g_amma) - UAA F579AzF
        ### TOPOLOGY
        #                               0 = AR*
        # 1 - 5 - 0    Rest - open      2 = AD2
        # |   |   |                     3 = AD
        # 4 - 3 - 2    des              4 = D
        #                               5 = AR
        #                               1 = R
        #
        #rates don't obey MR - will be adjusted
        #131112 synced with "3"
        rd = {

        (5, 0) : ['beta',      [ 8000, 0]] ,
        (0, 5) : ['alpha',     [ 3000, 0]] ,
        (3, 2) : ['d2_plus',   [  120, 0]] ,
        (2, 3) : ['d2_min',    [    5, 0]] ,

        (1, 4) : ['d0_plus',   [    1, 0]] ,
        (4, 1) : ['d0_min',    [    3, 0]] ,
        (5, 3) : ['d1_plus',   [  300, 0]] ,
        (3, 5) : ['d1_min',    [   25, 0]] ,
        (0, 2) : ['d2op_plus', [  120, 0]] ,
        (2, 0) : ['d2op_min',  [    2, 0]] ,

        (4, 3) : ['kd_plus',   [  5e6, 1]] ,
        (3, 4) : ['kd_min',    [  500, 0]] ,
        (1, 5) : ['k_plus',    [  5e6, 1]] ,
        (5, 1) : ['k_min',     [40000, 0]] ,

        }

        N_states = 6 # state this rather than obtain automatically.

        #states and their conductances
        open_states = {0 : 1, 2 : 0.3}
    
        
    if mech == "4KA":
        # mechanism 3KA without Stg on open state
        # 
        # 
        ### TOPOLOGY
        #                               0 = AR*
        # 1 - 5 - 0    Rest - open      2 = AD2
        # |   |   |                     3 = AD
        # 4 - 3 - 2    des              4 = D
        #                               5 = AR
        #                               1 = R
        #
        #140910 set up like 3KA
        #4x less des
        #140918 adjusted open state conductance to match state 0 in mech 3KA
        
        rd = {

        (5, 0) : ['beta',      [ 1600, 0]] ,
        (0, 5) : ['alpha',     [30000, 0]] ,
        (3, 2) : ['d2_plus',   [   12, 0]] ,
        (2, 3) : ['d2_min',    [   30, 0]] ,

        (1, 4) : ['d0_plus',   [    1, 0]] ,
        (4, 1) : ['d0_min',    [    3, 0]] ,
        (5, 3) : ['d1_plus',   [  300, 0]] ,
        (3, 5) : ['d1_min',    [  300, 0]] ,
        (0, 2) : ['d2op_plus', [  120, 0]] ,
        (2, 0) : ['d2op_min',  [   12, 0]] ,

        (4, 3) : ['kd_plus',   [  5e6, 1]] ,
        (3, 4) : ['kd_min',    [ 2500, 0]] ,
        (1, 5) : ['k_plus',    [  5e6, 1]] ,
        (5, 1) : ['k_min',     [40000, 0]] ,

        }

        N_states = 6 # state this rather than obtain automatically.

        #states and their conductances
        open_states = {0 : .08}
        
    

    if mech == "cp2":
        # reference mechanism (like 4)
        # values as published C & P 2012 Fig 7
        #
        ### TOPOLOGY
        #                               0 = AR*
        # 1 - 5 - 0    Rest - open      2 = AD2
        # |   |   |                     3 = AD
        # 4 - 3 - 2    des              4 = D
        #                               5 = AR
        #                               1 = R
        #MR not exact because d2- and alpha arbitrary
        #reduce d2- and alpha in ratio to represent AMPA->KA
        #d0_plus is 1 or 4???
        rd = {

        (5, 0) : ['beta',      [ 4000, 0]] ,
        (0, 5) : ['alpha',     [ 1000, 0]] ,
        (3, 2) : ['d2_plus',   [  150, 0]] ,
        (2, 3) : ['d2_min',    [   20, 0]] ,

        (1, 4) : ['d0_plus',   [    1, 0]] ,
        (4, 1) : ['d0_min',    [    9, 0]] ,
        (5, 3) : ['d1_plus',   [  600, 0]] ,
        (3, 5) : ['d1_min',    [  100, 0]] ,
        (0, 2) : ['d2op_plus', [  150, 0]] ,
        (2, 0) : ['d2op_min',  [   10, 0]] ,

        (4, 3) : ['kd_plus',   [  1e7, 1]] ,
        (3, 4) : ['kd_min',    [ 1500, 0]] ,
        (1, 5) : ['k_plus',    [  1e7, 1]] ,
        (5, 1) : ['k_min',     [20000, 0]] ,

        }

        N_states = 6 # state this rather than obtain automatically.

        #states and their conductances
        open_states = {0:.4}



    if F_states:
        return rd, N_states, open_states, F_states
    else:
        return rd, N_states, open_states

