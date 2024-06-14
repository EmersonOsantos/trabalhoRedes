import socket
import argparse
import time
import signal
import os
import sys


def timeout(signum, frame):
    raise Exception('...ACK PERDIDO!...')
signal.signal(signal.SIGALRM, timeout)



HOST = 'localhost'
PORT = 5000
BYTESSENDER=100 # Bytes por leitura e envio
PAUSA=0 #pausa entre pacotes



# tratamento de argumentos
parser = argparse.ArgumentParser(conflict_handler='resolve')
parser.add_argument('-h', help='Host destino')
parser.add_argument('-f', help='Arquivo para enviar')
argumentos = parser.parse_args()
# recebe ip destino, se for passado por argumentos
if argumentos.h:
    HOST=argumentos.h

print("<<<<<<<<<<<<<<<<<<<<<<<<   Sender UDP   >>>>>>>>>>>>>>>>>>>>>>>\n")

sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# busca ip local
ip_local = socket.gethostbyname(socket.gethostname()) 
print(f'IP Local: {ip_local}')
print(f'IP Destino: {HOST}:{PORT}\n')

# recebe nome do arquivo
if argumentos.f:
    namefile=argumentos.f
else:
    namefile =str(input('nome do arquivo > '))

# verifica com o receiver se  ja tem o arquivo

wAut=True #controle do primeiro while
whileAtivo=True #controle do laço segundo while
while wAut:
    sender.sendto(namefile.encode(),(HOST,PORT))
    try:
      signal.alarm(2)
      autorizado,destino=sender.recvfrom(100)
      signal.alarm(0)
      
      if autorizado.decode('utf-8')=='n':
        print(f'\n {namefile} já Existe no Destino!!!\n')
        whileAtivo=False
        wAut=False
        time.sleep(PAUSA)
        sys.exit(0)
      elif autorizado.decode('utf-8')=='y':
          print(f'\n....... iniciando transmisao do arquivo  {namefile} ........\n')
          wAut=False
      
    except Exception:
                  
        print('Receiver Não está Respondendo')
       
   




# manipulando arquivo

size = os.path.getsize(namefile)
sender.sendto(size.__str__().encode('utf-8'),destino) #envia tamanho do arquivo para receiver

cont=0

controleSequencia=bytes('0','utf-8')

arquivo=open(namefile,'rb')
pedacoArquivo=''
ackPerdido=False



while whileAtivo:    
    
    try:
       
        if ackPerdido==False:
            pedacoArquivo=(controleSequencia+(arquivo.read(BYTESSENDER-1)))

        if cont>(size):
          whileAtivo=False

    except:
        whileAtivo=False
    else:
        sender.sendto(pedacoArquivo,(HOST,PORT))
        #print(f'\n{pedacoArquivo}')

        if ackPerdido==False:       
            cont=cont+(BYTESSENDER-1)

        print('\r >>> Enviando >> 1+'+cont.__str__()+' de '+size.__str__()+' Bytes   ', end='')             
        time.sleep(PAUSA)

        try:
           signal.alarm(2)

           ack,destino=sender.recvfrom(100)
           #print(f'Ackkkkk  {ack.__str__()}  {controleSequencia.decode()}  {ack.decode()}')
           signal.alarm(0)
           if (controleSequencia.decode()=='0')and(ack.decode()=='2'):
               controleSequencia=bytes('1','utf-8')
               ackPerdido=False

           elif (controleSequencia.decode()=='1')and(ack.decode()=='3'):
               controleSequencia=bytes('0','utf-8')
               ackPerdido=False

           else:
               ackPerdido=True
               print('\n Pacote Perdido... Reenviando pacote')
                  
        except Exception as e :
            ackPerdido=True
            print()
            print(e)




mensagem,destino=sender.recvfrom(100)
print(f'\nMensagem do receiver >>>  {mensagem.decode()}\n')
print('\n>>>>>>>>>>>>>>>  Sender encerrado.... <<<<<<<<<<<<<<<< \n')









