import numpy as np
from scipy.fftpack import fft

from classes import LoraSymbolConfig
from lora_modulator import generate_symbol
from lora_channel import generate_awgn
from lora_plots import plot_signals


# image folder (to be replaced)
image_folder="/home/ederson/Desktop/figures/" 
# symbol, spreading factor, bandwidth and sampling frequency [opt].
symbol_cfg = LoraSymbolConfig(10, 7, 125E3)  

if __name__ == '__main__':
    
    # create a symbol
    x=generate_symbol(symbol_cfg.s,symbol_cfg.sf,symbol_cfg.bw,symbol_cfg.fs)
    # add noise to the symbol
    r=generate_awgn(x,20) # vector, snr 
    y=(x+r)  
    # generates symbol s=0
    x0=generate_symbol(0,symbol_cfg.sf,symbol_cfg.bw,symbol_cfg.fs)
    # generates conjugate of s=0
    x0_conj=np.conj(x0) 
    # dechirping
    dechirped=y*x0_conj 
    # fourier transform of dechirped signal
    fourier_transform=np.array(fft(dechirped)) 
    # argument(index) of power peak
    estimated_symbol = np.argmax(np.abs(fourier_transform))  
    # plot signals 
    plot_signals(symbol_cfg, x, y, x0_conj, dechirped, fourier_transform,estimated_symbol, image_folder)