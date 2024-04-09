import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys


subcode = subname = subtype = clas = None



def create_treeview():
    tree['columns'] = ('one', 'two', 'three', 'four','five')
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("one", width=70, stretch=tk.NO)
    tree.column("two", width=100, stretch=tk.NO)
    tree.column("three", width=60, stretch=tk.NO)

    tree.column("four", width=230, stretch=tk.NO)

    tree.column("five", width=70, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('one', text="Code")
    tree.heading('two', text="Name")
    tree.heading('three', text="Type")

    tree.heading('four', text="Full Name")


    tree.heading('five', text="Class")
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT * FROM SUBJECTS")
    for row in cursor:
        # print(row[0], row[1], row[2])
        if row[2] == 'T':
            t = 'Theory'
        elif row[2] == 'P':
            t = 'Practical'
        tree.insert(
            "",
            0,
            values=(row[0],row[1],t,row[3],row[4])
        )
    tree.place(x=550, y=100)



def parse_data():
    subcode = str(subcode_entry.get())
    subname = str(subname_entry.get("1.0", tk.END)).upper().rstrip()
    subtype = str(radio_var.get()).upper()

    clas = str(clas_entry.get()).upper()
    subnamefull = str(subnamefull_entry.get("1.0", tk.END)).upper().rstrip()
    if subcode=="":
        subcode = None
    if subname=="":
        subname = None
    if subnamefull=="":
        subnamefull = None
    if clas=="":
        clas = None
    if subcode is None or subname is None or subnamefull is None or clas is None:
        messagebox.showerror("Bad Input", "Please fill up Subject Code and/or Subject Name!")
        subcode_entry.delete(0, tk.END)
        subname_entry.delete("1.0", tk.END)

        subnamefull_entry.delete("1.0", tk.END)

        clas_entry.delete("1.0", tk.END)
        return

    conn.execute(f"REPLACE INTO SUBJECTS (SUBCODE, SUBNAME, SUBTYPE, SUBNAMEFULL, CLAS)\
        VALUES ('{subcode}','{subname}','{subtype}','{subnamefull}','{clas}')")
    conn.commit()
    update_treeview()
    
    subcode_entry.delete(0, tk.END)
    subname_entry.delete("1.0", tk.END)

    subnamefull_entry.delete("1.0", tk.END)

    clas_entry.delete(0, tk.END)

def update_data():
    subcode_entry.delete(0, tk.END)
    subname_entry.delete("1.0", tk.END)

    subnamefull_entry.delete("1.0", tk.END)

    clas_entry.delete(0, tk.END)
    try:
        # print(tree.selection())
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one subject at a time to update!")
            return

        row = tree.item(tree.selection()[0])['values']
        subcode_entry.insert(0, row[0])
        subname_entry.insert("1.0", row[1])

        if row[2][0] == "T":
            R1.select()
        elif row[2][0] == "P":
            R2.select()

        subnamefull_entry.insert("1.0", row[3])

        clas_entry.insert("0", row[4])
        conn.execute(f"DELETE FROM SUBJECTS WHERE SUBCODE = '{row[0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a subject from the list first!")
        return


def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a subject from the list first!")
        return
    for i in tree.selection():
        # print(tree.item(i)['values'][0])
        conn.execute(f"DELETE FROM SUBJECTS WHERE SUBCODE = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()



# main
if __name__ == "__main__":  


    conn = sqlite3.connect(r'db/data.db')


    conn.execute('CREATE TABLE IF NOT EXISTS SUBJECTS\
    (SUBCODE CHAR(10) NOT NULL PRIMARY KEY,\
    SUBNAME CHAR(50) NOT NULL,\
    SUBTYPE CHAR(1) NOT NULL,\
    SUBNAMEFULL CHAR(50) NOT NULL)')



    subtk = tk.Tk()
    subtk.geometry('1100x470')

    subtk.config(bg="#092138")
    subtk.title('Add/Update Subjects')

    # Label1
    tk.Label(
        subtk,
        text='List of Subjects',bg="#092138",fg="#fff",
        font=('comic', 20, 'bold')
    ).place(x=550, y=50)

    # Label2
    tk.Label(
        subtk,
        text='Add/Update Subjects',
        font=('comic', 20, 'bold'),bg="#092138",fg="#fff",
    ).place(x=100, y=50)

    # Label4
    tk.Label(
        subtk,
        text='Subject code:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=150)

    # Entry1
    subcode_entry = tk.Entry(
        subtk,
        font=('comic', 12),
        width=20
    )
    subcode_entry.place(x=300, y=150)
    
    # Label5
    tk.Label(
        subtk,
        text='Subject Short Name:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=200)

    # Text
    subname_entry = tk.Text(
        subtk,
        font=('comic', 12),
        width=20,
        height=1,
        wrap=tk.WORD
    )
    subname_entry.place(x=300, y=200)

    # Label5
    tk.Label(
        subtk,
        text='Subject Name Full:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=250)

    # Text
    subnamefull_entry = tk.Text(
        subtk,
        font=('comic', 12),
        width=20,
        height=1,
        wrap=tk.WORD
    )
    subnamefull_entry.place(x=300, y=250)


    # Label6
    tk.Label(
        subtk,
        text='Subject Type:',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=100, y=300)


    radio_var = tk.StringVar()

    # RadioButton1
    R1 = tk.Radiobutton(
        subtk,
        font=('comic', 12),bg="#092138",fg="#092138",
        variable=radio_var,
        value="T"
    )
    R1.place(x=290, y=300)
    R1.select()

    # RadioButton2
    R2 = tk.Radiobutton(
        subtk,
        font=('comic', 12),bg="#092138",fg="#092138",
        variable=radio_var,
        value="P"
    )
    R2.place(x=390, y=300)
    R2.select()
    # Label6
    tk.Label(
        subtk,
        text='Theory',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=310, y=300)

    # Label6
    tk.Label(
        subtk,
        text='Practical',
        font=('comic', 12),bg="#092138",fg="#fff",
    ).place(x=410, y=300)

    # Label4
    tk.Label(
        subtk,
        text='Class:',
        font=('comic', 12), bg="#092138", fg="#fff",
    ).place(x=100, y=350)

    # Entry1
    clas_entry = tk.Entry(
        subtk,
        font=('comic', 12),
        width=20
    )
    clas_entry.place(x=300, y=350)
    # Button1
    B1 = tk.Button(
        subtk,
        text='Add Subject',
        font=('comic', 12),bg="#cca307",fg="#fff",
        command=parse_data
    )
    B1.place(x=100,y=400)

    # Button2
    B2 = tk.Button(
        subtk,
        text='Update Subject',
        font=('comic', 12),bg="#cca307",fg="#fff",
        command=update_data
    )
    B2.place(x=210,y=400)

    # Treeview1
    tree = ttk.Treeview(subtk)
    create_treeview()
    update_treeview()

    # Button3
    B3 = tk.Button(
        subtk,
        text='Delete Subject(s)',
        font=('comic', 12),bg="#cca307",fg="#fff",
        command=remove_data
    )
    B3.place(x=350,y=400)

    tk.Button(
        subtk,
        text='< Back',
        font=('comic', 12), bg="#cca307", fg="#fff", width=5,
        command=subtk.destroy
    ).place(x=0, y=0)

    subtk.mainloop()
    conn.close() # close database ad=fter all operations