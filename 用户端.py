import socket
import threading
import base64
import emoji  # æ·»å emojiåº
from tkinter import Tk, Scrollbar, Listbox, Entry, Button, END

# åå»º socket å¯¹è±¡
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# è¿æ¥å°æå¡ç«¯
client_socket.connect(('127.0.0.1', 5555))

# åå»ºå¾å½¢ç¨æ·çé¢
root = Tk()
root.title("Chat App")

# æ¾ç¤ºèå¤©è®°å½çåè¡¨æ¡
message_list = Listbox(root, height=15, width=50, yscrollcommand=Scrollbar.set)
message_list.pack()

# è¾å¥æ¶æ¯çææ¬æ¡
entry_field = Entry(root, width=30)
entry_field.pack()

# ç®æ å®¢æ·ç«¯çå°å
target_address_entry = Entry(root, width=30)
target_address_entry.pack()

# åéæ¶æ¯çæé®
send_button = Button(root, text="Send", command=lambda: send_message(entry_field.get(), target_address_entry.get()))
send_button.pack()

# åéæ¶æ¯çå½æ°
def send_message(message, target_address):
    if target_address and message:
        if target_address.startswith("/p2p "):
            target_address = target_address[len("/p2p "):]
            message = f"/p2p {target_address}: {message}"
        else:
            message = f"You: {message}"

        encoded_message = base64.b64encode(message.encode())
        client_socket.send(encoded_message)
        entry_field.delete(0, END)

# æ¥æ¶æå¡ç«¯å¹¿æ­çæ¶æ¯
def receive():
    while True:
        try:
            encoded_message = client_socket.recv(1024)
            decoded_message = base64.b64decode(encoded_message).decode()
            message_list.insert(END, emoji.emojize(decoded_message))  # ä½¿ç¨emojiåº
        except:
            break

# å¯å¨æ¥æ¶æ¶æ¯ççº¿ç¨
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# è¿è¡å¾å½¢