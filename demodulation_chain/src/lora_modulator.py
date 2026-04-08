import numpy as np

from classes import LoraSymbolConfig

def generate_symbol(s,sf,bw,fs): 
    """ 
    Generate a LoRa symbol
    
    Args:
        s (int): symbol.
        sf (int): spreading factor.
        bw (float): bandwidth in Hz.
        fs (float): sampling frequency samples/s.
    Returns:
        np.narray[complex]: `symb_vec`, the complex samples of a lora symbol 
    """
    
    # number of samples and sampling period
    num_samples=2**sf 
    ts=1/fs 
    
    # adjust num_samples with fs and calculates inversion point
    num_samples=int(num_samples*fs/bw) 
    sample_lim=int((num_samples-s)*(fs/bw)) 
    
    # symbol vector generation
    symb_vec=[]
    for n in range(num_samples):
        if 0<=n<sample_lim:
            sample=np.exp(2*np.pi*1j*(((bw*ts*n)**2)/(2*num_samples)+(s/num_samples-1/2)*n*ts*bw)) 
        elif sample_lim<=n<num_samples:
            sample=np.exp(2*np.pi*1j*(((bw*ts*n)**2)/(2*num_samples)+(s/num_samples-3/2)*n*ts*bw))
        symb_vec.append(sample)
    return np.array(symb_vec) 