import socket
import threading
import base64
import markdown2
import emoji

# 创建 socket 对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定 IP 和端口
server_socket.bind(('0.0.0.0', 5555))

# 监听连接
server_socket.listen()

# 存储连接的客户端和对应的地址
clients = {}
addresses = {}

# 发送消息给指定客户端
def send_to_client(message, client_socket):
    try:
        client_socket.send(message)
    except:
        pass

# 广播消息给所有客户端
def broadcast(message, client_socket=None):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                remove_client(client)

# 移除断开连接的客户端
def remove_client(client_socket):
    addr = clients[client_socket]
    del clients[client_socket]
    del addresses[str(addr)]
    broadcast(f"Client {addr} has left the chat.")

# 处理客户端的消息
def handle_client(client_socket, addr):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            decoded_message = base64.b64decode(message).decode()

            # 判断消息类型并处理
            if decoded_message.startswith("/p2p "):
                target_addr, message_content = decoded_message[len("/p2p "):].split(": ", 1)
                if target_addr in addresses:
                    target_socket = addresses[target_addr]
                    send_to_client(message, target_socket)
                else:
                    client_socket.send(f"Client {target_addr} not found.".encode())
            elif decoded_message.startswith("/broadcast "):
                broadcast_message_content = decoded_message[len("/broadcast "):]
                broadcast_message = f"Broadcast from {addr}: {broadcast_message_content}"
                broadcast(base64.b64encode(broadcast_message.encode()), client_socket)
            else:
                broadcast_message = f"{addr}: {emoji.emojize(markdown2.markdown(decoded_message))}"  # 使用emoji库
                broadcast(base64.b64encode(broadcast_message.encode()), client_socket)

        except:
            remove_client(client_socket)
            break

# 接受客户端连接
while True:
    client_socket, addr = server_socket.accept()
    clients[client_socket] = addr
    addresses[str(addr)] = client_socket
    broadcast(f"Client {addr} has joined the chat.")
    print(f"Connection from {addr}")

    # 启动一个新线程来处理客户端
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()