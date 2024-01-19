import socket
import threading
import base64
import emoji
from tkinter import Tk, Scrollbar, Listbox, Entry, Button, END

# 创建 socket 对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到服务端
client_socket.connect(('127.0.0.1', 5555))

# 创建图形用户界面
root = Tk()
root.title("Chat App")

# 输入用户名的文本框
username_entry = Entry(root, width=30)
username_entry.pack()

# 显示聊天记录的列表框
message_list = Listbox(root, height=15, width=50, yscrollcommand=Scrollbar.set)
message_list.pack()

# 输入消息的文本框
entry_field = Entry(root, width=30)
entry_field.pack()

# 目标客户端的地址
target_address_entry = Entry(root, width=30)
target_address_entry.pack()

# 发送消息的按钮
send_button = Button(root, text="Send", command=lambda: send_message(entry_field.get(), target_address_entry.get()))
send_button.pack()

# 发送全服务器广播消息的按钮
broadcast_button = Button(root, text="Broadcast to All", command=lambda: send_broadcast(entry_field.get()))
broadcast_button.pack()

# 用户名
username = ""

# 设置用户名的函数
def set_username():
    global username
    username = username_entry.get()
    entry_field.focus_set()

# 发送消息的函数
def send_message(message, target_address):
    if username:
        if target_address and message:
            if target_address.startswith("/p2p "):
                target_address = target_address[len("/p2p "):]
                message = f"/p2p {target_address}: {username}: {message}"
            else:
                message = f"You ({username}): {message}"

            encoded_message = base64.b64encode(message.encode())
            client_socket.send(encoded_message)
            entry_field.delete(0, END)

# 发送全服务器广播消息的函数
def send_broadcast(message):
    if username and message:
        broadcast_message = f"Broadcast ({username}): {message}"
        encoded_message = base64.b64encode(broadcast_message.encode())
        client_socket.send(encoded_message)
        entry_field.delete(0, END)

# 接收服务端广播的消息
def receive():
    while True:
        try:
            encoded_message = client_socket.recv(1024)
            decoded_message = base64.b64decode(encoded_message).decode()
            message_list.insert(END, emoji.emojize(decoded_message))  # 使用emoji库
        except:
            break

# 启动接收消息的线程
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# 设置用户名按钮
set_username_button = Button(root, text="Set Username", command=set_username)
set_username_button.pack()

# 运行图形用户界面
root.mainloop()