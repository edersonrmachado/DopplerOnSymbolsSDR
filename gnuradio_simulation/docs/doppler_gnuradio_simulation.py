#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Doppler Gnuradio Simulation
# Author: Tapparel Joachim@EPFL,TCL, Jonas Feijó (modified by Ederson Machado)
# Description: Simulation of doppler effect impact on a sequence of LoRa symbols
# GNU Radio version: 3.10.1.1

from gnuradio import blocks
from gnuradio import doppler
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import gnuradio.lora_sdr as lora_sdr




class doppler_gnuradio_simulation(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Doppler Gnuradio Simulation", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.symbol = symbol = 512
        self.soft_decoding = soft_decoding = False
        self.sf = sf = 10
        self.samp_rate = samp_rate = 125000
        self.preamb_len = preamb_len = 8
        self.pay_len = pay_len = 100
        self.ldro = ldro = False
        self.impl_head = impl_head = True
        self.has_crc = has_crc = False
        self.file_to_save_samples = file_to_save_samples = "../data/fft_test.txt"
        self.doppler_shift = doppler_shift = 0
        self.doppler_rate = doppler_rate = -140.28
        self.cr = cr = 1
        self.clk_offset = clk_offset = 0
        self.center_freq = center_freq = 436.9e6
        self.bw = bw = 125000

        ##################################################
        # Blocks
        ##################################################
        self.lora_sdr_header_decoder_0 = lora_sdr.header_decoder(impl_head, cr, pay_len, has_crc, ldro, True)
        self.lora_sdr_hamming_dec_0 = lora_sdr.hamming_dec(soft_decoding)
        self.lora_sdr_gray_mapping_0 = lora_sdr.gray_mapping( soft_decoding)
        self.lora_sdr_frame_sync_0 = lora_sdr.frame_sync(int(center_freq), bw, sf, impl_head, [18], int(samp_rate/(bw)),preamb_len)
        self.lora_sdr_fft_demod_0 = lora_sdr.fft_demod( soft_decoding, False,file_to_save_samples)
        self.lora_sdr_dewhitening_0 = lora_sdr.dewhitening()
        self.lora_sdr_deinterleaver_0 = lora_sdr.deinterleaver( soft_decoding)
        self.lora_sdr_crc_verif_0 = lora_sdr.crc_verif( 0, False)
        self.doppler_modulate_doppler_0 = doppler.modulate_doppler(sf, samp_rate, bw, [18], int(20*2**sf*samp_rate/bw), 8, 0, int(doppler_rate))
        self.blocks_vector_source_x_0 = blocks.vector_source_i([symbol]*(pay_len+2), False, 1, [])
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_1.set_min_output_buffer(5120)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.lora_sdr_header_decoder_0, 'frame_info'), (self.lora_sdr_frame_sync_0, 'frame_info'))
        self.connect((self.blocks_throttle_1, 0), (self.lora_sdr_frame_sync_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.doppler_modulate_doppler_0, 0))
        self.connect((self.doppler_modulate_doppler_0, 0), (self.blocks_throttle_1, 0))
        self.connect((self.lora_sdr_deinterleaver_0, 0), (self.lora_sdr_hamming_dec_0, 0))
        self.connect((self.lora_sdr_dewhitening_0, 0), (self.lora_sdr_crc_verif_0, 0))
        self.connect((self.lora_sdr_fft_demod_0, 0), (self.lora_sdr_gray_mapping_0, 0))
        self.connect((self.lora_sdr_frame_sync_0, 0), (self.lora_sdr_fft_demod_0, 0))
        self.connect((self.lora_sdr_gray_mapping_0, 0), (self.lora_sdr_deinterleaver_0, 0))
        self.connect((self.lora_sdr_hamming_dec_0, 0), (self.lora_sdr_header_decoder_0, 0))
        self.connect((self.lora_sdr_header_decoder_0, 0), (self.lora_sdr_dewhitening_0, 0))


    def get_symbol(self):
        return self.symbol

    def set_symbol(self, symbol):
        self.symbol = symbol
        self.blocks_vector_source_x_0.set_data([self.symbol]*(self.pay_len+2), [])

    def get_soft_decoding(self):
        return self.soft_decoding

    def set_soft_decoding(self, soft_decoding):
        self.soft_decoding = soft_decoding

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf
        self.doppler_modulate_doppler_0.set_sf(self.sf)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)

    def get_preamb_len(self):
        return self.preamb_len

    def set_preamb_len(self, preamb_len):
        self.preamb_len = preamb_len

    def get_pay_len(self):
        return self.pay_len

    def set_pay_len(self, pay_len):
        self.pay_len = pay_len
        self.blocks_vector_source_x_0.set_data([self.symbol]*(self.pay_len+2), [])

    def get_ldro(self):
        return self.ldro

    def set_ldro(self, ldro):
        self.ldro = ldro

    def get_impl_head(self):
        return self.impl_head

    def set_impl_head(self, impl_head):
        self.impl_head = impl_head

    def get_has_crc(self):
        return self.has_crc

    def set_has_crc(self, has_crc):
        self.has_crc = has_crc

    def get_file_to_save_samples(self):
        return self.file_to_save_samples

    def set_file_to_save_samples(self, file_to_save_samples):
        self.file_to_save_samples = file_to_save_samples

    def get_doppler_shift(self):
        return self.doppler_shift

    def set_doppler_shift(self, doppler_shift):
        self.doppler_shift = doppler_shift

    def get_doppler_rate(self):
        return self.doppler_rate

    def set_doppler_rate(self, doppler_rate):
        self.doppler_rate = doppler_rate

    def get_cr(self):
        return self.cr

    def set_cr(self, cr):
        self.cr = cr

    def get_clk_offset(self):
        return self.clk_offset

    def set_clk_offset(self, clk_offset):
        self.clk_offset = clk_offset

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw




def main(top_block_cls=doppler_gnuradio_simulation, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
