import numpy as np
from scipy.fftpack import fft
import threading
import logging
import time


from doppler_gnu_simulation import doppler_simulation
from doppler_utils import read_fft_file, first_error_and_periodicity

#log file
log_file="simulation.log"

# log config
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


def run_flowgraph(test):
    
    test.start()
    test.wait()  
    
def run_test_multiple_times(NUMBER_OF_EXPERIMENTS,symbol_cfg, NUMBER_OF_SYMBOLS, doppler_shift, doppler_rate_tx,fft_file):
    print("\033[92m\nRunning gnuradio simulation...\033[0m")
    
    # clear log file
    open(log_file, "w").close()
    logging.info("[INFO] Experiment started...")
    
    # matrix and vectors 
    fft_abs_matrix=[]
    estimated_symbol_list=[]
    first_error_vec=[]
    periodicity_vec=[]  
    
    # test batch 
    valid_run_count=0
    not_valid_run_count=0
    i=0    
    while True:
        # launch simulator
        print(f"\033[92m\nRunning gnuradio flowgraph...{i+1}\033[0m")
        simulator= doppler_simulation(symbol_cfg, NUMBER_OF_SYMBOLS, doppler_shift, doppler_rate_tx,fft_file)
        logging.info(f"[INFO] Running test number {i+1}...")
        
        # use threading to detect timeout error on simulation 
        t = threading.Thread(target=run_flowgraph, args=(simulator,))
        t.start()
        t.join(timeout=8)

        # evaluates time out
        if t.is_alive():
            print("\033[31m[ERROR] Test timeout!\033[0m")
            logging.error("[ERROR] Test timeout!")
            simulator.stop()
            not_valid_run_count+=1
        else:        
            # calculate estimated symbols, fft_abs
            time.sleep(3)
            fft_abs_vec,estimated_symbol_vec = read_fft_file(fft_file)   
            #print(fft_abs_vec)
            #quit()
            # if fft_abs_vec has elements and they are not zero       
            #if (fft_abs_vec > 0).all() and len(fft_abs_vec) > 0:
            fft_abs_vec=fft_abs_vec/(np.max(fft_abs_vec))
            first_error, periodicity = first_error_and_periodicity(symbol_cfg,fft_abs_vec, estimated_symbol_vec)
            #print(f"First Symbol Shift Error Due to Doppler [e0]: {first_error}")
            #print(f"Number maximum of symbols before a Doppler error [nmax]: {first_error-1}")
            #print(f"One shift error periodicity [pe]: {periodicity}")
            
            # matrix vector storing        
            fft_abs_matrix.append(fft_abs_vec)
            estimated_symbol_list.append(estimated_symbol_vec)
            first_error_vec.append(first_error)
            periodicity_vec.append(periodicity)
            valid_run_count=valid_run_count+1
            
            logging.info(f"[INFO] Test {i+1} successfully run.")
            logging.info(f"[INFO] Successful tests {valid_run_count}.")
            logging.info(f"[INFO] Remaining {NUMBER_OF_EXPERIMENTS-valid_run_count} of {5*NUMBER_OF_EXPERIMENTS-(i+1)}.")
            #else:
            #    logging.error("[ERROR] Reading empty file!")
            #    not_valid_run_count+=1
             
            if valid_run_count==NUMBER_OF_EXPERIMENTS or i==5*NUMBER_OF_EXPERIMENTS:
                logging.info("[INFO] Experiment finished.")
                logging.shutdown()
                break
        i=i+1
    return np.array(fft_abs_matrix),np.array(estimated_symbol_list) ,np.array(first_error_vec), np.array(periodicity_vec)
    
