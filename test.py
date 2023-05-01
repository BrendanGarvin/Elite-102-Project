import unittest
import tkinter as tk
from tkinter import *
import os
import mysql.connector

connection = mysql.connector.connect(user = 'root', database = 'bank', password = '!Bolt2010!')

cursor = connection.cursor(buffered=True)
from main import *

root = tk.Tk()

class Tests(unittest.TestCase):
    def test_create_account(self):
        name = tk.StringVar(master=root, value='John Doge')
        birth = tk.StringVar(master=root, value='2000-02-02')
        newpin = tk.StringVar(master=root, value='1234')
        number = create_account(name, newpin, birth)
        cursor.execute('SELECT accnumber FROM info WHERE name = \'John Doge\'') 
        self.assertEquals(int(number), cursor.fetchone()[0])
        cursor.execute('DELETE FROM info WHERE name = \'John Doge\'') 
        connection.commit()

    def test_deposit(self):
        number = tk.StringVar(master=root, value='123456')
        amount = tk.StringVar(master=root, value='2000')
        cursor.execute('SELECT money FROM info WHERE name = \'John Doe\'')
        money = cursor.fetchone()[0]
        deposit_money(amount, number)
        self.assertEquals(money + int(amount.get()), cursor.fetchone()[0])

    def test_withdraw(self):
        number = tk.StringVar(master=root, value='123456')
        amount = tk.StringVar(master=root, value='2000')
        cursor.execute('SELECT money FROM info WHERE name = \'John Doe\'')
        money = cursor.fetchone()[0]
        withdraw_money(money, amount, number)
        self.assertEquals(money - int(amount.get()), cursor.fetchone()[0])

    def test_change_name(self):
        number = tk.StringVar(master=root, value='123456')
        name = tk.StringVar(master=root, value='John Doge')
        change_name(name, number)
        self.assertEquals(name.get(), cursor.fetchone()[0])
        testQuery = ('UPDATE info SET name = \"John Doe\" WHERE accnumber = ' + number.get())
        cursor.execute(testQuery)
        connection.commit()

if __name__ == '__main__':
    unittest.main()
    root.mainloop()