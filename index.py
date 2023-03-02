# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 15:38:33 2023

@author: User
"""


import streamlit as st
from  text_to_speech import t_to_s
from dict_ import show_def
from predict import predict_pronunciation





def predict_page():
    st.title("Hi I am Soumyadip !!!")
    word = st.text_input('What is the word',"Pizza").lower()
    mike = st.button("o<=")
    ok = st.button("Submit")

    if mike:
        t_to_s(word)
    if ok:
        text = predict_pronunciation(word)
        st.subheader(f"Pronunciation:{text}")
        st.subheader(f"The meaning of {word} is")
        if show_def(word):
            st.subheader("\n".join(show_def(word)))
        else:st.subheader("Not in my dictionary")



