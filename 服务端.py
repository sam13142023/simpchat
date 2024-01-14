import socket
import threading
import base64
import markdown2
import emoji  # æ·»å emojiåº

# åå»º socket å¯¹è±¡
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ç»å® IP åç«¯å£
server_socket.bind(('0.0.0.0', 5555))

# çå¬è¿æ¥
server_socket.listen()

# å­å¨è¿æ¥çå®¢æ·ç«¯åå¯¹åºçå°å
clients = {}
addresses = {}

# åéæ¶æ¯ç»æå®å®¢æ·ç«¯
def send_to_client(message, client_socket):
    try:
        client_socket.send(message)
    except:
        pass

# å¹¿æ­æ¶æ¯ç»ææå®¢æ·ç«¯
def broadcast(message, client_socket=None):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                remove_client(client)

# ç§»é¤æ­å¼è¿æ¥çå®¢æ·ç«¯
def remove_client(client_socket):
    addr = clients[client_socket]
    del clients[client_socket]
    del addresses[str(addr)]
    broadcast(f"Client {addr} has left the chat.")

# å¤çå®¢æ·ç«¯çæ¶æ¯
def handle_client(client_socket, addr):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            decoded_message = base64.b64decode(message).decode()

            # å¤æ­æ¶æ¯ç±»åå¹¶å¤ç
            if decoded_message.startswith("/p2p "):
                target_addr, message_content = decoded_message[len("/p2p "):].split(": ", 1)
                if target_addr in addresses:
                    target_socket = addresses[target_addr]
                    send_to_client(message, target_socket)
                else:
                    client_socket.send(f"Client {target_addr} not found.".encode())
            else:
                broadcast_message = f"{addr}: {emoji.emojize(markdown2.markdown(message_content))}"  # ä½¿ç¨emojiåº
                broadcast(base64.b64encode(broadcast_message.encode()), client_socket)

        except:
            remove_client(client_socket)
            break

# æ¥åå®¢æ·ç«¯è¿æ¥
while True:
    client_socket, addr = server_socket.accept()
    clients[client_socket] = addr
    addresses[str(addr)] = client_socket
    broadcast(f"Client {addr} has joined the chat.")
    print(f"Connection from {addr}")

    # å¯å¨ä¸ä¸ªæ°çº¿ç¨æ¥å¤çå®¢æ·ç«¯
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()