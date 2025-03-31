# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Andrew"
__date__ = "$17-Jun-2018 21:04:39$"

import numpy as np

#set up changing conductances across experiments as a matrix
#gamma_ij where i is the experiment and j is the Q matrix state

class ConductMat:
    
    def __init__ (self, N_expt, N_states):
        """initialising conductance matrix"""
        #each state for which the conductance should change is then a column of values 
        self.g_mat = np.zeros(shape = (N_expt, N_states))
        self.N_expt = int(N_expt)
        self.N_states = int(N_states)

    def get_open_states(self, expt):
        #make a dictionary of the conductances for the given experiment
        #open states always low numbered following DC's convention? 
        _open_states = {}
        
        i = expt
        for j in range (self.N_states):
            if self.g_mat[i,j] > 0 :
                _open_states[j] = self.g_mat[i,j]
            
        return _open_states
    
    def add_constant_g_vec(self, state, conductance):
        #write column vector of constant conductance into matrix
        self.g_mat[:, state] = conductance
    
    def add_range_g_vec(self, state, g_high, g_low=0):
        #make list of conductances
        conductance_column = np.linspace(g_low, g_high, self.N_expt)
        #write into matrix
        self.g_mat[:, state] = conductance_column
        