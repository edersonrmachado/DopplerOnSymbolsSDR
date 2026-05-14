import numpy as np
from scipy.fftpack import fft



from doppler_simulation_batch import run_test_multiple_times

from lora_classes import LoraSymbolConfig
from doppler_utils import *


# image folder (to be replaced)
image_folder="/home/ederson/Desktop/figures/" 
fft_file="../data/fft_mag.txt" 

# symbol, spreading factor, bandwidth, freq  and sampling frequency [opt].
symbol_cfg = LoraSymbolConfig(512, 11, 125E3,436.9e6)  

# sat altitude, transmission time, and analysis duration
SAT_ALTITUDE = 550e3
TX_TIME= 0 
TIME_INTERVAL=60
NUMBER_OF_SYMBOLS=260
NUM_BINS_AROUND_SYMBOL=10
NUMBER_OF_EXPERIMENTS=5

if __name__ == '__main__':
    
    # creates time vector
    resolution=0.001
    time_vec = np.arange(-TIME_INTERVAL/2, (TIME_INTERVAL/2)+resolution, resolution)
    
    # generate relative doppler shift vector in ppm
    rel_doppler_shift_vec=relative_doppler_shift(SAT_ALTITUDE,time_vec) 
    
    # doppler shift at tx_time [Hz]
    doppler_shift=relative_doppler_shift(SAT_ALTITUDE,TX_TIME)*symbol_cfg.f
    print(f"Doppler shift in Hz: {doppler_shift:.0f}")
    
    # generate relative doppler rate vector [dimensionless]
    rel_doppler_rate_vec=np.gradient(rel_doppler_shift_vec,time_vec)
   
    # doppler rate Hz/s at tx_time
    doppler_rate_tx=find_doppler_rate(TX_TIME, rel_doppler_rate_vec, time_vec)*symbol_cfg.f
    print(f"Doppler rate in Hz/s: {doppler_rate_tx:.2f}")
        

    
    fft_abs_matrix, estimated_symbol_list, first_error_vec, periodicity_vec=run_test_multiple_times(NUMBER_OF_EXPERIMENTS,symbol_cfg, NUMBER_OF_SYMBOLS, doppler_shift, doppler_rate_tx,fft_file)
    
    
    #fft_abs_matrix,estimated_symbol_list=
    
    #run_test_multiple_times(NUMBER_OF_EXPERIMENTS,symbol_cfg, NUMBER_OF_SYMBOLS, doppler_shift, doppler_rate_tx,fft_file)
   
    
    #print(len(fft_abs_matrix[0]))
    #print((estimated_symbol_list))
    
    
    print(f"Periodicity mean: {np.mean(periodicity_vec)}")
    print(f"First error mean: {np.mean(first_error_vec)}")