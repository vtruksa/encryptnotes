from tkinter import filedialog
import tkinter as tk

import pbkdf2

from Crypto.Cipher import AES

win = None
root = None
path = None
t = None

def setup(textbox, r):
    global t, root
    t = textbox 
    root = root

def open_file(textbox):
    global t, path
    t = textbox
    path = filedialog.askopenfilename(title="Open a file...")

    if path[-4:] != '.bin': alert("The selected file has a wrong format")

    ask_password(t="open")

def open_file_dragndrop(event):
    global t, path
    path = event.data
    if path[-4:] != '.bin': alert("The selected file has a wrong format")
    ask_password(t="open")

def save_file():
    if path is None: save_as()
    ask_password(t="save")

def save_as():
    global path
    t = textbox
    path = filedialog.asksaveasfilename(title="Save as...", defaultextension=".bin")
    print(type(t))
    if path: ask_password(t="save")
    else: alert("Invalid path")

def __encrypt_file(password):
    data = bytes(t.get('1.0', 'end-1c'), 'UTF-8')
    password = bytes(password.get(), 'UTF-8')
    win.destroy()

    key = pbkdf2.PBKDF2(password, salt=b'').read(16)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    f = open(path, 'wb')
    for ch in cipher.nonce, tag, ciphertext: f.write(ch)
    f.close()
    alert("File saved")

def __decrypt_file(password):
    password = bytes(password.get(), 'UTF-8')
    win.destroy()

    f = open(path, 'rb')
    nonce, tag, ciphertext = [f.read(x) for x in (16, 16, -1)]
    f.close()

    key = pbkdf2.PBKDF2(password, salt=b'').read(16)
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    try: data = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError: 
        alert("The password you've entered is incorrect")

    t.delete(1.0, tk.END)
    t.insert(tk.END, data)

def ask_password(t):
    global win
    win = tk.Toplevel(root)
    win.title("Enter a password")
    win.geometry("250x100+500+500")

    label = tk.Label(win, text="Enter your password...")
    label.pack()

    password = tk.Entry(win, show="*")
    password.pack()

    if t == "open": btn = tk.Button(win, text="Enter", command=lambda: __decrypt_file(password))
    else: btn = tk.Button(win, text="Enter", command=lambda: __encrypt_file(password))
    btn.pack()

    win.mainloop()

def alert(message):
    win = tk.Toplevel(root)
    win.title(message)
    label = tk.Label(win, text=message)
    label.pack()

    ok_btn = tk.Button(win, text="OK", command=lambda: win.destroy())
    ok_btn.pack()
    
    win.mainloop()