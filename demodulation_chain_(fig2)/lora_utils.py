import numpy as np 


def normalized_frequency(in_vector,bw,fs):
    """ 
    Calculates normalized frequency of a complex vector
    
    Args:
        in_vector (complex): entry vector.
        bw (float): bandwidth in Hz.
        fs (float): sampling frequency samples/s.
    Returns:
        np.ndarray: normalized inst. frequency vector (length=in_vector-1),
                    in units relative to the bandwidth [-0.5 to 0.5]*bw if bw=fs.
    """
    # aux vector 
    aux_vec=[0] * (len(in_vector) - 1) 
    # argument vector
    arg=[0] * (len(in_vector) - 1) 
    for n in range(len(in_vector)-1):
        aux_vec[n]=in_vector[n+1]*np.conj(in_vector[n])     
        arg[n]=np.angle(aux_vec[n]) 
    # instantaneous freq. [rad/samples]
    arg=np.array(arg)  
    # instantaneous freq. normalized with bw
    return arg*(fs/bw)/(2*np.pi) 