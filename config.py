__author__="Andrew"
__date__ ="$18-Sep-2014 09:35:33$"
import cPickle as pickle
import time

## Here we have the default configuration parameters for input to the aligator script

class ConfigIO:
    """create, read and write configuration files for the aligator script"""
    def __init__(self, Empty=False):
        #the defaults
        if Empty:
            #just a shell to get 'read_config' method to load a file    
            pass
            #Empty ConfigIO object created.
        else:
            self.populate_defaults()
                   
    def populate_defaults(self):    
        
        timestr = time.strftime("%y%m%d-%H%M%S") 
        
        #metadata
        self.created_timestamp = timestr
        self.working_directory = "/users/andrew/desktop/aligator trials"
        
        #this filename will be used to save the configuration 
        self.config_filename = "aligator_defaults.txt"
        self.description = "Default simulation parameter config file"
        
        #modify filename with project suffix if you want
        self.mod = "_CP_stg"
        #simulator params
        self.mech_list=['3KA', '4KA', '3','4']
        self.expt_list=["jumpfamily" ]
        self.rate=["d2_min", "d2op_min"]         #must be a list  
        self.power = [1, .7]
        self.v_range = 1.5
        self.pair_expt = False
        self.last_saved_timestamp = "Never"
        
        message = "ConfigIO object populated with Aligator default values."
        return message
    
    def clear_config(self, Verbose=False):
        
        message = None
        attributes = self.__dict__.keys()
        for k in attributes:
            delattr (self, k)
        
        if Verbose:
            message = "cleared attributes: " + str (attributes)
        
        return message
        
    def write_config(self, filename=None, Override=False, Verbose=False):
        
        if len (self.__dict__) == 0 and Override == False:
            if Verbose: message = "Config is empty, not saving (use keyword Override=True to save, and include a 'filename=Str' argument)"
            return message
        
        elif len (self.__dict__) == 0 and not isinstance(filename, basestring):
            if Verbose: message =  "Config is empty, can't save anything without a 'filename=Str' argument"
            return message
        
        else:    
            timestr = time.strftime("%y%m%d-%H%M%S") 
            self.last_saved_timestamp = timestr

            # if a meaningful new filename was supplied, update the configuration file to reflect that.
            # skipped by default
            if isinstance(filename, basestring): 
                self.config_filename = filename 
                message = "Updated ConfigIO object filename to {0} \n".format(self.config_filename)
            
            else:
                message = "No useable filename supplied.\n" 
                
             
            with open(self.config_filename,'wb') as fp:
                pickle.dump(self.__dict__, fp)
            
            message += "Wrote " + str(self.config_filename)  
            return message
            
    def read_config(self, filename, Verbose=False):
        message = None
        
        if not isinstance(filename, basestring):
            return "Error: filename supplied is not a string. Nothing done."
        
        with open(filename,'rb') as fp:
            self.__dict__ = pickle.load (fp)
            
        if hasattr(self, "config_filename") == False:
            message = "No filename found within config file, fixing..."
            self.config_filename = filename
            
        message = "Read file: {0} with internal filename record {1}".format(filename, self.config_filename)    
        
        if Verbose:
        
            if hasattr(self, "description"):
                message += "\n" + str(self.description)
            else:
                message += "\n" + "No description found."

            if hasattr(self, "created_timestamp"):
                message += "\n" + "created" + str(self.created_timestamp)
            else:
                message += "\n" + "No information about creation time or date."

            if hasattr(self, "last_saved_timestamp"):
                message += "\n" + "Last saved: " + str(self.last_saved_timestamp)
            else:
                message += "\n" + "No information about last save."
                
            message += "\n" + "Number of parameters (Tip: 2 indicates an empty file) : " + str(len(self.__dict__))
            
        return message