import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry  # pip install tkcalendar

import mysql.connector

mydb = mysql.connector.connect(host="localhost",port=3307, user="root", passwd="comp")

print(mydb)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE school_mgmt")

mycursor.execute("CREATE TABLE students (name VARCHAR(255), contact_number INT(10), email VARCHAR(255), gender BOOL(), date1 DATE())")


main = Tk()
main.title('AAA School Management System')
main.geometry('600x600')

Label(main, text="SCHOOL MANAGEMENT SYSTEM").pack()

Label(main, text="Name").pack()
name= Entry(main, width=19)
name.pack()

Label(main, text="Contact Number").pack()
contact= Entry(main, width=19)
contact.pack()

Label(main, text="Email Address").pack()
email= Entry(main, width=19)
email.pack()

Label(main, text="Gender").pack()
gender= OptionMenu(main, 'Male', "Female")
gender.pack()

Label(main, text="Date of Birth (DOB)").pack()
dob = DateEntry(main)
dob.pack()

Label(main, text="Stream").pack()
stream= Entry(main, width=19)
stream.pack()

def table_update():
    sql = "INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s)"
    val = (name.get(), contact.get(), email.get(), gender.get(), dob.get())
    mycursor.execute(sql, val)
    print(mydb)
    
btn = Button(main, text="Add Record")
btn.pack()


main.mainloop()
