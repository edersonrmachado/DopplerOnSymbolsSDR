import numpy as np 

from lora_classes import LoraSymbolConfig


def analytical_dechirping(symbol_cfg,cfo_int,cfo_frac):
    """Applies analytical dechirping 

    Args:
        symbol_cfg (LoraSymbolConfig): symbol config.
        cfo_int (int): carrier frequency offset integer part.
        cfo_frac (float): carrier frequency offset fractional part.
    Returns:
        analytical_dec (np.ndarray): analytical dechirp. vector (np.complex64)
        m_value (np.ndarray): m value (int64) 
    """
    num_samples=2**symbol_cfg.sf
    sample=np.arange(0,num_samples)
    sample_period=1/symbol_cfg.bw
    # applies equation
    analytical_dec=np.exp(2*np.pi*1j*sample*( (symbol_cfg.s)/num_samples) ) * np.exp(2*np.pi*1j*sample*( ((cfo_int+cfo_frac)*sample_period)))
    m_value=(cfo_int+cfo_frac)*num_samples*sample_period
    
    return analytical_dec.astype(np.complex64), m_value