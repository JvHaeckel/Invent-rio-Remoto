
import wmi                    # SIgnifica Windows Management Instrumentation - API oficial do Windows para administração (mais confiável)



c = wmi.WMI()

for i in c.Win32_Processor():
    print(i)

for i in c.Win32_Bios():
    print(i.SerialNumber)

gpu = c.Win32_VideoController()[0]

print(dir(gpu))