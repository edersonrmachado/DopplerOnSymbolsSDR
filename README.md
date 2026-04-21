![gnuradio](https://img.shields.io/badge/GNU%20Radio-3.10.11-important)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) 



# DopplerOnSymbolsSDR

This repository contains the code that can be used to study or reproduce the results of the article:

_Overview and experimental
validation of Doppler effect on
LEO satellite communication
using LoRa_


## Reprodution of figures

### List of folders:

- [`lora_packet`](lora_packet/README.md): reproduces fig 1.
- [`lora_demodulation_chain`](lora_demodulation_chain/README.md): reproduces fig 2.
- [`doppler_curve_example`](doppler_curve_example/README.md): reproduces fig 3.
- [`freq_shift_symbol_impact`](freq_shift_symbol_impact/README.md): reproduces fig 4.
- [`doppler_impact_symbol_sequence`](doppler_impact_symbol_sequence/README.md): reproduces fig 5.

## Reprodution of experiments 

### List of folders:

- [`gnuradio_simulation`](https://github.com/edersonrmachado/DopplerOnSymbolsSDR/tree/main/gnuradio_simulation): gnuradio simulation with Doppler shift insertion on the LoRa packet.
- [`gnuradio_emulation`](https://github.com/edersonrmachado/DopplerOnSymbolsSDR/tree/main/gnuradio_simulation): gnuradio emulation with Doppler shift insertion on the LoRa packet using limeSDR Mini.




## Credit
This work was implemented based on [https://github.com/tapparelj/gr-lora_sdr/](https://github.com/tapparelj/gr-lora_sdr/) by Joachin Tapparel et al.,  which is also inspired from  [https://github.com/rpp0/gr-lora](https://github.com/rpp0/gr-lora) by Pieter Robyns, Peter Quax, Wim Lamotte and William Thenaers. 

Some blocks functionalities have been modified to emulate the physical layer of LoRa  in the presence of Doppler effect. 

## Licence
Distributed under the GPL-3.0 License License. See LICENSE for more information.