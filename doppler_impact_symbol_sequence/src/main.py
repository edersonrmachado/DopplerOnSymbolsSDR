import numpy as np
from scipy.fftpack import fft

from lora_classes import LoraSymbolConfig
from doppler_utils import relative_doppler_shift,relative_doppler_rate_vec,evaluates_packet, find_doppler_rate
from doppler_impact_plots import plot_doppler_impact

# image folder (to be replaced)
image_folder="/home/ederson/Desktop/figures/" 

# symbol, spreading factor, bandwidth, freq  and sampling frequency [opt].
symbol_cfg = LoraSymbolConfig(512, 11, 125E3,436.9e6)  

# sat altitude, transmission time, and analysis duration
SAT_ALTITUDE = 550e3
TX_TIME= 0 
TIME_INTERVAL=600
NUMBER_OF_SYMBOLS=60
NUM_BINS_AROUND_SYMBOL=10

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
    
    # calculate estimated symbols, fft_abs
    fft_abs_vec,estimated_symbol_vec=evaluates_packet(symbol_cfg,NUMBER_OF_SYMBOLS,TX_TIME,time_vec,rel_doppler_rate_vec)
    
    # plot
    plot_doppler_impact(symbol_cfg, fft_abs_vec,estimated_symbol_vec,NUM_BINS_AROUND_SYMBOL, image_folder)