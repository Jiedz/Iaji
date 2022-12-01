#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 19:31:22 2022

@author: jiedz

This module defines a generic interface for an electronic oscilloscope
"""
# In[imports]
from signalslot import Signal
#import numpy
import warnings
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
        '''
        Connects the host to the oscilloscope and defines the related software instrument
        '''
        warnings.warn("Not fully implemented")
    #------------
    def acquire(self, channel_numbers:list[str]=None, channel_names:list[int]=None):
        '''
        Starts and finishes a single acquisition from the selected channels, enabling
        them if they are not
        '''
        assert channel_numbers is not None or channel_names is not None, \
            "either 'channel_numbers' or 'channel_names' must be specified"
        if channel_names is not None:
            channel_ids = channel_names
            all_channel_ids = self.channel_names 
        else:
            channel_ids = channel_numbers
            all_channel_ids = range(len(self.channels))
        #Activate only the selected channels
        #active_channel_numbers = [j for j in range(len(self.channels)) if self.channel(j+1).is_enabled()]
        for x in channel_ids:
            self.channel(x).enable(True)
        for x in list(set(all_channel_ids)-set(channel_ids)):
            self.channel(x).enable(False)
        #Acquire    
        warnings.warn("Not fully implemented")
    #------------
    def channel(self, channel_id):
        if type(channel_id) == str:
            return [self.channels[j] for j in range(len(self.channel_names)) if self.channel_names[j]==channel_id][0]
        else:
            return self.channels[channel_id-1]
        warnings.warn("Not fully implemented")
    #------------
    def stop(self):
        warnings.warn("Not fully implemented")
    #------------
    def wait(self):
        warnings.warn("Not fully implemented")
# In[OscilloscopeChannel]
class OscilloscopeChannel:
    def __init__(self, instrument, channel_number, name="Oscilloscope Channel"):
        self.instrument = instrument
        self.number = int(channel_number)
        self.name = name
        warnings.warn("Not fully implemented")
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
        warnings.warn("Not fully implemented")
    #------------
    def get_vertical_setup(self):
        warnings.warn("Not fully implemented")
    #------------
    def set_vertical_range(self, voltage_range):
        """
        Sets the voltage range for the input channel.

        :param channel: str
        :param voltage_range: float
            full range of the voltages displayed by the scope for the input channel.
        :return:
        """
        warnings.warn("Not fully implemented")
    #------------
    def set_vertical_offset(self, offset):
        """
        Sets the vertical offset for the input channel.

        :param channel: str
        :param offset: float
            vertical offset of the scope for the input channel.
        :return:
        """
        warnings.warn("Not fully implemented")
    #------------
    def enable(self, enabled):
        """
        Enables or disables the input channels.

        :param channel: str
        :param enable: bool
            If true, the input "C"+str(self.number)s is displayed.
        :return:
        """
        warnings.warn("Not fully implemented")
    #------------
    def is_enabled(self):
        warnings.warn("Not fully implemented")
    #------------    
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
        warnings.warn("Not fully implemented")
    #------------
    def get_coupling(self):
        """
        Gets the coupling type of the input channel

        :param channel: str
        :return:
        """
        warnings.warn("Not fully implemented")
    

