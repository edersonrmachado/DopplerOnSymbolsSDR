import numpy as np
import matplotlib.pyplot as plt


# save the plots on `image_folder` if true
SAVE_PLOTS=True
LEGEND=True

# fig name
fig_1='freq_shift_symbol_impact.pdf'

def plot_freq_shift(fft_abs_vec, est_symb_vec,cfo_int_values,cfo_frac_values,m_values,image_folder):
    """Generate plots and save [opt].
    
    Args:
        fft_abs_vec (list of np.ndarray): list of ffts (complex64).
        est_symb_vec (list of np.ndarray): list of estimated symbols (int64).
        cfo_int_values (list of int): list of cfo_int values.
        cfo_frac_values (list of floats): list of cfo_frac values.
        m_values (list of floats): list of m values.
        image_folder: path to save figure.
    """

    # set plot  fonts
    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['font.family'] = 'STIXGeneral'
    
    # plots - customized style
    fig_facecolor='#FFFFFF'
    dpi_set=600
    fig_width=3.5
    fig_height=2.2
    fontsize_ticks=9.1 
    fontsize_leg=8
    fontsize_xy_labels=10 
    lwid_leg=1.5 
    lwid_plots=1
    
    # fig
    fig,ax=plt.subplots(figsize=(fig_width, fig_height),dpi=dpi_set,facecolor=fig_facecolor) 
    
    # legend config
    legend_title=r"     "+r"$CFO \ [Hz]$         $m$"
    legend_vec=[rf"${cfo_int_values[0]+cfo_frac_values[0]:5.1f}$"+r"                   "+rf"${m_values[0]:2.1f}$",
                rf"${cfo_int_values[1]+cfo_frac_values[1]:5.1f}$"+r"    "+rf"${m_values[1]:2.1f}$",
                rf"${cfo_int_values[2]+cfo_frac_values[2]:5.1f}$"+r"       "+rf"${m_values[2]:2.1f}$", 
                rf"${cfo_int_values[3]+cfo_frac_values[3]:5.1f}$"+r"             "+rf"${m_values[3]:2.1f}$",
                rf"${cfo_int_values[4]+cfo_frac_values[4]:5.1f}$"+r"         "+rf"${m_values[4]:2.1f}$"
    ]
    
    # plots
    ax.plot(fft_abs_vec[0],lw=lwid_plots, label=legend_vec[0])
    ax.plot(fft_abs_vec[1],lw=lwid_plots, label=legend_vec[1])
    ax.plot(fft_abs_vec[2],lw=lwid_plots, label=legend_vec[2])
    ax.plot(fft_abs_vec[3],lw=lwid_plots, label=legend_vec[3])
    ax.plot(fft_abs_vec[4],lw=lwid_plots, label=legend_vec[4])
    
    # add legend
    legend=ax.legend(
        loc='upper right', 
        bbox_to_anchor=(1.0, 1.0), 
        frameon=True, 
        edgecolor='#808080',
        facecolor='white', 
        fontsize=fontsize_leg,
        title_fontsize=fontsize_leg,
        handlelength=1,
        title=legend_title)
    for line in legend.get_lines():
        line.set_linewidth(lwid_leg) 

    # plot config
    x_ticks = np.concatenate(([0], est_symb_vec, [127]))
    ax.set_xticks(x_ticks)
    ax.set_ylabel(r'FFT modulus $ \left  | \ C[k] \ \right |$',fontsize=fontsize_xy_labels)
    ax.set_xlabel(r'$k$ samples',fontsize=fontsize_xy_labels)
    ax.tick_params(axis='x', labelsize=fontsize_ticks)  
    ax.tick_params(axis='y', labelsize=fontsize_ticks)  
    ax.set_xlim(0, 127)
    ax.grid()
        
    # save option
    if SAVE_PLOTS:
        plt.savefig(image_folder+fig_1,bbox_inches='tight') 
    
    plt.show()
    
    
    