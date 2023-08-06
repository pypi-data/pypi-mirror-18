# Copyright (C) 2016 Joseph B. Bak-Colema
#This software may be modified and distributed under the terms of the MIT 
#license. See the LICENSE file for details
from __future__ import division, print_function, absolute_import
import h5py
import numpy as np

def read_field(path, field, subdir='fields'):
    """
    Returns a specified field from a fovea output (.h5) file
    
    Parameters
    ----------
    path : str
        The absolute or relative path to the specified datafile
    field : str
        The name of the specific field
    subdir : str, default is 'field'
        The h5 subdirectory where the field is found. Usual output
        is found in 'field'
    """
    hf = h5py.File(path)
    flist = hf[subdir] #Get a list of fields
      
    val_return = np.empty(flist[field].shape)#Create empty np array
    
    flist[field].read_direct(val_return) #Store in numpy array
    hf.close() #Close File

    return val_return

def view_fields(path,subdir='fields'):
    """
    Returns a list of all fields contained within a fovea output
   
    path : str
        The absolute or relative path to the specified file (.h5)
    subdir : str, default 'fields'
        Where in the file all fields of interest are found
    """

    hf = h5py.File
    hf = h5py.File(path)
    flist = hf[subdir]
    flist = [item for item in flist]
    
    return flist

def count_fish(path,check='x',idx=0):
    """
    Returns the number of fish in a foveator file
    path : str
        The absolute or relative path to the specified datafile (.h5)
    check : str, default 'x'
        Which field to check for number of fish
    idx : int, default 0
        Which axis of check indicates the correct number of fish. 
    """
    
    test_dat = read_field(path, check)
    return np.shape(test_dat)[0]

def count_frames(path, check='x',idx=0):
    """
    Returns the number of frames in a foveator file
    path : str
        The absolute or relative path to the specified datafile (.h5)
    check : str, default 'x'
        Which field to check for the length of the file
    idx : int, default 0
        Which axis of check indicates the correct number of fish. 
    """

    test_dat = read_field(path, check)
    return np.shape(test_dat)[1]


