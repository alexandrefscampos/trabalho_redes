import socket
import os

def deposit_file(client_socket):
    # Obtém o caminho do arquivo que o cliente deseja depositar
    file_path = input("Digite o caminho completo do arquivo que deseja depositar: ")

    # Removendo os espaços vazios, caso existam
    file_path = str(file_path).strip()

    # Verifica se o arquivo existe
    if not os.path.isfile(file_path):
        print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
        client_socket.close()
        exit()

    # Nome do arquivo (apenas o nome, sem o caminho completo)
    file_name = os.path.basename(file_path)

    # Quantidade de cópias desejadas
    num_copies = input("Digite a quantidade de cópias desejadas: ")

    # Removendo os espaços vazios, caso existam, e fazendo o cast para int
    num_copies = int(str(num_copies).strip())

    if num_copies <= 0:
        print('O número de cópias deve ser maior que 0')
        return

    # Cria a mensagem a ser enviada ao servidor
    message = f"depositar {num_copies} {file_name}"

    # Envia a mensagem ao servidor
    client_socket.send(message.encode())

    # Envia o arquivo ao servidor
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(BUFFER_SIZE)
            if not data:
                break
            client_socket.send(data)

    print('Arquivo depositado:', file_name)

def restore_file(client_socket):
    # Nome do arquivo que o cliente deseja recuperar
    file_name = input("Digite o nome do arquivo que deseja recuperar: ")

    # Removendo os espaços vazios, caso existam
    file_name = str(file_name).strip()

    # Cria a mensagem a ser enviada ao servidor
    message = f"recuperar 0 {file_name}"

    # Envia a mensagem ao servidor
    client_socket.send(message.encode())

    # Recebe a resposta do servidor
    response = client_socket.recv(BUFFER_SIZE).decode()

    if response == "Arquivo não encontrado":
        print(f"Arquivo {file_name} não encontrado.")
    else:
        # Pasta de destino para o arquivo recuperado
        restored_dir = os.path.join(os.getcwd(), "restored_data")

        # Verifica se o diretório de destino existe, senão cria o diretório
        if not os.path.exists(restored_dir):
            os.makedirs(restored_dir)
            print(f"Diretório {restored_dir} criado.")

        # Caminho completo do arquivo recuperado
        file_path = os.path.join(restored_dir, file_name)

        # Salva o arquivo recuperado no cliente
        with open(file_path, 'wb') as file:
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                file.write(data)

        print("Arquivo recuperado:", file_name)

# Configurações do cliente
HOST = "127.0.0.1"  # Endereço IP do servidor
PORT = 12345  # Porta do servidor
BUFFER_SIZE = 4096  # Tamanho do buffer de envio/recebimento



def main():

    # Cria um socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta ao servidor usando o endereço e a porta definidos
    client_socket.connect((HOST, PORT))

    # Opção do cliente: depositar ou receber arquivo
    option = input("Digite 'depositar' para depositar um arquivo ou 'recuperar' para receber um arquivo: ")

    # Removendo os espaços vazios, caso existam
    option = str(option).strip()

    if option == 'depositar':
        deposit_file(client_socket)

    elif option == 'recuperar':
        restore_file(client_socket)

    else:
        print("Opção inválida.")

    # Fecha a conexão com o servidor
    client_socket.close()

if __name__ == "__main__":
    main()