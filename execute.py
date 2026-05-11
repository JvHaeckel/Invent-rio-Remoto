import customtkinter as ctk
from tkinter import messagebox
import socket       # é usado para rede/comunicação, pegar o nome do computador na rede
import platform     # pega informações do sistema operacional
import wmi        # SIgnifica Windows Management Instrumentation - API oficial do Windows para administração

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def cadastrar():

    nome_usuario = nome.get()
    sobrenome_usuario = sobrenome.get()
    setor_usuario = setor.get()

    c = wmi.WMI()

    serial = c.Win32_BIOS()[0].SerialNumber
    modelo = c.Win32_ComputerSystem()[0].Model
    # fabricante = c.Win32_ComputerSystem()[0].Manufacturer COLOCAR??

    hostname = socket.gethostname()  # pega nome da máquina no Windows
    windows = platform.platform()    # pega SO
    sistema = platform.system()      # pega nome do sistema
    processador = platform.processor()    # pega o processador
    arquitetura = platform.architecture() # versão 32 ou 64bits
    ram = round(
    int(c.Win32_ComputerSystem()[0].TotalPhysicalMemory) / (1024**3)
)
    


    info = f"""
Nome: {nome_usuario}
Sobrenome: {sobrenome_usuario}
Setor: {setor_usuario}

Hostname: {hostname}
Sistema: {sistema}
Processador: {processador}
Arquitetura: {arquitetura}
Ram:{ram}
Serial: {serial}
Modelo: {modelo}
Windows: {windows}
"""

    messagebox.showinfo("Dados coletados", info)

janela = ctk.CTk()
janela.geometry("300x250")
janela.title("Rodotur TI")

titulo = ctk.CTkLabel(
    janela,
    text="Cadastro Máquinas",
    font=("Arial", 20)
)
titulo.pack(pady=10)

nome = ctk.CTkEntry(
    janela,
    placeholder_text="Nome",
    width=200
)
nome.pack(pady=8)

sobrenome = ctk.CTkEntry(
    janela,
    placeholder_text="Sobrenome",
    width=200
)
sobrenome.pack(pady=8)

setor = ctk.CTkEntry(
    janela,
    placeholder_text="Setor",
    width=200
)
setor.pack(pady=8)

botao = ctk.CTkButton(
    janela,
    text="Cadastrar",
    font=("Arial",16),
    command=cadastrar
)

botao.pack(pady=12)

janela.mainloop()