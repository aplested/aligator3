#! /usr/bin/python

__author__="Andrew"
__date__ ="$Jun 21, 2011 2:53:11 PM$"

# Revised 2026-05-04 for Synaptic Biophyics course

if __name__ == "__main__":
    ## from https://stackoverflow.com/questions/11536764
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        import rcj_Processor as r
    
    else:
        import rcj_Processor as r
    
    print("RCJ - Calculation of relaxations in response to Realistic Concentration Jumps")
    print("Version 0.3 - Python3 conversion")

    ### Here one can set input directory and so on

    input_settings = {
    'directory'     : 'tests',           # demo input file in tests directory
    'single_files'  : True  ,            # simulate from individual rate files
    'MR'            : 'Automatic'        # approach for handling Microscopic Reversibility
    }
    # 'MR' setting is passed to jump_parameters eventually - should be in there to begin with??
    
    ### Here one can set the parameters of the jump
    ### All time parameters are in microseconds

    jump_parameters = {
    'step_size'     : 8 ,           #the sampling step.
    'pulse_rise'    : 2000 ,        #how far into the record should the jump occur
    'rise_time'     : [200, 500] ,       # list of 10-90% rise times for error functions ;each jump made in turn
    'pulse_width'   : [1000] ,      # list of pulse widths, each made in turn
    'record_length' : 60000,
    'peak_conc'     : 2e-3,         # in molar
    'shape'         : 'rcj'         # can one write inst-Exp here? Does it work?
    }

    ### Here one can control the output format and order

    output_format = {
    'jump_y_offset' : .5,         # The display offset for the jump (Adds 1.2 to all values on [Molar] scale)
    'Occupancies'   : True,        # Output of state occupancies - parallel output merge fails if True
    'P-open'        : True,        # Output of Open probability
    'merge_parallel': False,       # Merge output files after each set rather than for all sims at the end
    'get_rise_fall' : True         # Use threshold algorithm to find 10-90% rise and fall times
    }

    print("The following parameters will be used")
    
    for key in jump_parameters:
        print(key, jump_parameters[key])

    for key in output_format:
        print(key, output_format[key])

    if input_settings['single_files']:

        r.rcj_batch (input_settings, jump_parameters, output_format)

    else:
        ## NOT IMPLEMENTED YET
        r.rcj_batch_generate_mechs (input_settings, jump_parameters, output_format)
