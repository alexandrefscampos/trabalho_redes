# Trabalho de Redes - MATA59
##  Professor: Gustavo Bittencourt.
##  Alunos: Alexandre Campos, Raquel Paradella, Pedro Beckhauser

Neste trabalho nossa equipe implementou um sistema de armazenamento e recuperação de arquivos utilizando o modelo cliente-servidor via sockets. A linguagem escolhada para a realização do trabalho foi o python.

Para rodar é necessário ter o python instalado em sua máquina, para o passso-a-passo consulte [este link](https://www.python.org/downloads/). São necessários dois terminais na raiz do nosso diretório, um que opere o cliente, e outro com o servidor. Para rodá-los, utilize os comandos:

Servidor:
```
sh setup_server.sh
```

Client:
```
sh setup_client.sh
```

Primeiro passo é rodar o servidor, que esperará a conexão do cliente. No cliente são disponibilizadas duas funções, a de depositar um arquivo para o servidor, e a de recuperar. 

### Depositar um arquivo:
Para o depósito, é necessário especificar qual o caminho completo para o arquivo a ser armazenado, o número de cópias que serão salvas no servidor, dessa forma o servidor irá criar um número de cópias de desejadas na pasta `data_storage`, caso não exista. Se o arquivo já foi depositado, serão atualizadas somente o número de cópias que estão salvas.

### Recuperar um arquivo:
Já para recuperar, informe o nome do arquivo e sua extensão, será criada então uma cópia recuperada na pasta `restored_data` caso ele já exista. Caso contrário será informado que o arquivo solicitado não está armazenado no nosso servidor.
