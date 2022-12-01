#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 19:31:22 2022

@author: jiedz

This module defines a generic interface for an electronic oscilloscope
"""
# imports
from signalslot import Signal
import numpy
# In[Oscilloscope]
class Oscilloscope:
    def __init__(self, address, name:str="Oscilloscope", channel_names:list[str] = [], connect=True):
        self.name = name
        self.address = address
        self.instrument = None
        self.channels = []
        self.channel_names = channel_names
        self.channel_names_changed = Signal()
        if connect:
            try:
                self.connect()
                self.channels = [OscilloscopeChannel(instrument=self.instrument, channel_number=j+1, name=channel_names[j]) for j in range(len(channel_names))]
                self.traces = dict(zip(channel_names, [None for j in range(len(channel_names))]))
            except: 
                print('WARNING: it was not possible to connect to the oscilloscope '+self.name)
                return
    #------------ 
    def connect(self):
        raise NotImplementedError
    #------------
    def acquire(self, channel_numbers:list[str]=None, channel_names:list[int]=None):
        assert channel_numbers is not None or channel_names is not None, \
            "either 'channel_numbers' or 'channel_names' must be specified"
        raise NotImplementedError
    #------------
    def channel(self, name:str=None, number:int=None):
        assert name is not None or number is not None, \
            "either 'name' or 'number' must be specified"
        if name is not None:
            return self.channels[numpy.where(self.channel_names==name)]
        else:
            return self.channels[number-1]
        raise NotImplementedError
    #------------
    def stop(self):
        raise NotImplementedError
    #------------
    def wait(self):
        raise NotImplementedError
# In[OscilloscopeChannel]
class OscilloscopeChannel:
    def __init__(self, instrument, channel_number, name="Oscilloscope Channel"):
        self.instrument = instrument
        self.number = int(channel_number)
        self.name = name
    #------------ 
    def setup_vertical(self, voltage_range, offset):
        """
        Sets the voltage range and the vertical offset for the input channel.

        :param channel: str
        :param voltage_range: float
            full range of the voltages displayed by the scope for the input channel.
        :param offset: float
            vertical offset of the scope for the input channel.
        :return:
            the list of command strings being sent to the scope
        """
        raise NotImplementedError

    def get_vertical_setup(self):
        raise NotImplementedError

    def set_vertical_range(self, voltage_range):
        """
        Sets the voltage range for the input channel.

        :param channel: str
        :param voltage_range: float
            full range of the voltages displayed by the scope for the input channel.
        :return:
        """
        raise NotImplementedError

    def set_vertical_offset(self, offset):
        """
        Sets the vertical offset for the input channel.

        :param channel: str
        :param offset: float
            vertical offset of the scope for the input channel.
        :return:
        """
        raise NotImplementedError

    # --------------------------------------------------------------------------------------------------------------
    # Other

    def enable(self, enabled):
        """
        Enables or disables the input channels.

        :param channel: str
        :param enable: bool
            If true, the input "C"+str(self.number)s is displayed.
        :return:
        """
        raise NotImplementedError

    def is_enabled(self):
        raise NotImplementedError
        
    def set_coupling(self, coupling):
        """
        Sets the coupling type of the channel input.

        :param channel: str
        :param coupling: str
            Coupling type.
            Valid arguments:
                - "A1M": (AC, 1 MOhm input impedance)
                - "D1M": (DC, 1 MOhm input impedance)
                - "D50": (DC, 50 Ohm input impedance)
                - "GND": grounded input
        :return:
            the command being sent to the scope
        """
        raise NotImplementedError

    def get_coupling(self):
        """
        Gets the coupling type of the input channel

        :param channel: str
        :return:
        """
        raise NotImplementedError
    

