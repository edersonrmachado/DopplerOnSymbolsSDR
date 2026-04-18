import numpy as np
from scipy.fftpack import fft


# Earth's radius [m], gravity acc. [m/s^2] and lightspeed [m/s]
#EARTH_RADIUS = 6378137     
EARTH_RADIUS = 6371000     

GRAVITY = 9.80665     
LIGHTSPEED = 299792458   


def relative_doppler_shift(H,t):
    """
    Calculate rel. doppler shift according to simplified equation.

    Args:
        H (float): satellite altitude in meters.
        t (np.ndarray): time relative to the zenith vector [seconds].

    Returns:
        rel_doppler_shift (np.ndarray): relative doppler shift [dimensionless]. 
    """
    
    rel_doppler_shift=1/(1+((1/LIGHTSPEED)*np.sqrt((GRAVITY*EARTH_RADIUS)/(1+H/EARTH_RADIUS)))*(np.sin((np.sqrt(GRAVITY / EARTH_RADIUS) / (1 + H / EARTH_RADIUS) ** (3 / 2)) * t)/np.sqrt((1+H/EARTH_RADIUS)**2-2*(1+H/EARTH_RADIUS)*np.cos((np.sqrt(GRAVITY / EARTH_RADIUS) / (1 + H / EARTH_RADIUS) ** (3 / 2)) * t)+1)))-1
  
    return rel_doppler_shift

def relative_doppler_rate_vec(rel_doppler_shift,dt): 
    """Calculate relative Doppler rate."""
    return np.gradient(rel_doppler_shift, dt)

def find_doppler_rate(tx_time, rel_doppler_rate_vec, time_vec):
    """Find the approx. doppler rate value at tx_time from doppler rate vector."""
    time_index = np.abs(time_vec - tx_time).argmin()
    return rel_doppler_rate_vec[time_index]

def estimate_symbol_with_doppler(symbol_cfg,tx_time,time_vec,rel_doppler_rate_vec,accum_doppler_shift_vec):
    """
    Estimate the symbol value. 
    
    Args:
        symbol_cfg (LoraSymbolConfig): symbol config.
        tx_time (int): time of transmission relative to zenith.
        time_vec (np.ndarray): the visibility window (float64) [sec].
        rel_doppler_rate_vec (np.ndarray): vec to search inst. dop. rate (float64).
        accum_doppler_shift_vec (list of float64): accum. values of doppler shift.
        
    Returns:
        fft_abs (np.ndarray): fft abs of the dem. symbol (float32).
        estimated_symbol (int64): estimated symbol. 
    """
    
    num_samples=2**symbol_cfg.sf
    sample=np.arange(0,num_samples)
    sample_period=1/symbol_cfg.bw 
    symbol_period=sample_period*num_samples
    doppler_rate=find_doppler_rate(tx_time,rel_doppler_rate_vec,time_vec)*symbol_cfg.f
    doppler_shift=sum(accum_doppler_shift_vec)
    y=np.exp(2*np.pi*1j*sample*((symbol_cfg.s/num_samples)+doppler_shift*sample_period+sample*doppler_rate*(sample_period**2)/2))
    y = y.astype(np.complex64) 
    accum_doppler_rate=doppler_rate*symbol_period
    accum_doppler_shift_vec.append(accum_doppler_rate)
    fft_abs=np.abs(np.array(fft(y)))   
    estimated_symbol = np.argmax(fft_abs)
    
    return fft_abs,estimated_symbol 
    

def evaluates_packet(symbol_cfg,num_of_symbols,tx_time,time_vec,rel_doppler_rate_vec):
    """
    Evaluate doppler impact on the packet.
    
    Args:
        symbol_cfg (LoraSymbolConfig): symbol config.
        num_of_symbols (int): the num of symbols in the packet.
        tx_time (int): time of transmission relative to zenith.
        time_vec (np.ndarray): the visibility window (float64) [sec].
        rel_doppler_rate_vec (np.ndarray): vec to search inst. dop. rate (float64).
    
    Returns:
        fft_abs_vec (np.ndarray): vec. of fft. abs. of all symbols (float32).
        estimated_symbol_vec (list of int64): vec. of all estimated symbol. 
    """
    
    fft_abs_vec=[]
    estimated_symbol_vec=[]
    fft_peak_values=[]
    symbol_idxs=[]
    accum_doppler_shift_vec=[]
    
    for symbol_idx in range(1,num_of_symbols+1):
        fft_abs, estimated_symbol= estimate_symbol_with_doppler(
            symbol_cfg,
            tx_time,
            time_vec,
            rel_doppler_rate_vec,
            accum_doppler_shift_vec,
        )
        
        fft_abs_vec.append(fft_abs)
        estimated_symbol_vec.append(estimated_symbol)
        symbol_idxs.append(symbol_idx)
    
    return np.array(fft_abs_vec),np.array(estimated_symbol_vec)