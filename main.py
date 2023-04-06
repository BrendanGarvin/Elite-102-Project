import tkinter as tk
from tkinter import *
import os

root = tk.Tk()

def new_window():
    w.config(text="OOOOOOOOOOOOOOOOOOOOOOOOOOOOH")

w = Label (root, text="Welcome to Beaver Bank\n", font=('Times', 20))
w.grid(row = 0, column = 1)

numberText = Label (root, text="Account Number:", font=("Times", 20))
numberText.grid(row = 1, column = 0, sticky = W, pady = 2)

numberinputtxt = Entry(root, width=20, font=('Times 20'))
numberinputtxt.grid(row = 1, column = 1, columnspan = 2, sticky = W+E, pady = 2)

pinText = Label (root, text="PIN:", font=("Times", 20))
pinText.grid(row = 2, column = 0, sticky = E, pady = 2)

pininputtxt = Entry(root, width=20, font=('Times 20'))
pininputtxt.grid(row = 2, column = 1, columnspan = 2, sticky = W+E, pady = 2)


b1 = Button(root, text="Click to Change Text", command=new_window)
b1.grid(row = 3, column = 2, sticky = W, pady = 2)


root.mainloop()

