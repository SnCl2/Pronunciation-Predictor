# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 08:23:58 2023

@author: User
"""

import pyttsx3 as pt



def t_to_s(word):
        speech = pt.init()
        speech.say(word)
        speech.runAndWait()
        speech = None
    
