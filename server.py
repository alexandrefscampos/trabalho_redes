import socket
import os
import random
import shutil

# Função para salvar as cópias do arquivo no lado do servidor
def save_copies(file_path, num_copies):
    # Obtém o diretório e nome do arquivo
    directory = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)

    # Lista os arquivos no diretório
    file_list = os.listdir(directory)

    # Verifica se o número de cópias é maior do que o número atual de arquivos
    if num_copies > len(file_list):
        # Calcula o número de cópias a serem criadas
        num_copies_to_create = num_copies - len(file_list)

        # Cria as cópias adicionais do arquivo
        for i in range(num_copies_to_create):
            copy_name = f"copy{len(file_list) + i + 1}_{file_name}"
            copy_path = os.path.join(directory, copy_name)
            shutil.copy2(file_path, copy_path)
            print(f"Cópia {copy_name} criada em {copy_path}")

    elif num_copies < len(file_list):
        # Exclui as cópias excedentes do arquivo
        for i in range(len(file_list) - num_copies):
            copy_name = file_list[num_copies + i]
            copy_path = os.path.join(directory, copy_name)
            os.remove(copy_path)
            print(f"Cópia {copy_name} excluída.")
    else:
        print(f"As {num_copies} cópias do arquivo {file_name} já estão armazenadas no servidor")

# Função para depositar as cópias do arquivo no lado do servidor
def deposit_file(file_name, client_socket, num_copies):
    print('Recebido arquivo:', file_name)

    # Caminho completo do diretório do arquivo
    directory_path = os.path.join(STORAGE_DIR, file_name)

    # Verifica se o diretório já existe, senão cria o diretório
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Diretório {directory_path} criado.")

    # Caminho completo do arquivo
    file_path = os.path.join(directory_path, file_name)

    # Verifica se o arquivo já existe no diretório
    if os.path.exists(file_path):
        print(f"Arquivo {file_name} já existe.")

        # Atualiza o número de cópias do arquivo
        save_copies(file_path, num_copies)
    else:
        # Recebe o arquivo do cliente e salva no servidor
        with open(file_path, 'wb') as file:
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                file.write(data)

        print('Arquivo salvo:', file_name)

        # Salva as cópias do arquivo
        save_copies(file_path, num_copies)

# Função para recuperar as cópias do arquivo no lado do servidor
def restore_file(file_name, client_socket):
    # Caminho completo do diretório do arquivo
    directory_path = os.path.join(os.getcwd(), STORAGE_DIR, file_name)

    if not os.path.exists(directory_path):
        print(f"Arquivo {file_name} não encontrado.")
        client_socket.send("Arquivo não encontrado".encode())
    else:
        # Lista os arquivos na subpasta
        file_list = os.listdir(directory_path)

        if len(file_list) == 0:
            print(f"Arquivo {file_name} não encontrado.")
            client_socket.send("Arquivo não encontrado".encode())
        else:
            # Escolhe aleatoriamente uma das cópias do arquivo
            chosen_file = random.choice(file_list)

            print(f"Enviando arquivo {chosen_file} para o cliente")

            # Caminho completo do arquivo escolhido
            file_path = os.path.join(directory_path, chosen_file)

            # Abre o arquivo e envia para o cliente
            with open(file_path, 'rb') as file:
                file_data = file.read()

            # Envia os dados do arquivo para o cliente
            client_socket.sendall(file_data)

            print(f'Arquivo enviado: {chosen_file}')

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12345  # Porta do servidor
BUFFER_SIZE = 4096  # Tamanho do buffer de recebimento/envio
STORAGE_DIR = "data_storage" # Pasta que servirá como armazenamento

def main():
    # Cria o diretório "data_storage" se não existir
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

    # Cria um socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincula o socket à porta e endereço definidos
    server_socket.bind((HOST, PORT))

    # Define o número máximo de conexões pendentes
    server_socket.listen(1)

    print("Aguardando conexão do cliente...")

    while True:
        # Aguarda uma conexão
        client_socket, address = server_socket.accept()
        print('Conexão estabelecida com:', address)

        # Recebe a mensagem do cliente contendo a operação e o nome do arquivo
        message = client_socket.recv(BUFFER_SIZE).decode()
        operation, num_copies, file_name = message.split(" ")
        num_copies = int(num_copies)

        if operation == 'depositar':
            deposit_file(file_name, client_socket, num_copies)
        elif operation == 'recuperar':
            restore_file(file_name, client_socket)
        else:
            print("Operação inválida.")

        # Fecha a conexão com o cliente
        client_socket.close()
        print('Conexão fechada com:', address)

if __name__ == "__main__":
    main()