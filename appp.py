import datetime
from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from unicodedata import name
from tkcalendar import *
import mysql
import mysql.connector
from tabulate import tabulate

mydb = mysql.connector.connect(host="localhost", user="root", passwd='comp', database='smdb')
mycursor = mydb.cursor()

paddings = {'padx': 5, 'pady': 5}
font = {'font': ('Helvetica', 11)}
entry_font = {'font': ('Helvetica', 11, 'italic')}

main = Tk()
main.geometry('500x500')
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
    Label(top, text="Adm No.", **font).grid(column=0, row=1, **paddings)
    admno= Entry(top, width=19, **entry_font)
    admno.grid(column=1, row=1, **paddings)

    Label(top, text="Name", **font).grid(column=0, row=2, **paddings)
    name= Entry(top, width=19, **entry_font)
    name.grid(column=1, row=2, **paddings)

    Label(top, text="Contact No.", **font).grid(column=0, row=3, **paddings)
    contact= Entry(top, width=19, **entry_font)
    contact.grid(column=1, row=3, **paddings)

    Label(top, text="Gender", **font).grid(column=0, row=4, **paddings)
    gender= Entry(top, width=19, **entry_font)
    gender.grid(column=1, row=4, **paddings)

    Label(top, text="Date of Birth (DOB)", **font).grid(column=0, row=5, **paddings)
    dob = DateEntry(top)
    dob.grid(column=1, row=5, **paddings)

    Label(top, text="Class", **font).grid(column=0, row=6, **paddings)
    class_= Entry(top, width=19, **entry_font)
    class_.grid(column=1, row=6, **paddings)
    
    def add_records():
        sql = "INSERT INTO students (admno, name, contact, gender, dob, class) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (str(admno.get()), str(name.get()), str(contact.get()), str(gender.get()), str(dob.get()), str(class_.get()))
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo('status','Record Added.')
        name.delete(0, 'end') 
        contact.delete(0, 'end')
        admno.delete(0, 'end')
        class_.delete(0, 'end')
        gender.delete(0,'end')

    btna = Button(top, text="  Add  ", command=add_records)
    btna.grid(column=1, row=7, **paddings)

def rec_show():
    top2 = Toplevel(main)
    mycursor.execute('SELECT * FROM students')
    txt = mycursor.fetchall()
    txt1=tabulate(txt, headers=["Adm No.", "Name", "Contact", "Gender", "DOB", "Class"])

    lbframe = LabelFrame(top2, text='Records')
    lbframe.pack()
    txt_box = ScrolledText(lbframe)
    txt_box.configure(wrap='word')
    txt_box.insert(END, txt1)
    txt_box.configure(state='disabled')
    txt_box.grid(column=0, row=0, **paddings)

    lbframen = LabelFrame(top2, text='More Options')
    lbframen.pack()
    srch=Label(lbframen, text='Search', **font)
    srch.grid(column=0, row=0, **paddings)
    search_box=Entry(lbframen, width=19, **entry_font)
    search_box.grid(column=1, row=0, **paddings)
    txt_box2 = ScrolledText(top2, height=5)
    txt_box2.configure(wrap='word')

    def srch():
        for i in txt:
            if i[0]==int(search_box.get()):
                l=[]
                l.append(i)
                messagebox.showinfo('Status', 'Record(s) Found.')
                txt_box2.insert(END, tabulate(l, headers=["Adm No.", "Name", "Contact", "Gender", "DOB", "Class"]))
                txt_box2.pack()
                txt_box2.configure(state='disabled')
    srchbtn = Button(lbframen, text="Search", command=srch)
    srchbtn.grid(column=1, row=1)

    
    top2.mainloop()

def rec_del():
    top3=Toplevel(main)
    lb1 = LabelFrame(top3, text='Modify Records')
    lb1.pack()
    ent = Entry(lb1, width=19, **entry_font)
    ent.grid(column=0, row=0, **paddings)
    ent.insert(0, "Enter Adm No.")
    def delr():
        sql = "DELETE FROM students WHERE admno=%s"
        val = (str(ent.get()), )
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo('status','Record Deleted.')
        
    delbtn = Button(lb1, text='Delete', command=delr)
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
