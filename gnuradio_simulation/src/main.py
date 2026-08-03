import numpy as np
from scipy.fftpack import fft

from lora_classes import LoraSymbolConfig
from doppler_utils import *
from doppler_impact_plots import plot_doppler_impact
from doppler_gnu_simulation import doppler_simulation

# image folder (to be replaced)
image_folder="/home/ederson/Desktop/figures/" 
fft_file="../data/fft_mag.txt" 

# symbol, spreading factor, bandwidth, freq  and sampling frequency [opt].
symbol_cfg = LoraSymbolConfig(512, 11, 125E3,436.9e6)  

# sat altitude, transmission time, and analysis duration
SAT_ALTITUDE = 550e3
TX_TIME= 0 
TIME_INTERVAL=60
NUMBER_OF_SYMBOLS=68
NUM_BINS_AROUND_SYMBOL=10
NUMBER_OF_EXPERIMENTS=1

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
    
    # run gnuradio simulation
    print("\033[92m\nRunning gnuradio simulation...\033[0m")
    simulator= doppler_simulation(symbol_cfg, NUMBER_OF_SYMBOLS, doppler_shift, doppler_rate_tx,fft_file)
    simulator.start()
    simulator.wait()
    print("\033[92m\nSimulation finished.\n\033[0m")

    # calculate estimated symbols, fft_abs
    fft_abs_vec,estimated_symbol_vec = read_fft_file(fft_file)
    
    # plot
    plot_doppler_impact(symbol_cfg, fft_abs_vec,estimated_symbol_vec,NUM_BINS_AROUND_SYMBOL, image_folder)
    