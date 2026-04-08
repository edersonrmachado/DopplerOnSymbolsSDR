import numpy as np

from doppler_utils import relative_doppler_shift,relative_doppler_rate
from doppler_plots import plot_doppler

# image folder (to be replaced)
image_folder="/home/ederson/Desktop/figures/" 

SAT_ALTITUDE=500000
TIME_INTERVAL=300 

if __name__ == '__main__':
    
    # creates time vector
    num_points=100000
    time_vec = np.linspace(-TIME_INTERVAL, TIME_INTERVAL, num_points)
    dt=time_vec[1]-time_vec[0] 
    
    # generate relative doppler shift vector in ppm
    rel_doppler_shift=relative_doppler_shift(SAT_ALTITUDE,time_vec) 
    
    # generate relative doppler rate vector in ppm/s
    rel_doppler_rate=relative_doppler_rate(rel_doppler_shift,dt) 
    
    # plot relative doppler shift and rate
    plot_doppler(rel_doppler_shift,rel_doppler_rate,time_vec, image_folder)