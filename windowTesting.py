import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.columnconfigure(0, weight = 1)
window.rowconfigure(0, weight=1)

mainframe = tk.Frame(bg = "red", borderwidth=5, relief=tk.RAISED)
mainframe.grid(column = 0, row = 0, pady = 5, padx = 5, sticky = "nsew")

mainframe.rowconfigure(0, weight = 1, minsize=50)
mainframe.columnconfigure([0, 1, 2, 3], weight = 1, minsize=50)

label1 = tk.Label(master = mainframe, text="1", bg="black", fg="white")
label2 = tk.Label(master = mainframe, text="2", bg="black", fg="white")
label3 = tk.Label(master = mainframe, text="3", bg="black", fg="white")
label4 = tk.Label(master = mainframe, text="4", bg="black", fg="white")

label1.grid(row=0, column=0, padx = 5, pady = 5)
label2.grid(row=0, column=1, sticky="ew", padx = 5, pady = 5)
label3.grid(row=0, column=2, sticky="ns", padx = 5, pady = 5)
label4.grid(row=0, column=3, sticky="nsew", padx = 5, pady = 5)

window.mainloop()