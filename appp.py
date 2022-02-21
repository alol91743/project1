import datetime
from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkcalendar import *
import mysql.connector
from tabulate import tabulate

mydb = mysql.connector.connect(host="localhost", user="root", passwd='comp', database='smdb') #change port to 3307
mycursor = mydb.cursor()

paddings = {'padx': 5, 'pady': 5}
font = {'font': ('Helvetica', 11)}
entry_font = {'font': ('Helvetica', 11, 'italic')}

main = Tk()
main.geometry('500x400')
main.title('AAA School Management System')
logo = PhotoImage(file='AAA.png')
panel = Label(main, image = logo)
panel.pack(fill = "both", pady=10)

lb=LabelFrame(main, text='Login')
lb.pack()
#Login page
uidl = Label(lb, text='Username', **font)
uidl.grid(column=0, row=0, **paddings)

uid = Entry(lb, width=25, **entry_font)
uid.grid(column=1, row=0, **paddings)

pwdl = Label(lb, text='Password', **font)
pwdl.grid(column=0, row=1, **paddings)

pwd = Entry(lb, width=25, show="*", **entry_font)
pwd.grid(column=1, row=1, **paddings)


def rec_add():
    top1= Toplevel(main)
    top1.geometry('400x300')
    top= LabelFrame(top1, text="Add Records")
    top.pack()
    Label(top, text="Name", **font).grid(column=0, row=1, **paddings)
    name= Entry(top, width=19, **entry_font)
    name.grid(column=1, row=1, **paddings)

    Label(top, text="Contact Number", **font).grid(column=0, row=2, **paddings)
    contact= Entry(top, width=19, **entry_font)
    contact.grid(column=1, row=2, **paddings)

    Label(top, text="Email Address", **font).grid(column=0, row=3, **paddings)
    email= Entry(top, width=19, **entry_font)
    email.grid(column=1, row=3, **paddings)

    Label(top, text="Gender", **font).grid(column=0, row=4, **paddings)
    gender= Entry(top, width=19, **entry_font)
    gender.grid(column=1, row=4, **paddings)

    Label(top, text="Date of Birth (DOB)", **font).grid(column=0, row=5, **paddings)
    dob = DateEntry(top)
    dob.grid(column=1, row=5, **paddings)

    Label(top, text="Stream", **font).grid(column=0, row=6, **paddings)
    stream= Entry(top, width=19, **entry_font)
    stream.grid(column=1, row=6, **paddings)
    
    def add_records():
        sql = "INSERT INTO students (name, contact, email, gender, dob, stream) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (str(name.get()), str(contact.get()), str(email.get()), str(gender.get()), str(dob.get()), str(stream.get()))
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo('status','Record Added.')
        name.delete(0, 'end') 
        contact.delete(0, 'end')
        email.delete(0, 'end')
        stream.delete(0, 'end')
        gender.delete(0,'end')

        

    btna = Button(top, text="  Add  ", command=add_records)
    btna.grid(column=1, row=7, **paddings)

def rec_show():
    top2 = Toplevel(main)
    mycursor.execute('SELECT * FROM students')
    txt = mycursor.fetchall()
    txt1=tabulate(txt, headers=["Name", "Contact", "Email", "Gender", "DOB", "Stream"])
    lbframe = LabelFrame(top2, text='Records')
    lbframe.pack()
    txt_box = ScrolledText(lbframe)
    txt_box.configure(wrap='word')
    txt_box.insert(END, txt1)
    txt_box.configure(state='disabled')
    txt_box.pack()
    top2.mainloop()
def rec_del():
    top3=Toplevel(main)
    lb_del = LabelFrame(top3)
    ent = Entry(top3, width=19, **entry_font)
    ent.grid(column=0, row=0, **paddings)
    ent.insert(0, "Enter name")
    def delr():
        mycursor.execute("DELETE * FROM students WHERE name='"+ent.get()+"'")
        mydb.commit()
        messagebox.showinfo('status','Record Deleted.')
        
    delbtn = Button(top3, text='Delete', command=delr)
    delbtn.grid(column=0, row=1, **paddings)
lbframe2=LabelFrame(main, text='Options')
btn_add = Button(lbframe2, text='Add Records', command=rec_add, **font)
btn_show = Button(lbframe2, text='Show Records', command=rec_show, **font)
btn_del = Button(lbframe2, text='Delete Records', command=rec_del, **font)
def checkid():
    uidg=uid.get()
    mycursor.execute('SELECT * from users')
    if (uid.get(), pwd.get()) in mycursor.fetchall():
        messagebox.showinfo('Status', 'Logged in.')
        for widget in lb.winfo_children():
            widget.configure(state='disabled')
        if uidg=='admin':
            lbframe2.pack()
            btn_add.grid(column=0, row=0, **paddings)
            btn_show.grid(column=1, row=0, **paddings)
            btn_del.grid(column=2, row=0, **paddings)
        else:
            btn_show.grid(**paddings)
            
    else:
        messagebox.showerror('Error','Enter Valid Crentials.')

def forgot_pwd():
    messagebox.showinfo('Help', 'Contact tech supervisor.')
    
loginbtn = Button(lb, text = 'Login', command=checkid, **font)
loginbtn.grid(column=1, row=3, **paddings)
helpbtn = Button(lb, text = 'Forgot password?', command=forgot_pwd, **font)
helpbtn.grid(column=1, row=4, **paddings)

main.mainloop()
