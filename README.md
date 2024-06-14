# TRABALHO DE FUNDAMENTOS DE REDES

      O sender.py realiza o envio um arquivo para o receiver.py.


# sender.py

      O sender.py quando executado recebe o nome do arquivo "arquivo+extençao",
   o arquivo deve estar na mesma pasta que o sender.py

      Pode ser passado como argumento o endereço do Host eo nome do Arquivo,
   usando as flags -h e -f  "-h endereçoHost -f nomeArquivo".

   exemplo: "python3 sender.py -h 127.0.0.1 -f podcast.png"

      Caso nenhum argumento seja passado, será pedido o nome do Arquivo e o Host por padrão é "localhost".

      E realiza o envio para o receiver.py 

         nome do arquivo >  espera autorização > envia tamanho do arquivo > envia 100Bytes > espera ACKresposta > ............. > 
         espera mensagendo receiver.py.



# receiver.py
 
      O Receiver informa o ip local e a porta, e fica aguardando o sender.py

         recebe nome do arquivo > verifica se nao existe um arquivo com o mesmo nome > autoriza o sender.py > recebe o tamanho do arquivo >

         recebe 100Bytes > verifica o Byte inicial > ........... > escreve o Arquivo recebido > envia mensagem para o sender.py.

   

