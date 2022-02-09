from ast import And
import datetime
from operator import and_
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkcalendar import *
import mysql.connector

mydb = mysql.connector.connect(host="localhost", port=3306, user="root", passwd='comp', database='smdb') #change port to 3307

print(mydb)

mycursor = mydb.cursor()



main = Tk()
main.title('AAA School Management System')
main.geometry('600x400')

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
gender= Entry(main, width=19)
gender.pack()

Label(main, text="Date of Birth (DOB)").pack()
dob = DateEntry(main)
dob.pack()

Label(main, text="Stream").pack()
stream= Entry(main, width=19)
stream.pack()

rec_confirm = Label(main, text='Record Added')





'''def checkemp():
    return (not name.get()) and (not contact.get()) and (not email.get()) and (not stream.get())'''

def add_records():
    sql = "INSERT INTO students (name, contact, email, gender, dob, stream) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (str(name.get()), str(contact.get()), str(email.get()), str(gender.get()), str(dob.get()), str(stream.get()))
    mycursor.execute(sql, val)
    mydb.commit()
    
    name.delete(0, 'end') 
    contact.delete(0, 'end')
    email.delete(0, 'end')
    y.set('Choose an option.')
    stream.delete(0, 'end')

    rec_confirm.pack()

def rec_show():
    top = Toplevel(main)
    mycursor.execute('SELECT * FROM students')
    txt = mycursor.fetchall()
    txt_box = ScrolledText(top)
    txt_box.configure(wrap='word')
    for i in txt:
        txt_box.insert(END, i)
        txt_box.insert(END, '\n')
    txt_box.pack()
    top.mainloop()


btn = Button(main, text="Add Record", command=add_records)
btn.pack()
rec = Button(main, text="Show Records", command=rec_show)
rec.pack()


main.mainloop()

