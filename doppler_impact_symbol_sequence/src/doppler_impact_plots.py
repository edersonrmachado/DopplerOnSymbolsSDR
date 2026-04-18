import numpy as np
import matplotlib.pyplot as plt


# save the plots on `image_folder` if true
SAVE_PLOTS=True

# fig name
fig_1='errors_occurance.pdf'

def plot_doppler_impact(symbol_cfg, fft_abs_vec,estimated_symbol_vec, num_bins_around_symb, image_folder):
    """Generate plots and save [opt].
    
    Args:
        symbol_cfg (LoraSymbolConfig): symbol config.
        fft_abs_vec:  (dtype=complex128).
        y (np.ndarray): symbol with noise (dtype=complex128).
        num_bins_around_symb (int): limitates the FFT slice to show. 
        image_folder (str): to save figures.  
    """
    
    # set plot fonts
    plt.rcParams['mathtext.fontset'] = 'stix' 
    plt.rcParams['font.family'] = 'STIXGeneral'
    
    # number of samples, samples and symbol idx for plot
    num_samples=2**symbol_cfg.sf
    samples=np.arange(0,num_samples) 
    symbol_idx=list(range(1,len(fft_abs_vec)+1))
  
    # plots - customized style
    fig_width=2.2
    fig_height=2
    fig_facecolor=None 
    dpi_set=600
    fft_color='seagreen'
    lwid_plots=0.8
    alpha_value=0.7
    pad_xtick=-4.5
    pad_ytick=-4.8
    pad_ztick=-4.5
    pad_ylabel=-10
    pad_xlabel=-8
    pad_zlabel=-13
    fontsize_ticks=6.5
    fontsize_label_titles=7.3
    no_error_ytick_step=20
        
    # fig. 1 3d plot symbol sequence demodulation
    fig1=plt.figure(figsize=(fig_width, fig_height),dpi=dpi_set,facecolor=fig_facecolor) 
    ax = fig1.add_subplot(1, 1, 1, projection='3d')
    ax.view_init(azim=-45, elev=35)
    
    # normalize fft abs amplitude 
    fft_abs_vec=fft_abs_vec/(num_samples-1)
    
    # cut samples and fft abs vec to highlight only interest region 
    cut_fft_abs_vec = []
    for item in fft_abs_vec:
        cut_fft_abs = item[symbol_cfg.s-num_bins_around_symb:symbol_cfg.s+num_bins_around_symb+1]
        cut_fft_abs_vec.append(cut_fft_abs)
    cut_fft_abs_vec=np.array(cut_fft_abs_vec)
    cut_samples=samples[symbol_cfg.s-num_bins_around_symb:symbol_cfg.s+num_bins_around_symb+1]
    
    # vectors to indicate error positions  
    one_shift_error_symbol_idxs=[]
    one_shift_error_symbol_values=[]
    xticks_vec=[cut_samples[0],symbol_cfg.s,cut_samples[-1]]
    
    # plot
    last_estimated_symbol=symbol_cfg.s
    for i in range(len(fft_abs_vec)):
        if last_estimated_symbol!=estimated_symbol_vec[i]:
            ax.plot(cut_samples,cut_fft_abs_vec[i], zs=1+i, zdir='y', color='red',linestyle='-',lw=lwid_plots, zorder=3)
            last_estimated_symbol=estimated_symbol_vec[i]
            one_shift_error_symbol_values.append(last_estimated_symbol)
            one_shift_error_symbol_idxs.append(i+1)
            xticks_vec.append(last_estimated_symbol)
        else:
            ax.plot(cut_samples,cut_fft_abs_vec[i], zs=1+i, zdir='y', color=fft_color,linestyle='-',lw=lwid_plots,alpha=alpha_value)
    xticks_vec.sort()
    ax.set_xticks(xticks_vec)
        
    # plot ticks values in red if errors, otherwise black
    if len(one_shift_error_symbol_idxs) > 0:
        ax.set_yticks([1, *one_shift_error_symbol_idxs, len(symbol_idx)])
        yticks = ax.get_yticks()
        yticks_labels = ax.get_yticklabels()
        xticks = ax.get_xticks()
        xticks_labels = ax.get_xticklabels()
        # red color on one shift error
        for i in range(len(yticks)):
            if int(yticks[i]) in one_shift_error_symbol_idxs:
                yticks_labels[i].set_color('red')
        for i in range(len(xticks)):
            if int(xticks[i]) in one_shift_error_symbol_values:
                xticks_labels[i].set_color('red')
    else:
        yticks_vec = [1,len(symbol_idx)]
        for i in range(no_error_ytick_step, len(symbol_idx) + 1,no_error_ytick_step):
            yticks_vec.append(i)
            yticks_vec = sorted(set(yticks_vec))
        ax.set_yticks(yticks_vec)
        
    # customize annotation
    ax.set_zlim3d([0,1])
    ax.set_zticks([0,1]) 
    ax.set_xlabel(r'k-samples',fontsize=fontsize_label_titles, labelpad=pad_xlabel)
    ax.set_ylabel(r'p symbol',fontsize=fontsize_label_titles,labelpad=pad_ylabel)
    ax.tick_params(axis='x', labelsize=fontsize_ticks,pad=pad_xtick)  
    ax.tick_params(axis='y', labelsize=fontsize_ticks,pad=pad_ytick)  
    ax.tick_params(axis='z', labelsize=fontsize_ticks,pad=pad_ztick)      
    ax.set_zlabel(r"Normalized"+ "\n" +r"FFT $ \left | \tilde{C}[k,p] \right | $",fontsize=fontsize_label_titles,labelpad=pad_zlabel)
    ax.set_xticklabels([]) 
    
    # customize x-axis view
    red_tick_start=((symbol_cfg.s-xticks_vec[0])/2)+xticks_vec[0]
    red_ticks_dist=(symbol_cfg.s-red_tick_start)/(len(one_shift_error_symbol_values))
    i=0
    for tick in xticks_vec:
        if tick != xticks_vec[0] and tick != xticks_vec[-1] and tick != symbol_cfg.s:
            ax.text(x=(red_tick_start+red_ticks_dist*i), y=ax.get_ylim()[0]+pad_xtick+1, z=ax.get_zlim()[0], 
            s=str(tick), ha='right', va='top',fontsize=fontsize_ticks,color='red')
            i=i+1
        else:
            ax.text(x=tick, y=ax.get_ylim()[0]+pad_xtick+1, z=ax.get_zlim()[0], 
                s=str(tick), ha='right', va='top',fontsize=fontsize_ticks)
        
    # plot tick indicator in red (error symbols)
    xticks = ax.get_xticks()
    yticks = ax.get_yticks()
    for tick_obj, tick_val in zip(ax.xaxis.get_major_ticks(), xticks):
        if tick_val in one_shift_error_symbol_values:
            tick_obj.tick1line.set_color('red')
            tick_obj.tick2line.set_color('red')
    for tick_obj, tick_val in zip(ax.yaxis.get_major_ticks(), yticks):
        if tick_val in one_shift_error_symbol_idxs:
            tick_obj.tick1line.set_color('red')
            tick_obj.tick2line.set_color('red')
    
    # adjust fig size
    left=0.01
    bottom=0.05
    width=0.85
    height=0.9
    ax.set_position([left, bottom, width, height])
    
    # save option
    if SAVE_PLOTS:   
        plt.savefig(image_folder+fig_1)
    
    # show plot
    plt.show()