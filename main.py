import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os, sys
sys.path.insert(0, 'windows/')
import timetable_stud
import timetable_fac
import sqlite3

def challenge():
    conn = sqlite3.connect(r'db/data.db')

    user = str(combo1.get())
    if user == "Student":
        cursor = conn.execute(f"SELECT PASSW, SECTION, NAME, ROLL FROM STUDENT WHERE SID='{id_entry.get()}'")
        cursor = list(cursor)
        if len(cursor) == 0:
            messagebox.showwarning('Bad id', 'No such user found!')
        elif passw_entry.get() != cursor[0][0]:
            messagebox.showerror('Bad pass', 'Incorret Password!')
        else:
            nw = tk.Tk()
            tk.Label(
                nw,
                text=f'{cursor[0][2]}\tSection: {cursor[0][1]}\tRoll No.: {cursor[0][3]}',
                font=('comic', 12, 'italic'),
            ).pack()
            m.destroy()
            timetable_stud.student_tt_frame(nw, cursor[0][1])
            nw.mainloop()

    elif user == "Faculty":
        cursor = conn.execute(f"SELECT PASSW, INI, NAME, EMAIL FROM FACULTY WHERE FID='{id_entry.get()}'")
        cursor = list(cursor)
        if len(cursor) == 0:
            messagebox.showwarning('Bad id', 'No such user found!')
        elif passw_entry.get() != cursor[0][0]:
            messagebox.showerror('Bad pass', 'Incorret Password!')
        else:
            nw = tk.Tk()
            tk.Label(
                nw,
                text=f'{cursor[0][2]} ({cursor[0][1]})\tEmail: {cursor[0][3]}',
                font=('comic', 12, 'italic'),
            ).pack()
            m.destroy()
            timetable_fac.fac_tt_frame(nw, cursor[0][1])
            nw.mainloop()

    elif user == "Admin":
        if id_entry.get() == 'admin' and passw_entry.get() == 'admin':
            m.destroy()
            os.system('py windows\\admin_screen.py')
            # sys.exit()
        else:
            messagebox.showerror('Bad Input', 'Incorret Username/Password!')
            


m = tk.Tk()

m.geometry('1280x720')

m.config(bg="#092138")
m.title('Welcome')

tk.Label(
    m,
    text='Automated Time Table Generator',
    font=('comic', 20, 'bold'),bg="#092138",fg="#ffffff",
    wrap=900
).pack(pady=20)

modify_frame = tk.LabelFrame(text='Login', font=('comic'), bg="#f0edda", padx=70,pady=4)
modify_frame.place(x=470, y=130)

tk.Label(
    modify_frame,
    text='Username',bg="#f0edda",
    font=('comic', 15)
).pack(pady=10)

id_entry = tk.Entry(
    modify_frame,
    font=('comic', 12),
    width=21
)
id_entry.pack()

# Label5
tk.Label(
    modify_frame,
    text='Password',bg="#f0edda",
    font=('comic', 15)
).pack(pady=10)

# toggles between show/hide password
def show_passw():
    if passw_entry['show'] == "●":
        passw_entry['show'] = ""
        B1_show['text'] = '●'
        B1_show.update()
    elif passw_entry['show'] == "":
        passw_entry['show'] = "●"
        B1_show['text'] = '○'
        B1_show.update()
    passw_entry.update()


# Entry2
passw_entry = tk.Entry(
    modify_frame,
    font=('comic', 12),
    width=21,
    show="●"
)
passw_entry.pack()

B1_show = tk.Button(
    modify_frame,
    text='○',
    font=('comic', 12, 'bold'),

    command=show_passw,
    padx=5,

)
B1_show.pack(padx=15,pady=5)

combo1 = ttk.Combobox(
    modify_frame,font=('comic', 12),
    width=18,
    values=['Student', 'Faculty', 'Admin']
)
combo1.pack(pady=16)
combo1.current(0)

tk.Button(
    modify_frame,
    text='Login',
    font=('comic', 12, 'bold'),
    width=12,bg="#cca307",fg="#fff",
    padx=30,
    command=challenge
).pack(pady=10)

m.mainloop()