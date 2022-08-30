# -*- coding: utf-8 -*-
"""
@author: Maria Leandra
adaptado de: https://pysimplegui.readthedocs.io/en/latest/
"""

import os.path
import PySimpleGUI as sg
import sys

sys.path.append("C:/Users/hp/Documents/DOUTORADO INF/AULAS DOUTORADO/PROJETO FINAL DE PROGRAMACAO\ENTREGA_FINAL INF2102/utils_GUI/login.py")
from login import login
sys.path.append("C:/Users/hp/Documents/DOUTORADO INF/AULAS DOUTORADO/PROJETO FINAL DE PROGRAMACAO\ENTREGA_FINAL INF2102/utils_GUI/rede.py")
from rede import rede

def analyzer():
    sg.theme('BlueMono')
    
    layout = [
        [
        sg.Text("Cargar pasta"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse('Upload')],
        [sg.Listbox(values=[], enable_events=True, size=(40, 20),key="-FILE LIST-")],
         [sg.Button("Avaliar" , font=12),sg.Button("sair", font=12)],
        ]
    return sg.Window("Biosleep ", layout, font='Any 20')

def visualizer(AUROC, AUPRC, folder):
    
    sg.theme('BlueMono')

    BORDER_COLOR = '#C7D5E0'
    DARK_HEADER_COLOR = '#1B2838'
    BPAD_LEFT_INSIDE = (0, 10)
    BPAD_RIGHT = ((10,20), (10, 20))

    block_sup = [ [sg.Text( f'Paciente: {folder}', font='Any 18')]
                ]

    block_inf = [
                [sg.Text('Resultados do Análise', font='Any 18',justification='c', text_color='blue')],
                [sg.T(f'AUROC: {AUROC}')],
                [sg.T('AUPRC:  {AUPRC}' )],
                [sg.T('Total de eventos RERA encontrados: ')],
                [sg.T('Total de eventos asociados a Apnea/ Hipopneia encontrados: ')]
                ]

    layout = [

               [sg.Column(block_sup, size=(500, 320), pad=BPAD_LEFT_INSIDE)],
               [sg.Column(block_inf, size=(500, 150), pad=BPAD_RIGHT)],
               [sg.Button('Salvar'),sg.Button('Novo Paciente'), sg.Button('Sair')],]

    return sg.Window('BioSleep', layout, font='Any 20',background_color=BORDER_COLOR)

# criar as janelas iniciais
janela1, janela2 = analyzer(), None

while True:
        usuario = login()
        usuario.Iniciar()
          
        window, event, values = sg.read_all_windows() 
    
        # quando janela for fechada
        if window == janela1 and event == sg.WINDOW_CLOSED:
            break
        
        if window == janela1: 
            if event == "-FOLDER-":
            
                folder = values["-FOLDER-"]
                try:
                    file_list = os.listdir(folder)
                except:
                    file_list =[]
                
                fnames = [f for f in file_list 
                          if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".hea",".mat"))]
                window["-FILE LIST-"].update(fnames)
                
            elif  event == "-FILE LIST-":
                try:
                    filename = os.path.join(
                        values["-FOLDER-"], values["-FILE LIST-"][0]
                    )
                except:
                    pass
                
            if event == 'Avaliar':
                    
               model = 'C:/Users/hp/Documents/DOUTORADO INF/AULAS DOUTORADO/PROJETO FINAL DE PROGRAMACAO/ENTREGA_FINAL INF2102/pesos/cnn1_t1.hdf5' 
               sg.popup_no_titlebar('avaliando Por favor espere!!....')
               cnn = rede(folder, model)
               AUROC, AUPRC = cnn.evaluate_model()
                
            if event == "Sair":
            #     # sg.popup_no_titlebar('GoodBay!', font='18', text_color='blue')
                janela1.close()   
            
        # quando queremos ir para a proxima janela

        janela2 = visualizer(AUROC,AUPRC,folder)
        cnn.predict_model(save_fig=True)
        janela1.hide()
            
        # quando queremos voltar para janela anterior   
        if window == janela2 and event == 'Novo Paciente':
            janela2.hide()
            janela1.un_hide()
        
        if window == janela2 and event == 'Sair' or event == sg.WIN_CLOSED:
            sg.popup_no_titlebar('GoodBay!', font='18', text_color='blue')
            janela2.close()
            
        window.close()

