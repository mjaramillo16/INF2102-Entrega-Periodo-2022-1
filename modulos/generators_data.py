# -*- coding: utf-8 -*-
'''
autor: Maria Leandra
Codigo adaptado de https://github.com/MousaviSajad/SleepEEGNet/
https://github.com/meiwenPKU/SleepNet-Advanced/
'''

import numpy as np
from keras.utils.np_utils import to_categorical
import sys
sys.path.append("C:/Users/hp/Documents/DOUTORADO INF/AULAS DOUTORADO/PROJETO FINAL DE PROGRAMACAO\ENTREGA_FINAL INF2102/modulos/processing_data.py")
import processing_data as prod


def generator(df_files,min_index, max_index, batch_size=256, step=10, num_classes=3,num_patient_per_block=1): 
  '''
  
  input:
      dir_path: the path of the directory which contains all edf files, where features[nsrrid].shape=(k,N,M), k (=1,2) is the number of channels
                N is the number of epochs for one patient, M is the number of features for one epoch
      labels: the labels for each feature vectors
      min_index (max_index): indices of the edf files which are used to generate samples
      shuffle: whether to shuffle the samples or draw them in chronological order
      batch_size: the number of samples per batch
      step: the period, in timesteps, at which you sample feature array.
      
      Description:
      Generator which yields timeseries samples and their labels on the fly
  '''
  if max_index == None:
      max_index = len(df_files)
  start_subject_index = min_index 

  while 1:
    samples = []
    labels = []
    count = 0
    # #read the data from randomly selected num_patient_per_block subjects
    selected_index_nsrrid = np.arange(start_subject_index, min(start_subject_index+num_patient_per_block,max_index))
    for index in selected_index_nsrrid: 
      record_name = df_files.header.values[index][:-4]
      eeg_raw, Fs = prod.adjust_data(record_name) # lista tamanho z/Fs*30 de segmentos de tamanho [1,Fs*30, 6]
      z = len(eeg_raw)
      count+=z

      # if N == N_channels and M == 30*FreqSample:
      cl = prod.adjust_labels(record_name, Fs)
      for i in range(z):
          samples.append(eeg_raw[i][:,::step,:])
          labels.append(cl[i])

    # print(count)
    num_sample = len(samples)
    indexes = np.arange(num_sample)
    np.random.shuffle(indexes)

    for i in range(0,num_sample,batch_size):
        if i+batch_size > num_sample:
            break

        batch_sample = [samples[p] for p in indexes][i:i+batch_size]
        batch_label = np.array([labels[o] for o in indexes][i:i+batch_size])
        # print((np.array(batch_sample)*0.001).shape, to_categorical(batch_label, num_classes=num_classes).shape)
        yield np.array(batch_sample), to_categorical(batch_label, num_classes=num_classes)
                
    start_subject_index += num_patient_per_block
    if start_subject_index >= max_index:
        start_subject_index = min_index


def generator_test(df_files,min_index, max_index, batch_size=256, num_classes=3,step=10,num_patient_per_block=1): 
#   '''
#   generator which yields timeseries samples and their labels on the fly
#   input:
#       df_files: the DataFrame which contains all path files 
#       labels: the labels for each feature vectors
#       min_index (max_index): indices of the edf files which are used to generate samples
#       shuffle: samples in chronological order
#       batch_size: the number of samples per batch
#       step: the period, in timesteps, at which you sample feature array.
#       
#   '''
  if max_index == None:
      max_index = len(df_files)
  start_subject_index = min_index 

  while 1:

    samples = []
    labels = []

    # #read the data from randomly selected num_patient_per_block subjects
    selected_index_nsrrid = np.arange(start_subject_index, min(start_subject_index+num_patient_per_block,max_index))
    for index in selected_index_nsrrid: 
      record_name = df_files.header.values[index][:-4]
      eeg_raw, Fs = prod.adjust_data(record_name)
      z = 300 #len(eeg_raw)
      cl = prod.adjust_labels(record_name, Fs)
      for i in range(z):
          samples.append(eeg_raw[i][:,::step,:])
          labels.append(cl[i])

    
    num_sample = len(samples)
    indexes = np.arange(num_sample)

    for i in range(0,num_sample,batch_size):
        if i+batch_size > num_sample:
            break

        batch_sample = [samples[p] for p in indexes][i:i+batch_size]
        batch_label = np.array([labels[o] for o in indexes][i:i+batch_size])
        # print((np.array(batch_sample)*0.001).shape, to_categorical(batch_label, num_classes=num_classes).shape)
        yield np.array(batch_sample), to_categorical(batch_label, num_classes=num_classes)

    start_subject_index += num_patient_per_block
    if start_subject_index >= max_index:
        start_subject_index = min_index