import numpy as np
import matplotlib.pyplot as plt


# save the plots on `image_folder` if true
SAVE_PLOTS=True


def plot_doppler(rel_doppler_shift,rel_doppler_rate,time_vec, image_folder):
    """
    Generate plots and save [opt].
    
    Args:
        rel_doppler_shift (np.ndparray): doppler shift vector.
        rel_doppler_rate (np.ndparray): doppler rate vector.
        time_vec (np.ndparray): time vector [sec].    
        image_folder (str): to save figures.  
    """
    
    # fig names
    fig_1='doppler_curves.pdf'

    # plots - customized style
    fig_facecolor='#FFFFFF'
    dpi_set=600
    fig_width=3.5 
    fig_height=2.2 
    fontsize_xticks=10 
    fontsize_labels=11
    fontsize_text=9 
    fontsize_text2=11
    dop_shift_color='black'
    dop_rate_color='darkgreen'
    
    # text 
    margin=0.25
    max_dop_shift = np.max(rel_doppler_shift)
    t_max_dop_shift = time_vec[np.argmax(rel_doppler_shift)]
    min_dop_shift = np.min(rel_doppler_shift)
    t_min_dop_shift = time_vec[np.argmin(rel_doppler_shift)]
    max_dop_rate = np.max(rel_doppler_rate)
    t_max_dop_rate = time_vec[np.argmax(rel_doppler_rate)]
    min_dop_rate = np.min(rel_doppler_rate)
    t_min_dop_rate = time_vec[np.argmin(rel_doppler_rate)]
    
    fig, ax1 = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi_set, facecolor=fig_facecolor)
    
    # doppler shift ppm 
    ax1.plot(time_vec, rel_doppler_shift, color=dop_shift_color)
    ax1.text(t_max_dop_shift, max_dop_shift+0.5, f' Max: {max_dop_shift:.2f}', horizontalalignment='left', verticalalignment='bottom',fontsize=fontsize_text)
    ax1.text(t_min_dop_shift-10, min_dop_shift-5.5, f' Min: {min_dop_shift:.2f}', horizontalalignment='right', verticalalignment='bottom',fontsize=fontsize_text)
    ax1.set_xlim(np.min(time_vec),np.max(time_vec) )
    ax1.set_ylim(min_dop_shift+min_dop_shift*margin,max_dop_shift+max_dop_shift*margin )
    ax1.set_xlabel('Time (s)',fontsize=fontsize_labels)
    ax1.set_ylabel('Static Doppler $\delta_F$ [ppm]', color=dop_shift_color,fontsize=fontsize_labels)
    ax1.tick_params(axis='y', labelcolor=dop_shift_color,labelsize=fontsize_xticks)
    ax1.text(t_max_dop_shift-(t_max_dop_shift/1.5), max_dop_shift+max_dop_shift*(0.1*margin)-1, '$\delta_F$', fontsize=fontsize_text2, ha='right', va='center')
    ax1.grid(True)
    
    # doppler rate ppm/s
    ax2 = ax1.twinx()  
    ax2.plot(time_vec, rel_doppler_rate, color=dop_rate_color,linestyle='-.')
    ax2.set_ylabel("Doppler rate ${\delta_F}'$ [ppm/s]", color=dop_rate_color, fontsize=fontsize_labels)
    ax2.tick_params(axis='y', labelcolor=dop_rate_color, labelsize=fontsize_xticks)
    ax1.tick_params(axis='x', labelsize=fontsize_xticks)
    ax2.text(t_min_dop_rate -50, min_dop_rate -0.05, f'Min: {min_dop_rate:.2f}', horizontalalignment='center', verticalalignment='top',fontsize=fontsize_text)
    ax2.set_ylim((min_dop_shift+min_dop_shift*margin)/20,(max_dop_shift+max_dop_shift*margin)/20)
    ax2.text(t_min_dop_shift-(t_min_dop_shift/3), max_dop_rate-min_dop_rate*0.1+0.09, "${\delta_F}'$", fontsize=fontsize_text2, ha='right', va='center')
    
    # save option
    if SAVE_PLOTS:
        fig.savefig(image_folder+fig_1,bbox_inches='tight') 
    
    plt.show()