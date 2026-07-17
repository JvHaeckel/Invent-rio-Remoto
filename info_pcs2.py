# Código de TESTE do executável aqui eu faço as alterações e testo para depois enviar ao info_pcs ( O executável foi feito em cima do inf_pcs2)


import customtkinter as ctk
from tkinter import messagebox
import socket                 # é usado para rede/comunicação, pegar o nome do computador na rede
import platform               # pega informações do sistema operacional
import wmi                    # SIgnifica Windows Management Instrumentation - API oficial do Windows para administração (mais confiável)
import requests               # requisição para externo ness
import traceback
import os
from datetime import datetime

ctk.set_appearance_mode("dark")  # define o tema escuro da interface
ctk.set_default_color_theme("blue") # define a cor padrão dos componentes

def log(mensagem):
    try:
        caminho_log = os.path.join(
            os.path.expanduser("~"),
            "Documents",
            "inventario_log.txt"
        )

        with open(caminho_log, "a", encoding="utf-8") as arquivo:
            data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            arquivo.write(f"[{data}] {mensagem}\n")

    except:
        pass


def cadastrar(): # função executada quando clicar no botão cadastrar

    try:

       
        log("====================================")
        log("Iniciando cadastro")
        nome_usuario = nome.get().upper().strip()           # pega o nome digitado no campo nome
        sobrenome_usuario = sobrenome.get().upper().strip() # pega o sobrenome digitado
        setor_usuario = setor.get().upper().strip()         # pega o setor digitado
        
        if  nome_usuario =="" or sobrenome_usuario =="" or setor_usuario =="": 
            messagebox.showerror(
                "Erro",
                "Preencha todos os campos"
            )
            return

        hostname = socket.gethostname()  # pega nome da máquina no Windows na rede
        sistema = platform.system()      # pega nome do sistema

        log(f"Hostname: {hostname}")
        log(f"Sistema: {sistema}")

        c = wmi.WMI()    # abrir conexão com o inventário interno do Windows
        log("Conectado ao WMI")

        windows_version = c.Win32_OperatingSystem()[0].Version    # pega SO TÉCNICO (colocamos zero pq retorna uma lista com apenas 1 item e queremos o primeiro)
        windows = c.Win32_OperatingSystem()[0].Caption            # pega nome do Windows amigável
        log(f"Windows: {windows}")
        log(f"Versão: {windows_version}")

        processador = c.Win32_Processor()[0].Name    # pega o processador
        log(f"Processador: {processador}")

        placa_video = c.Win32_VideoController()[0].Name      # pega a placa de video
        log(f"Placa de vídeo: {placa_video}")

        disco = c.Win32_DiskDrive()[0]
        modelo_disco = disco.Model.upper()
        if disco.Size:                                            # tive que fazer esse tratamento pq ao tentar converter e não conseguir ele travava o Executável
            tamanho_disco = round(int(disco.Size) / (1024**3)) 
        else:
            tamanho_disco = ""

        log(f"Modelo Disco: {modelo_disco}")
        log(f"Tamanho Disco: {tamanho_disco}")

        cores = c.Win32_Processor()[0].NumberOfCores
        threads = c.Win32_Processor()[0].NumberOfLogicalProcessors
        log(f"Cores: {cores}")
        log(f"Threads: {threads}")

        memoria = c.Win32_ComputerSystem()[0].TotalPhysicalMemory
        if memoria:
            ram = round(int(memoria) / (1024**3))
        else:
            ram = ""

        log(f"RAM: {ram}")
            
        arquitetura_so = c.Win32_OperatingSystem()[0].OSArchitecture # versão 32 ou 64bits, coloca esse zero no fim pq deixa menos feio nas infos
        arquitetura_pc = c.Win32_Processor()[0].AddressWidth  # arquitetura do hardware/processador
    
        serial_bios = c.Win32_BIOS()[0].SerialNumber # serial da BIOS da máquina
        serial_chassi = c.Win32_SystemEnclosure()[0].SerialNumber # serial do Hardware
        
        modelo = c.Win32_ComputerSystem()[0].Model # pega o modelo do computador/notebook
        fabricante = c.Win32_ComputerSystem()[0].Manufacturer # COLOCAR??
        
        log(f"Modelo: {modelo}")
        log(f"Fabricante: {fabricante}")
        log(f"Serial BIOS: {serial_bios}")
        log(f"Serial Chassi: {serial_chassi}")
                
        
        dados = {
            "nome": nome_usuario,
            "sobrenome": sobrenome_usuario,
            "setor": setor_usuario,
            "hostname": hostname,
            "sistema": sistema,
            "windows": windows,
            "windows_version": windows_version,
            "processador": processador,
            "ram": ram,

            "modelo_disco": modelo_disco,
            "tamanho_disco": tamanho_disco,

            "placa_video": placa_video,
            "cores": cores,
            "threads": threads,
            "arquitetura_so": arquitetura_so,
            "arquitetura_pc": arquitetura_pc,
            "serial_chassi": serial_chassi,
            "serial_bios": serial_bios,
            "modelo": modelo,
            "fabricante": fabricante
        }

        url = "https://script.google.com/macros/s/AKfycbzzuobumMCF4vIUGTpTmuQKhOoq0ZyhUu3sulEQUR5tMBSvJ9Cm5zdPzK6hJg7wl_sS-w/exec"
               
        
        
        log("Enviando dados ao Google Apps Script")
        resposta = requests.post(url, json=dados, timeout = 45)
        log(f"Status HTTP: {resposta.status_code}")

        if resposta.status_code == 200:
            log("Cadastro realizado com sucesso")
            messagebox.showinfo(
                "Sucesso",
                "Computador cadastrado com sucesso!"
            )
            janela.destroy() # Fecha a janela 

        else:
            log(f"Erro HTTP {resposta.status_code}")
            log(resposta.text)
            messagebox.showerror(
                "Erro",
                f"Falha ao enviar!\nCódigo: {resposta.status_code}\n{resposta.text}"
            )
    except Exception:

        erro = traceback.format_exc()

        log("ERRO INESPERADO")
        log(erro)

        messagebox.showerror(
            "Erro inesperado",
            "Ocorreu um erro durante a execução.\n\n"
            "Foi criado o arquivo inventario_log.txt na pasta Documentos.\n"
            "Envie esse arquivo para o TI."
        )

def validar_texto(texto):
    for caractere in texto:
        if caractere.isdigit():
            return False
    return True

janela = ctk.CTk() # cria a janela do programa

validacao = janela.register(validar_texto)        # chama a função para impedir números

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
    width=200,
    validate = "key",                              # validar enquanto digita
    validatecommand = (validacao, "%P")        # qual função será usada
)
nome.pack(pady=8) # posiciona o campo nome

sobrenome = ctk.CTkEntry( # cria o campo de entrada do sobrenome
    janela,
    placeholder_text="Sobrenome",
    width=200,
    validate = "key",
    validatecommand = (validacao,"%P")
)
sobrenome.pack(pady=8) # posiciona o campo sobrenome

setor = ctk.CTkEntry( # cria o campo de entrada do setor
    janela,
    placeholder_text="Setor",
    width=200,
    validate = "key",
    validatecommand = (validacao,"%P")
)
setor.pack(pady=8) # posiciona o campo setor

botao = ctk.CTkButton( # cria o botão cadastrar
    janela,
    text="Cadastrar",
    font=("Arial",16),
    command=cadastrar
)
botao.pack(pady=12) # posiciona o botão na janela

janela.mainloop()  # Sem isso a janela fecha de vez