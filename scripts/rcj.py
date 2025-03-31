#! /usr/bin/python

__author__="Andrew"
__date__ ="$Jun 21, 2011 2:53:11 PM$"

import rcj_Processor as r

if __name__ == "__main__":

    print "RCJ - Calculation of relaxations in response to Realistic Concentration Jumps"
    print "Version 0.1"

    ### set input directory and so on

    input_settings = {
    'directory'     : '//users/andrew/desktop/rcj',          #put rcj_input in the home directory
    'single_files'  : True  ,                 #simulate from individual rate files
    'MR'            : 'Automatic'
    }
    # 'MR' setting is passed to jump_parameters eventually - should be in there to begin with??
    
    ### Here one can set the parameters of the jump

    jump_parameters = {
    'step_size'     : 8 ,           #the sampling step. All time params are in microseconds
    'pulse_rise'    : 2000 ,        #how far into the record should the jump occur
    'rise_time'     : [200] , # list of 10-90% rise times for error functions ;each jump made in turn
    'pulse_width'   : [2500] , # list of pulse widths, each made in turn
    'record_length' : 60000,
    'peak_conc'     : 2e-3,          #in molar
    'shape'         : 'rcj'
    }

    ### Here one can control the output format and order

    output_format = {
    'jump_y_offset' : 1.2,         #the display offset for the jump (Adds 1.2 to all values in jump [Molar])
    'Occupancies'   : True,        #Output of state occupancies - parallel output merge fails if True
    'P-open'        : True,        #Output of Open probability
    'merge_parallel': False,        #Merge output files after each set of sims, rather than for all sims at the end
    'get_rise_fall' : True         #Use threshold algorithm to find 10-90% rise and fall times
    }

    for key in jump_parameters:
        print key, jump_parameters[key]

    for key in output_format:
        print key, output_format[key]

    if input_settings['single_files']:

        r.rcj_batch (input_settings, jump_parameters, output_format)

    else:
        ## NOT IMPLEMENTED YET
        r.rcj_batch_generate_mechs (input_settings, jump_parameters, output_format)
