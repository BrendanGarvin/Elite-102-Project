import tkinter as tk
from tkinter import *
import os
import datetime
import random


import mysql.connector

connection = mysql.connector.connect(user = 'root', database = 'bank', password = '!Bolt2010!')

cursor = connection.cursor(buffered=True)


root = tk.Tk()

number = tk.StringVar()
pin = tk.StringVar()
amount = tk.StringVar()
name = tk.StringVar()
birth = tk.StringVar()
newpin = tk.StringVar()

def validate(date_text):
        try:
            datetime.date.fromisoformat(date_text)
        except ValueError:
            print('date')
            return False
        return True

def create_account_button():
    #Test if valid entries
    if not (validate(birth.get()) and newpin.get().isnumeric() and len(name.get()) > 0):
        w = Label(root, text="Please enter valid values.\n", font=('Times 20'))
        w.grid(row = 0, column = 0, columnspan=2)
        return
    
    accnumber = create_account(name, newpin, birth)

    clear_widgets()
    w = Label(root, text="New user created.\n Welcome " + name.get() + '! \n Your account number is ' + accnumber + '.', font=('Times 20'))
    w.grid(row = 0, column = 0)

    exit = Button(root, text="Exit", command = welcomeScreen, width=10, font=('Times', 14))
    exit.grid(row = 1, column = 0, pady = 2)

def create_account(name, newpin, birth):
    #Get new unique accnumber
    accnumber = ''
    intable = True
    while (intable):
        for x in range(6):
            accnumber = accnumber + str(random.randint(1,9))
        testQuery = ('SELECT * FROM info WHERE accnumber = ' + accnumber)
        cursor.execute(testQuery)
        if(cursor.fetchone() == None):
            intable = False
    
    testQuery = ('INSERT INTO info Values (NULL, \"' + name.get() + '\" , ' + str(accnumber) + ', ' + newpin.get() + ', \"' + birth.get() + '\", 0)' )
    cursor.execute(testQuery)

    connection.commit()
    return accnumber

def check_balance():
    cursor.execute('SELECT money FROM info WHERE accnumber = '+number.get()) 
    money = cursor.fetchone()[0]
    w = Label (root, text="Your balance is: $" + str(money) + '\n', font=('Times', 20))
    w.grid(row = 0, column = 0, columnspan=2)
    return str(money)

def deposit_money_button():
    if not(amount.get().isnumeric()):
        w = Label(root, text="Please enter a number.\n", font=('Times'), width=30)
        w.grid(row = 0, column = 0, columnspan=2)
        return

    deposit_money(amount, number)
    clear_widgets()

    w = Label(root, text="You deposited $" + amount.get() + '. You now have $' + str(cursor.fetchone()[0]) +' in your account.', font=('Times'))
    w.grid(row = 0, column = 0)

    exit = Button(root, text="Go back to main menu", command = logInScreen, font=('Times', 14))
    exit.grid(row = 1, column = 0, sticky = '', pady = 2)

def deposit_money(money, number):
    testQuery = ('SELECT money FROM info WHERE accnumber = ' + number.get())
    cursor.execute(testQuery)

    testQuery = ('UPDATE info SET money = ' + str(int(money.get()) + cursor.fetchone()[0]) + ' WHERE accnumber = ' + number.get()) 
    cursor.execute(testQuery)

    connection.commit()

    testQuery = ('SELECT money FROM info WHERE accnumber = ' + number.get())
    return cursor.execute(testQuery)

def withdraw_money_button():
    if not(amount.get().isnumeric()):
        w = Label(root, text="Please enter a number.\n", font=('Times'), width=30)
        w.grid(row = 0, column = 0, columnspan=2)
        return

    testQuery = ('SELECT money FROM info WHERE accnumber = ' + number.get())
    cursor.execute(testQuery)
    currentMoney = cursor.fetchone()[0]

    if(currentMoney < int(amount.get())):
        w = Label(root, text="Please enter a valid amount of money to withdraw.\n", font=('Times'))
        w.grid(row = 0, column = 0, columnspan=2)
        return
    
    withdraw_money(currentMoney, amount, number)

    clear_widgets()
    w = Label(root, text="You withdrew $" + amount.get() + '. You now have $' + str(cursor.fetchone()[0]) +' in your account.', font=('Times'))
    w.grid(row = 0, column = 0)

    exit = Button(root, text="Go back to main menu", command = logInScreen, font=('Times', 14))
    exit.grid(row = 1, column = 0, sticky = '', pady = 2)

def withdraw_money(currentMoney, amount, number):
    testQuery = ('UPDATE info SET money = ' + str(currentMoney - int(amount.get())) + ' WHERE accnumber = ' + number.get()) 
    cursor.execute(testQuery)

    connection.commit()

    testQuery = ('SELECT money FROM info WHERE accnumber = ' + number.get())
    return cursor.execute(testQuery)

def change_name_button():
    if(len(name.get()) > 0):
        change_name(name, number)
    else:
        w = Label (root, text="Please Enter a Valid Name\n", font=('Times', 20))
        w.grid(row = 0, column = 1)

def change_name(name, number):
    testQuery = ('UPDATE info SET name = \"' + name.get() + '\" WHERE accnumber = ' + number.get())
    cursor.execute(testQuery)

    connection.commit()
    return cursor.execute('SELECT name FROM info WHERE name = \'' + name.get() + "\'")

def change_birth():
    if(validate(birth.get())):
        testQuery = ('UPDATE info SET birth = \"' + birth.get() +'\" WHERE accnumber = ' + number.get())
        cursor.execute(testQuery)

        connection.commit()
    else:
        w = Label (root, text=" Please Enter a Valid Birth \n", font=('Times', 20))
        w.grid(row = 0, column = 1)

def change_pin():
    if(len(newpin.get()) == 4):
        testQuery = ('UPDATE info SET pin = \"' + newpin.get() +'\" WHERE accnumber = ' + number.get())
        cursor.execute(testQuery)

        connection.commit()
        global pin
        pin = newpin
    else:
        w = Label (root, text="  Please Enter a Valid PIN  \n", font=('Times', 20))
        w.grid(row = 0, column = 1)

def delete_account():
    cursor.execute('SELECT name FROM info WHERE accnumber = '+number.get())
    name = cursor.fetchone()[0]
    
    testQuery = ('DELETE FROM info WHERE accnumber = ' + number.get())
    cursor.execute(testQuery)

    connection.commit()

    clear_widgets()
    w = Label(root, text='Deleted Account for ' + name + '.', font=('Times 20'))
    w.grid(row = 0, column = 0)

    exit = Button(root, text="Exit", command = welcomeScreen, width=10, font=('Times', 14))
    exit.grid(row = 1, column = 0, pady = 2)


def clear_widgets():
    for widget in root.winfo_children():
        widget.destroy()

#Main Screen
def welcomeScreen():
    clear_widgets()
    name = tk.StringVar()
    birth = tk.StringVar()
    newpin = tk.StringVar()

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
    createACC = Button(root, text="Create Account", command = createAccountScreen, width=15, font=('Times', 14))
    createACC.grid(row = 3, column = 0, sticky = '', pady = 2)

    logIn = Button(root, text="Log In", command = logInScreen, width=10, font=('Times', 14))
    logIn.grid(row = 3, column = 1, sticky = '', pady = 2)

    exit = Button(root, text="Exit", command = root.destroy, width=10, font=('Times', 14))
    exit.grid(row = 3, column = 2, sticky = W, pady = 2)

def createAccountScreen():
    clear_widgets()
    global name
    global birth
    global newpin
    name = tk.StringVar()
    birth = tk.StringVar()
    newpin = tk.StringVar()


    w = Label(root, text="Create a new account\n", font=('Times 20'))
    w.grid(row = 0, column = 0, columnspan=2)

    nameText = Label (root, text="Full Name:", font=("Times", 20))
    nameText.grid(row = 1, column = 0, sticky = E, pady = 2)

    nameinputtxt = Entry(root, textvariable = name, width=20, font=('Times 20'))
    nameinputtxt.grid(row = 1, column = 1, sticky = E, pady = 2)

    birthText = Label (root, text="Date of Birth \n (YYYY/MM/DD):", font=("Times", 20))
    birthText.grid(row = 2, column = 0, sticky = W, pady = 2)

    birthinputtxt = Entry(root, textvariable = birth, width=20, font=('Times 20'))
    birthinputtxt.grid(row = 2, column = 1, sticky = E, pady = 2)

    pinText = Label (root, text="PIN (4 digits):", font=("Times", 20))
    pinText.grid(row = 3, column = 0, sticky = E, pady = 2)

    pininputtxt = Entry(root, textvariable = newpin, width=20, font=('Times 20'))
    pininputtxt.grid(row = 3, column = 1, sticky = E, pady = 2)

    deposit = Button(root, text='Create', command=create_account_button, width=15, font=('Times 14'))
    deposit.grid(row = 4, column = 0, sticky ='', pady = 2)

    exit = Button(root, text="Exit", command = welcomeScreen, width=10, font=('Times', 14))
    exit.grid(row = 4, column = 1, sticky = W, pady = 2)

#Command when Log In button is pressed on main screen
def logInScreen():

    #Checks if user pin equals the actual pin
    testQuery = ('SELECT pin FROM info WHERE accnumber = '+number.get()) 
    cursor.execute(testQuery)
    accpin = cursor.fetchone()
    if(accpin != None and accpin[0] == pin.get()):
        #Log In Screen
        clear_widgets()
        global amount
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
        w.grid(row = 0, column = 0, columnspan=3)

def depositScreen():
    clear_widgets()


    w = Label(root, text="How much money would you like to deposit?\n", font=('Times'))
    w.grid(row = 0, column = 0, columnspan=2)

    amountinputtxt = Entry(root, textvariable = amount, width=20, font=('Times 20'), justify=CENTER)
    amountinputtxt.grid(row = 1, column = 0, columnspan = 2, sticky = W+E, pady = 2)

    deposit = Button(root, text='Deposit', command=deposit_money_button, width=15, font=('Times 14'))
    deposit.grid(row = 2, column = 0, sticky ='', pady = 2)

    exit = Button(root, text="Cancel", command = logInScreen, width=10, font=('Times', 14))
    exit.grid(row = 2, column = 1, sticky = W, pady = 2)

def withdrawScreen():
    clear_widgets()


    w = Label(root, text="How much money would you like to withdraw?\n", font=('Times'))
    w.grid(row = 0, column = 0, columnspan=2)

    amountinputtxt = Entry(root, textvariable = amount, width=20, font=('Times 20'), justify=CENTER)
    amountinputtxt.grid(row = 1, column = 0, columnspan = 2, sticky = W+E, pady = 2)

    deposit = Button(root, text='Withdraw', command=withdraw_money_button, width=15, font=('Times 14'))
    deposit.grid(row = 2, column = 0, sticky ='', pady = 2)

    exit = Button(root, text="Cancel", command = logInScreen, width=10, font=('Times', 14))
    exit.grid(row = 2, column = 1, sticky = W, pady = 2)

def editScreen():

    clear_widgets()
    global name
    global birth
    global newpin
    name = tk.StringVar()
    birth = tk.StringVar()
    newpin = tk.StringVar()


    w = Label (root, text="Edit Account\n", font=('Times', 20))
    w.grid(row = 0, column = 1)

    nametxt = Label (root, text="Name:", font=('Times', 20))
    nametxt.grid(row = 1, column = 0, sticky = E)

    nameinputtxt = Entry(root, textvariable = name, width=20, font=('Times 20'))
    nameinputtxt.grid(row = 1, column = 1, pady = 2)

    changeName = Button(root, text='Change Name', command=change_name_button, width=15, font=('Times 14'))
    changeName.grid(row = 1, column = 2, sticky ='', pady = 2)

    birthtxt = Label (root, text="Birth\n (YYYY-MM-DD):", font=('Times', 20))
    birthtxt.grid(row = 2, column = 0, sticky = E)

    birthinputtxt = Entry(root, textvariable = birth, width=20, font=('Times 20'))
    birthinputtxt.grid(row = 2, column = 1, pady = 2)

    changeBirth = Button(root, text='Change Birth', command=change_birth, width=15, font=('Times 14'))
    changeBirth.grid(row = 2, column = 2, sticky ='', pady = 2)

    pintxt = Label (root, text="PIN (4 Digits):", font=('Times', 20))
    pintxt.grid(row = 3, column = 0, sticky = E)

    pininputtxt = Entry(root, textvariable = newpin, width=20, font=('Times 20'))
    pininputtxt.grid(row = 3, column = 1, pady = 2)

    changePIN = Button(root, text='Change PIN', command=change_pin, width=15, font=('Times 14'))
    changePIN.grid(row = 3, column = 2, sticky ='', pady = 2)

    delete = Button(root, text="Delete Account", command = delete_account, font=('Times', 14))
    delete.grid(row = 4, column = 0, sticky = '', pady = 2)

    exit = Button(root, text="Exit", command = logInScreen, width=10, font=('Times', 14))
    exit.grid(row = 4, column = 1, sticky = '', pady = 2)

welcomeScreen()

root.mainloop()

