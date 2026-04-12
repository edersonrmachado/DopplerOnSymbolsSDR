import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt

from packet_classes import LoraSamplesConfig
from packet_utils import read_samples, cut_samples
from packet_plots import plot_packet


# image folder (to be replaced)
image_folder="/home/ederson/Desktop/figures/" 
samples_file = "../data/f436sf11bw250cr5sr1M024.iq"

samples_cfg=LoraSamplesConfig(436e6,11,250E3,5,1.024E6)

if __name__ == '__main__':
    
    # read samples from file
    samples=read_samples(samples_file)
    
    # cut samples to show only interest zone
    cut_start=1627209 
    symbols_to_cut=31
    samples=cut_samples(samples_cfg,samples,cut_start,symbols_to_cut)
    
    
    plot_packet(samples_cfg, samples, image_folder)