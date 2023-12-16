import tkinter as tk

from tkinterdnd2 import TkinterDnD, DND_FILES
from util import *

root = TkinterDnD.Tk()
root.title("CryptedBook")

root.minsize(400, 400)
root.geometry("960x540+100+100")

btns = tk.Canvas(root, width=960, height=30)
btns.pack()

open_btn = tk.Button(btns, text="Open file...", command=lambda: open_file(textbox))
open_btn.pack(side='left', padx='5')
save_btn = tk.Button(btns, text="Save as...", command=lambda: save_file(textbox))
save_btn.pack(side='left', padx='5')

textbox = tk.Text(root, height = 500, width=960)
textbox.pack()

textbox.drop_target_register(DND_FILES)
textbox.dnd_bind('<<Drop>>', open_file_dragndrop)

setup(textbox)

root.mainloop()