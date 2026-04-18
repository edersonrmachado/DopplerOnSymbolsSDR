### LoRa modulation/demodulation chain.

This module has the functions to modulate and demodulate a LoRa symbol.The steps to reproduce the symbol demodulation example (s = 10), as shown in fig. 2, are described below.

<p align="center">
<img src="figures/fig2.png" alt="drawing" width="450"/>
</p>

<p align="center"><em>Fig. 2. LoRa demodulation chain for a symbol s=10, with SF=7, B=125 kHz. The illustration includes the instantaneous frequency, FFT magnitude spectrum, and the complex baseband representation of the signal throughout the processing blocks, leading to the final symbol estimation ŝ.</em></p>

1. Creates a venv and install required packages  

```bash
    python3 -m venv venv 
    source venv/bin/activate 
    pip install -r requirements.txt
```

2. Open `src/main.py` and specify a folder to save the  `.sgv` figures:

```python
image_folder="/home/ederson/Desktop/figures/" 
```

3. Run the code:

```bash
python main.py 
```

4. Open the drawio model file: `docs/doppler_chain.drawio`, activate `Mathematical Typeseting` on the `Extra` menu and import the `.sgv` figures:

<p align="center">
<img src="figures/drawio.png", alt="drawing2", width="600"/>
</p>