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

#Delete Row method
#testQuery = (DELTE FROM info WHERE accnumber = ')

#Update Money Method
#testQuery = ('UPDATE info SET money = 2000 WHERE accnumber = 123456') 

#cursor.execute(testQuery)

#connection.commit()


root = tk.Tk()

number = tk.StringVar()
pin = tk.StringVar()
amount = tk.StringVar()

def create_account():
    return

def check_balance():
    return

def deposit_money():
    clear_widgets()

    testQuery = ('SELECT money FROM info WHERE accnumber = ' + number.get())
    cursor.execute(testQuery)

    testQuery = ('UPDATE info SET money = ' + str(int(amount.get()) + cursor.fetchone()[0]) + ' WHERE accnumber = ' + number.get()) 
    cursor.execute(testQuery)

    connection.commit()

    testQuery = ('SELECT money FROM info WHERE accnumber = ' + number.get())
    cursor.execute(testQuery)

    w = Label(root, text="You deposited " + amount.get() + '. You now have ' + str(cursor.fetchone()[0]) +' in your account.', font=('Times'))
    w.grid(row = 0, column = 0)

    exit = Button(root, text="Go back to main menu", command = logInScreen, font=('Times', 14))
    exit.grid(row = 1, column = 0, sticky = '', pady = 2)

def withdraw_money():
    return


def clear_widgets():
    for widget in root.winfo_children():
        widget.destroy()

#Main Screen
def welcomeScreen():
    clear_widgets()

    #Grid of labels and input
    w = Label (root, text="Welcome to Beaver Bank\n", font=('Times', 20))
    w.grid(row = 0, column = 0, columnspan=3)

    numberText = Label (root, text="Account Number:", font=("Times", 20))
    numberText.grid(row = 1, column = 0, sticky = W, pady = 2)

    numberinputtxt = Entry(root, textvariable = number, width=20, font=('Times 20'))
    numberinputtxt.grid(row = 1, column = 1, columnspan = 2, sticky = W+E, pady = 2)

    pinText = Label (root, text="PIN:", font=("Times", 20))
    pinText.grid(row = 2, column = 0, sticky = E, pady = 2)

    pininputtxt = Entry(root, textvariable = pin, width=20, font=('Times 20'))
    pininputtxt.grid(row = 2, column = 1, columnspan = 2, sticky = W+E, pady = 2)

    #Buttons
    createACC = Button(root, text="Create Account", command = create_account, width=15, font=('Times', 14))
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
        clear_widgets()
        amount = tk.StringVar()

        #Log In Message
        cursor.execute('SELECT name FROM info WHERE accnumber = '+number.get())
        w = Label (root, text="Welcome " + cursor.fetchone()[0] +"!\n", font=('Times', 20))
        w.grid(row = 0, column = 0, columnspan=2)

        #Buttons
        balance = Button(root, text='Check Balance', command=check_balance, width=15, font=('Times 14'))
        balance.grid(row = 1, column = 0, sticky ='', pady = 2)

        deposit = Button(root, text='Deposit Money', command=depositScreen, width=15, font=('Times 14'))
        deposit.grid(row = 1, column = 1, sticky ='', pady = 2)

        withdraw = Button(root, text='Withdraw', command=withdrawScreen, width=15, font=('Times 14'))
        withdraw.grid(row = 2, column = 0, sticky ='', pady = 2)

        editACC = Button(root, text='Edit Account', command=editScreen, width=15, font=('Times 14'))
        editACC.grid(row = 2, column = 1, sticky ='', pady = 2)

        exit = Button(root, text="Exit", command = welcomeScreen, width=10, font=('Times', 14))
        exit.grid(row = 3, column = 1, sticky = W, pady = 2)

    else:
        w = Label (root, text="    Insert a Valid Value     \n", font=('Times', 20))
        w.grid(row = 0, column = 1)

def depositScreen():
    clear_widgets()


    w = Label(root, text="How much money would you like to deposit?\n", font=('Times'))
    w.grid(row = 0, column = 0, columnspan=2)

    amountinputtxt = Entry(root, textvariable = amount, width=20, font=('Times 20'), justify=CENTER)
    amountinputtxt.grid(row = 1, column = 0, columnspan = 2, sticky = W+E, pady = 2)

    deposit = Button(root, text='Deposit', command=deposit_money, width=15, font=('Times 14'))
    deposit.grid(row = 2, column = 0, sticky ='', pady = 2)

    exit = Button(root, text="Cancel", command = logInScreen, width=10, font=('Times', 14))
    exit.grid(row = 2, column = 1, sticky = W, pady = 2)

def withdrawScreen():
    return

def editScreen():
    return

welcomeScreen()

root.mainloop()

