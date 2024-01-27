import tkinter as tk
import pbkdf2

from tkinter import ttk, filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES

from Crypto.Cipher import AES

from util import *

class App():
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("CryptedBook")
        self.root.iconbitmap("icon.ico")

        self.root.minsize(400, 400)
        self.root.geometry("960x540+100+100")

        self.btns = tk.Canvas(self.root, width=960, height=30)
        self.btns.pack()

        self.style = ttk.Style()
        self.style.configure("btnmenu.TButton", font="Ariel")

        self.open_btn = ttk.Button(self.btns, text="Open file...", command=self.open_file, style="btnmenu.TButton")
        self.open_btn.pack(side="left")
        self.save_btn = ttk.Button(self.btns, text="Save", style='btnmenu.TButton', command=self.save_file)
        self.save_btn.pack(side='left')
        self.save_as_btn = ttk.Button(self.btns, text="Save as...", command=self.save_as, style="btnmenu.TButton")
        self.save_as_btn.pack(side='left')

        self.textbox = tk.Text(self.root, height=500, width=960)
        self.textbox.pack()
        self.textbox.drop_target_register(DND_FILES)
        self.textbox.dnd_bind("<<Drop>>", self.open_file)

        self.path = None

        self.root.mainloop()

    def open_file(self, event=None):
        if event is None: self.path = filedialog.askopenfilename(title="Open a file...")
        else: self.path = event.data

        if self.path[-4:] != '.bin':
            self.alert("The selected file has a wrong format")
            self.path = None
        else: self.ask_password("open")

    def save_file(self):
        if self.path is None: self.save_as()
        else: self.ask_password(t="save")

    def save_as(self):
        path = filedialog.asksaveasfilename(title="Save as...", defaultextension=".bin")
        if path: 
            self.path = path
            self.ask_password(t="save")
        else: alert("Invalid path")

    def ask_password(self, t):
        self.extra_win = tk.Toplevel(self.root)
        self.extra_win.title("Enter a password")
        self.extra_win.geometry("250x100+500+500")
        
        label = tk.Label(self.extra_win, text="Enter your password")
        label.pack()

        self.password_input = tk.Entry(self.extra_win, show="⬤")
        self.password_input.pack()

        if t == "open": btn = tk.Button(self.extra_win, text="Enter", command=self.__decrypt)
        else: btn = tk.Button(self.extra_win, text="Enter", command=self.__encrypt)
        btn.pack()

        self.extra_win.mainloop()

    def __encrypt(self):
        data = bytes(self.textbox.get("1.0", "end-1c"), "UTF-8")
        self.password = bytes(self.password_input.get(), "UTF-8")
        self.extra_win.destroy()

        key = pbkdf2.PBKDF2(self.password, salt=b'').read(16)
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        f = open(self.path, 'wb')
        for ch in cipher.nonce, tag, ciphertext: f.write(ch)
        f.close()
        self.alert("File saved")

    def __decrypt(self):
        self.password = bytes(self.password_input.get(), 'UTF-8')
        self.extra_win.destroy()

        f = open(self.path, 'rb')
        nonce, tag, ciphertext = [f.read(x) for x in (16, 16, -1)]
        f.close()

        key = pbkdf2.PBKDF2(self.password, salt=b'').read(16)
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        try: 
            data = cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError:
            self.alert("The password you've entered is incorrect")
            return

        self.textbox.delete(1.0, tk.END)
        self.textbox.insert(tk.END, data)

    def alert(self, message):
        win = tk.Toplevel(root)
        win.title("Alert")
        label = tk.Label(win, text=message)
        label.pack()

        ok_btn = tk.Button(win, text="OK", command=lambda: win.destroy())
        ok_btn.pack()

        win.mainloop()

App()