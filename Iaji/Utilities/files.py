#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 14:11:40 2022

@author: jiedz
This module contains useful functions to deal with data loading and saving
"""
# In[imports]
from PyQt5.QtWidgets import QFileDialog
import os
# In[Loading data with a GUI]
def select_directory(start_directory=None, title="Select directory"):
    """
    INPUTS
    -----------
    start_directory : str
        the absolute path of the starting directory.
    """
    if start_directory is None:
        start_directory = os.getcwd()
    #Let the user choose a different data path, if needed.
    #--------------------------------
    directory = QFileDialog.getExistingDirectory(caption=title, directory=start_directory)
    return directory
#--------------------------------
def select_file(start_directory=None, title="Select file"):
    """
    INPUTS
    -----------
    start_directory : str
        the absolute path of the starting directory.
    """
    if start_directory is None:
        start_directory = os.getcwd()
    #Let the user choose a different data path, if needed.
    #--------------------------------
    file_path = QFileDialog.getOpenFileName(caption=title, directory=start_directory)[0]
    return file_path