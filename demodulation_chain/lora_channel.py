import numpy as np

DEBUG_PRINT=False

def generate_awgn(vector,snr):
    
    # modulo of complex vector (signal)
    magnitude = np.abs(vector)   
    # instantaneous power of complex vector 
    power_inst_vector= magnitude**2 
    # average power of the complex vector
    power_mean=np.mean(power_inst_vector) 
    # db power of the complex vector
    power_mean_db = 10 * np.log10(power_mean)  
    # db average power of requested noise 
    noise_mean_db=power_mean_db-snr 
    # linear average  (watts) of requested noise
    noise_mean=10**(noise_mean_db/10) 
    # average and standard deviation of noise 
    mu,sigma = 0, np.sqrt(noise_mean)
    # generates complex noise components
    noise_real=np.random.normal(mu,sigma,len(vector))/np.sqrt(2)
    noise_imag=np.random.normal(mu,sigma,len(vector))/np.sqrt(2)
    noise_complex = noise_real + 1j * noise_imag
    
    if DEBUG_PRINT:
        # magnitude of complex noise vector samples (noise signal)
        magnitude_noise=np.abs(noise_complex)
        # instantaneous power of complex noise vector 
        power_inst_noise=magnitude_noise**2
        # average power of the noise complex vector 
        power_mean_noise=np.mean(power_inst_noise)
        # db power of the noise complex vector
        power_mean_noise_db=10 * np.log10(power_mean_noise) 
        print("Theorectical values:")
        print(f"Average power of the signal = {power_mean:.2f}")
        print(f"Average power of the signal [dB] = {power_mean_db:.2f}")
        print(f"Average power of the noise [dB] ={noise_mean_db:.2f}")
        print(f"Average power of the noise = {noise_mean:.5f}")
        print("Obtained values:")
        print(f"Average power of the noise = {power_mean_noise:.5f}")
        print(f"Average power of the noise [dB] ={power_mean_noise_db:.5f}")
        print()
    
    return noise_complex