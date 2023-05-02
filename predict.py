# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 13:19:26 2023

@author: Soumyadip Nag
"""
import numpy as np
from tensorflow.keras.models import  Model
from tensorflow.keras.layers import Embedding, Input, LSTM, Dense
import pickle


char_vocab_size = 37
phone_vocab_size = 78
max_len_op = 30
# Loading the importent component of the model

# Tokenizer for the word (word to char)
with open('char_tokenizer.pickle', 'rb') as handle:
    char_tokenizer = pickle.load(handle)
# Tokenizer for the Pronunciation (word to char)
with open('phone_tokenizer.pickle', 'rb') as handle:
    phone_tokenizer = pickle.load(handle)
# Creating the components of Encoder
char_input = Input(shape=(None,))
x = Embedding(char_vocab_size, 256, mask_zero=True)(char_input)
x=LSTM(128, return_sequences=True)(x)
output_y, state_h, state_c = LSTM(256, return_state=True)(x)

# Creating the components of Decoder
ph_input = Input(shape=(None,))
embedding_layer = Embedding(phone_vocab_size, 256, mask_zero=True)
x = embedding_layer(ph_input)
decoder_lstm = LSTM(256, return_sequences=True, return_state=True)
output_y, _ , _ = decoder_lstm(x, initial_state=[state_h, state_c])
softmax_dense = Dense(phone_vocab_size, activation='softmax')
output = softmax_dense(output_y)

model = Model(inputs=[char_input, ph_input],outputs=output)


#load weights of the model
model.load_weights("model.h5")
# Encoder
encoder = Model(char_input, [state_h, state_c])

# Decoder
decoder_input_h = Input(shape=(256,))
decoder_input_c = Input(shape=(256,))
x = embedding_layer(ph_input)
x, decoder_output_h, decoder_output_c = decoder_lstm(x, initial_state=[decoder_input_h, decoder_input_c])
x = softmax_dense(x)
decoder = Model([ph_input] + [decoder_input_h, decoder_input_c], 
                                [x] + [decoder_output_h, decoder_output_c])
# Main code for prediction
def predict_pronunciation(ch_input):
    # Lowering the input
    ch_input=ch_input.lower()
    # Tokenizing the input
    input_seq = char_tokenizer.texts_to_sequences([ch_input])
    # Axising the cell state and hidden state of the incoder
    next_h, next_c = encoder.predict(input_seq,verbose=0)
    # Creating the start cockne
    curr_token = np.zeros((1,1))
    curr_token[0][0] = phone_tokenizer.word_index['startseq']

    pred_sentence = ''
    
    # Decoder Loop
    for i in range(max_len_op):
        output, next_h, next_c = decoder.predict([curr_token] + [next_h, next_c],verbose=0)
        next_token = np.argmax(output[0, 0, :])
        next_word = phone_tokenizer.index_word[next_token]
        if next_word == 'endseq':
            break
        else:
            pred_sentence += ' ' + next_word
            curr_token[0] = next_token

    return pred_sentence

