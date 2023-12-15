import tkinter as tk
from util import *

root = tk.Tk()
root.title("CryptedBook")

root.minsize(400, 400)
root.geometry("960x540+100+100")

btns = tk.Canvas(root, width=960, height=30)
btns.pack()

textbox = tk.Text(root, height = 500, width=960)

open_btn = tk.Button(btns, text="Open file...", command=lambda: open_file(textbox))
open_btn.pack(side='left', padx='5')
save_btn = tk.Button(btns, text="Save as...", command=lambda: save_file(textbox))
save_btn.pack(side='left', padx='5')

textbox.pack()

root.mainloop()