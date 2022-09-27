#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 17:00:54 2022

@author: jiedz
This module contains utility function for strings.
"""
# In[imports]
# In[]
def remove_duplicates(l):
    l_no_duplicates = []
    for element in l:
        if element not in l_no_duplicates:
            l_no_duplicates.append(element)
    return l_no_duplicates