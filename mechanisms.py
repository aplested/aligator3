#This module handles the mechanism

#module is becoming huge. Need to package up mechanisms better
#in a subdirectory?

def mechanism(mech="4"):
    # rate dictionaries for the given mechanisms
    #

    if mech == "None":
        return None, None, None

    built_ins = ["1", "2", "3", "3M", "3s", "4", "5", "6", "cp2", "dck", "3KA", "4KA", "3b", "4b", "dckF", "dckD2" ,"dckFD", "JW1", "GG1", "GG5", "flipF"]
    
    
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
            print ("couldn't find or import mechanism, using default (mech. dckF)")
            mech = "4"

    #By default, mechanisms don't include fluorescence
    F_states = None

    if mech == "dckF":
        # del castillo katz mechanism with desensitization for PCF simulations
        # Topology
        # 3 - 1 - 0
        #     |   
        #     2 
        
        rd = {      
        
        (1, 0) :  ['beta'  , [5000, 0]] ,
        (0, 1) :  ['alpha' , [1000, 0]] ,
        (1, 2) :  ['d_pl'  , [500, 0]] ,
        (2, 1) :  ['d_min' , [10, 0]] ,
        (3, 1) :  ['k_pl'  , [3e6, 1]]  ,
        (1, 3) :  ['k_min' , [10000, 0]],
        }

        N_states = 4
        open_states = {0 : 1} 
        F_states = {0 : 1, 1 :  0.2, 2: 0, 3: 0.2} 

        #used in simulations 140402
        """F_vectors = [
        {0 : 0,     1 :  0.5,   2: 0.0, 3: 0.5},
        {0 : 1,     1 :  0.5,   2: 0,   3: 0.5},
        {0 : 0.5,   1 :  1,     2: 1,   3: 0},
        {0 : 0,     1 :  0,     2: 1,   3: 0 },
        {0 : 0.5,   1: 0.5,     2: 0.3,   3: 0.2},
        {0 : 0,     1: 0.5,     2: 1,   3: 0.5}
        ]"""
    
    if mech == "dckD2":
        # del castillo katz mechanism with 2 branched des (2 and 3) for PCF simulations
        # Topology
        #
        #    3
        #    |
        #4 - 1 - 0
        #    |   
        #    2 
        #     

        rd = {      
        
        (1, 0) :  ['beta'  , [1000, 0]] ,
        (0, 1) :  ['alpha' , [200, 0]] ,
        (1, 2) :  ['d2_pl'  , [100, 0]] ,
        (2, 1) :  ['d2_min' , [500, 0]] ,
        (1, 3) :  ['d3_pl' , [5000, 0]] ,
        (3, 1) :  ['d3_min', [5, 0 ]],
        (4, 1) :  ['k_pl'  , [5e6, 1]]  ,
        (1, 4) :  ['k_min' , [1000, 0]],
        }

        N_states = 5
        open_states = {0 : 1} 
        F_states = {0 : 1}
        
    if mech == "dckF2":
        # del castillo katz mechanism with 2des for PCF simulations
        # Topology
        # 4 - 1 - 0
        #     |   
        #     2 
        #     |
        #     3

        rd = {      
        
        (1, 0) :  ['beta'  , [5000, 0]] ,
        (0, 1) :  ['alpha' , [2000, 0]] ,
        (1, 2) :  ['d_pl'  , [200, 0]] ,
        (2, 1) :  ['d_min' , [200, 0]] ,
        (2, 3) :  ['d2_pl' , [100, 0]] ,
        (3, 2) :  ['d2_min', [40, 0 ]],
        (4, 1) :  ['k_pl'  , [5e6, 1]]  ,
        (1, 4) :  ['k_min' , [1000, 0]],
        }

        N_states = 5
        open_states = {0 : 1} 
        F_states = {0 : 1, 1 :  0.2, 2: 0, 3: 0.2, 4: 0.1} 
    
    if mech == "JW1" :
        #Jones and Westbrook mechanism for GABAR (1995 paper rates)
        #Topology
        #
        #   5   3
        #6 -4 - 2
        #   1   0
        rd = {      
        (2, 0) :  ['beta2'  , [2500, 0]] ,
        (0, 2) :  ['alpha2' , [142, 0]] ,
        (4, 1) :  ['beta1'  , [200, 0]] ,
        (1, 4) :  ['alpha1' , [1111, 0]] ,
        (3, 2) :  ['r2' ,   [20, 0]] ,
        (2, 3) :  ['d2',    [875, 0 ]],
        (5, 4) :  ['r1' ,   [0.13, 0]] ,
        (4, 5) :  ['d1',    [13, 0 ]],
        (4, 2) :  ['k_on'  , [3e6, 1]]  ,
        (2, 4) :  ['2k_off' , [300, 0]],
        (6, 4) :  ['2k_on'  , [6e6, 1]]  ,
        (4, 6) :  ['k_off' , [150, 0]]
        }
        N_states = 7
        open_states = {0 : 1, 1 : 1}
        F_states = {0 : 1} 
    
    if mech == "GG5" :
        #Jones and Westbrook mechanism for GABAR (1995 paper rates) with extra open des
        #As GG4 but moving des to monoliganded physical sense)
        #Topology
        #kind of works for faster and slower F signals. Need to tune a bit. 
        #
        #   5   3
        #7 -6 - 4 
        #   1   0 - 2
        rd = {      
        (4, 0) :  ['beta2', [400, 0]],
        (0, 4) :  ['alpha2',[100, 0]],
        (6, 1) :  ['beta1' ,[50, 0]],
        (1, 6) :  ['alpha1',[200, 0]],
        (2, 0) :  ['r2',    [2, 0]],
        (0, 2) :  ['d2',    [10, 0]],
        (5, 6) :  ['r3',    [20, 0]],
        (6, 5) :  ['d3',    [10, 0 ]],
        (3, 4) :  ['r1',    [50, 0]],
        (4, 3) :  ['d1',    [200, 0 ]],
        (6, 4) :  ['k_on',  [3e6, 1]],
        (4, 6) :  ['2k_off',[200, 0]],
        (7, 6) :  ['2k_on', [6e6, 1]],
        (6, 7) :  ['k_off', [100, 0]],
        }
        N_states = 8
        open_states = {0 : 1, 1 : 1}
        F_states = {0 : 1} 
  
  
    if mech == "GG4" :
        #Double gate (GG) modification of Jones and Westbrook mechanism for GABAR (1995 paper rates)
        #As GG3 but with an extra des state
        #Topology
        #
        #       5
        #7 -6 - 4 - 3
        #   1   0 - 2
        rd = {      
        (4, 0) :  ['beta2', [200, 0]],
        (0, 4) :  ['alpha2',[100, 0]],
        (6, 1) :  ['beta1' ,[50, 0]],
        (1, 6) :  ['alpha1',[200, 0]],
        (2, 0) :  ['r2',    [200, 0]],
        (0, 2) :  ['d2',    [50, 0]],
        (5, 4) :  ['r3',    [5, 0]],
        (4, 5) :  ['d3',    [20, 0 ]],
        (3, 4) :  ['r1',    [50, 0]],
        (4, 3) :  ['d1',    [200, 0 ]],
        (6, 4) :  ['k_on',  [3e6, 1]],
        (4, 6) :  ['2k_off',[200, 0]],
        (7, 6) :  ['2k_on', [6e6, 1]],
        (6, 7) :  ['k_off', [100, 0]],
        }
        N_states = 8
        open_states = {0 : 1, 1 : 1}
        F_states = {0 : 1} 
  
    if mech == "GG3" :
        #Double gate (GG) modification of Jones and Westbrook mechanism for GABAR (1995 paper rates)
        #As GG1 but no connection between 2 and 3
        #Topology
        #
        #         3
        #6 -5 - 4   2
        #   1     0
        rd = {      
        (4, 0) :  ['beta2', [200, 0]],
        (0, 4) :  ['alpha2',[100, 0]],
        (5, 1) :  ['beta1' ,[50, 0]],
        (1, 5) :  ['alpha1',[200, 0]],
        (2, 0) :  ['r2',    [200, 0]],
        (0, 2) :  ['d2',    [50, 0]],
        (3, 4) :  ['r1',    [50, 0]],
        (4, 3) :  ['d1',    [200, 0 ]],
        (5, 4) :  ['k_on',  [3e6, 1]],
        (4, 5) :  ['2k_off',[200, 0]],
        (6, 5) :  ['2k_on', [6e6, 1]],
        (5, 6) :  ['k_off', [100, 0]],
        }
        N_states = 7
        open_states = {0 : 1, 1 : 1}
        F_states = {0 : 1} 
        
    if mech == "GG1" :
        #Double gate (GG) modification of Jones and Westbrook mechanism for GABAR (1995 paper rates)
        #Don't know what rate to allow for MR at this stage - guess one of the D-D (2-3) transitions?
        #or should it be allowed to ignore - interaction with Cl?
        #Topology
        #
        #         3
        #6 -5 - 4   2
        #   1     0
        rd = {      
        (4, 0) :  ['beta2', [500, 0]],
        (0, 4) :  ['alpha2',[100, 0]],
        (5, 1) :  ['beta1' ,[100, 0]],
        (1, 5) :  ['alpha1',[200, 0]],
        (3, 2) :  ['d12',   [20, 0]],
        (2, 3) :  ['d21',   [2, 0]],
        (2, 0) :  ['r2',    [1, 0]],
        (0, 2) :  ['d2',    [2, 0]],
        (3, 4) :  ['r1',    [200, 0]],
        (4, 3) :  ['d1',    [20, 0 ]],
        (5, 4) :  ['k_on',  [3e6, 1]],
        (4, 5) :  ['2k_off',[300, 0]],
        (6, 5) :  ['2k_on', [6e6, 1]],
        (5, 6) :  ['k_off', [150, 0]],
        }
        N_states = 7
        open_states = {0 : 1, 1 : 1}
        F_states = {0 : 1} 
    
    if mech == "GG2" :
        #Double gate (GG) modification of Jones and Westbrook mechanism for GABAR (1995 paper rates)
        #Don't know what rate to allow for MR at this stage - guess one of the D-D (2-3) transitions?
        #or should it be allowed to ignore - interaction with Cl?
        #more like JW because it has a monoliganded fast des state (6).
        #Topology
        #
        #   6     3
        #7 -5 - 4   2
        #   1     0
        rd = {      
        (4, 0) :  ['beta2', [500, 0]],
        (0, 4) :  ['alpha2',[100, 0]],
        (5, 1) :  ['beta1' ,[100, 0]],
        (1, 5) :  ['alpha1',[200, 0]],
        (3, 2) :  ['d12',   [20, 0]],
        (2, 3) :  ['d21',   [2, 0]],
        (2, 0) :  ['r2',    [1, 0]],
        (0, 2) :  ['d2',    [2, 0]],
        (3, 4) :  ['r1',    [200, 0]],
        (4, 3) :  ['d1',    [20, 0 ]],
        (5, 4) :  ['k_on',  [3e6, 1]],
        (4, 5) :  ['2k_off',[300, 0]],
        (7, 5) :  ['2k_on', [6e6, 1]],
        (5, 7) :  ['k_off', [150, 0]],
        (6, 5) :  ['r0', [10,0]],
        (5, 6) :  ['d0', [200,0]]
        }
        N_states = 8
        open_states = {0 : 1, 1 : 1}
        F_states = {0 : 1}
        
    if mech == "flipF":
        # flip with fluorescence and des
        #8-7-6
        #  | |
        #  5-4
        #  | |
        #3-1 0-2
        rd = {      
        (4, 0) :  ['beta2'  , [2500, 0]] ,
        (0, 4) :  ['alpha2' , [500, 0]] ,
        (5, 1) :  ['beta1'  , [400, 0]] ,
        (1, 5) :  ['alpha1' , [1111, 0]] ,
        (2, 0) :  ['r2' ,   [10, 0]] ,
        (0, 2) :  ['d2',    [10, 0 ]],
        (3, 1) :  ['r1' ,   [4, 0]] ,
        (1, 3) :  ['d1',    [4, 0 ]],
        (5, 4) :  ['kf_on'  , [3e6, 1]]  ,
        (4, 5) :  ['2kf_off' , [60, 0]],
        (8, 7) :  ['2k_on'  , [6e6, 1]]  ,
        (7, 8) :  ['k_off' , [150, 0]] ,
        (7, 6) :  ['k_on'  , [3e6, 1]]  ,
        (6, 7) :  ['2k_off' , [300, 0]],
        (7, 5) :  ['f1+' , [200, 0]],
        (5, 7) :  ['f1-' , [200, 0]],
        (6, 4) :  ['f2+' , [500, 0]],
        (4, 6) :  ['f2-', [200,0]]
        }
        N_states = 9
        open_states = {0 : 1, 1 : 1}
        F_states = {0 : 1} 
        
    if mech == "dckFD":
        # del castillo katz -FLIP mechanism with after_D for CC PCF simulations
        # Topology
        # 4 - 3 - 2 - 0 - 1

        rd = {      
        
        (2, 0) :  ['beta'  , [500, 0]] ,
        (0, 2) :  ['alpha' , [100, 0]] ,
        (0, 1) :  ['d_pl'  , [15, 0]] ,
        (1, 0) :  ['d_min' , [30, 0]] ,
        (3, 2) :  ['F+' ,   [100, 0]] ,
        (2, 3) :  ['F-',    [50, 0 ]],
        (4, 3) :  ['k_pl'  , [4e6, 1]]  ,
        (3, 4) :  ['k_min' , [1000, 0]],
        }

        N_states = 5
        open_states = {0 : 1} 
        F_states = {0 : 1, 1 :  0.2, 2: 0, 3: 0.2, 4: 0.1}        

    if mech == "1":
        # Simul13;32 - d2 connected to open
        # trying to get deact right - alpha down but
        # The list is as follows: (Initial state, Final State, Rate, Conc_dep = 1)

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
        open_states = [0]

    if mech == "2":
        # same mechanism (new numbering) with Stg on open state
        ### TOPOLOGY
        # 6 - 5 - 0 - 1
        # |   |   |
        # 4 - 3 - 2

        # 0 = AR*
        # 1 = AR* + Stg
        # 2 = AD2
        # 3 = AD
        # 4 = D
        # 5 = AR
        # 6 = R
        #
        rd = {
        (0, 2) :  ['d2op_plus', [300, 0]] ,
        (2, 0) :  ['d2op_min',[10, 0 ]] ,
        (1, 0) :  ['stg_min', [3,0]] ,
        (0, 1) :  ['stg_plus', [20,0]] ,
        (5, 0) :  ['beta'  , [12000, 0]] ,
        (0, 5) :  ['alpha' , [5000, 0]] ,
        (5, 3) :  ['d1_plus' , [700, 0]] ,
        (3, 5) :  ['d1_min', [400, 0]] ,
        (3, 2) :  ['d2_plus' , [500, 0]] ,
        (2, 3) :  ['d2_min', [50, 0] ]   ,
        (3, 4) :  ['kd_min', [8000, 0]]  ,
        (4, 3) :  ['kd_plus' , [1e7, 1]]  ,
        (6, 5) :  ['k_plus'  , [1e7, 1]]  ,
        (5, 6) :  ['k_min' , [20000, 0]],
        (6, 4) :  ['d0_plus' , [1, 0]],
        (4, 6) :  ['d0_min', [9, 0]],
        }
        N_states = 7
        open_states = [0,1]

    if mech == "3":
        # mechanism () with Stg on open + resting state
        # 130523
        #
        #131120adjusting 0,1 and 1,0 to match macro k-super
        #140123-152123_mechs is the best candidate for paper
        #
        ### TOPOLOGY
        # 8 - 7 - 1    Stg-active       0 = AR*
        # |   |   |                     1 = ARS*
        # 6 - 5 - 0    Rest - open      2 = AD2
        # |   |   |                     3 = AD
        # 4 - 3 - 2    des              4 = D
        #                               5 = AR
        #                               6 = R
        #                               7 = ARS
        #                               8 = RS
        #
        # S-op min set to give right CR shift 131210
        # resting6-8 must be low because of high conductance of #1
        # matching to des rates, to ksuper and trying to remove bumps
        # tweaks to beta, sop_plus and d2 lifetime
        # overall it works
        ##
        #
        #
        #140123-152123_mechs is the best candidate for paper
        # MR on (0,5) and (0,1) and vary (2,3) and (2,0) [1, .7] powers
        
        rd = {
        (8, 6) : ['s_r_min',   [    1, 0]] ,
        (6, 8) : ['s_r_plus',  [ 0.07, 0]] ,
        (7, 5) : ['s_bd_min',  [    1, 0]] ,
        (5, 7) : ['s_bd_plus', [ 0.07, 0]] ,
        (1, 0) : ['s_op_min',  [    3, 0]] ,
        (0, 1) : ['s_op_plus', [   15, 0]] ,

        (5, 0) : ['beta',      [ 8000, 0]] ,
        (0, 5) : ['alpha',     [ 3000, 0]] ,
        (7, 1) : ['s_beta',    [500000,0]] ,
        (1, 7) : ['s_alpha',   [ 3000, 0]] ,
        (3, 2) : ['d2_plus',   [  120, 0]] ,
        (2, 3) : ['d2_min',    [    5, 0]] ,

        (6, 4) : ['d0_plus',   [    1, 0]] ,
        (4, 6) : ['d0_min',    [    3, 0]] ,
        (5, 3) : ['d1_plus',   [  300, 0]] ,
        (3, 5) : ['d1_min',    [   25, 0]] ,
        (0, 2) : ['d2op_plus', [  120, 0]] ,
        (2, 0) : ['d2op_min',  [    2, 0]] ,

        (4, 3) : ['kd_plus',   [  5e6, 1]] ,
        (3, 4) : ['kd_min',    [ 2500, 0]] ,
        (6, 5) : ['k_plus',    [  5e6, 1]] ,
        (5, 6) : ['k_min',     [40000, 0]] ,
        (8, 7) : ['s_k_plus',  [  5e6, 1]] ,
        (7, 8) : ['s_k_min',   [40000, 0]] ,
        }

        N_states = 9
        #states and their normalised conductances
        open_states = {0 : 0.4, 1 :  1} 
    
    if mech == "3M":
        # mechanism () with Stg on open + resting state
        # 250329 MR corrected on lower left loop (thanks to Shiny)
        #
        ##250329 kd_min is halved, tiny tweaks to D0 (+/-)
        #
        #
        ### TOPOLOGY
        # 8 - 7 - 1    Stg-active       0 = AR*
        # |   |   |                     1 = ARS*
        # 6 - 5 - 0    Rest - open      2 = AD2
        # |   |   |                     3 = AD
        # 4 - 3 - 2    des              4 = D
        #                               5 = AR
        #                               6 = R
        #                               7 = ARS
        #                               8 = RS
        #
        # S-op min set to give right CR shift 131210
        # resting 6-8 must be low because of high conductance of #1
        # matching to des rates, to ksuper and trying to remove bumps
        # tweaks to beta, sop_plus and d2 lifetime
        # overall it works
        ##
        #
        #
        #
        # MR on (0,5) and (0,1) and vary (2,3) and (2,0) [1, .7] powers
        
        rd = {
        (8, 6) : ['s_r_min',   [    1, 0]] ,
        (6, 8) : ['s_r_plus',  [ 0.07, 0]] ,
        (7, 5) : ['s_bd_min',  [    1, 0]] ,
        (5, 7) : ['s_bd_plus', [ 0.07, 0]] ,
        (1, 0) : ['s_op_min',  [    3, 0]] ,
        (0, 1) : ['s_op_plus', [   15, 0]] ,

        (5, 0) : ['beta',      [ 8000, 0]] ,
        (0, 5) : ['alpha',     [ 3000, 0]] ,
        (7, 1) : ['s_beta',    [500000,0]] ,
        (1, 7) : ['s_alpha',   [ 3000, 0]] ,
        (3, 2) : ['d2_plus',   [  120, 0]] ,
        (2, 3) : ['d2_min',    [    5, 0]] ,

        (6, 4) : ['d0_plus',   [  0.9, 0]] ,
        (4, 6) : ['d0_min',    [  2.5, 0]] ,
        (5, 3) : ['d1_plus',   [  300, 0]] ,
        (3, 5) : ['d1_min',    [   25, 0]] ,
        (0, 2) : ['d2op_plus', [  120, 0]] ,
        (2, 0) : ['d2op_min',  [    2, 0]] ,

        (4, 3) : ['kd_plus',   [  5e6, 1]] ,
        (3, 4) : ['kd_min',    [ 1200, 0]] ,
        (6, 5) : ['k_plus',    [  5e6, 1]] ,
        (5, 6) : ['k_min',     [40000, 0]] ,
        (8, 7) : ['s_k_plus',  [  5e6, 1]] ,
        (7, 8) : ['s_k_min',   [40000, 0]] ,
        }

        N_states = 9
        #states and their normalised conductances
        open_states = {0 : 0.4, 1 :  1}
        
    if mech == "3s":
        # mechanism () with Stg on open + resting state
        #151026 running with the same open state conductance for states 1 and 0
        #to provide additional information for NatComms submission
        #
        ### TOPOLOGY
        # 8 - 7 - 1    Stg-active       0 = AR*
        # |   |   |                     1 = ARS*
        # 6 - 5 - 0    Rest - open      2 = AD2
        # |   |   |                     3 = AD
        # 4 - 3 - 2    des              4 = D
        #                               5 = AR
        #                               6 = R
        #                               7 = ARS
        #                               8 = RS
        #
        #small superactivation, almost no hump
        
        rd = {
        (8, 6) : ['s_r_min',   [    1, 0]] ,
        (6, 8) : ['s_r_plus',  [ 0.07, 0]] ,
        (7, 5) : ['s_bd_min',  [    1, 0]] ,
        (5, 7) : ['s_bd_plus', [ 0.07, 0]] ,
        (1, 0) : ['s_op_min',  [    3, 0]] ,
        (0, 1) : ['s_op_plus', [   15, 0]] ,

        (5, 0) : ['beta',      [ 8000, 0]] ,
        (0, 5) : ['alpha',     [ 3000, 0]] ,
        (7, 1) : ['s_beta',    [500000,0]] ,
        (1, 7) : ['s_alpha',   [ 3000, 0]] ,
        (3, 2) : ['d2_plus',   [  120, 0]] ,
        (2, 3) : ['d2_min',    [    5, 0]] ,

        (6, 4) : ['d0_plus',   [    1, 0]] ,
        (4, 6) : ['d0_min',    [    3, 0]] ,
        (5, 3) : ['d1_plus',   [  300, 0]] ,
        (3, 5) : ['d1_min',    [   25, 0]] ,
        (0, 2) : ['d2op_plus', [  120, 0]] ,
        (2, 0) : ['d2op_min',  [    2, 0]] ,

        (4, 3) : ['kd_plus',   [  5e6, 1]] ,
        (3, 4) : ['kd_min',    [ 2500, 0]] ,
        (6, 5) : ['k_plus',    [  5e6, 1]] ,
        (5, 6) : ['k_min',     [40000, 0]] ,
        (8, 7) : ['s_k_plus',  [  5e6, 1]] ,
        (7, 8) : ['s_k_min',   [40000, 0]] ,
        }

        N_states = 9
        #states and their normalised conductances
        open_states = {0 : 1, 1 :  1}    
        
    if mech == "4":
        # mechanism 3 without Stg on open state
        # 130623
        # move 6 ->1 to avoid problems with Qmat
        # These rates are not good - MR adjusts to crazy...
        ### TOPOLOGY
        #                               0 = AR*
        # 1 - 5 - 0    Rest - open      2 = AD2
        # |   |   |                     3 = AD
        # 4 - 3 - 2    des              4 = D
        #                               5 = AR
        #                               1 = R
        #
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
        (3, 4) : ['kd_min',    [ 2500, 0]] ,
        (1, 5) : ['k_plus',    [  5e6, 1]] ,
        (5, 1) : ['k_min',     [40000, 0]] ,

        }

        N_states = 6 # state this rather than obtain automatically.

        #states and their conductances
        open_states = {0 : .4}
    
    if mech == "3KA":
        # mechanism 3 for KA with Stg on open + resting state
        #
        #        #
        ### TOPOLOGY
        # 8 - 7 - 1    Stg-active       0 = AR*
        # |   |   |                     1 = ARS*
        # 6 - 5 - 0    Rest - open      2 = AD2
        # |   |   |                     3 = AD
        # 4 - 3 - 2    des              4 = D
        #                               5 = AR
        #                               6 = R
        #                               7 = ARS
        #                               8 = RS
        #
        #140123-152123_mechs is the best glutamate candidate for paper
        # MR on (0,5) and (0,1) and vary (2,3) and (2,0) [1, .7] powers
        # 140910 setting up: beta set to 1000, sBeta 100000
        #reduce des 4x, sbeta 20000, beta 200
        #need to make des weak to get high alpha - eg 5>3 and 3>2 slow
        #adjust des to make s op plus slower
        #140910-173803_mechs is the best
        
        rd = {
        (8, 6) : ['s_r_min',   [    1, 0]] ,
        (6, 8) : ['s_r_plus',  [ 0.07, 0]] ,
        (7, 5) : ['s_bd_min',  [    1, 0]] ,
        (5, 7) : ['s_bd_plus', [ 0.07, 0]] ,
        (1, 0) : ['s_op_min',  [    3, 0]] ,
        (0, 1) : ['s_op_plus', [   15, 0]] ,

        (5, 0) : ['beta',      [ 1600, 0]] ,
        (0, 5) : ['alpha',     [30000, 0]] ,
        (7, 1) : ['s_beta',    [100000, 0]] ,
        (1, 7) : ['s_alpha',   [30000, 0]] ,
        (3, 2) : ['d2_plus',   [   12, 0]] ,
        (2, 3) : ['d2_min',    [   30, 0]] ,

        (6, 4) : ['d0_plus',   [    1, 0]] ,
        (4, 6) : ['d0_min',    [    3, 0]] ,
        (5, 3) : ['d1_plus',   [  300, 0]] ,
        (3, 5) : ['d1_min',    [  300, 0]] ,
        (0, 2) : ['d2op_plus', [  120, 0]] ,
        (2, 0) : ['d2op_min',  [   12, 0]] ,

        (4, 3) : ['kd_plus',   [  5e6, 1]] ,
        (3, 4) : ['kd_min',    [ 2500, 0]] ,
        (6, 5) : ['k_plus',    [  5e6, 1]] ,
        (5, 6) : ['k_min',     [40000, 0]] ,
        (8, 7) : ['s_k_plus',  [  5e6, 1]] ,
        (7, 8) : ['s_k_min',   [40000, 0]] ,
        }

        N_states = 9
        #states and their normalised conductances
        open_states = {0 : 0.08, 1 :  1} 
        
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
        
    if mech == "3b":
        # mechanism () with Stg on open + resting state
        # stg changes binding 15 fold and beta 2.5 fold (eg Maclean) 140122
        # used in paper Fig S3
        #
        ### TOPOLOGY
        # 8 - 7 - 1    Stg-active       0 = AR*
        # |   |   |                     1 = ARS*
        # 6 - 5 - 0    Rest - open      2 = AD2
        # |   |   |                     3 = AD
        # 4 - 3 - 2    des              4 = D
        #                               5 = AR
        #                               6 = R
        #                               7 = ARS
        #                               8 = RS
        #
  
        rd = {
        (8, 6) : ['s_r_min',   [    1, 0]] ,
        (6, 8) : ['s_r_plus',  [  0.3, 0]] ,
        (7, 5) : ['s_bd_min',  [    1, 0]] ,
        (5, 7) : ['s_bd_plus', [  4.5, 0]] ,
        (1, 0) : ['s_op_min',  [    1, 0]] ,
        (0, 1) : ['s_op_plus', [11.25, 0]] ,

        (5, 0) : ['beta',      [ 8000, 0]] ,
        (0, 5) : ['alpha',     [ 1500, 0]] ,
        (7, 1) : ['s_beta',    [20000 ,0]] ,
        (1, 7) : ['s_alpha',   [ 1500, 0]] ,
        (3, 2) : ['d2_plus',   [  200, 0]] ,
        (2, 3) : ['d2_min',    [    5, 0]] ,

        (6, 4) : ['d0_plus',   [    1, 0]] ,
        (4, 6) : ['d0_min',    [    4, 0]] ,
        (5, 3) : ['d1_plus',   [  250, 0]] ,
        (3, 5) : ['d1_min',    [    5, 0]] ,
        (0, 2) : ['d2op_plus', [  400, 0]] ,
        (2, 0) : ['d2op_min',  [   10, 0]] ,

        (4, 3) : ['kd_plus',   [  5e6, 1]] ,
        (3, 4) : ['kd_min',    [ 1500, 0]] ,
        (6, 5) : ['k_plus',    [  5e6, 1]] ,
        (5, 6) : ['k_min',     [75000, 0]] ,
        (8, 7) : ['s_k_plus',  [  5e6, 1]] ,
        (7, 8) : ['s_k_min',   [ 5000, 0]] ,
        }

        N_states = 9
        #states and their normalised conductances
        open_states = {0 : 0.4, 1 : 1}
    
    if mech == "4b":
        # synced to mech 3b
        #
        #
        ### TOPOLOGY
        #       
        #                               0 = AR*
        # 1 - 5 - 0    Rest - open      2 = AD2
        # |   |   |                     3 = AD
        # 4 - 3 - 2    des              4 = D
        #                               5 = AR
        #                               1 = R
        #                             
        #
  
        rd = {

        (5, 0) : ['beta',      [ 8000, 0]] ,
        (0, 5) : ['alpha',     [ 1500, 0]] ,
        (3, 2) : ['d2_plus',   [  200, 0]] ,
        (2, 3) : ['d2_min',    [    5, 0]] ,

        (1, 4) : ['d0_plus',   [    1, 0]] ,
        (4, 1) : ['d0_min',    [    4, 0]] ,
        (5, 3) : ['d1_plus',   [  250, 0]] ,
        (3, 5) : ['d1_min',    [    5, 0]] ,
        (0, 2) : ['d2op_plus', [  400, 0]] ,
        (2, 0) : ['d2op_min',  [   10, 0]] ,

        (4, 3) : ['kd_plus',   [  5e6, 1]] ,
        (3, 4) : ['kd_min',    [ 1500, 0]] ,
        (1, 5) : ['k_plus',    [  5e6, 1]] ,
        (5, 1) : ['k_min',     [75000, 0]] ,

        }

        N_states = 6
        #states and their normalised conductances
        open_states = {0 : 0.4}

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

    if mech == "3_auto":
        # mechanism () with Stg on open + resting state
        # Adjusting 0-1 and 6-8 to give autoinactivation
        # not possible with one binding site! because it's a steady state
        # phenomenon - we do not know the kinetics at least

        ### TOPOLOGY
        # 8 - 7 - 1    Stg-active       0 = AR*
        # |   |   |                     1 = ARS*
        # 6 - 5 - 0    Rest - open      2 = AD2
        # |   |   |                     3 = AD
        # 4 - 3 - 2    des              4 = D
        #                               5 = AR
        #                               6 = R
        #                               7 = ARS
        #                               8 = RS
        #
        rd = {
        (8, 6) : ['s_r_min',   [  0.5, 0]] ,
        (6, 8) : ['s_r_plus',  [    2, 0]] ,
        (7, 5) : ['s_bd_min',  [  0.5, 0]] ,
        (5, 7) : ['s_bd_plus', [    2, 0]] ,
        (1, 0) : ['s_op_min',  [   20, 0]] ,
        (0, 1) : ['s_op_plus', [   20, 0]] ,

        (5, 0) : ['beta',      [10000, 0]] ,
        (0, 5) : ['alpha',     [ 2500, 0]] ,
        (7, 1) : ['s_beta',    [20000, 0]] ,
        (1, 7) : ['s_alpha',   [  500, 0]] ,
        (3, 2) : ['d2_plus',   [  250, 0]] ,
        (2, 3) : ['d2_min',    [   10, 0]] ,

        (6, 4) : ['d0_plus',   [    1, 0]] ,
        (4, 6) : ['d0_min',    [    7, 0]] ,
        (5, 3) : ['d1_plus',   [ 1000, 0]] ,
        (3, 5) : ['d1_min',    [  400, 0]] ,
        (0, 2) : ['d2op_plus', [   40, 0]] ,
        (2, 0) : ['d2op_min',  [    4, 0]] ,

        (4, 3) : ['kd_plus',   [  1e7, 1]] ,
        (3, 4) : ['kd_min',    [ 1000, 0]] ,
        (6, 5) : ['k_plus',    [  1e7, 1]] ,
        (5, 6) : ['k_min',     [20000, 0]] ,
        (8, 7) : ['s_k_plus',  [  1e7, 1]] ,
        (7, 8) : ['s_k_min',   [20000, 0]] ,
        }

        N_states = 9
        #states and their normalised conductances
        open_states = {0 : 0.4, 1 : 1}


    if mech == "5":
        # mechanism 3 with Stg and with CTZ
        # 0,2; 5,3; 6,4 : set to 0.1
    # 131216
    #updated with candidate 2 for Carbone and Plested#2
        #
        ### TOPOLOGY
        # 8 - 7 - 1    Stg-active       0 = AR*
        # |   |   |                     1 = ARS*
        # 6 - 5 - 0    Rest - open      2 = AD2
        # |   |   |                     3 = AD
        # 4 - 3 - 2    des              4 = D
        #                               5 = AR
        #                               6 = R
        #                               7 = ARS
        #                               8 = RS
        #
        rd = {
        (8, 6) : ['s_r_min',   [    1, 0]] ,
        (6, 8) : ['s_r_plus',  [ 0.07, 0]] ,
        (7, 5) : ['s_bd_min',  [    1, 0]] ,
        (5, 7) : ['s_bd_plus', [ 0.07, 0]] ,
        (1, 0) : ['s_op_min',  [    3, 0]] ,
        (0, 1) : ['s_op_plus', [   15, 0]] ,

        (5, 0) : ['beta',      [ 8000, 0]] ,
        (0, 5) : ['alpha',     [ 3000, 0]] ,
        (7, 1) : ['s_beta',    [500000,0]] ,
        (1, 7) : ['s_alpha',   [ 3000, 0]] ,
        (3, 2) : ['d2_plus',   [  120, 0]] ,
        (2, 3) : ['d2_min',    [    5, 0]] ,

        (6, 4) : ['d0_plus',   [  0.1, 0]] ,
        (4, 6) : ['d0_min',    [    3, 0]] ,
        (5, 3) : ['d1_plus',   [  0.1, 0]] ,
        (3, 5) : ['d1_min',    [   25, 0]] ,
        (0, 2) : ['d2op_plus', [  0.1, 0]] ,
        (2, 0) : ['d2op_min',  [    2, 0]] ,

        (4, 3) : ['kd_plus',   [  5e6, 1]] ,
        (3, 4) : ['kd_min',    [ 2500, 0]] ,
        (6, 5) : ['k_plus',    [  5e6, 1]] ,
        (5, 6) : ['k_min',     [40000, 0]] ,
        (8, 7) : ['s_k_plus',  [  5e6, 1]] ,
        (7, 8) : ['s_k_min',   [40000, 0]] ,
        }

        N_states = 9
        #states and their normalised conductances
        open_states = {0 : 0.4, 1 : 1}

    if mech == "6":
        # mechanism 4 without Stg but with CTZ
        # 0,2; 5,3; 6,4 : 10x slower than in Mech 5
        # 130823
        #
        ### TOPOLOGY
        #                               0 = AR*
        # 1 - 5 - 0    Rest - open      2 = AD2
        # |   |   |                     3 = AD
        # 4 - 3 - 2    Des -closed      4 = D
        #                               5 = AR
        #                               1 = R
        #
        rd = {

        (5, 0) : ['beta',      [10000, 0]] ,
        (0, 5) : ['alpha',     [ 4000, 0]] ,
        (3, 2) : ['d2_plus',   [  500, 0]] ,
        (2, 3) : ['d2_min',    [   50, 0]] ,

        (1, 4) : ['d0_plus',   [  0.1, 0]] ,
        (4, 1) : ['d0_min',    [    9, 0]] ,
        (5, 3) : ['d1_plus',   [   80, 0]] ,
        (3, 5) : ['d1_min',    [  400, 0]] ,
        (0, 2) : ['d2op_plus', [   30, 0]] ,
        (2, 0) : ['d2op_min',  [   10, 0]] ,

        (4, 3) : ['kd_plus',   [  5e6, 1]] ,
        (3, 4) : ['kd_min',    [ 4000, 0]] ,
        (1, 5) : ['k_plus',    [  5e6, 1]] ,
        (5, 1) : ['k_min',     [10000, 0]] ,

        }

        N_states = 6
        #states and their conductances
        open_states = {0:1}


    if F_states:
        return rd, N_states, open_states, F_states
    else:
        return rd, N_states, open_states

