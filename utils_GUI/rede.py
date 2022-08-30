# -*- coding: utf-8 -*-
"""
autor: Maria Leandra
'''
Codigo adaptado de https://github.com/MousaviSajad/SleepEEGNet/
https://github.com/meiwenPKU/SleepNet-Advanced/
'''

"""

import numpy as np
from numpy.random import seed
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten,Conv2D, BatchNormalization,MaxPooling2D, ReLU
import tensorflow as tf
import sys
sys.path.append("C:/Users/hp/Documents/DOUTORADO INF/AULAS DOUTORADO/PROJETO FINAL DE PROGRAMACAO/ENTREGA_FINAL INF2102/modulos/generators_data.py")
sys.path.append("C:/Users/hp/Documents/DOUTORADO INF/AULAS DOUTORADO/PROJETO FINAL DE PROGRAMACAO/ENTREGA_FINAL INF2102/modulos/processing_data.py")
sys.path.append("C:/Users/hp/Documents/DOUTORADO INF/AULAS DOUTORADO/PROJETO FINAL DE PROGRAMACAO/ENTREGA_FINAL INF2102/modulos/plot_results.py")

import generators_data as gene
import plot_results as pr
import processing_data as prod

# gera números pseudo-aleatórios. Garante reprodutibilidade no experimento
seed(7)

class rede():
    '''
    Input:
    filename = Path the folder with patient files [string]
    model_file = Path the model weights [.hdf5 format]
    
    This class contains the deep neural network architecture
    and associated functions that allow analysis of EEG signals.
    * model(): network architecture
    * evaluate_model(): allows you to evaluate the data using the
    Keras model.evaluate function
    *predict_model(): allows to predict data using keras model.predict,
    in addition to including the calculation of custom metrics such as 
    the confusion matrix, AUROC and AUPRC
        '''
    def __init__(self, filename, model_file):

        self.rootDir = filename
        self.model_file = model_file
    
    def model(self):
        
        window = 30
        Fs= 200
        step= 2
     
        conv = Sequential(name='cnn')
        conv.add(Conv2D(32, (1,3), activation = 'relu',padding = 'same', input_shape = (1, window*Fs//step, 6)))
        conv.add(MaxPooling2D(pool_size=(1,2)))
        conv.add(Conv2D(64, (1,3), activation = 'relu'))
        conv.add(MaxPooling2D(pool_size=(1,2)))
        conv.add(Conv2D(128, (1,3), activation = 'relu'))
        conv.add(MaxPooling2D((1,2)))
        conv.add(Conv2D(256, (1,3), activation = 'relu'))
        conv.add(MaxPooling2D(1,2))
        conv.add(Flatten())
        conv.add(Dense(128, activation = 'linear'))
        conv.add(BatchNormalization())
        conv.add(ReLU())
        conv.add(Dense(3, activation = 'sigmoid'))
        conv.summary()
          
        conv.compile(loss='binary_crossentropy', optimizer='adam',
                     metrics=['acc', tf.keras.metrics.AUC(num_thresholds=1000, name='AUCROC'),
                            tf.keras.metrics.AUC(num_thresholds=1000,curve='PR', 
                                                 name='AUPRC')])
      # carga o arquivo de pesos da rede 
        conv.load_weights(self.model_file)
    
        return conv
      
    """# ** Funções para Testar o modelo**"""
    
    def evaluate_model(self):
        
        conv = self.model()
        files = prod.get_files(self.rootDir)
        np.random.seed(seed=0)
        test_data = gene.generator_test(files,min_index=0, max_index=1,batch_size=128, step=2)
        scores_test = conv.evaluate(test_data,verbose=0)
        
        # print('Test Accuracy Performance:', scores_test[1])
        # print('Test loss Performance:' , scores_test[0])
        return scores_test[2], scores_test[3]
    
    def predict_model(self, save_fig):
        
        conv = self.model()
        files = self.load_data(self.rootDir)
        
        np.random.seed(seed=0)
        test_data = gene.generator_test(files,min_index=0, max_index=1,batch_size=128, step=2)
        predict = conv.predict_generator(test_data)

        np.random.seed(seed=0)
        test_data = gene.generator_test(files, min_index=0,max_index=1,batch_size=128, step=2)
        labels = []   # store all the generated label batches
        # maximum number of iterations, in each iteration one batch is generated; 
        # the proper value depends on batch size and size of whole data
        # steps por epoca para cada conjunto
        
        # steps_te = prod.contador(files)//128
        max_iter = 300 #steps_te
        
        h = 0
        for d, l in test_data:
            for j in range(128):
              labels.append(l[j])
            h += 1
            if h == max_iter:
                break
        
        y_true = np.array(labels) # categorical
        print(y_true.shape, predict.shape)
        
        pr.mis_metricas(predict, y_true, self.rootDir, save_fig=save_fig)
        
        
if __name__ == "__main__":
    
    path = 'C:/Users/hp/Documents/DOUTORADO INF/AULAS DOUTORADO/PROJETO FINAL DE PROGRAMACAO/ENTREGA_FINAL INF2102/data/tr03-0005'
    model = 'C:/Users/hp/Documents/DOUTORADO INF/AULAS DOUTORADO/PROJETO FINAL DE PROGRAMACAO/ENTREGA_FINAL INF2102/pesos/cnn1_t1.hdf5' 
    cnn = rede(path, model)
    AUROC, AUPRC = cnn.evaluate_model()
    cnn.predict_model(save_fig=True)