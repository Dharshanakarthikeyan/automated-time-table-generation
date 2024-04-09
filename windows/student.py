import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

fid = passw = conf_passw = name = roll = section = None



def create_treeview():
    tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 5)))
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("#1", width=70, stretch=tk.NO)
    tree.column("#2", width=200, stretch=tk.NO)
    tree.column("#3", width=80, stretch=tk.NO)
    tree.column("#4", width=80, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('#1', text="sid")
    tree.heading('#2', text="Name")
    tree.heading('#3', text="Roll")
    tree.heading('#4', text="Section")
    tree['height'] = 12



def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT SID, NAME, ROLL, SECTION FROM STUDENT")
    for row in cursor:
        tree.insert(
            "",
            0,
            values=(row[0], row[1], row[2], row[3])
        )
    tree.place(x=600, y=100)



def parse_data():
    fid = str(fid_entry.get())
    passw = str(passw_entry.get())
    conf_passw = str(conf_passw_entry.get())
    name = str(name_entry.get()).upper()
    roll = str(roll_entry.get())
    section = str(sec_entry.get()).upper()

    if fid == "" or passw == "" or \
        conf_passw == "" or name == "" or \
        roll == "" or section == "":
        messagebox.showwarning("Bad Input", "Some fields are empty! Please fill them out!")
        return

    if passw != conf_passw:
        messagebox.showerror("Passwords mismatch", "Password and confirm password didnt match. Try again!")
        passw_entry.delete(0, tk.END)
        conf_passw_entry.delete(0, tk.END)
        return
  
    conn.execute(f"REPLACE INTO STUDENT (SID, PASSW, NAME, ROLL, SECTION)\
        VALUES ('{fid}','{passw}','{name}', '{roll}', '{section}')")
    conn.commit()
    update_treeview()
    
    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    sec_entry.delete(0, tk.END)
    


def update_data():
    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    sec_entry.delete(0, tk.END)
    try:
        # print(tree.selection())
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one student at a time to update!")
            return

        q_fid = tree.item(tree.selection()[0])['values'][0]
        cursor = conn.execute(f"SELECT * FROM STUDENT WHERE SID = '{q_fid}'")

        cursor = list(cursor)
        fid_entry.insert(0, cursor[0][0])
        passw_entry.insert(0, cursor[0][1])
        conf_passw_entry.insert(0, cursor[0][1])
        name_entry.insert(0, cursor[0][2])
        roll_entry.insert(0, cursor[0][3])
        sec_entry.insert(0, cursor[0][4])
        
        conn.execute(f"DELETE FROM STUDENT WHERE SID = '{cursor[0][0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a student from the list first!")
        return



def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a student from the list first!")
        return
    for i in tree.selection():
        # print(tree.item(i)['values'][0])
        conn.execute(f"DELETE FROM STUDENT WHERE SID = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()



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




# main
if __name__ == "__main__":  


    conn = sqlite3.connect(r'db/data.db')


    conn.execute('CREATE TABLE IF NOT EXISTS STUDENT\
    (SID CHAR(10) NOT NULL PRIMARY KEY,\
    PASSW CHAR(50) NOT NULL,\
    NAME CHAR(50) NOT NULL,\
    ROLL INTEGER NOT NULL,\
    SECTION CHAR(5) NOT NULL)')






    subtk = tk.Tk()
    subtk.geometry('1100x470')

    subtk.config(bg="#092138")
    subtk.title('Add/Update Students')

    # Label1
    tk.Label(
        subtk,
        text='List of Students',
        font=('comic', 20, 'bold'),bg="#092138",fg="#fff",
    ).place(x=600, y=50)

    # Label2
    tk.Label(
        subtk,
        text='Add/Update Students',
        font=('comic', 20, 'bold'),bg="#092138",fg="#fff",
    ).place(x=100, y=50)


    # Label4
    tk.Label(
        subtk,
        text='Student id:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=130)

    # Entry1
    fid_entry = tk.Entry(
        subtk,
        font=('comic', 12),
        width=20
    )
    fid_entry.place(x=260, y=130)

    # Label5
    tk.Label(
        subtk,
        text='Password:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=170)

    # Entry2
    passw_entry = tk.Entry(
        subtk,
        font=('comic', 12),
        width=20,
        show="●"
    )
    passw_entry.place(x=260, y=170)

    B1_show = tk.Button(
        subtk,
        text='○',
        font=('comic', 9, 'bold'),
        command=show_passw
    )
    B1_show.place(x=460,y=170)

    # Label6
    tk.Label(
        subtk,
        text='Confirm Password:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=210)

    # Entry3
    conf_passw_entry = tk.Entry(
        subtk,
        font=('comic', 12),
        width=20,
        show="●"
    )
    conf_passw_entry.place(x=260, y=210)

    # Label7
    tk.Label(
        subtk,
        text='Student Name:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=250)

    # Entry4
    name_entry = tk.Entry(
        subtk,
        font=('comic', 12),
        width=25,
    )
    name_entry.place(x=260, y=250)

    # Label8
    tk.Label(
        subtk,
        text='Roll no.:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=290)

    # Entry5
    roll_entry = tk.Entry(
        subtk,
        font=('comic', 12),
        width=5,
    )
    roll_entry.place(x=260, y=290)

    # Label9
    tk.Label(
        subtk,
        text='Section:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=330)


    cursor = conn.execute("SELECT DISTINCT SECTION FROM STUDENT")
    sec_li = [row[0] for row in cursor]
    # sec_li.insert(0, 'NULL')
    print(sec_li)
    sec_entry = ttk.Combobox(
        subtk,
        values=sec_li,
    )
    sec_entry.pack(side=tk.LEFT)
    sec_entry.current(0)

    sec_entry.place(x=260, y=330)

    # Button1
    B1 = tk.Button(
        subtk,
        text='Add Student',
        font=('comic', 12),bg="#cca307",fg="#fff",
        command=parse_data
    )
    B1.place(x=100,y=400)

    # Button2
    B2 = tk.Button(
        subtk,
        text='Update Student',
        font=('comic', 12),bg="#cca307",fg="#fff",
        command=update_data
    )
    B2.place(x=220,y=400)

    # Treeview1
    tree = ttk.Treeview(subtk)
    create_treeview()
    update_treeview()

    # Button3
    B3 = tk.Button(
        subtk,
        text='Delete Student(s)',
        font=('comic', 12),bg="#cca307",fg="#fff",
        command=remove_data
    )
    B3.place(x=360,y=400)

    tk.Button(
        subtk,
        text='< Back',
        font=('comic', 12), bg="#cca307", fg="#fff", width=5,
        command=subtk.destroy
    ).place(x=0, y=0)

    subtk.mainloop()
    conn.close() # close database after all operations
