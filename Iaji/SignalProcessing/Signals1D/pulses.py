#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 21:38:27 2022

@author: jiedz

This module defines a pulse and pulse train, with their related properties
"""
# In[imports]
import numpy
from matplotlib import pyplot
from Iaji.Mathematics.Parameter import Parameter
import sympy
sympy.init_printing()
# In[Global constants]
PEAK_TYPES = ["flat", "exp"]
WINDOW_TYPES = ["rect", "trapz", "exp"]
# In[Pulse]
class Pulse(Parameter):
    def __init__(self):
        super().__init__()    
    #-----------------------
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
    def set_shape_standard(self, start, stop, peak_type:str=None, window_type:str="rect", **params):
        if peak_type is not None:
            assert peak_type in PEAK_TYPES, \
                "%s is not a supported peak type: \n %s"%(peak_type, PEAK_TYPES)
        if window_type is not None:
            assert window_type in WINDOW_TYPES, \
                "%s is not a supported window type: \n %s"%(window_type, WINDOW_TYPES)
        #Window types
        x = self.symbolic.expression_symbols[0]
        if window_type == "rect":     
            self.window_shape = sympy.Piecewise((0, x<=start), \
                                                 (1, (x>start) & (x<=stop)), \
                                                     (0, x>stop))
        elif window_type == "trapz":
            assert "rise" in list(params.keys()) and "fall" in list(params.keys()), \
                "'trapz' window type requires 'rise' and 'fall' values for the independent variable"
            rise = params["rise"]
            fall = params["fall"]
            self.window_shape = sympy.Piecewise((0, x<=start), \
                                                ((x-start)/rise, (x>start) & (x<=start+rise)), \
                                                 (1, (x>start+rise) & (x<=stop-fall)), \
                                                     (1-(x-(stop-fall))/fall, (x>stop-fall) & (x<stop)), \
                                                         (0, x>=stop))
        elif window_type == "exp":
            assert "rise" in list(params.keys()) and "fall" in list(params.keys()), \
                "'exp' window type requires 'rise' and 'fall' values for the independent variable"
            rise = params["rise"]
            fall = params["fall"]
            epsilon = 1e-6
            f = (epsilon)**((start+rise)/rise) * sympy.exp(-1/rise*sympy.log(epsilon)*x)
            g = (epsilon)**(-(stop-fall)/fall) * sympy.exp(1/fall*sympy.log(epsilon)*x)
            self.window_shape = sympy.Piecewise((0, x<=start), \
                                                (f, (x>start) & (x<= start+rise)), \
                                                 (1, (x>start+rise) & (x<=stop-fall)), \
                                                     (g, (x>stop-fall) & (x<stop)), \
                                                         (0, x>=stop))
        self.peak_shape = 1
        #Peak type
        if peak_type == "exp":
            assert "initial_level" in list(params.keys()) and "final_level" in list(params.keys()), \
                "'exp' peak type requires 'initial_level' and 'final_level' values for the dependent variable"
            initial_level = params["initial_level"]
            final_level = params["final_level"]
            if window_type == "rect":
                rise = fall = 0
            a = 1/(stop-start-(fall+rise))*sympy.log(final_level/initial_level)
            b = initial_level*sympy.exp(-a*(start+rise))
            p = b*sympy.exp(a*x)
            self.peak_shape *= sympy.Piecewise((initial_level, x<=start+rise), \
                                                 (p, (x>start+rise) & (x<=stop-fall)), \
                                                     (final_level, x>stop-fall))
        self.symbolic.expression = self.peak_shape*self.window_shape
    #----------------------
    def plot(self, x1, x2, n_points:int=1000, fs:float=None, axis=None, color="tab:purple"):
        if axis is None:
            axis = pyplot.figure().add_subplot(111)
        axis.plot(*self.sample(x1, x2, n_points=n_points, fs=fs), marker=".", color=color)
        axis.grid(True)
        return axis
    #----------------------
    def sample(self, x1, x2, n_points:int=1000, fs:float=None):
        if fs is not None:
            dt = 1/fs
            n_points = int(numpy.floor((x2-x1)/dt))
        x = numpy.linspace(x1, x2, n_points)
        if self.symbolic.numeric_evaluation_module == "numpy":
            y = self.symbolic.expression_lambda(x)
        else:
            y = numpy.array([float(self.symbolic.expression_lambda(x0)) for x0 in x])
        return x, y
        