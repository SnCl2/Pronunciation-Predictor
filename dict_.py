# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 09:18:35 2023

@author: User
"""
import pandas as pd
dict_path="english Dictionary.csv"
df=pd.read_csv(dict_path)

def show_def(word):
    return df[df["word"]==word]["def"].tolist()

