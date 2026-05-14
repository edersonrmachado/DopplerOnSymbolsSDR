import numpy as np
from scipy.fftpack import fft
import threading

from doppler_gnu_simulation import doppler_simulation

# Earth's radius [m], gravity acc. [m/s^2] and lightspeed [m/s]
#EARTH_RADIUS = 6378137     
EARTH_RADIUS = 6371000     

GRAVITY = 9.80665     
LIGHTSPEED = 299792458   


def relative_doppler_shift(H,t):
    """
    Calculate rel. doppler shift according to simplified equation.

    Args:
        H (float): satellite altitude in meters.
        t (np.ndarray): time relative to the zenith vector [seconds].

    Returns:
        rel_doppler_shift (np.ndarray): relative doppler shift [dimensionless]. 
    """
    
    rel_doppler_shift=1/(1+((1/LIGHTSPEED)*np.sqrt((GRAVITY*EARTH_RADIUS)/(1+H/EARTH_RADIUS)))*(np.sin((np.sqrt(GRAVITY / EARTH_RADIUS) / (1 + H / EARTH_RADIUS) ** (3 / 2)) * t)/np.sqrt((1+H/EARTH_RADIUS)**2-2*(1+H/EARTH_RADIUS)*np.cos((np.sqrt(GRAVITY / EARTH_RADIUS) / (1 + H / EARTH_RADIUS) ** (3 / 2)) * t)+1)))-1
  
    return rel_doppler_shift

def relative_doppler_rate_vec(rel_doppler_shift,dt): 
    """Calculate relative Doppler rate."""
    return np.gradient(rel_doppler_shift, dt)

def find_doppler_rate(tx_time, rel_doppler_rate_vec, time_vec):
    """Find the approx. doppler rate value at tx_time from doppler rate vector."""
    time_index = np.abs(time_vec - tx_time).argmin()
    return rel_doppler_rate_vec[time_index]

def estimate_symbol_with_doppler(symbol_cfg,tx_time,time_vec,rel_doppler_rate_vec,accum_doppler_shift_vec):
    """
    Estimate the symbol value. 
    
    Args:
        symbol_cfg (LoraSymbolConfig): symbol config.
        tx_time (int): time of transmission relative to zenith.
        time_vec (np.ndarray): the visibility window (float64) [sec].
        rel_doppler_rate_vec (np.ndarray): vec to search inst. dop. rate (float64).
        accum_doppler_shift_vec (list of float64): accum. values of doppler shift.
        
    Returns:
        fft_abs (np.ndarray): fft abs of the dem. symbol (float32).
        estimated_symbol (int64): estimated symbol. 
    """
    
    num_samples=2**symbol_cfg.sf
    sample=np.arange(0,num_samples)
    sample_period=1/symbol_cfg.bw 
    symbol_period=sample_period*num_samples
    doppler_rate=find_doppler_rate(tx_time,rel_doppler_rate_vec,time_vec)*symbol_cfg.f
    doppler_shift=sum(accum_doppler_shift_vec)
    y=np.exp(2*np.pi*1j*sample*((symbol_cfg.s/num_samples)+doppler_shift*sample_period+sample*doppler_rate*(sample_period**2)/2))
    y = y.astype(np.complex64) 
    accum_doppler_rate=doppler_rate*symbol_period
    accum_doppler_shift_vec.append(accum_doppler_rate)
    fft_abs=np.abs(np.array(fft(y)))   
    estimated_symbol = np.argmax(fft_abs)
    
    return fft_abs,estimated_symbol 
    

def evaluates_packet(symbol_cfg,num_of_symbols,tx_time,time_vec,rel_doppler_rate_vec):
    """
    Evaluate doppler impact on the packet.
    
    Args:
        symbol_cfg (LoraSymbolConfig): symbol config.
        num_of_symbols (int): the num of symbols in the packet.
        tx_time (int): time of transmission relative to zenith.
        time_vec (np.ndarray): the visibility window (float64) [sec].
        rel_doppler_rate_vec (np.ndarray): vec to search inst. dop. rate (float64).
    
    Returns:
        fft_abs_vec (np.ndarray): vec. of fft. abs. of all symbols (float32).
        estimated_symbol_vec (list of int64): vec. of all estimated symbol. 
    """
    
    fft_abs_vec=[]
    estimated_symbol_vec=[]
    fft_peak_values=[]
    symbol_idxs=[]
    accum_doppler_shift_vec=[]
    
    for symbol_idx in range(1,num_of_symbols+1):
        fft_abs, estimated_symbol= estimate_symbol_with_doppler(
            symbol_cfg,
            tx_time,
            time_vec,
            rel_doppler_rate_vec,
            accum_doppler_shift_vec,
        )
        
        fft_abs_vec.append(fft_abs)
        estimated_symbol_vec.append(estimated_symbol)
        symbol_idxs.append(symbol_idx)
    
    return np.array(fft_abs_vec),np.array(estimated_symbol_vec)


def read_fft_file(filename):
    """_summary_

    Args:
        filename (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    fft_abs_vec = []
    estimated_symbol_vec= []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            fft_abs = np.array(line.split(","), dtype=float)
            estimated_symbol=np.argmax(fft_abs)
            fft_abs_vec.append(fft_abs) # guarda em uma lista
            estimated_symbol_vec.append(estimated_symbol)
            #print(f'FFT len: {len(fft_abs)}, Sym. estimate: {estimated_symbol}')
        #print(f'num elementos {len(fft_abs_vec)}')
        if len(fft_abs_vec)>0:
            # delete last symbol fft due to inconsistences
            if len(fft_abs_vec[-1]) !=len(fft_abs_vec[0]) :
                fft_abs_vec=fft_abs_vec[:-1] 
            print(f"Num. symbols demodulated: {len(fft_abs_vec)}")
                      
    return np.array(fft_abs_vec),np.array(estimated_symbol_vec)


def first_error_and_periodicity(symbol_cfg, fft_abs_vec, estimated_symbol_vec):
    
    # vectors to indicate error positions
    one_shift_error_symbol_idxs=[]  
    one_shift_error_symbol_values=[]
    
    # plot
    last_estimated_symbol=symbol_cfg.s
    for i in range(len(fft_abs_vec)):
        if last_estimated_symbol!=estimated_symbol_vec[i]:
            last_estimated_symbol=estimated_symbol_vec[i]
            one_shift_error_symbol_values.append(last_estimated_symbol)
            one_shift_error_symbol_idxs.append(i+1)
    
    if len(one_shift_error_symbol_idxs) > 0:
    # evaluates first error and peridodicity
        first_error=one_shift_error_symbol_idxs[0]
        one_shift_error_symbol_idxs_arr=np.array(one_shift_error_symbol_idxs)
        if len(one_shift_error_symbol_idxs)>1:
            one_shift_error_periodicity=round(np.mean(np.diff(one_shift_error_symbol_idxs_arr)))
            #print(f"One shift error periodicity [pe]: {one_shift_error_periodicity}")
        else:
            one_shift_error_periodicity=2*first_error
            #print(f"One shift error periodicity [pe]: {one_shift_error_periodicity}")
        
        
    return first_error, one_shift_error_periodicity

'''

def run_experiment(experiment):
    #buffer = io.StringIO()
    #sys.stdout = buffer
    
    experiment.start()
    
    #sys.stdout = sys.__stdout__  # volta ao normal

    #saida = buffer.getvalue().splitlines()

    #print(f"SAIDA \n {saida}")
    
    experiment.wait()  
    
def run_experiment_multiple_times(NUMBER_OF_EXPERIMENTS,symbol_cfg, NUMBER_OF_SYMBOLS, doppler_shift, doppler_rate_tx,fft_file):
    print("\033[92m\nRunning gnuradio simulation...\033[0m")
    # clear log file
    open(log_file, "w").close()
    logging.info("Experiment started...")
    
    
    
    fft_abs_matrix=[]
    estimated_symbol_list=[]
    first_error_vec=[]
    periodicity_vec=[]  
    for i in range(NUMBER_OF_EXPERIMENTS):
        print(f"\033[92m\nRunning gnuradio flowgraph...{i+1}\033[0m")
        simulator= doppler_simulation(symbol_cfg, NUMBER_OF_SYMBOLS, doppler_shift, doppler_rate_tx,fft_file)
        #simulator.start()
        #simulator.wait()
        
        logging.info(f"Running number {i+1}...")
        t = threading.Thread(target=run_experiment, args=(simulator,))
        
        t.start()

        t.join(timeout=7)

       
        
        if t.is_alive():
            print("\033[31m[ERROR] Experiment timeout!\033[0m")
            logging.error("[ERROR] Experiment timeout!")
            simulator.stop()
                
        
        
        
        # calculate estimated symbols, fft_abs
        fft_abs_vec,estimated_symbol_vec = read_fft_file(fft_file)          
        
        one_shift_error_symbol_idxs=[]  
        one_shift_error_symbol_values=[]
        
        # plot
        last_estimated_symbol=symbol_cfg.s
        for i in range(len(fft_abs_vec)):
            if last_estimated_symbol!=estimated_symbol_vec[i]:
                last_estimated_symbol=estimated_symbol_vec[i]
                one_shift_error_symbol_values.append(last_estimated_symbol)
                one_shift_error_symbol_idxs.append(i+1)
        
        
        #first_error, periodicity = first_error_and_periodicity(symbol_cfg,fft_abs_vec, estimated_symbol_vec)
        
        #fft_abs_matrix.append(fft_abs_vec)
        #estimated_symbol_list.append(estimated_symbol_vec)
        #first_error_vec.append(first_error)
        #periodicity_vec.append(periodicity)

        #print(f"First Symbol Shift Error Due to Doppler [e0]: {first_error}")
        #print(f"Number maximum of symbols before a Doppler error [nmax]: {first_error-1}")
        #print(f"One shift error periodicity [pe]: {periodicity}") 
               
    return np.array(fft_abs_matrix),np.array(estimated_symbol_list) #,np.array(first_error_vec), np.array(periodicity_vec)
        

    # plot ticks values in red if errors, otherwise black
   
        
    
    print("\033[92m\nRunning gnuradio simulation...\033[0m")
    simulator= doppler_simulation(symbol_cfg, NUMBER_OF_SYMBOLS, doppler_shift, doppler_rate_tx,fft_file)
    simulator.start()
    simulator.wait()
    print("\033[92m\nSimulation finished.\n\033[0m")
    
    # calculate estimated symbols, fft_abs
    fft_abs_vec,estimated_symbol_vec = read_fft_file(fft_file)
    '''
    