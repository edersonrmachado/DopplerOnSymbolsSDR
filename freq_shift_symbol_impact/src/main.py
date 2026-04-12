import numpy as np
from scipy.fftpack import fft

from lora_classes import LoraSymbolConfig
from freq_shift_utils import analytical_dechirping
from freq_shift_plots import plot_freq_shift

# image folder (to be replaced)
image_folder="/home/ederson/Desktop/figures/" 

# symbol, spreading factor, bandwidth.
symbol_cfg = LoraSymbolConfig(50, 7, 125E3)  


if __name__ == '__main__':
    
    # carrier frequency offset values and vector instantiation
    cfo_int_values=[0,-14340, -6403,7292,14008]
    cfo_frac_values=[0.0,-0.4,-0.6,0.7,0.5]
    m_values=[]
    fft_abs_vec=[]
    est_symb_vec=[]
    
    # calculates ffts, estimated symbols and m values
    for i in range(len(cfo_int_values)):
        # analytical dechirping and m_values
        analytical_dec, m_value = analytical_dechirping(symbol_cfg,cfo_int_values[i],cfo_frac_values[i])
        
        # fourier transform
        fft_abs=np.abs(np.array(fft(analytical_dec)))   
        
        # estimated symbol
        estimated_symbol = np.argmax(fft_abs)   
        
        # append to vectors
        m_values.append(m_value)
        fft_abs_vec.append(fft_abs)
        est_symb_vec.append(estimated_symbol)

    # plot and save [opt]
    plot_freq_shift(fft_abs_vec, est_symb_vec,cfo_int_values,cfo_frac_values,m_values,image_folder)
    
    
    