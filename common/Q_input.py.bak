### Library of routines for interpreting + modifying Q matrix data

__author__="Andrew"
__date__ ="$Jan 3, 2011 4:21:11 PM$"

import os,sys

def interpret_line(mech_line, commands, prog='Unknown'):
    '''
    Interpret each line of a text file with all info for mechanism

    Argument:
        mech_line -- a single string made from one line of a mech file
    Keyword Argument:
        prog -- if previously determined, can be provided

    Returns - string (rate name) and list [values] or string (rm command)
    '''
    #print prog

    #remove first element of line, splitting at spaces
    #print "%r"%mech_line   RAW string for debugging
    l = mech_line.split()
    short = mech_line.strip()
    first_element = l.pop(0)

    if prog == 'Unknown':
        try:
            #in meaningful lines, the DC format has an integer number for the rate as the first element
            dc_rate_num = int(first_element)
            format = 'DCProgs_prt'
        except:
            format = 'RCJ Native'
            
    elif prog == 'SCALCS':
        format = 'DOS_DCProgs_prt'
    
    elif prog == 'Win_HJCFIT':
        format = 'DCProgs_prt'
    
    elif prog == 'RCJ':
        format = 'RCJ Native'

    
    if first_element in commands:      # Remove rate or MR commands

        return first_element, l, None

    elif first_element.find('(') == 0 and len(short.split()) == 1:     # To catch irrelevant DCProgs rate info (constrained) (Micro-Rev)
        return '*rm', None, None                                   #Should miss rate constants beginning with '(' ; if such an abomination exists
                                                            #Because len(short.split()) should be > 1 in that case.
        # return a null-'remove command' to act as pass

    elif format == 'RCJ Native':

        rate_name = first_element
        s = []
        y = []
        for elem in l:
            s.append(elem)
        x = tuple(s[:1])
        for e in s[2:]:
            y.append(float(e)) 

    elif format == 'DOS_DCProgs_prt':
        #DOS format isn't the same as the windows Beta
        
        l = mech_line.split('\x00')       #null character
                                        #not sure why this is here, obviously for older prt styles
        
        split_line = l[0]
        print split_line,'hi;'
        sll = split_line.find('(')
        slr = split_line.find(')') + 1
        #if verbose: print sl, sll, slr
        try:
            from_to = eval(split_line[sll:slr])  #grab from_to info as tuple
        except:
            print mech_line, split_line[sll:slr], 'dcfile input fail - modify script or file'
            return  '*rm', None, None
            # return a null-remove command to act as pass

        rate_name = split_line[20:30].strip()
        #if verbose:print rate_name
        
        r_c = split_line[31:].strip()       #previously used l[-1]. Is this required for very old prts??
        
        #if verbose:print r_c   
        
        rate_const = float(r_c)

        mux_conc = 0
        if split_line[6] == '*':
            mux_conc = 1
            #rate must be multiplied by concentration

        #subtract 1 because states are zero biased in qmat.py
        x = (from_to[0]-1, from_to[1]-1)
        y = [rate_const, mux_conc]

    elif format == 'DCProgs_prt':
    #DC Progs HJCFIT Windows Beta format
        try:
            from_to = eval(mech_line[7:14])
        except:
            print mech_line, mech_line[7:14], 'dcfile input fail - modify script or file'
            return None,'*rm'
            # return a null-remove command to act as pass

        #print from_to
        rate_name = mech_line[18:27].strip()

        r_c = mech_line[43:55].strip()
        rate_const = float(r_c)

        mux_conc = 0

        #Assume that association rates contain a '+' sign (and other rates don't) -- RISKY!!
        if rate_name.find('+') <> -1:
            mux_conc = 1
            
        #subtract 1 because states are zero biased in qmat.py
        x = (from_to[0]-1, from_to[1]-1)
        y = [rate_const, mux_conc]
    

    return rate_name, x, y

def modify_by_hand(rate_dictionary):

    '''
    takes dictionary of rates, allows user modification
    Argument : -- rate_dictionary : a dictionary of rate information

    returns - dictionary
    '''
    commands = {'*ls':'list rates in mechanism',
                '*rm [Rate Name]':'remove a rate from mechanism'}

    instructions = "To add or modify a rate, please type (separated by spaces):\n"\
    "1)the rate name 2)initial & 3)final states 4)rate value and 5)binding info [0=not association rate, 1=assoc. rate]\n"\
    "Example formatting: alpha 0 1 1000 0\n"\
    "Commands:\n"
    
    for c in commands:
        instructions += c + ' : ' + commands[c]+'\n'

    print instructions
    #input loop
    while 1:

        mech_input = raw_input('?: ')

        if mech_input == '*ls':

            report('',rate_dictionary)
            print instructions

        elif mech_input != '' and mech_input != '*ls':

            a, b, c = interpret_line(mech_input)

            if b != '*rm':
                if rate_dictionary.has_key(a):
                    print "changing rate: %s to %s" %(a,b)
                    rate_dictionary[a] = b

                elif rate_dictionary.has_key(a) == False:
                    print "adding rate: %s " %a,b
                    rate_dictionary[a] = b

            elif b == '*rm':
                if rate_dictionary.has_key(a):
                    print "removing rate [%s] ..." %a
                    del rate_dictionary[a]
            
                elif rate_dictionary.has_key(a) == False and a != None:
                    print 'rate [%s] not in list, ignoring request to remove it' %a

                else:
                    print 'Error: no rate given, please use *rm [Rate Name], where [Rate Name] is a valid name in the mechanism'

        else:
            return rate_dictionary

def rates_read (mech_text, prog):
    '''
    Extract rate information from a list of strings
        Arguments : 
         mech_text  -- a list of lines, with rate information
         prog       -- progam that produced printout
        Returns - a dictionary of rates, and lists of MR exclusion and inclusion edges
    '''

    commands = {'*rm'   : 'remove rate',
                 '*MR_avoid': 'do not use edge for MR',
                 '*MR_use'  : 'use edge for MR'}

    rate_dictionary = {}
    MR_include = []
    MR_exclude = []

    while mech_text != []:

        #pop first line from list
        m_l = mech_text.pop(0)

        if m_l != '\r\n' and m_l != '\n':                   #skip blank lines
            a, b, c = interpret_line(m_l, commands, prog)
            #      returns rate_name
            #           x = (from_to[0]-1, from_to[1]-1)
            #           y = [rate_const, mux_conc]



            if a not in commands and b != None:
                rate_dictionary[b] = [a, c]

            if a != '*rm' and b == None:
               pass

            if a =='*rm' and b != None:
                del rate_dictionary[b]

            if a =='*MR_use' and b != None:
                MR_include.append(b)

            if a =='*MR_avoid' and b != None:
                MR_exclude.append(b)
    
    if MR_include == []: MR_include = [None]
    if MR_exclude == []: MR_exclude = [None]
    
    return rate_dictionary, MR_include, MR_exclude



def chop_HJC_prt (prt, prog='Win_HJCFIT'):

    '''
    Edit and clean prt file output from dcprogs to give mechanism rates only

    Argument:
        prt     -- log file from DCPROGS as a single string
    Keyword Argument :
        prog    -- choose program 'HJCFIT' (default) or 'SCALCS'
        
    Return --  text string of rates in mechanism
            -- the number of open states as an integer
    '''
    open_text = "Number of open states"
    
    if prog == 'Win_HJCFIT':
        
        top = "Simplex used log(rate constant) for searching"
        bottom = "Equilibrium constants calculated for fitted rate constants"
        last_bit = "initial        final"

    elif prog == 'SCALCS':
        
        top = "Values of rate constants"
        bottom = "Equilibrium constants calculated from these rate constants"
        last_bit = "calculated by microscopic rev"
    
    if prt.find(open_text) != -1:
        a = prt.index(open_text)
        b = len(open_text)
        number_open_states = int(prt[a+b+2:a+b+6])
        print open_text,':', number_open_states

    else:
        number_open_states = int(raw_input("Didn't find the number of open states, how many?"))

    #loop until all examples are gone
    while prt.find(top) != -1:

        #find index of "Simplex used log(rate constant) for searching"
        a = prt.index(top)
        #remove everything before this phrase, and the phrase itself
        prt = prt[a+len(top):]

    #loop until all examples are gone
    while prt.find(bottom) != -1:

        #find index of "Equilibrium constants calculated for fitted rate constants"
        a = prt.index(bottom)
        #remove everything after this phrase and itself
        prt = prt[:a]
    
    a = prt.index(last_bit)
    prt = prt[a+len(last_bit):]     #slice off 'initial        final'

    return '   '+prt.strip(), number_open_states


def report (original_input, rates_in_dict_format):

    '''
    arguments   -- original input - a text string from the input file
                -- rates_in_dict_format - a dictionary of rates
    returns     -- nothing
    '''

    #print original_input

    print 'Rate Dict:\n----------\n'
    for key in rates_in_dict_format:
        print key,':', rates_in_dict_format[key]
    print "Number of rates : ", len(rates_in_dict_format)
    print "Number of states : ", number_of_states(rates_in_dict_format)
    
    #print '\ndone'

def number_of_states(rate_dictionary):
    '''
    find the number of states by querying a rate dictionary
    returns --
            number of states
    '''
    N_S = {}
    for key in rate_dictionary:
        #get initial state for all rates
        sn = key[0]
        #race to the top

        if N_S.has_key(sn) == False:  
        # Not strictly necessary, values of N_S dict would be overwritten
            N_S [sn] = None

    return len(N_S)


