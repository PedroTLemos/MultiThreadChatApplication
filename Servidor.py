from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def aceitar_conexoes():
    while True:
        cliente, endereco_cliente = SERVER.accept()
        print("%s:%s conectou." % endereco_cliente)
        cliente.send(bytes("Bem-vindo! Digite seu nome e aperte ENTER", "utf8"))
        enderecos[cliente] = endereco_cliente
        Thread(target=atender_cliente, args=(cliente,)).start()

def atender_cliente(cliente):
    nome = cliente.recv(BUFSIZ).decode("utf8")
    wel = 'Bem-vindo, %s! Se você, em algum momento, desejar se desconectar, digite bye\n' \
          'Caso queira enviar uma mensagem para todos, digite send -all seguido da mensagem\n' \
          'Caso queira enviar uma mensagem para um usuario especifico, digita send -user [nome do usuario] ' \
          'seguido da mensagem\n' \
          'Caso queira uma lista dos usuarios presentes, digite list' % nome
    cliente.send(bytes(wel, "utf8"))
    msg = "%s se juntou ao chat!" % nome
    broadcast(bytes(msg, "utf8"))
    clientes[cliente] = nome

    while True:
        msg = cliente.recv(BUFSIZ)
        msg = msg.decode("utf8")
        msg = msg.split()
        if msg[0] == "send":
            if msg[1] == "-all":
                broadcast(msg[2], nome + ": ")
            elif msg[1] == "-user":
                if msg[2] in clientes:
                    msg[2].send(bytes(msg[3], "utf8"))
                else:
                    temp = "Usuario nao existente!"
                    cliente.send(bytes(temp, "utf8"))
            else:
                temp = "Comando invalido"
                cliente.send(bytes(temp, "utf8"))
        elif msg[0] == "list":
            temp = "Usuarios disponiveis:"
            for cliente in clientes:
                temp = temp + " %s" % cliente
            cliente.send(bytes(temp, "utf8"))
        elif msg[0] == "bye":
            cliente.send(bytes("bye", "utf8"))
            cliente.close()
            del clientes[cliente]
            broadcast(bytes("%s saiu do chat" % nome, "utf8"))
            break

def broadcast(msg, prefixo=""):

    for socket in clientes:
        socket.send(bytes(prefixo, "utf8")+msg)








clientes = {}
enderecos = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Aguardando conexao...")
    ACCEPT_THREAD = Thread(target=aceitar_conexoes)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()