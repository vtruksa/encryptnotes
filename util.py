from tkinter import filedialog
import tkinter as tk

import pbkdf2

from Crypto.Cipher import AES

win = None
path = None
t = None

def open_file(textbox):
    global t, path
    t = textbox
    path = filedialog.askopenfilename(title="Open a file...")

    if path: ask_password(t="open")
    else: print("No file selected")

def save_file(textbox):
    global t, path
    t = textbox
    path = filedialog.asksaveasfilename(title="Save as...", defaultextension=".txt")
    print(type(t))
    if path: ask_password(t="save")
    else: print("No file selected")

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

def __decrypt_file(password):
    password = bytes(password.get(), 'UTF-8')
    win.destroy()

    f = open(path, 'rb')
    nonce, tag, ciphertext = [f.read(x) for x in (16, 16, -1)]
    f.close()

    key = pbkdf2.PBKDF2(password, salt=b'').read(16)
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    #if t.get('1.0', 'end-1c') is not None: t.delete(0, 'end')
    t.insert(index=0, chars=str(data))

def ask_password(t):
    global win
    win = tk.Tk()
    win.title("Enter a password")
    win.geometry("250x100+500+500")

    label = tk.Label(win, text="Enter your password...")
    label.pack()

    password = tk.Entry(win)
    password.pack()

    if t == "open": btn = tk.Button(win, text="Enter", command=lambda: __decrypt_file(password))
    else: btn = tk.Button(win, text="Enter", command=lambda: __encrypt_file(password))
    btn.pack()

    win.mainloop()