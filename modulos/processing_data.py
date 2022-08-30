# -*- coding: utf-8 -*-
'''
Codigo adaptado de https://github.com/MousaviSajad/SleepEEGNet/
https://github.com/meiwenPKU/SleepNet-Advanced/
'''


import numpy as np
import wfdb
import h5py
import pandas as pd
import os
import gc

def find(condition):
    ''' -----------------------------------------------------------------------------
    Procura valores dada uma condição.
    ''' 
    res, = np.nonzero(np.ravel(condition))
    return res
  
def import_data(file_name): 

    ''' -----------------------------------------------------------------------------
    input: 'dirName'
    output: matriz de tamanho [n_samples,6], frequencia de amostragem (int) e tamanho do
    registro (float).
    
    Retorna um array com os registros de 6 channels EEG, a Frequencia de amostragem Fs
     e o tamanho do registro
    # # exem> file_name = '/data/training/tr03-0005/tr03-0005'
       ''' 
    
    this_data, fields = wfdb.io.rdsamp(file_name, channels=[0,1,2,3,4,5])
    Fs = fields['fs']
    n_samples = fields['sig_len']
    return this_data, Fs, n_samples #saida [n_samples,6]

 
def import_arousals(file_name): 
    ''' -----------------------------------------------------------------------------
    input: 'dirName'
    output: matriz de tamanho [n_samples,1], 
    Importe o vetor de labels, dado o nome do arquivo.
    e.g. /data/tr04-0808/tr04-0808
    ''' 
    # Importa os aurosals do registro
    file_name = file_name + '-arousal.mat'
    f = h5py.File(file_name, 'r') 
    arousals = np.array(f['data']['arousals'])
    return arousals 

def get_files(rootDir): 
    ''' -----------------------------------------------------------------------------
      input: 'dirName' (e.g. ./data/tr04-0808/)
      output: DataFrame 
      Dado o nome do arquivo, extrai os caminhos dos arquivos con extensões .mat, .hea 
      e .arousal e os salva num frame
      
      ''' 
    header_loc, arousal_loc, signal_loc = [], [], []
      # rootDir = 'C:/Users/hp/Documents/Modelos_tesis/data/training'/  'content/drive/My Drive/data/training'
      # rootDir = rootDir
      
    for dirName, subdirList, fileList in os.walk(rootDir, followlinks=True):
    # print(filelist)
        for fname in fileList:
            if '.hea' in fname:
                header_loc.append(dirName + '/' + fname)
            if '-arousal.mat' in fname:
                arousal_loc.append(dirName + '/' + fname)
            if 'mat' in fname and 'arousal' not in fname:
                signal_loc.append(dirName + '/' + fname)
        
    # combine into a data frame
    data_locations = {'header':      header_loc,
                  'arousal':     arousal_loc,
                  'signal':      signal_loc, 
                  }
    
    # Convert to a data-frame
    df = pd.DataFrame(data=data_locations, columns=['header', 'arousal','signal'])
    return df


def adjust_data(record_name):
    '''------------------------------------------------------------------------------------------
    input: file name
    output: EEG record segmentado  (Lista de arrays com tamanhos [1,Fs*30, 6])
    
    Ajusta o registro de dados para que seja compativel com a entrada aceita pela rede neural
    '''
    x = []
    eeg_raw,Fs,N = import_data(record_name) #[len_data,6]
    eeg_raw = np.expand_dims(eeg_raw, axis=0) # [1,len_data, 6]
    # eeg_raw = eeg_raw.reshape(1,1,eeg_raw.shape[0],6) #[1,1,len_data, 6] caso precisar 4 dimensões
    n_samples = 30*Fs
    for k in range(0, (N-n_samples+1), n_samples):
       # data = eeg_raw[:,:,k:k+n_samples,:] # 4 dim
       data = eeg_raw[:,k:k+n_samples,:]
       x.append(data)
    return x, Fs #saida:lista tamanho N/Fs*30 de segmentos de tamanho [1,Fs*30, 6]

def adjust_labels(record_name, Fs):
    '''------------------------------------------------------------------------------------------
        input: file name e frequencia de amostragem (Fs)
        output: EEG record segmentado  (Lista de arrays com tamanhos [1,Fs*30/n_samples])
        
        Ajusta os labels de dados para que sejam compativeis com a entrada aceita pela rede neural
    '''
    y = []
    labels = import_arousals(record_name)
    n_samples = 30*Fs
         
    for k in range(0, (labels.shape[0]-n_samples+1), n_samples):
           clas = np.max(labels[k:k+n_samples])
           y.append(clas)
        
    return y # l es en formato np., Y en lista

def contador(df_files):
   '''------------------------------------------------------------------------------------------
        input: file name e frequencia de amostragem (Fs)
        output: EEG record segmentado  (Lista de arrays com tamanhos [1,Fs*30/n_samples])
        
        Ajusta os labels de dados para que sejam compativeis com a entrada aceita pela rede neural
        ''' 
   cont = 0
     # For each subject in the DataFrame_files set...
   for i in range(0, np.size(df_files, 0)):
        gc.collect()
        record_name = df_files.header.values[i][:-4]
        # print(record_name)
        signal_names, Fs, n_samples = import_data(record_name)
        cont += (n_samples//(Fs*30))
   return cont

