# -*- coding: utf-8 -*-
"""
@author: Maria Leandra
adaptado de: https://github.com/NBLobo/proj-07_login/
"""
from os import system 
import PySimpleGUI as sg

class login:
    def __init__(self):
        # Layout da janela
        sg.theme('BlueMono')
        layout = [
            [sg.Text('Login', font=12, size=(10, 1)), sg.Input(
                key='login', font=12, size=(20, 1))],
            [sg.Text('Senha', font=12, size=(10, 1)), sg.Input(
                key='senha', password_char='*', font=12, size=(20, 1))],
            [sg.Button('Novo Usuário', font=12), sg.Button('Login', font=12),
             sg.Button('Recuperar senha', font=12), sg.Button('Sair', font=12)]
        ]

    # Declarar Janela
        self.janela = sg.Window('BioSleep',layout, font='Any 20')
        self.janela1_ativa = False

    def buscar_usuario(self, login, senha):
        usuarios = []
        try:
            with open('usuarios.txt', 'r+', encoding='Utf-8', newline='') as arquivo:
                for linha in arquivo:
                    linha = linha.strip(",")
                    usuarios.append(linha.split())
    #login, senha = fazer_login()
                for usuario in usuarios:
                    nome = usuario[0]
                    password = usuario[1]
                    if login == nome and senha == password:
                        return True
        except FileNotFoundError:
            return False
        
    def buscar_usuario2(self, login):
        # retorna a senha dado o nome de usuário
        usuarios = []
        try:
            with open('usuarios.txt', 'r+', encoding='Utf-8', newline='') as arquivo:
                for linha in arquivo:
                    linha = linha.strip(",")
                    usuarios.append(linha.split())
    #login, senha = fazer_login()
                for usuario in usuarios:
                    nome = usuario[0]
                    password = usuario[1]
                    if login == nome:
                        return  nome, password
        except FileNotFoundError:
            return False

    # Limpa o Nome do login e a senha digitada na janela

    def limpar(self, login, senha):
        self.janela['login'].update('')
        self.janela['senha'].update('')
        self.janela['login'].SetFocus()
        return

    def Iniciar(self):
        # sg.popup_no_titlebar('Welcome to BioSleep ', font=20, text_color='blue')
        while True:
            eventos, valores = self.janela.read()
            login = self.janela['login'].get()
            senha = self.janela['senha'].get()
            if eventos == sg.WINDOW_CLOSED:
                break
    # Opção 1
            if eventos == 'Novo Usuário':
                if login == senha:
                    sg.popup_no_titlebar(
                        'Sua senha deve ser diferente do nome do usuário.', font=12, text_color='red')
                    self.limpar(valores['login'], valores['senha'])

                else:
                    user = self.buscar_usuario(login, senha)
                    if user == True:
                        sg.popup_no_titlebar('Usuário já existe!',
                                             font='12', text_color='red')
                        self.limpar(valores['login'], valores['senha'])

                    else:

                        with open('usuarios.txt', 'a+', encoding='Utf-8', newline='') as arquivo:
                            arquivo.writelines(f' {login} {senha}\n')
                            sg.popup_no_titlebar(
                                'Novo Usuário Aprovado!', font=12, text_color='blue',)

    # Opção 2
            if eventos == 'Login':
                user = self.buscar_usuario(login, senha)
                if user == True:
                    login = login.capitalize()
                    self.janela.hide() # oculta a janela 
            # Janela de Boas vindas
                    self.janela1_ativa = True
                    layout1 = [
                        [sg.Text(
                            f'{login}, voce esta logado(a).')],
                         [sg.Button('OK')]
                    ]
                    janela1 = sg.Window(' ', layout1, font="Helvetica 14")
                    eventos1, valores1 = janela1.read()
                    if eventos1 == sg.WINDOW_CLOSED or 'OK':
                        
                        self.janela.un_hide()
                        self.limpar(valores['login'], valores['senha'])
                        janela1.close()
                else:
                    sg.popup_no_titlebar('Você deve ter digitado o nome de usuário e/ou a senha errado.\n Por favor verifique.', font=12, text_color='red')
                    self.limpar(valores['login'], valores['senha'])

    # Opção 3
            if eventos == 'Recuperar senha':
                user, senha = self.buscar_usuario2(login)
                if user:
                    sg.popup_no_titlebar(f'Seus dados de Usuário são:\n Usuário: {user} \n senha: {senha} ',font='12', text_color='red')
                    self.janela.hide()
                    self.limpar(valores['login'], valores['senha'])
                else:
                    sg.popup_no_titlebar('O usuário não existe ou os dados estão errados!\n Tente de novo ',font='12', text_color='red')
                    self.janela.hide()
                    self.limpar(valores['login'], valores['senha'])
    # Opção 4
            if eventos == 'Sair':
                sg.popup_no_titlebar('GoodBay!', font='18', text_color='blue')
                # self.janela1.close()
        self.janela.close()
            
if __name__ == "__main__":

    usuario = login()
    usuario.Iniciar()