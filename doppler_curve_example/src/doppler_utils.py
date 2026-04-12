import numpy as np


# Earth's radius [m], gravity acc. [m/s^2] and lightspeed [m/s]
EARTH_RADIUS = 6378137     
GRAVITY = 9.80665     
LIGHTSPEED = 299792458   


def relative_doppler_shift(H,t):
    """Calculate relative doppler shift according to simplified equation

    Args:
        H (float): satellite altitude in meters.
        t (np.ndarray): time relative to the zenith vector [seconds].

    Returns:
        np.ndarray: relative doppler shift [ppm]. 
    """
    
    rel_doppler_shift=1/(1+((1/LIGHTSPEED)*np.sqrt((GRAVITY*EARTH_RADIUS)/(1+H/EARTH_RADIUS)))*(np.sin((np.sqrt(GRAVITY / EARTH_RADIUS) / (1 + H / EARTH_RADIUS) ** (3 / 2)) * t)/np.sqrt((1+H/EARTH_RADIUS)**2-2*(1+H/EARTH_RADIUS)*np.cos((np.sqrt(GRAVITY / EARTH_RADIUS) / (1 + H / EARTH_RADIUS) ** (3 / 2)) * t)+1)))-1
  
    return rel_doppler_shift*1e6

def relative_doppler_rate(rel_doppler_shift,dt): 
    '''Calculate relative Doppler rate ppm/s'''
    return np.gradient(rel_doppler_shift, dt)