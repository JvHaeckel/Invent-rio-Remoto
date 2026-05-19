import customtkinter as ctk
from tkinter import messagebox
import socket                 # é usado para rede/comunicação, pegar o nome do computador na rede
import platform               # pega informações do sistema operacional
import wmi                    # SIgnifica Windows Management Instrumentation - API oficial do Windows para administração (mais confiável)


ctk.set_appearance_mode("dark")  # define o tema escuro da interface
ctk.set_default_color_theme("blue") # define a cor padrão dos componentes


def cadastrar(): # função executada quando clicar no botão cadastrar

    nome_usuario = nome.get() # pega o nome digitado no campo nome
    sobrenome_usuario = sobrenome.get() # pega o sobrenome digitado
    setor_usuario = setor.get()    # pega o setor digitado
    
    hostname = socket.gethostname()  # pega nome da máquina no Windows na rede
    sistema = platform.system()      # pega nome do sistema

    c = wmi.WMI()    # abrir conexão com o inventário interno do Windows


    windows_version = c.Win32_OperatingSystem()[0].Version    # pega SO TÉCNICO (colocamos zero pq retorna uma lista com apenas 1 item e queremos o primeiro)
    windows = c.Win32_OperatingSystem()[0].Caption            # pega nome do Windows amigável
    processador = c.Win32_Processor()[0].Name    # pega o processador
    placa_video = c.Win32_VideoCOntroller()[0].Name      # pega a placa de video

    ram = round( # pega a memória RAM total em bytes e converte para GB
    int(c.Win32_ComputerSystem()[0].TotalPhysicalMemory) / (1024**3)
)
    arquitetura_so = c.Win32_OperatingSystem()[0].OSArchitecture # versão 32 ou 64bits, coloca esse zero no fim pq deixa menos feio nas infos
    arquitetura_pc = c.Win32_Processor()[0].AddressWidth  # arquitetura do hardware/processador
   
    serial_bios = c.Win32_BIOS()[0].SerialNumber # serial da BIOS da máquina
    serial_chassi = c.Win32_SystemEnclosure()[0].SerialNumber # serial do Hardware
    
    modelo = c.Win32_ComputerSystem()[0].Model # pega o modelo do computador/notebook
    fabricante = c.Win32_ComputerSystem()[0].Manufacturer # COLOCAR??
    cores = c.Win32_Processor()[0].NumberOfCores
    
    # cria o texto formatado com todas as informações coletadas
    info = f"""
Nome: {nome_usuario}
Sobrenome: {sobrenome_usuario}
Setor: {setor_usuario}
Hostname: {hostname}
Sistema: {sistema}
Windows : {windows}
Windows Version: {windows_version}
Processador: {processador}
Ram: {ram} GB
Placa de Vídeo: {placa_video}
Core: {cores}
Arquitetura SO: {arquitetura_so}
Arquitetura PC: {arquitetura_pc} bits
Serial Chassi: {serial_chassi}
Serial Bios: {serial_bios}
Modelo: {modelo}
Fabricante: {fabricante}
"""

    messagebox.showinfo("Dados coletados", info) # exibe uma caixa mostrando os dados coletados


janela = ctk.CTk() # cria a janela do programa
janela.geometry("300x250") #  tamanho da janela
janela.title("Rodotur TI") #  título da janela

titulo = ctk.CTkLabel(  # cria o texto do título
    janela,
    text="Cadastro Máquinas",
    font=("Arial", 20)
)
titulo.pack(pady=10)  # posiciona o título na janela

nome = ctk.CTkEntry(  # cria o campo de entrada do nome
    janela,
    placeholder_text="Nome",
    width=200
)
nome.pack(pady=8) # posiciona o campo nome

sobrenome = ctk.CTkEntry( # cria o campo de entrada do sobrenome
    janela,
    placeholder_text="Sobrenome",
    width=200
)
sobrenome.pack(pady=8) # posiciona o campo sobrenome

setor = ctk.CTkEntry( # cria o campo de entrada do setor
    janela,
    placeholder_text="Setor",
    width=200
)
setor.pack(pady=8) # posiciona o campo setor

botao = ctk.CTkButton( # cria o botão cadastrar
    janela,
    text="Cadastrar",
    font=("Arial",16),
    command=cadastrar
)
botao.pack(pady=12) # posiciona o botão na janela

janela.mainloop() # mantém a janela aberta executando o loop principal