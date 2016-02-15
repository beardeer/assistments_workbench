# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 10:51:58 2015

@author: xxiong
"""

import os
import ConfigParser

config = ConfigParser.ConfigParser()
current_folder = os.path.dirname(os.path.realpath(__file__))
config.read(current_folder + '/config.ini')