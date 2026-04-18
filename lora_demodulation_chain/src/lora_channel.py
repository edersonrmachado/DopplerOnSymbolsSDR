import numpy as np

# print debug info about noise and signal power
DEBUG_PRINT=True

def generate_awgn(vector,snr):
    """
    Generate AWGN noise vector according to SNR and an input vector.
    
    Args:
        vector (complex): signal vector.
        snr (float): signal-to-noise ratio (dB).
    
    Returns:
        np.narray[complex]: `noise_complex`, the complex noise vector generated.
    """
    
    # magnitude, inst. and  average  power  of complex vector (signal)
    magnitude = np.abs(vector)   
    power_inst_vector= magnitude**2 
    power_mean=np.mean(power_inst_vector) 
    power_mean_db = 10 * np.log10(power_mean)  
    
    # average power, average and standard deviation of requested noise 
    noise_mean_db=power_mean_db-snr 
    noise_mean=10**(noise_mean_db/10) 
    mu,sigma = 0, np.sqrt(noise_mean)
    
    # generates complex noise components
    noise_real=np.random.normal(mu,sigma,len(vector))/np.sqrt(2)
    noise_imag=np.random.normal(mu,sigma,len(vector))/np.sqrt(2)
    noise_complex = noise_real + 1j * noise_imag
    
    if DEBUG_PRINT:
        
        # magnitude, inst. and average power of complex noise vector generated
        magnitude_noise=np.abs(noise_complex)
        power_inst_noise=magnitude_noise**2
        power_mean_noise=np.mean(power_inst_noise)
        power_mean_noise_db=10 * np.log10(power_mean_noise) 
        
        # show theoretical/practical obtained values
        print("Theoretical values:")
        print(f"Average power of the signal (linear)= {power_mean:.2f} ")
        print(f"Average power of the signal [dB] = {power_mean_db:.2f}")
        print(f"Average power of the noise (linear) = {noise_mean:.5f}")
        print(f"Average power of the noise [dB] = {noise_mean_db:.2f}")
        print()
        print("Obtained values:")
        print(f"Average power of the noise (linear) = {power_mean_noise:.5f}")
        print(f"Average power of the noise [dB] = {power_mean_noise_db:.2f}")
        print()
    
    return noise_complex