import numpy as np
from scipy.fftpack import fft

from lora_classes import LoraSymbolConfig
from lora_modulator import generate_symbol
from lora_channel import generate_awgn
from lora_plots import plot_signals

# image folder (to be replaced)
image_folder="/home/ederson/Desktop/figures/" 

# symbol, spreading factor, bandwidth and sampling frequency [opt].
symbol_cfg = LoraSymbolConfig(10, 7, 125E3)  

if __name__ == '__main__':
    
    # generate a symbol
    x=generate_symbol(symbol_cfg.s,symbol_cfg.sf,symbol_cfg.bw,symbol_cfg.fs)
    
    # generate noise and add to the symbol
    r=generate_awgn(x,20) # vector, snr 
    y=(x+r)  
    
    # generate symbol 0 and its conjugate
    x0=generate_symbol(0,symbol_cfg.sf,symbol_cfg.bw,symbol_cfg.fs)
    x0_conj=np.conj(x0) 
    
    # dechirping
    dechirped=y*x0_conj 
    
    # fourier transform of dechirped signal
    fourier_transform=np.array(fft(dechirped)) 
    
    # argument (index) of power peak
    estimated_symbol = np.argmax(np.abs(fourier_transform))  
    
    # plot signals (comment to disable plot)
    plot_signals(symbol_cfg, x, y, x0_conj, dechirped, fourier_transform,estimated_symbol, image_folder)