### Doppler impact in a sequence of symbols (packet).

This file shows the steps to reproduce the Doppler impact on a symbol sequence, reproducing the fig.5: 

<p align="center">
<img src="figures/fig5.png", alt="drawing" width="300"/>
</p>

<p align="center"><em>Occurrence the errors (one unit symbol shift represented by the red markers) due to Doppler in a symbol sequence, with SF=11 and B=125 kHz. The k-axis was truncated for illustration..</em></p>

1. Install Doppler modulate block
   
2. Install modified lora OOT block



3. Use local python with gnuradio installed to use its blocks




4. Open `src/main.py` and specify a folder to save the figure:

```python
image_folder="/home/ederson/Desktop/figures/" 
```

3. Run the code:  
  
```bash
python3 main.py 
```