#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Daniel Estevez <daniel@destevez.net>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

from gnuradio import gr
import pmt

from .ao40_uncoded_crc import crc

class check_ao40_uncoded_crc(gr.basic_block):
    """
    docstring for block check_ao40_uncoded_crc
    """
    def __init__(self, verbose):
        gr.basic_block.__init__(self,
            name="check_ao40_uncoded_crc",
            in_sig=[],
            out_sig=[])

        self.verbose = verbose
        
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('ok'))
        self.message_port_register_out(pmt.intern('fail'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytes(pmt.u8vector_elements(msg))
        if crc(packet) == 0:
            if self.verbose:
                print("CRC OK")
            self.message_port_pub(pmt.intern('ok'), msg_pmt)
        else:
            if self.verbose:
                print("CRC failed")
            self.message_port_pub(pmt.intern('fail'), msg_pmt)
