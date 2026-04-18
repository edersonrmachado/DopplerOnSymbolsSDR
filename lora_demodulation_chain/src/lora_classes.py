from dataclasses import dataclass
from typing import Optional

@dataclass
class LoraSymbolConfig:
    """
    LoRa symbol config dataclass
    
    Attributes:
        s (int): Symbol value.
        sf (int): Spreading factor.
        bw (float): Bandwidth [Hz].
        fs (optional[float]): Sampling frequency [samples/s or Hz]. Default to `bw` if not provided. 
    """
    
    s: int
    sf: int
    bw: float
    fs: Optional [float] = None
    
    def __post_init__(self):
        if self.fs is None:
            self.fs = self.bw 