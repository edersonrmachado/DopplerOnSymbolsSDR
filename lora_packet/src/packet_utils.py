import numpy as np 
import os

from packet_classes import LoraSamplesConfig

def read_samples(file_name):
    """Reads complex64 samples from a binary .iq file.

    Args:
        file_name (str): Path to the .iq file.
    Returns:
        np.ndarray: array of complex64 samples.
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"File not found!: {file_name}")
    
    samples = np.fromfile(file_name, dtype=np.complex64)
    return samples       

def cut_samples(samples_cfg,samples, cut_start,symbols_to_cut):
    """ Cut the samples to show only interested zone
        
        Args:
            samples_cfg (samples cfg class)
            samples (complex64): sample vector
            cut_start (int): inicial sample
            symbols_to_cut (int): number of symbols to show 
        Returns:
            samples (complex64): the sample vector sliced
    """
    symbol_period=2**samples_cfg.sf/samples_cfg.bw
    end_cut=cut_start+int(samples_cfg.fs*symbol_period*symbols_to_cut) 
    
    return samples[cut_start:end_cut]
     