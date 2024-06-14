import socket
import time
import os
import sys


print("<<<<<<<<<<<<<<<<<<<   RECEIVER UDP   >>>>>>>>>>>>>>>>>>>>>\n")
HOST = 'localhost'
PORT = 5000
PAUSA=0 #pausa entre pacotes


receiver = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
receiver.bind((HOST, PORT))

ip_local = socket.gethostbyname(socket.gethostname())
print(f'IP Local: {ip_local}:{PORT}')

print('Aguardando o arquivo!!\n')

namefile, cliente = receiver.recvfrom(100) #recebe nome do arquivo
print(f'Nome do arquivo recebido = {namefile.decode()}')

# verifica se o arquivo ja existe

existeArquivo = os.path.exists(namefile)



if existeArquivo:
    receiver.sendto(bytes('n','utf-8'),cliente) # nao autoriza transmitir o arquivo
    print(f'\n{namefile.decode()} já Existe no Diretorio!!!\n\n')
    sys.exit()
else:
    receiver.sendto(bytes('y','utf-8'),cliente)  # autoriza transmitir o arquivo








# recebe arquivo
size, cliente = receiver.recvfrom(100) #recebe tamanho do arquivo
print(f'\n Tamanho do arquivo= {size.decode()} Bytes\n')
file=[]
controleSequencia=48

qq=True
pedacoErrado=False
pedacoArquivo=''
cont=0

while qq:
    
    if pedacoErrado:
         print('\n Parte errada do arquivo')
    else:        
        pedacoArquivo, cliente = receiver.recvfrom(100)        
        #print(f'\ncontroleSequencia {controleSequencia},  pedacoArquivo[0]  {pedacoArquivo[0]}\n')         
    try:
        if pedacoArquivo[0]!=controleSequencia:           
            pedacoErrado=True
            print(f'bit recebido {pedacoArquivo[0].to_bytes()} , bit esperado {controleSequencia.__str__()}')
            time.sleep(PAUSA)
    except:
        qq=False
    else:
        if pedacoArquivo[0]==48:
               pedacoArquivo=pedacoArquivo.removeprefix(controleSequencia.to_bytes())
               receiver.sendto(bytes('2','utf-8'),cliente)
               controleSequencia=49
               pedacoErrado=False
               #print( '\n 0 ok \n')
               #print(controleSequencia)

        elif pedacoArquivo[0]==49:
               pedacoArquivo=pedacoArquivo.removeprefix(controleSequencia.to_bytes())
               receiver.sendto(bytes('3','utf-8'),cliente)
               controleSequencia=48
               pedacoErrado=False
               #print( '\n 1 ok \n')
               #print(controleSequencia)
       
        file.append(pedacoArquivo.__bytes__())
        

        if pedacoErrado!= True:
            cont=cont+99
        print('\r >Baixando >> '+cont.__str__()+' de '+size.decode()+' Bytes   ', end='')
     
        if cont>int(size.decode()):
                qq=False

     
        time.sleep(PAUSA)

print('\n-----------------------------------------------------------\n')

# Montagem do arquivo
f = open(namefile,'ab+')
f.writelines(file)
f.close()



time.sleep(3)
mensagem='Arquivo Recebido!!!'
print(mensagem)
receiver.sendto(bytes(mensagem,'utf-8'),cliente)
print(f'\n...........fim receiver............. \n')



