__author__ = "Andrew"
__date__ = "$06-Jun-2017 20:55:48$"

import sys

class Logger(object):
    # redirect stdout (and thus print() function) to logfile *and* terminal
    # http://stackoverflow.com/a/616672
    # and
    # http://mail.python.org/pipermail/python-list/2007-May/438106.html
    
    def __init__(self, logfilename):
        self.file = open(logfilename, "a")
        self.stdout = sys.stdout
        sys.stdout = self
        #print ("Log begins")
    
    def close(self):
         if self.stdout is not None:
             sys.stdout = self.stdout
             self.stdout = None
         if self.file is not None:
             self.file.close()
             self.file = None
             
    def write(self, data):
         self.file.write(data)
         self.stdout.write(data)
         
    def flush(self):
         self.file.flush()
         self.stdout.flush()
         
    def __del__(self):
         self.close()
