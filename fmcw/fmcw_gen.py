import numpy as np 


class FMCWSignal: 


    def __init__(self, bandwidth_hz, sweep_time_s, sampling_freq_hz): 

        self.bandwidth_hz = bandwidth_hz
        self.sweep_time_s = sweep_time_s
        self.sampling_freq_hz = sampling_freq_hz
        self.num_samples = sampling_freq_hz * sweep_time_s

    def get_time(self, num_chirps=1): 
        return np.linspace(0,self.sweep_time_s*num_chirps,self.num_samples*num_chirps, endpoint=False )

    def generate_chirp(self):
        phase = 
        pass

    def get_sequential_signals(self): 


