import tkinter as tk

from tkinter import ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from util import *

root = TkinterDnD.Tk()
root.title("CryptedBook")
root.iconbitmap("icon.ico")

root.minsize(400, 400)
root.geometry("960x540+100+100")

btns = tk.Canvas(root, width=960, height=30)
btns.pack()

style = ttk.Style()
style.configure("btnmenu.TButton", font="Ariel")

open_btn = ttk.Button(btns, text="Open file...", command=lambda: open_file(textbox), style="btnmenu.TButton")
open_btn.pack(side='left')
save_btn = ttk.Button(btns, text="Save", style='btnmenu.TButton')
save_btn.pack(side='left')
save_as_btn = ttk.Button(btns, text="Save as...", command=lambda: save_as(textbox), style="btnmenu.TButton")
save_as_btn.pack(side='left')

textbox = tk.Text(root, height = 500, width=960)
textbox.pack()

textbox.drop_target_register(DND_FILES)
textbox.dnd_bind('<<Drop>>', open_file_dragndrop)

setup(textbox, root)

root.mainloop()