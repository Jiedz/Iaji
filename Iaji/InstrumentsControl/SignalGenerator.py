# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 09:27:48 2022

@author: IYSU
This module defines a generic interface for a radio-frequency signal generator
"""
# In[imports]
#import numpy
import warnings
from signalslot import Signal
# In[Signal generator]
class SignalGenerator:
    # -------------------------------------------
    def __init__(self, address, name="Signal Generator", channel_names:list[str] = [], connect=True):
        self.address = address
        self.name = name
        self.instrument = None
        self.channel_names = channel_names
        try:
            self.connect()
        except ConnectionError: 
            print("WARNING: it was not possible to connect to the signal generator "+self.name)
        self.channels = [SignalGeneratorChannel(instrument=self.instrument, name=self.channel_names[j], channel_number=j+1) for j in range(len(self.channel_names))]
    # -------------------------------------------
    def connect(self):
        warnings.warn("Not fully implemented")
    # -------------------------------------------
    def enable(self, enabled):
        '''
        Turn ON or OFF all channels
        :param enabled: bool
            if True, all channels are turned ON.
        :return:
        '''
        for j in range(len(self.channel_names)):
            self.channel(j).enable(enabled)
    # -------------------------------------------
    def channel(self, channel_id):
        if type(channel_id) == str:
            return [self.channels[j] for j in range(len(self.channel_names)) if self.channel_names[j]==channel_id][0]
        else:
            return self.channels[channel_id-1]
        warnings.warn("Not fully implemented")
    #------------
    def lock_phase(self, locked=True):
        warnings.warn("Not fully implemented")
    # -------------------------------------------
# In[Signal generator channel]
class SignalGeneratorChannel:
    # -------------------------------------------
    def __init__(self, instrument, channel_number, name="Signal Generator Channel"):
        self.instrument = instrument
        self.name = name
        self.number = int(channel_number)
        self.phase_changed = Signal()
    # -------------------------------------------
    def set_parameter(self, parameter_name, parameter_value):
        if parameter_name == "waveform":
            self.set_waveform(parameter_value)
        elif parameter_name == "frequency":
            self.set_frequency(parameter_value)
        elif parameter_name == "amplitude":
            self.set_amplitude(parameter_value)
        elif parameter_name == "offset":
            self.set_offset(parameter_value)
        elif parameter_name == "duty cycle":
            self.set_duty_cycle(parameter_value)
        else:
            error_message = "Trying to set invalid parameter to signal generator '"+self.name+"'." \
                            +"\n Parameter with name "+parameter_name+" was not recognized."
            raise InvalidParameterError(error_message)
    # -------------------------------------------
    def set_waveform(self, waveform):
        command_string = "C"+str(self.number) \
                       + ":BSWV "\
                       + "WVTP," + waveform
        self.instrument.write(command_string)
        self.waveform = waveform
        return command_string
    # -------------------------------------------
    def set_frequency(self, frequency):
        command_string = "C"+str(self.number) \
                       + ":BSWV "\
                      + "FRQ," + str(frequency)
        self.instrument.write(command_string)
        self.frequency = frequency
        return command_string
    # -------------------------------------------
    def set_phase(self, phase, **kwargs):
        """
        :param phase: float
            phase [degrees]
        :return:
        """
        command_string = "C"+str(self.number) \
                       + ":BSWV "\
                      + "PHSE," + str(phase)
        self.instrument.write(command_string)
        self.phase = phase
        self.phase_changed.emit(phase=phase)
        return command_string
    # -------------------------------------------
    def set_amplitude(self, amplitude):
        command_string = "C"+str(self.number) \
                       + ":BSWV "\
                       + "AMP," + str(amplitude)
        self.instrument.write(command_string)
        self.amplitude = amplitude
        return command_string
    # -------------------------------------------
    def set_offset(self, offset):
        command_string = "C"+str(self.number) \
                       + ":BSWV "\
                       + "OFST," + str(offset)
        self.instrument.write(command_string)
        self.offset = offset
        return command_string
    # -------------------------------------------
    def set_duty_cycle(self, duty_cycle):
        if self.waveform != "SQUARE":
            print("WARNING: did not set duty cycle to signal generator '"+self.name+"' because its waveform is not 'SQUARE'. It is "+self.waveform)
            return            
        command_string = "C"+str(self.number) \
                       + ":BSWV "\
                       + "DUTY," + str(duty_cycle)
        self.instrument.write(command_string)
        self.duty_cycle = duty_cycle
        return command_string
    # -------------------------------------------
    def set_low_level(self, level):
        if self.waveform != "SQUARE":
            print("WARNING: did not set low level to signal generator '"+self.name+"' because its waveform is not 'SQUARE'. It is "+self.waveform)
            return
        command_string = "C" + str(self.number) \
                         + ":BSWV " \
                         + "LLEV," + str(level)
        self.instrument.write(command_string)
        self.low_level = level
        return command_string
    # -------------------------------------------
    def set_high_level(self, level):
        if self.waveform != "SQUARE":
            print("WARNING: did not set high level to signal generator '"+self.name+"' because its waveform is not 'SQUARE'. It is "+self.waveform)
            return
        command_string = "C" + str(self.number) \
                         + ":BSWV " \
                         + "HLEV," + str(level)
        self.instrument.write(command_string)
        self.high_level = level
        return command_string
    # -------------------------------------------
    def get_parameter(self, parameter_type):
        parameter_types = ["waveform", "frequency", "phase", "amplitude", "offset", "low level", "high level", "duty cycle"]
        assert parameter_type in parameter_types,\
        "invalid parameter type. Accepted arguments are %s"%parameter_types
        #answer = self.instrument.write("C%s:BSWV?"%self.number)
        answer = self.instrument.query("C%s:BSWV?" % self.number)
        if parameter_type == "waveform":
            value = answer.split("WVTP")[1].split(",")[1]
        elif parameter_type == "frequency":
            value = answer.split("FRQ")[1].split(",")[1].split("HZ")[0]
        elif parameter_type == "phase":
            value = answer.split("PHSE")[1].split(",")[1]
        elif  parameter_type == "amplitude":
            value = answer.split("AMP")[1].split(",")[1].split("V")[0]
        elif  parameter_type == "offset":
            value = answer.split("OFST")[1].split(",")[1].split("V")[0]
        elif parameter_type == "low level":
            value = answer.split("LLEV")[1].split(",")[1].split("V")[0]
        elif parameter_type == "high level":
            value = answer.split("HLEV")[1].split(",")[1].split("V")[0]
        elif parameter_type == "duty cycle":
            value = answer.split("DUTY")[1].split(",")[1]
        else:
            return
        if parameter_type != "waveform":
            if value != "":
                value = float(value)
            else:
                return
        setattr(self, parameter_type, value)
        return value
    # -------------------------------------------
    '''
    def turn_off(self):
        self.instrument.write("C"+str(self.number)+":OUTP off")
        print("C"+str(self.number)+":OUTP off")
        self.output = "off"

        
    def turn_on(self):
        self.instrument.write("C"+str(self.number)+":OUTP on")
        self.output = "on"
    '''
    # -------------------------------------------
    def enable(self, enabled):
        """
        Same as self.turn_on() and self.turn_off(), depending on the input argument.
        :param enabled: bool
            If true, the channel is enabled.
        :return:
        """
        state = "on"*(enabled==True) + "off"*(enabled==False)
        self.instrument.write("C"+str(self.number)+":OUTP "+state)
        self.output = state
        

