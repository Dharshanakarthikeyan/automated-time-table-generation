import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

fid = passw = conf_passw = name = ini = email = subcode1 = subcode2 = subcode3 = subcode4 = sub1_hr = sub2_hr = sub3_hr = sub4_hr = dep =  None


def create_treeview():
    tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 8)))
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("#1", width=70, stretch=tk.NO)
    tree.column("#2", width=200, stretch=tk.NO)
    tree.column("#3", width=80, stretch=tk.NO)
    tree.column("#4", width=80, stretch=tk.NO)

    tree.column("#5", width=80, stretch=tk.NO)

    tree.column("#6", width=80, stretch=tk.NO)

    tree.column("#7", width=80, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('#1', text="Fid")
    tree.heading('#2', text="Name")
    tree.heading('#3', text="Subject 1")
    tree.heading('#4', text="Subject 2")

    tree.heading('#5', text="Subject 3")

    tree.heading('#6', text="Subject 4")

    tree.heading('#7', text="Dept")
    tree['height'] = 15


def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT FID, NAME, SUBCODE1, SUBCODE2, SUBCODE3, SUBCODE4, DEP FROM FACULTY")
    for row in cursor:
        tree.insert(
            "",
            0,
            values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        )
    tree.place(x=600, y=100)


def parse_data():
    fid = str(fid_entry.get())
    passw = str(passw_entry.get())
    conf_passw = str(conf_passw_entry.get())
    name = str(name_entry.get()).upper()
    ini = str(ini_entry.get()).upper()
    email = str(email_entry.get())
    subcode1 = str(combo1.get())
    subcode2 = str(combo2.get())

    subcode3 = str(combo3.get())

    subcode4 = str(combo4.get())
    sub1_hr = str(sub1.get())

    sub2_hr = str(sub2.get())

    sub3_hr = str(sub3.get())

    sub4_hr = str(sub4.get())

    dep = str(dep_entry.get()).upper()
    if fid == "" or passw == "" or \
        conf_passw == "" or name == "":
        messagebox.showwarning("Bad Input", "Some fields are empty! Please fill them out!")
        return

    if passw != conf_passw:
        messagebox.showerror("Passwords mismatch", "Password and confirm password didnt match. Try again!")
        passw_entry.delete(0, tk.END)
        conf_passw_entry.delete(0, tk.END)
        return

    if subcode1 == "NULL":
        messagebox.showwarning("Bad Input", "Subject 1 cant be NULL")
        return
    
    conn.execute(f"REPLACE INTO FACULTY (FID, PASSW, NAME, INI, EMAIL, SUBCODE1, SUBCODE2, SUBCODE3, SUBCODE4, SUB1_HR, SUB2_HR, SUB3_HR, SUB4_HR, DEP)\
        VALUES ('{fid}','{passw}','{name}', '{ini}', '{email}', '{subcode1}', '{subcode2}', '{subcode3}', '{subcode4}', '{sub1_hr}', '{sub2_hr}', '{sub3_hr}', '{sub4_hr}', '{dep}')")
    conn.commit()
    update_treeview()

    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    ini_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

    dep_entry.delete(0, tk.END)
    combo1.current(0)
    combo2.current(0)

    combo3.current(0)
    combo4.current(0)
    sub1.delete(0, tk.END)
    sub2.delete(0, tk.END)
    sub3.delete(0, tk.END)

    sub4.delete(0, tk.END)

    dep.delete(0, tk.END)
def update_data():
    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    ini_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    combo1.current(0)
    combo2.current(0)

    combo3.current(0)

    combo4.current(0)

    sub1.delete(0, tk.END)
    sub2.delete(0, tk.END)
    sub3.delete(0, tk.END)

    dep_entry.delete(0, tk.END)
    sub4.delete(0, tk.END)
    try:
        # print(tree.selection())
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one faculty at a time to update!")
            return

        q_fid = tree.item(tree.selection()[0])['values'][0]
        cursor = conn.execute(f"SELECT * FROM FACULTY WHERE FID = '{q_fid}'")

        cursor = list(cursor)
        fid_entry.insert(0, cursor[0][0])
        passw_entry.insert(0, cursor[0][1])
        conf_passw_entry.insert(0, cursor[0][1])
        name_entry.insert(0, cursor[0][2])
        ini_entry.insert(0, cursor[0][3])
        email_entry.insert(0, cursor[0][4])
        combo1.current(subcode_li.index(cursor[0][5]))
        combo2.current(subcode_li.index(cursor[0][6]))

        combo3.current(subcode_li.index(cursor[0][7]))

        sub1.insert(0, cursor[0][8])

        sub2.insert(0, cursor[0][9])

        sub3.insert(0, cursor[0][10])

        combo4.current(subcode_li.index(cursor[0][11]))
        sub4.insert(0, cursor[0][12])

        dep_entry.insert(0, cursor[0][13])
        conn.execute(f"DELETE FROM FACULTY WHERE FID = '{cursor[0][0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a faculty from the list first!")
        return


def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a faculty from the list first!")
        return
    for i in tree.selection():
        # print(tree.item(i)['values'][0])
        conn.execute(f"DELETE FROM FACULTY WHERE FID = '{tree.item(i)['values'][0]}'")
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

    conn.execute('CREATE TABLE IF NOT EXISTS FACULTY\
    (FID CHAR(10) NOT NULL PRIMARY KEY,\
    PASSW CHAR(50) NOT NULL,\
    NAME CHAR(50) NOT NULL,\
    INI CHAR(5) NOT NULL,\
    EMAIL CHAR(50) NOT NULL,\
    SUBCODE1 CHAR(10) NOT NULL,\
    SUBCODE2 CHAR(10),\
    SUBCODE3 CHAR(10) )')




    subtk = tk.Tk()
    subtk.geometry('1200x650')

    subtk.config(bg="#092138")
    subtk.title('Add/Update Faculties')

    # Label1
    tk.Label(
        subtk,
        text='List of Faculties',
        font=('comic', 20, 'bold'),bg="#092138",fg="#fff",
    ).place(x=600, y=50)

    # Label2
    tk.Label(
        subtk,
        text='Add/Update Faculties',
        font=('comic', 20, 'bold'),bg="#092138",fg="#fff",
    ).place(x=100, y=50)


    # Label4
    tk.Label(
        subtk,
        text='Faculty id:',
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
        text='Faculty Name:',
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
        text='Initials:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=290)

    # Entry5
    ini_entry = tk.Entry(
        subtk,
        font=('comic', 12),
        width=5,
    )
    ini_entry.place(x=260, y=290)

    # Label9
    tk.Label(
        subtk,
        text='Email:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=330)

    # Entry6
    email_entry = tk.Entry(
        subtk,
        font=('comic', 12),
        width=25,
    )
    email_entry.place(x=260, y=330)


    cursor = conn.execute("SELECT SUBNAME FROM SUBJECTS")
    subcode_li = [row[0] for row in cursor]
    subcode_li.insert(0, 'NULL')

    # Label10
    tk.Label(
        subtk,
        text='Subject 1:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=370)

    # ComboBox1
    combo1 = ttk.Combobox(
        subtk,
        values=subcode_li,
    )
    combo1.place(x=260, y=370)
    combo1.current(0)

    # Label9
    tk.Label(
        subtk,
        text='No of Hours:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=420, y=370)

    # Entry6

    sub1 = tk.Entry(
        subtk,
        font=('comic', 12),
        width=5,
    )
    sub1.place(x=515, y=370)

    # Label11
    tk.Label(
        subtk,
        text='Subject 2:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=410)

    # ComboBox2
    combo2 = ttk.Combobox(
        subtk,
        values=subcode_li,
    )
    combo2.place(x=260, y=410)
    combo2.current(0)


    # Label9
    tk.Label(
        subtk,
        text='No of Hours:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=420, y=410)

    # Entry6
    sub2 = tk.Entry(
        subtk,
        font=('comic', 12),
        width=5,
    )
    sub2.place(x=515, y=410)

    # Label11
    tk.Label(
        subtk,
        text='Subject 3:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=450)

    # ComboBox2
    combo3 = ttk.Combobox(
        subtk,
        values=subcode_li,
    )
    combo3.place(x=260, y=450)
    combo3.current(0)


    # Label9
    tk.Label(
        subtk,
        text='No of Hours:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=420, y=450)

    # Entry6
    sub3 = tk.Entry(
        subtk,
        font=('comic', 12),
        width=5,
    )
    sub3.place(x=515, y=450)


    # Label11
    tk.Label(
        subtk,
        text='Subject 4:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=490)

    # ComboBox2
    combo4 = ttk.Combobox(
        subtk,
        values=subcode_li,
    )
    combo4.place(x=260, y=490)
    combo4.current(0)


    # Label9
    tk.Label(
        subtk,
        text='No of Hours:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=420, y=490)

    # Entry6
    sub4 = tk.Entry(
        subtk,
        font=('comic', 12),
        width=5,
    )
    sub4.place(x=515, y=490)

    # Label4
    tk.Label(
        subtk,
        text='Department:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=535)

    # Entry1
    dep_entry = tk.Entry(
        subtk,
        font=('comic', 12),
        width=20
    )
    dep_entry.place(x=260, y=535)



    # Button1
    B1 = tk.Button(
        subtk,
        text='Add Faculty',
        font=('comic', 12),bg="#cca307",fg="#fff",
        command=parse_data
    )
    B1.place(x=100,y=575)

    # Button2
    B2 = tk.Button(
        subtk,
        text='Update Faculty',
        font=('comic', 12),bg="#cca307",fg="#fff",
        command=update_data
    )
    B2.place(x=220,y=575)

    # Treeview1
    tree = ttk.Treeview(subtk)
    create_treeview()
    update_treeview()

    # Button3
    B3 = tk.Button(
        subtk,
        text='Delete Faculty(s)',
        font=('comic', 12),bg="#cca307",fg="#fff",
        command=remove_data
    )
    B3.place(x=370,y=575)

    tk.Button(
        subtk,
        text='< Back',
        font=('comic', 12), bg="#cca307", fg="#fff", width=5,
        command=subtk.destroy
    ).place(x=0, y=0)

    subtk.mainloop()
    conn.close() # close database after all operations
