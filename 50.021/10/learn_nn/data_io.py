'''
@author: Sebastian Bach
@maintainer: Sebastian Bach
@contact: sebastian.bach@hhi.fraunhofer.de
@date: 14.08.2015
@version: 1.0
@copyright: Copyright (c)  2015, Sebastian Bach, Alexander Binder, Gregoire Montavon, Klaus-Robert Mueller
@license : BSD-2-Clause
'''

import os
import numpy as np
import scipy.io as scio
na = np.newaxis


#--------------------
#   data reading
#--------------------

def read(path, fmt = None):
    '''
    Read [N x D]-sized block-formatted data from a given path.
    Supported data formats are
        plain text (ascii-matrices)
        numpy-compressed data (npy- or npz-files)
        matlab data files (mat-files)
    
    Parameters
    ----------
    
    path : str
        the path to the file to read
        
    fmt : str
        optional. if explicitly given, the file will be interpreted as mat, txt, npy or npz. elsewise, interpretation format will be inferred from the file name
        
        
    Returns
    -------
    
    data : numpy.ndarray
        
    '''
    
    if fmt is None: #try to infer format
        fmt = os.path.splitext(path)[1].replace('.','').lower()
    
    data = _read_as[fmt](path)
            
    return data
  

def _read_np(path):
    print 'loading np-formatted data from',path
    return np.load(path)


def _read_mat(path):
    print 'loading matlab formatted data from', path
    return scio.loadmat(path)['data']
    
    
def _read_txt(path):
    print 'loading plain text data from',path
    return np.loadtxt(path)

_read_as = {'npy':_read_np,\
            'npz':_read_np,\
            ''   :_read_np,\
            'mat':_read_mat,\
            'txt':_read_txt,\
            }


#--------------------
#   data writing
#--------------------


def write(data, path, fmt = None):
    '''
    Write [N x D]-sized block-formatted data to a given path.
    Supported data formats are
        plain text (ascii-matrices)
        numpy-compressed data (npy- or npz-files)
        matlab data files (mat-files)
    
    Parameters
    ----------
    
    data : numpy.ndarray
        a [N x D] - shaped, two-dimensional array of data.
    
    path : str
        the path to write the data to
        
    fmt : str
        optional. if explicitly given, the file will be written as mat, txt, npy or npz. elsewise, interpretation format will be inferred from the file name
                
    '''

    if fmt is None: #try to infer format
        fmt = os.path.splitext(path)[1].replace('.','').lower()
    
    _write_as[fmt](data,path)


def _write_np(data, path):
    print  'writing data in npy-format to',path
    np.save(path, data)

def _write_mat(data, path):
    print 'writing data in mat-format to',path
    scio.savemat(path, {'data':data}, appendmat = False)
    
def _write_txt(data, path):
    print 'writing data as plain text to',path
    np.savetxt(path, data)


_write_as = {'npy':_write_np,\
             'npz':_write_np,\
             ''   :_write_np,\
             'mat':_write_mat,\
             'txt':_write_txt,\
            }
