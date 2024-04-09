import tkinter as tk
import sys
import os
import threading

def run_sub(): os.system('py windows\\subjects.py')
def run_fac(): os.system('py windows\\faculty.py')
def run_stud(): os.system('py windows\\student.py')
def run_sch(): os.system('py windows\\scheduler.py')
def run_tt_s(): os.system('py windows\\timetable_stud.py')
def run_tt_f(): os.system('py windows\\timetable_fac.py')

ad = tk.Tk()
ad.geometry('1280x720')

ad.config(bg="#092138")
ad.title('Admin Dashboard')
tk.Label(
    ad,
    text='Automated Time Table Generator',
    font=('comic', 20, 'bold'),bg="#092138",fg="#ffffff",
    wrap=900
).pack(pady=20)

tk.Label(
    ad,
    text='WELCOME ADMINISTRATOR',
    font=('comic', 20, 'bold'),bg="#092138",fg="#ffffff",
    pady=5
).pack()

tk.Label(
    ad,
    text='(Admin Dashboard)',
    font=('comic', 12, 'italic'),bg="#092138",fg="#ffffff",
).pack(pady=2)

modify_frame = tk.LabelFrame(text='Add Items', font=('comic'), bg="#f0edda", padx=50,pady=4)
modify_frame.place(x=380, y=230)

tk.Button(
    modify_frame,
    text='Subjects',
    font=('comic'),bg="#cca307",fg="#fff",width=12,
    command=run_sub
).pack(pady=20)

tk.Button(
    modify_frame,
    text='Faculties',
    font=('comic'),bg="#cca307",fg="#fff",width=12,
    command=run_fac
).pack(pady=20)

tk.Button(
    modify_frame,
    text='Students',
    font=('comic'),bg="#cca307",fg="#fff",width=12,
    command=run_stud
).pack(pady=20)

tt_frame = tk.LabelFrame(text='Timetable', font=('comic'), bg="#f0edda", padx=30,pady=4)
tt_frame.place(x=650, y=230)

tk.Button(
    tt_frame,
    text='Schedule Periods',
    font=('comic'),bg="#cca307",fg="#fff",
    command=run_sch
).pack(pady=20)

tk.Button(
    tt_frame,
    text='View Class-Wise',
    font=('comic'),bg="#cca307",fg="#fff",width=15,
    command=run_tt_s
).pack(pady=20)

tk.Button(
    tt_frame,
    text='View Faculty-wise',
    font=('comic'),bg="#cca307",fg="#fff",width=15,
    command=run_tt_f
).pack(pady=20)


tk.Button(
    ad,
    text='Quit',
    font=('comic'),bg="#cca307",fg="#fff",width=9,
    command=ad.destroy
).place(x=590, y=170)

ad.mainloop()