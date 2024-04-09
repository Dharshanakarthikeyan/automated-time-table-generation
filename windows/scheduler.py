import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

days = 6
periods = 5
recess_break_aft = 3  # recess after 3rd Hour
section = None
butt_grid = []

period_names = list(map(lambda x: 'Hour ' + str(x), range(1, 5 + 1)))
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday', 'Saturday']


def update_p(d, p, tree, parent):
    # print(section, d, p, str(sub.get()))
    print("update sub")
    print("---------------------")

    print(d)
    print(p)
    print(tree)
    print(parent)
    print("---------------------")
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one subject at a time!")
            parent.destroy()
            return
        row = tree.item(tree.selection()[0])['values']
        if row[0] == 'NULL' and row[1] == 'NULL':
            conn.execute(f"DELETE FROM SCHEDULE WHERE ID='{section + str((d * periods) + p)}'")
            conn.commit()
            update_table()
            parent.destroy()
            return

        conn.commit()
        print(row)
        conn.execute(f"REPLACE INTO SCHEDULE (ID, DAYID, PERIODID, SUBCODE, SECTION, FINI)\
            VALUES ('{section + str((d * periods) + p)}', {d}, {p}, '{row[1]}', '{section}', '{row[0]}')")
        conn.commit()
        update_table()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a subject from the list!")
        parent.destroy()
        return

    parent.destroy()


def process_button(d, p):
    print(d, p)
    add_p = tk.Tk()



    cursor = conn.execute("SELECT SUBCODE FROM SUBJECTS")
    subcode_li = [row[0] for row in cursor]
    subcode_li.insert(0, 'NULL')

    # Label10
    tk.Label(
        add_p,
        text='Check  for Substitution',
        font=('comic', 12, 'bold')
    ).pack()

    tk.Label(
        add_p,
        text=f'Day: {day_names[d]}',
        font=('comic', 12)
    ).pack()

    tk.Label(
        add_p,
        text=f'Hour: {p+1}',
        font=('comic', 12)
    ).pack()

    tree = ttk.Treeview(add_p)
    tree['columns'] = ('one', 'two')
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("one", width=70, stretch=tk.NO)
    tree.column("two", width=80, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('one', text="Faculty")
    tree.heading('two', text="Subject Code")

    cursor = conn.execute("SELECT DISTINCT FACULTY.INI, FACULTY.SUBCODE1, FACULTY.SUBCODE2, FACULTY.SUBCODE3, FACULTY.SUBCODE4, FACULTY.DEP, SUBJECTS.SUBNAME\
    FROM FACULTY, SUBJECTS\
    WHERE FACULTY.DEP='CS' AND FACULTY.SUBCODE1=SUBJECTS.SUBNAME OR FACULTY.SUBCODE2=SUBJECTS.SUBNAME OR FACULTY.SUBCODE3=SUBJECTS.SUBNAME OR FACULTY.SUBCODE4=SUBJECTS.SUBNAME ")
    for row in cursor:
        print(row)
        tree.insert(
            "",
            0,
            values=(row[0], row[-1])
        )
    tree.insert("", 0, value=('NULL', 'NULL'))
    tree.pack(pady=10, padx=30)

    tk.Button(
        add_p,
        text="OK",
        padx=15,
        command=lambda x=d, y=p, z=tree, d=add_p: update_p(x, y, z, d)
    ).pack(pady=20)

    add_p.mainloop()


def select_sec():
    global section
    section = str(combo1.get())
    print(section)
    update_table()


def update_table():
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute(f"SELECT SUBCODE, FINI FROM SCHEDULE\
                WHERE DAYID={i} AND PERIODID={j} AND SECTION='{section}'")
            cursor = list(cursor)
            print(cursor)
            if len(cursor) != 0:
                butt_grid[i][j]['text'] = str(cursor[0][0]) + '\n' + str(cursor[0][1])
                butt_grid[i][j].update()
                print(i, j, cursor[0][0])
            else:
                butt_grid[i][j]['text'] = "No Class"
                butt_grid[i][j].update()


def load(d, p, tree, parent):
    cursor = conn.execute("SELECT SUBCODE FROM SUBJECTS")
    subcode_li = [row[0] for row in cursor]
    iii = subcode_li.find("CS6")
    ii = subcode_li.find("CS4, LT4, LE4")
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one subject at a time!")
            parent.destroy()
            return
        row = tree.item(tree.selection()[0])['values']
        if row[0] == 'III-CSC':

            section = ["III-CSC-A", "III-CSC-B", "III-CSC-C"]
            a = section + str((d * periods) + p)
            print(a)
            SUBNAME = subcode_li.find("CS6")
            cursor = conn.execute("SELECT FACULTY.INI, FACULTY.SUBCODE1, FACULTY.SUBCODE2, SUBJECTS.SUBNAME\
                FROM FACULTY, SUBJECTS\
                WHERE FACULTY.SUBCODE1=SUBJECTS.SUBNAME OR FACULTY.SUBCODE2=SUBJECTS.SUBNAME")
            for row in cursor:
                row[0] = cursor.sample()
            a = section + str((d * periods) + p)
            print(a)
            conn.execute(f"INSERT INTO SCHEDULE (ID, DAYID, PERIODID, SUBCODE, SECTION, FINI)\
                        VALUES ('{a}', {d}, {p}, '{row[1]}', '{section}', '{row[0]}')")
            conn.commit()
            update_table()
        if row[0] == 'COG':

            section = ["II-COG"]
            a = section + str((d * periods) + p)
            print(a)
            SUBNAME = subcode_li.find("CS4, UE4, LT4, CG4, MA4, CC")
            cursor = conn.execute("SELECT FACULTY.INI, FACULTY.SUBCODE1, FACULTY.SUBCODE2, SUBJECTS.SUBNAME\
                FROM FACULTY, SUBJECTS\
                WHERE FACULTY.SUBCODE1=SUBJECTS.SUBNAME OR FACULTY.SUBCODE2=SUBJECTS.SUBNAME")
            for row in cursor:
                row[0] = cursor.sample()
            a = section + str((d * periods) + p)
            print(a)
            conn.execute(f"INSERT INTO SCHEDULE (ID, DAYID, PERIODID, SUBCODE, SECTION, FINI)\
                        VALUES ('{a}', {d}, {p}, '{row[1]}', '{section}', '{row[0]}')")
            conn.commit()
            update_table()
        if row[0] == 'MSC':

            section = ["II-MSC-CSC"]
            a = section + str((d * periods) + p)
            print(a)
            SUBNAME = subcode_li.find("PCS4")
            cursor = conn.execute("SELECT FACULTY.INI, FACULTY.SUBCODE1, FACULTY.SUBCODE2, SUBJECTS.SUBNAME\
                FROM FACULTY, SUBJECTS\
                WHERE FACULTY.SUBCODE1=SUBJECTS.SUBNAME OR FACULTY.SUBCODE2=SUBJECTS.SUBNAME")
            for row in cursor:
                row[0] = cursor.sample()
            a = section + str((d * periods) + p)
            print(a)
            conn.execute(f"INSERT INTO SCHEDULE (ID, DAYID, PERIODID, SUBCODE, SECTION, FINI)\
                        VALUES ('{a}', {d}, {p}, '{row[1]}', '{section}', '{row[0]}')")
            conn.commit()
            update_table()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a subject from the list!")
        parent.destroy()
        return

    parent.destroy()


conn = sqlite3.connect(r'db/data.db', timeout=1)

conn.execute('CREATE TABLE IF NOT EXISTS SCHEDULE\
(ID CHAR(10) NOT NULL PRIMARY KEY,\
DAYID INT NOT NULL,\
PERIODID INT NOT NULL,\
SUBCODE CHAR(10) NOT NULL,\
SECTION CHAR(5) NOT NULL,\
FINI CHAR(10) NOT NULL)')

tt = tk.Tk()

tt.title('Scheduler')

title_lab = tk.Label(
    tt,
    text='TIME TABLE',
    font=('comic', 20, 'bold'),
    pady=5
)
title_lab.pack()

tk.Button(
    tt,
    text='< Back',
    font=('comic', 12, 'bold'), bg="#cca307", fg="#fff", width=5,
    command=tt.destroy
).place(x=0, y=0)

table = tk.Frame(tt)
table.pack()

first_half = tk.Frame(table)
first_half.pack(side='left')

recess_frame = tk.Frame(table)
recess_frame.pack(side='left')

second_half = tk.Frame(table)
second_half.pack(side='left')

recess = tk.Label(
    recess_frame,

    text='B\n\nR\n\nE\n\nA\n\nK',
    font=('comic', 18, 'italic'),
    width=3,
    relief='sunken'
)
recess.pack()

for i in range(days):
    b = tk.Label(
        first_half,
        text=day_names[i],
        font=('comic', 12, 'bold'),
        width=9,
        height=2,
        bd=5,
        relief='raised'
    )
    b.grid(row=i + 1, column=0)

for i in range(periods):
    if i < recess_break_aft:
        b = tk.Label(first_half)
        b.grid(row=0, column=i + 1)
    else:
        b = tk.Label(second_half)
        b.grid(row=0, column=i)

    b.config(
        text=period_names[i],
        font=('comic', 12, 'bold'),
        width=9,
        height=1,
        bd=5,
        relief='raised'
    )

for i in range(days):
    b = []
    for j in range(periods):
        if j < recess_break_aft:
            bb = tk.Button(first_half)
            bb.grid(row=i + 1, column=j + 1)
        else:
            bb = tk.Button(second_half)
            bb.grid(row=i + 1, column=j)

        bb.config(
            text='Hello World!',
            font=('comic', 10),
            width=13,
            height=3,
            bd=5,
            relief='raised',
            wraplength=80,
            justify='center',
            command=lambda x=i, y=j: process_button(x, y)
        )
        b.append(bb)

    butt_grid.append(b)
    # print(b)
    b = []
sec_select_f = tk.Frame(tt, pady=25)
sec_select_f.pack()

tk.Label(
    sec_select_f,
    text='Select Class:',
    font=('comic', 11, 'bold')
).pack(side=tk.LEFT)

cursor = conn.execute("SELECT DISTINCT SECTION FROM STUDENT")
sec_li = [row[0] for row in cursor]
# sec_li.insert(0, 'NULL')
print(sec_li)
combo1 = ttk.Combobox(
    sec_select_f,
    values=sec_li, width=10,
)
combo1.pack(side=tk.LEFT)
combo1.current(0)

b = tk.Button(
    sec_select_f,
    text="OK",
    font=('comic', 9, 'bold'), width=1,
    padx=10,
    command=select_sec
)
b.pack(side=tk.LEFT, padx=8)
b.invoke()

print(butt_grid[0][1], butt_grid[1][1])
update_table()

tt.mainloop()