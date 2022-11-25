#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 22:37:58 2022

@author: jiedz
Test script for the Pulse module
"""

# In[imports]
from Iaji.SignalProcessing.Signals1D.pulses import Pulse
# In[]
p = Pulse()
p.set_shape_standard(start=-200e-9, stop=200e-9, window_type="exp", \
                     rise=20e-9, fall=40e-9)
p.plot(-500e-9, 500e-9)