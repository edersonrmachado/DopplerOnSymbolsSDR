from dataclasses import dataclass
from typing import Optional


@dataclass
class LoraSamplesConfig:
    """
    LoRa  config for file samples
    
    Attributes:
        freq (float): Symbol value.
        sf (int): Spreading factor.
        bw (float): Bandwidth [Hz].
        fs (float): Sampling rate [samples/s or Hz].
          
    """
    
    freq: float
    sf: int
    bw: float
    cr: int
    fs: float
    