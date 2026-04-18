import numpy as np
import matplotlib.pyplot as plt

from lora_utils import normalized_frequency

# save the plots on `image_folder` if true
SAVE_PLOTS=True

def plot_signals(symbol_cfg, x, y, x0_conj,dechirped, fourier_transform,estimated_symbol, image_folder):
    """
    Generate plots and save [opt].
    
    Args:
        symbol_cfg (LoraSymbolConfig): symbol config.
        x (np.ndarray): entry symbol (dtype=complex128).
        y (np.ndarray): symbol with noise (dtype=complex128).
        x0_conj (np.ndarray): conjugate of s=0 (dtype=complex128).
        dechirped (np.ndarray): dechirped symbol (dtype=complex128).
        fourier_transform (np.ndarray): final FFT (dtype=complex128). 
        estimated_symbol (np.int64): estimated symbol.      
        image_folder (str): to save figures.  
    """
    
    # fig names
    fig_1='fig1.svg'
    fig_2='fig2.svg'
    fig_3='fig3.svg'
    fig_4='fig4.svg'
        
    # calculates normalized frequency of x, y, x0_conj and dechirped sig.
    freq_normal_x=normalized_frequency(x,symbol_cfg.bw, symbol_cfg.fs)
    freq_normal_y=normalized_frequency(y,symbol_cfg.bw,symbol_cfg.fs) 
    freq_normal_x0_conj=normalized_frequency(x0_conj,symbol_cfg.bw, symbol_cfg.fs) 
    freq_normal_dec=normalized_frequency(dechirped,symbol_cfg.bw, symbol_cfg.fs)
    
    # number of samples adjustment with fs for plots
    num_samples=2**symbol_cfg.sf 
    num_samples=int(num_samples*symbol_cfg.fs/symbol_cfg.bw) 
    n_samples=num_samples
    
    # plots - customized style
    fig_width=3.5
    fig_height=6.2
    fig_facecolor="#F7F7F7"
    dpi_set=600
    fontsize_xticks=23
    lwid_plots=3.5
    border_width=1.5
    pad_xlabel=-20
    pad_ylabel=10
    fontsize_xlabel=25
    fontsize_ylabel=26
    marker_size=7.5
    fontsize_yticks=24
    vert_space_plots=0.34
    fontsize_yticks_bw=28
    pad_ylabel_fft=3
    
    # fig. 1 modulated symbol x[n]
    fig1=plt.figure(figsize=(fig_width, fig_height),dpi=dpi_set,facecolor=fig_facecolor) 
    
    # freq x[n]
    ax = fig1.add_subplot(2, 1, 1)
    ax.set_yticks([-0.5,  0.5])
    ax.set_yticklabels(['-'+r'$\frac{B}{2}$',r'$\frac{B}{2}$'],fontsize=fontsize_yticks_bw)
    ax.set_xticks([0,n_samples-1])
    ax.set_xticklabels([0,n_samples-1],fontsize=fontsize_xticks)
    ax.set_ylabel('Frequency',fontsize=fontsize_ylabel,labelpad=pad_ylabel)
    ax.set_xlabel('n samples',labelpad=pad_xlabel,fontsize=fontsize_xlabel)
    ax.plot(freq_normal_x, marker='o',markersize=marker_size)
    
    # border width
    for spine in ax.spines.values():
        spine.set_linewidth(border_width)
    
    # real imag x[n] 
    ax = fig1.add_subplot(2, 1, 2)
    ax.set_yticks([-1, 1])  
    ax.set_yticklabels([-1,1],fontsize=fontsize_xticks)
    ax.set_xticks([0,n_samples-1])
    ax.set_xticklabels([0,n_samples-1],fontsize=fontsize_xticks)
    ax.set_xlabel('n samples',labelpad=pad_xlabel,fontsize=fontsize_xlabel)
    ax.set_ylabel('Amplitude',fontsize=fontsize_ylabel,labelpad=pad_ylabel)
    ax.plot(np.real(x),label='Real',lw=lwid_plots)
    ax.plot(np.imag(x),label='Imag.',color="lightcoral",lw=lwid_plots)
    
    # border width
    for spine in ax.spines.values(): 
        spine.set_linewidth(border_width)  
    fig1.subplots_adjust(hspace=vert_space_plots)
    
    # save option
    if SAVE_PLOTS:
        plt.savefig(image_folder+fig_1,bbox_inches='tight') 
    
    # fig. 2 symbol with noise y[n]
    fig2=plt.figure(figsize=(fig_width, fig_height),dpi=300,facecolor=fig_facecolor) 
    
    #  freq y[n] 
    ax = fig2.add_subplot(2, 1, 1)
    ax.set_yticks([-0.5,  0.5])
    ax.set_xticks([0,n_samples-1])
    ax.set_xticklabels([0,n_samples-1],fontsize=fontsize_xticks)
    ax.set_yticklabels(['-'+r'$\frac{B}{2}$',r'$\frac{B}{2}$'],fontsize=fontsize_yticks_bw)
    ax.set_xlabel('n samples',labelpad=pad_xlabel,fontsize=fontsize_xlabel)
    ax.plot(freq_normal_y, marker='o',markersize=marker_size)
    
    # border width
    for spine in ax.spines.values():
        spine.set_linewidth(border_width)
    
    # real imag y[n]
    ax = fig2.add_subplot(2, 1, 2)
    ax.set_yticks([-1, 1])  
    ax.set_yticklabels([-1,1],fontsize=fontsize_xticks)
    ax.set_xticks([0,n_samples-1])
    ax.set_xticklabels([0,n_samples-1],fontsize=fontsize_xticks)
    ax.set_xlabel('n samples',labelpad=pad_xlabel,fontsize=fontsize_xlabel)
    ax.plot(np.real(y),label='Real',lw=lwid_plots)
    ax.plot(np.imag(y),label='Imag.',color="lightcoral",lw=lwid_plots)
    for spine in ax.spines.values():
        spine.set_linewidth(border_width)  
    fig2.subplots_adjust(hspace=vert_space_plots)
    
    # save option
    if SAVE_PLOTS:
        plt.savefig(image_folder+fig_2,bbox_inches='tight') 
            
    # fig. 3 dechirped signal
    fig3=plt.figure(figsize=(fig_width, fig_height),dpi=300,facecolor=fig_facecolor) 
    
    #  freq dechirped
    freq_normal_dec = np.round(freq_normal_dec, 6)
    ax = fig3.add_subplot(2, 1, 1)
    ymin=-0.05
    ymax=1.05
    ax.set_ylim(ymin, ymax)
    ax.set_yticks([0, 1])
    ax.set_xticks([0,n_samples-1])
    ax.set_xticklabels([0,n_samples-1],fontsize=fontsize_xticks)
    ax.set_yticklabels(['0','B'],fontsize=fontsize_yticks)
    ax.set_xlabel('n samples',labelpad=pad_xlabel,fontsize=fontsize_xlabel)
    ax.plot(freq_normal_dec, marker='o',markersize=marker_size)
    
    # border width
    for spine in ax.spines.values():
        spine.set_linewidth(border_width)  
    
    # real imag dechirped
    ax = fig3.add_subplot(2, 1, 2)
    ax.set_yticks([-1, 1])  
    ax.set_yticklabels([-1,1],fontsize=fontsize_xticks)
    ax.set_xticks([0,n_samples-1])
    ax.set_xticklabels([0,n_samples-1],fontsize=fontsize_xticks)
    ax.set_xlabel('n samples',labelpad=pad_xlabel,fontsize=fontsize_xlabel)
    ax.plot(np.real(dechirped),label='Real',lw=lwid_plots)
    ax.plot(np.imag(dechirped),label='Imag.',color="lightcoral",lw=lwid_plots)
    
    # border width
    for spine in ax.spines.values():
        spine.set_linewidth(border_width)  
    fig3.subplots_adjust(hspace=vert_space_plots)
    
    # save option
    if SAVE_PLOTS:
        plt.savefig(image_folder+fig_3,bbox_inches='tight') 
        
    # fig 4 final FFT
    fig4=plt.figure(figsize=(fig_width, fig_height),dpi=300,facecolor=fig_facecolor) 
    
    ax = fig4.add_subplot(2, 1, 1)
    ax.set_yticks([ 0, 2**symbol_cfg.sf])
    ax.set_yticklabels([0,2**symbol_cfg.sf],fontsize=fontsize_yticks)
    ax.plot(np.abs(fourier_transform), marker='o',markersize=marker_size)
    ax.set_xticks([0,n_samples-1])
    ax.set_xticklabels([0,n_samples-1],fontsize=fontsize_xticks)
    ax.set_xlabel('k bins',labelpad=pad_xlabel,fontsize=fontsize_xlabel)
    ax.set_ylabel('Magnitude',labelpad=pad_ylabel_fft,fontsize=fontsize_ylabel)
    current_ticks = ax.get_xticks()
    new_tick = estimated_symbol  
    new_ticks = np.append(current_ticks, estimated_symbol)
    ax.set_xticks(new_ticks) 
    ax.set_xticks([0,estimated_symbol,n_samples-1])
    ax.set_xticklabels(['',estimated_symbol, n_samples-1],fontsize=fontsize_xticks)
    
    # border width
    for spine in ax.spines.values():
        spine.set_linewidth(border_width)  
    fig4.subplots_adjust(hspace=vert_space_plots)
    
    # save option
    if SAVE_PLOTS:
        plt.savefig(image_folder+fig_4,bbox_inches='tight') 
    
    # show plots
    plt.show()