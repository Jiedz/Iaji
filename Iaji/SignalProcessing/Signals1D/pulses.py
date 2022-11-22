#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 21:38:27 2022

@author: jiedz

This module defines a pulse and pulse train, with their related properties
"""
# In[imports]
import numpy
import matplotlib
from matplotlib import pyplot
from Iaji.Mathematics.Parameter import Parameter
import sympy
# In[Global constants]
PEAK_TYPES = ["flat", "exp"]
WINDOW_TYPES = ["rect", "trapz", "exp"]
# In[Pulse]
class Pulse(Parameter):
    def __init__(self):
        super().__init__()    
    #-----------------------
    def plot(self, x1, x2, n_points:int=1000, axis=None, color="tab:purple"):
        if axis is None:
            axis = pyplot.figure().add_subplot(111)
        x = numpy.linspace(x1, x2, n_points)
        axis.plot(x, self.symbolic.expression_lambda(x), marker=".", color=color)
        axis.grid(True)
        return axis
    #----------------------
    def set_shape_free(self, shape:str=None, **kwargs):
        '''
        INPUTS
        ---
        shape: string containing the mathematical expression of the pulse. The independent variable must be denoted as 'x'
        **kwargs:
                peak_shape: string containing the mathematical expression of the shape of the pulse's peak
                window_shape: string containing the mathematical expression of the window that multiplies the peak shape function
        '''  
        if shape is not None:
            self.symbolic.expression = sympy.sympify(shape)
        else:
            assert "peak_shape" in list(kwargs.keys()) \
                or "window_shape" in list(kwargs.keys()), \
                    "Either 'peak_shape' or 'window_shape' arguments must be specified"
            self.peak_shape, self.window_shape = (1, 1)
            if "peak_shape" in list(kwargs.keys()):
                self.peak_shape *= sympy.sympify(kwargs["peak_shape"])
            if "window_shape" in list(kwargs.keys()):  
                self.window_shape *= sympy.sympify(kwargs["window_shape"])
            self.symbolic.expression = self.peak_shape*self.window_shape
    #----------------------
    def set_shape_standard(self, start, stop, peak_type:str=None, window_type:str=None, **params):
        if peak_type is not None:
            assert peak_type in PEAK_TYPES, \
                "%s is not a supported peak type: \n %s"%(peak_type, PEAK_TYPES)
        if window_type is not None:
            assert window_type in WINDOW_TYPES, \
                "%s is not a supported window type: \n %s"%(window_type, WINDOW_TYPES)
        #self.window_shape = sympy.sympify("heaviside(x+%f, 1)-heaviside(x+%f, 1)"%(stop, start))
        #Take care of the window types
        if window_type == "trapz":
            assert "rise" in list(params.keys()) and "fall" in list(params.keys()), \
                "'trapz' window type requires 'rise' and 'fall' values for the independent variable"
            rise = params["rise"]
            fall = params["fall"]
            x = self.symbolic.expression_symbols[0]
            self.window_shape = sympy.Piecewise(((x-start)/rise, (x>start) & (x< start+rise)), \
                                                 (1, (x>start+rise) & (x<stop-fall)), \
                                                     (1-(x-(stop-fall))/fall, (x>stop-fall) & (x<stop)))
            
        self.peak_shape = 1
        self.symbolic.expression = self.peak_shape*self.window_shape
        #ciao
           
        