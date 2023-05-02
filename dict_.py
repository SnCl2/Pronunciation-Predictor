# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 09:18:35 2023

@author: Soumyadip Nag
"""
# Importing dependency
import pandas as pd
# This program return the meaning of a given word from the english Dictionary.csv
dict_path="english Dictionary.csv"
df=pd.read_csv(dict_path)
def show_def(word):
    return df[df["word"]==word]["def"].tolist()

