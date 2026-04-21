from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class LoraSymbolConfig:
    """
    LoRa symbol config dataclass
    
    Attributes:
        s (int): Symbol value.
        sf (int): Spreading factor.
        bw (float): Bandwidth [Hz].
        f (optional[float]): carrier frequency [Hz]
        fs (optional[float]): Sampling frequency [samples/s or Hz]. Default to `bw` if not provided. 
    """
    
    s: int
    sf: int
    bw: float
    f: Optional [float] = None
    fs: Optional [float] = None
    
    def __post_init__(self):
        if self.fs is None:
            self.fs = self.bw 
            

      