# Versão criada para testar no pc antes de jogar para o sheets

import customtkinter as ctk
from tkinter import messagebox
import socket
import platform
import wmi

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def cadastrar():

    try:
        nome_usuario = nome.get().upper().strip()
        sobrenome_usuario = sobrenome.get().upper().strip()
        setor_usuario = setor.get().upper().strip()

        if nome_usuario == "" or sobrenome_usuario == "" or setor_usuario == "":
            messagebox.showerror("Erro", "Preencha todos os campos")
            return

        hostname = socket.gethostname()
        sistema = platform.system()

        c = wmi.WMI()

        windows = c.Win32_OperatingSystem()[0].Caption
        windows_version = c.Win32_OperatingSystem()[0].Version

        processador = c.Win32_Processor()[0].Name
        cores = c.Win32_Processor()[0].NumberOfCores
        threads = c.Win32_Processor()[0].NumberOfLogicalProcessors

        placa_video = c.Win32_VideoController()[0].Name

        ram = round(int(c.Win32_ComputerSystem()[0].TotalPhysicalMemory) / (1024**3))

        arquitetura_so = c.Win32_OperatingSystem()[0].OSArchitecture
        arquitetura_pc = c.Win32_Processor()[0].AddressWidth

        serial_bios = c.Win32_BIOS()[0].SerialNumber
        serial_chassi = c.Win32_SystemEnclosure()[0].SerialNumber

        modelo = c.Win32_ComputerSystem()[0].Model
        fabricante = c.Win32_ComputerSystem()[0].Manufacturer


        info = f"""
nome: {nome_usuario}
sobrenome: {sobrenome_usuario}
setor: {setor_usuario}
hostname: {hostname}
sistema: {sistema}
windows: {windows}
versão: {windows_version}
processador: {processador}
cores: {cores}
threads: {threads}
ram: {ram} gb
placa de vídeo: {placa_video}
arquitetura so: {arquitetura_so}
arquitetura pc: {arquitetura_pc}
modelo: {modelo}
fabricante: {fabricante}
serial bios: {serial_bios}
serial chassi: {serial_chassi}
"""

        messagebox.showinfo("Informações da Máquina", info)

    except Exception as e:
        messagebox.showerror("ERRO", str(e))


def validar_texto(texto):
    for c in texto:
        if c.isdigit():
            return False
    return True


janela = ctk.CTk()
janela.geometry("300x250")
janela.title("Rodotur TI")

validacao = janela.register(validar_texto)


ctk.CTkLabel(janela, text="Cadastro Máquinas", font=("Arial", 20)).pack(pady=10)


nome = ctk.CTkEntry(janela, placeholder_text="Nome", width=200,
                    validate="key", validatecommand=(validacao, "%P"))
nome.pack(pady=8)

sobrenome = ctk.CTkEntry(janela, placeholder_text="Sobrenome", width=200,
                         validate="key", validatecommand=(validacao, "%P"))
sobrenome.pack(pady=8)

setor = ctk.CTkEntry(janela, placeholder_text="Setor", width=200,
                     validate="key", validatecommand=(validacao, "%P"))
setor.pack(pady=8)


ctk.CTkButton(janela, text="Cadastrar", font=("Arial", 16),
              command=cadastrar).pack(pady=12)


janela.mainloop()