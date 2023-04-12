import tkinter as tk
from tkinter import *
import os

import mysql.connector

connection = mysql.connector.connect(user = 'root', database = 'bank', password = '!Bolt2010!')

cursor = connection.cursor()

#Insert Row Method
#testQuery = ('INSERT INTO info VALUES (NULL, \"John Doe\" , 123456, 0000, \"1950-01-01\", 0)') 

#Select Data Method
#testQuery = ('SELECT * FROM info')

#Update Money Method
testQuery = ('UPDATE info SET money = 2000 WHERE accnumber = 123456') 

cursor.execute(testQuery)

testQuery = ('SELECT * FROM info')

cursor.execute(testQuery)


for item in cursor:

    print(item)

connection.commit()


root = tk.Tk()


number = tk.StringVar()
pin = tk.StringVar()


def clear_widgets():
    for widget in root.winfo_children():
        widget.destroy()

def welcomeScreen():
    clear_widgets()
    w = Label (root, text="Welcome to Beaver Bank\n", font=('Times', 20))
    w.grid(row = 0, column = 1)

    numberText = Label (root, text="Account Number:", font=("Times", 20))
    numberText.grid(row = 1, column = 0, sticky = W, pady = 2)

    numberinputtxt = Entry(root, textvariable = number, width=20, font=('Times 20'))
    numberinputtxt.grid(row = 1, column = 1, columnspan = 2, sticky = W+E, pady = 2)

    pinText = Label (root, text="PIN:", font=("Times", 20))
    pinText.grid(row = 2, column = 0, sticky = E, pady = 2)

    pininputtxt = Entry(root, textvariable = pin, width=20, font=('Times 20'))
    pininputtxt.grid(row = 2, column = 1, columnspan = 2, sticky = W+E, pady = 2)

    createACC = Button(root, text="Create Account", command = root.destroy, width=15, font=('Times', 14))
    createACC.grid(row = 3, column = 0, sticky = '', pady = 2)

    logIn = Button(root, text="Log In", command = logInScreen, width=10, font=('Times', 14))
    logIn.grid(row = 3, column = 1, sticky = '', pady = 2)

    exit = Button(root, text="Exit", command = root.destroy, width=10, font=('Times', 14))
    exit.grid(row = 3, column = 2, sticky = W, pady = 2)

#Command when Log In button is pressed on main screen
def logInScreen():

    #Checks if user pin equals the actual pin
    testQuery = ('SELECT pin FROM info WHERE accnumber = '+number.get()) 
    cursor.execute(testQuery)
    accpin = cursor.fetchone()
    if(accpin != None and accpin[0] == pin.get()):

        #Log In Screen
        print("works")
        clear_widgets()
        w = Label (root, text="Welcome NAME!\n", font=('Times', 20))
        w.grid(row = 0, column = 1)
    else:
        w = Label (root, text="    Print a Valid Value     \n", font=('Times', 20))
        w.grid(row = 0, column = 1)


welcomeScreen()

root.mainloop()

