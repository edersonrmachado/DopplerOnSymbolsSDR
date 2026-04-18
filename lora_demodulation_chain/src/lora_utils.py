import numpy as np 


def normalized_frequency(in_vector,bw,fs):
    """
    Calculate normalized frequency of a complex vec.
    
    Args:
        in_vector (complex): entry vector.
        bw (float): bandwidth in Hz.
        fs (float): sampling frequency samples/s.
    
    Returns:
        np.ndarray: normalized inst. frequency vector (length=in_vector-1),
                    in units relative to the bandwidth [-0.5 to 0.5]*bw if bw=fs.
    """
    
    # auxiliar and argument vectors 
    aux_vec=[0] * (len(in_vector) - 1) 
    arg=[0] * (len(in_vector) - 1) 
    
    # calculate inst. freq. [rad/samples] and bw relative normalized freq.
    for n in range(len(in_vector)-1):
        aux_vec[n]=in_vector[n+1]*np.conj(in_vector[n])     
        arg[n]=np.angle(aux_vec[n]) 
    inst_frec=np.array(arg)  
    norm_frec=inst_frec*(fs/bw)/(2*np.pi) 
    return norm_frec 