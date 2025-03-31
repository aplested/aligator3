
__author__="Andrew"
__date__ ="$Jan 11, 2011 12:01:30 PM$"

## 14/06/11 Added capability to simulate multiple pulse widths from same input file
##          and input and output option dictionaries

## 21/06/11 Removed executable hook and main module to rcj.py

import os.path
import os
import rcj_lib
import IO_utils as rcj_IO
import shutil
import Q_input

def get_rise_fall (file_containing_trace):
    '''
    calculate rise and fall times from thresholds

    Arguments : file_containing_trace - a string with the full path of the text
                                            file containing the trace

    Returns   : two floats, rise and fall (in samples, not time)
    '''

    #read a single trace as a numpy array
    tr = rcj_IO.read_trace(file_containing_trace)

    #get the step count for the rise and fall time
    #by default, 10-90%
    return rcj_lib.crossing_time_measure(tr, 0.1, 0.9, False)

    

def run_rcj(prt_file, input_opts, output_opts, jump_parameters, Root_dir):
    '''
    Arguments:  prt_file            -   the text rate input filename
                input_opts          -   dictionary including microscopic reversibility options
                output_opts         -   dictionary of O/P FOrmat params
                jump_parameters     -   dictionary of parameters for jump
                Root_dir            -   the path in which to create the results directory


    Returns:    out_dir             -   the path where results were saved
                saved_file_list     -   the list of the individual trace files from each sim
                success             -   flag in case simulation failed
    '''

    print 'Running RCJ on %s' %prt_file

    sim_dir_name = prt_file[:-4]+'_sim'      # -4 to remove .txt suffix
    rcj_IO.make_folder(sim_dir_name,Root_dir)
                                                        # make folder returns output directory
    input_file = os.path.join(Root_dir,prt_file)

    out_dir = os.path.join(Root_dir,sim_dir_name)
    
    MR_option = input_opts['MR']
    #try
    saved_file_list = multi_rcj_setup( jump_parameters, MR_option, output_opts, input_file, out_dir,True,False )   #verbose and no user intervention

    #move original prt into new dir
    shutil.copy2(input_file,os.path.join(out_dir,prt_file))
    success = True
    #os.remove(input_file)          # leave input file in place for re-run if required

    #except:
     #   success = False
      #  if not rcj_IO.ask_ok("Jump simulation on %s failed. Continue"%prt_file):
       #n     sys.exit(1)

    return out_dir, saved_file_list,  success

def rcj_single(rates, parameters):

    jump = rcj_lib.make_jump(parameters)
    relax = rcj_lib.rcj_calc_nump (jump, rates, parameters)
    return jump, relax

def multi_rcj_setup(Parameters, MR_option, op_fo, input_filename = 'ke08ceko2b.txt',output_directory = '.', verbose = False, user = True):

    '''
    Arguments:  Parameters          -   jump parameters - can contain value lists
                MR_option           -   how to define MR - 'automatic' or 'HardCoded'
                op_fo               -   dictionary of O/P FOrmat params
                input_filename      -   text file to get rates
                output_directory    -   path to save results
                verbose             -   give extra terminal output if true
                user                -   user intervention on rates

    Returns

    '''
    if verbose:
        print 'Taking rates from:',input_filename

    saved =[]
    #convert HJCFIT prt to text ratefile, and grab the number of open states
    rates_filename, N_open, src_prog = rcj_IO.prt_to_rates(input_filename,output_directory)   
    
    if verbose:
        print 'Detected that ',input_filename, ' is a ',src_prog,' printout file'
    
    open_states = []            #make a list of the numbered open states (assume they begin at 0, as per convention
    for o in range (N_open):
        open_states.append(o)
    if verbose: print 'Open state list', open_states
    
    prt_file_lines, read_from_file   = rcj_IO.read_rate_file (rates_filename)

    rate_dict, MR_ex, MR_in = Q_input.rates_read(prt_file_lines, src_prog)
    
    if verbose: Q_input.report (read_from_file, rate_dict)

    if user:
        rates = Q_input.modify_by_hand (rate_dict)
    else: rates = rate_dict


    Parameters ['N_states']  = Q_input.number_of_states(rates) 

    input_filename = os.path.basename(input_filename)  #extract name of file from full path
        
    for pwidth in Parameters['pulse_width']:
        for rise in Parameters['rise_time']:

            if verbose: print 'Calculating %s microsec jump with %s microsec rise for %s...' %(pwidth,rise,input_filename)

            P_copy = Parameters.copy()
            P_copy['rise_time'] = rise      #send parameters dict with single rise time
            P_copy['pulse_width'] = pwidth  #send parameters dict with single pulse width
            
            P_copy['MR_option'] = MR_option
            
            if MR_option == 'Automatic':
                P_copy['MR_avoid'] = MR_ex
                P_copy['MR_use'] = MR_in
            
            jump, relax = rcj_single(rates, P_copy)

            jump_data_out = rcj_lib.compose_rcj_out(jump, relax, open_states,op_fo['jump_y_offset'],op_fo['Occupancies'],op_fo['P-open'])

            save_filename = input_filename[:-4]+' rt_'+str(rise)+'_pw_'+str(pwidth) +'.xls'   # -4 : remove '.txt', space after ip fname for split on merge
            full_save_path = os.path.join(output_directory,save_filename)

            rcj_IO.simple_save (jump_data_out,full_save_path)
            saved.append(save_filename)
                      
    if verbose: print 'Calculations for %s done.'%(input_filename)

    return saved

def rcj_batch (ip_set, jump_paras, op_set):
    '''
    batch simulation of jump responses from arbitrary number of rate files

    Arguments:          
    ip_set      -   the input settings dictionary - currently only a working directory

    jump_paras  -   dictionary of the detail of the jump; multiple rise times and widths are possible
                    'step_size'     #the sample step in microseconds
                    'pulse_rise'    #in mus
                    'rise_time'     #erf rise in mus, can be list for multiple : [0,250,500] ;each jump made in turn
                    'pulse_width'   # list of pulse widths, each made in turn
                    'record_length'
                    'peak_conc'     #in molar
                    'shape'     : options include

    op_set      -   dictionary of output settings
                    'jump_y_offset'  #display offset of jump (Adds to all values in jump [Molar])
                    'Occupancies'    #Output of state occupancies - Merging fails if True
                    'P-open'         #Output of Open probability
                    'merge_parallel' #Merge files after each set of sims, rather than for all sims at the end
                    'get_rise_fall'  #Use threshold algorithm to find 10-90% rise and fall times
    '''
    simulated ={}               #make a dictionary of the paths to files that are used for simulations
    rf_times_by_file = {}       #dictionary of rise and fall times for each simulated file

    FilesInPath, Data_Root = rcj_IO.getpath(False,ip_set['directory'])              # if False : user can decide directory

    sys_ignored = False
    
    for prt_file in FilesInPath:                #iterate over file objects found

        if prt_file[-3:] == 'txt' and prt_file[:3] != 'rcj' and prt_file[:3] != 'ali':         
        #check for txt suffix, ignore others and aligator- or rcj-associated

            output_directory, saved_files, sim_success = run_rcj(prt_file, ip_set, op_set, jump_paras, Data_Root)

            if sim_success:
                simulated[prt_file] = output_directory

            if op_set['get_rise_fall']:
                os.chdir(output_directory)
                print "Getting rise and fall times"
                s = jump_paras['step_size']
                for trace_file in saved_files:
                    rise_in_samp,fall_in_samp = get_rise_fall (trace_file)
                    rf_times_by_file[trace_file] = [rise_in_samp*s,fall_in_samp*s]

            if op_set['merge_parallel']:
                print 'merging output...\n'
                os.chdir(output_directory)
                column_prefices = ['jump','popen']
                rcj_IO.rcj_merge(saved_files,column_prefices)

        elif os.path.isdir(prt_file):          #ignore directories!
            print 'Ignoring direcory: %s' %prt_file

        elif prt_file[0] == "." and not sys_ignored: #UNIX hidden file
            sys_ignored = True
            print 'Ignoring all hidden files'

        elif prt_file[0] == "." and sys_ignored: pass

        else : print 'Ignoring %s' %prt_file        #ignore all other files

    print 'Summary:'

    if len(simulated) == 0:
        print "Nothing done"
    else:
        for k in simulated.keys():
            print ' %s sent to RCJ,' % (k)
            if not op_set['merge_parallel']:
                print 'merging output...\n'
                os.chdir(simulated[k])              #values are paths to individual simulation directories
                column_titles = ['jump','popen']
                rcj_IO.rcj_merge(os.listdir(simulated[k]),column_titles)

            else:
                print 'output merged during run\n'


        #send table with header to file
        rcj_IO.write_table(rf_times_by_file,'file\trise (mus)\tfall (mus)\n',Data_Root)

            