import numpy as np
import matplotlib.pyplot as plt


# save the plots on `image_folder` if true
SAVE_PLOTS=True

# fig name
fig_1='packet_format.pdf'

def plot_packet(samples_cfg, samples, image_folder):
    """ 
    Generate plots and save [opt].
    
    Args:
        samples: complex64 samples vector.
        image_folder (str): to save figure.  
    """
    
    # set plot  fonts
    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['font.family'] = 'STIXGeneral'
    
    # plots - customized style
    fig_facecolor='#FFFFFF'
    dpi_set=600
    fig_width=3.5
    fig_height=1.15
    fontsize_ticks=9 
    fontsize_xy_labels=10
    fontsize_text=8 
    fontsize_text_num=7.5
    vert_line_color="grey"
    
    # fig
    fig,ax=plt.subplots(figsize=(fig_width, fig_height),dpi=dpi_set,facecolor=fig_facecolor) 
    
    # spectrogram 
    symbol_period=2**samples_cfg.sf/samples_cfg.bw
    samples_per_fft_block=256
    num_overlap_samples=0
    color_map='afmhot_r'
    plt.specgram(samples, NFFT=samples_per_fft_block, Fs=samples_cfg.fs ,noverlap=num_overlap_samples,vmin=-65,vmax=-35,cmap=color_map)

    # ticks
    plt.yticks(ticks=[samples_cfg.fs/-2, -125e3, 0,125e3, samples_cfg.fs/2], labels=['435.488M',r'$f_0-\frac{B}{2}$', r'$f_0$',r'$f_0 +\frac{B}{2}$', r'$436.512~MHz$'],fontsize=fontsize_ticks,fontweight='bold')
      
    # limits
    y_inf=-(samples_cfg.bw/2)-5e3 
    y_arrow=samples_cfg.bw/2+50e3
    plt.ylim([y_inf, y_arrow])
    plt.grid(axis='y',color='grey', linestyle='--', linewidth=0.3) 
    x_max=0.15
    plt.xlim(0,x_max)
    
    # vertical lines
    vert_lines=[0,8*symbol_period,10*symbol_period,12.25*symbol_period,12.25*symbol_period+18*symbol_period]
    for line in vert_lines: 
        plt.axvline(line, color=vert_line_color, linestyle='-', linewidth=0.5)
    
    # left and right arrows
    vert_lines[4]=vert_lines[4]-0.11
    for i in range(len(vert_lines)-1):
        x_init_arrow=vert_lines[i] 
        x_end_arrow =vert_lines[i+1] 
        ax.hlines(y=y_arrow, xmin=x_init_arrow, xmax=x_end_arrow, color='black', linewidth=0.5)
        ax.annotate('', xy=(x_init_arrow, y_arrow), xytext=(x_init_arrow - 0.00001, y_arrow),
                arrowprops=dict(
                    arrowstyle='<|-',  
                    color='black',
                    linewidth=0.1,       
                    shrinkA=0.01, shrinkB=0.01,  
                    mutation_scale=8      
                ))
        if x_end_arrow<vert_lines[-1]:
            ax.annotate('', xy=(x_end_arrow, y_arrow), xytext=(x_end_arrow + 0.00001, y_arrow),
            arrowprops=dict(
                arrowstyle='<|-',  
                color='black',
                linewidth=0.1,       
                shrinkA=0.01, shrinkB=0.01,
                mutation_scale=8      
            ))
    
    # text annotation
    y_text_lin_1=235e3
    y_text_lin_2=200e3
    y_text_lin_center=215e3
    y_text_numbers=y_arrow-40e3
    x_ellipses = vert_lines[4]+0.0075
    y_ellipses=y_arrow+12e3
    ax.text(x_ellipses, y_ellipses, '...', color='black', fontsize=15, ha='center', va='center')
    plt.text(4*symbol_period, y_text_lin_1, r'Preamble', fontsize=fontsize_text, color='black', ha='center')
    plt.text(4*symbol_period, y_text_numbers, r'8', fontsize=fontsize_text_num, color='black', ha='center')
    plt.text(4*symbol_period, y_text_lin_2, r'upchirps', fontsize=fontsize_text, color='black', ha='center')
    plt.text(9*symbol_period, y_text_lin_1,  r'Sync', fontsize=fontsize_text, color='black', ha='center')
    plt.text(9*symbol_period, y_text_numbers, r'2', fontsize=fontsize_text_num, color='black', ha='center')
    plt.text(9*symbol_period, y_text_lin_2,  r'word', fontsize=fontsize_text, color='black', ha='center')
    plt.text(11.2*symbol_period, y_text_lin_center, r'SFD', fontsize=fontsize_text, color='black', ha='center')
    plt.text(11.2*symbol_period, y_text_numbers, r'2.25', fontsize=fontsize_text_num, color='black', ha='center')
    plt.text(15.5*symbol_period, y_text_lin_1, r'Information', fontsize=fontsize_text, color='black', ha='center')
    plt.text(15.5*symbol_period, y_text_lin_2, r'symbols ', fontsize=fontsize_text, color='black', ha='center')
    
    # colored boxes
    color_preamble='green'
    color_sw='green'
    color_sfd='green'
    color_inf_symb='darkred'
    colors=[color_preamble,color_sw,color_sfd,color_inf_symb]
    vert_lines[4]=vert_lines[4]+0.11
    borda=125e3
    plt.axvspan(vert_lines[0], vert_lines[1], ymin=(-borda-y_inf)/(y_arrow-y_inf), ymax=(borda-y_inf)/(y_arrow-y_inf),color=colors[0], alpha=0.2)  
    plt.axvspan(vert_lines[1], vert_lines[2], ymin=(-borda-y_inf)/(y_arrow-y_inf), ymax=(borda-y_inf)/(y_arrow-y_inf), color=colors[1], alpha=0.2)  
    plt.axvspan(vert_lines[2], vert_lines[3], ymin=(-borda-y_inf)/(y_arrow-y_inf), ymax=(borda-y_inf)/(y_arrow-y_inf),color=colors[2], alpha=0.2)  
    plt.axvspan(vert_lines[3], vert_lines[4], ymin=(-borda-y_inf)/(y_arrow-y_inf), ymax=(borda-y_inf)/(y_arrow-y_inf),color=colors[3], alpha=0.2)
    
    # plot config
    plt.xlabel(r'Time',fontweight='normal',fontsize=fontsize_xy_labels)
    plt.ylabel(r'Frequency',fontweight='normal',fontsize=fontsize_xy_labels)
    plt.xticks(fontsize=fontsize_ticks,fontweight='normal')
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    
    # remove borders 
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    
    # save option
    if SAVE_PLOTS:
        plt.savefig(image_folder+fig_1,bbox_inches='tight') 
    
    plt.show()
    
    
    