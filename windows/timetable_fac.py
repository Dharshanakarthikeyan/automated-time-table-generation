import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

days = 6
periods = 5
recess_break_aft = 3 # recess after 3rd Hour
fini = None
butt_grid = []


period_names = list(map(lambda x: 'Hour ' + str(x), range(1, 5+1)))
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday', 'Saturday']



def select_fac():
    global fini
    fini = str(combo1.get())
    print(fini)
    update_table(fini)



def update_table(fini):
    for i in range(days):
        for j in range(periods):

            conn = sqlite3.connect(r'db/data.db')

            cursor = conn.execute(f"SELECT SECTION, SUBCODE, SUBTYPE FROM SCHEDULE\
                            WHERE DAYID={i} AND PERIODID={j} AND FINI='{fini}'")

            cursor = list(cursor)
            print(cursor)

            butt_grid[i][j]['bg'] = 'white'
            if len(cursor) != 0:
                subtype = cursor[0][2]
                print(subtype)
                butt_grid[i][j]['fg'] = 'white'
                if subtype == 'T':
                    butt_grid[i][j]['bg'] = 'green'
                elif subtype == 'P':
                    butt_grid[i][j]['bg'] = '#ac9200'

                sec_li = [x[0] for x in cursor]
                t = ', '.join(sec_li)
                butt_grid[i][j]['text'] = "Sections: " + t
                print(i, j, cursor[0][0])
            else:
                butt_grid[i][j]['fg'] = 'black'
                butt_grid[i][j]['text'] = "No Class"
                butt_grid[i][j].update()



def process_button(d, p):
    print(d, p, fini)
    details = tk.Tk()
    cursor = conn.execute(f"SELECT SECTION, SUBCODE, SUBTYPE FROM SCHEDULE\
                WHERE DAYID={d} AND PERIODID={p} AND FINI='{fini}'")
    cursor = list(cursor)
    print("section", cursor)
    if len(cursor) != 0:
        sec_li = [x[0] for x in cursor]
        t = ', '.join(sec_li)
        subcode = cursor[0][1]

        subtype = cursor[0][2]
        cur1 = conn.execute(f"SELECT SUBNAME FROM SUBJECTS\
            WHERE SUBNAME='{subcode}'")
        cur1 = list(cur1)
        subname = str(cur1[0][0])

        if subtype == 'T':
            subtype = 'Theory'
        elif subtype == 'P':
            subtype = 'Practical'

    #     print(subcode, fini, subname, subtype, fname, femail)
    else:
        sec_li = subcode = subname = subtype = t = 'None'

    tk.Label(details, text='Class Details', font=('comic', 15, 'bold')).pack(pady=15)
    tk.Label(details, text='Day: '+day_names[d], font=('comic'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Hour: '+str(p+1), font=('comic'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Code: '+subcode, font=('comic'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subect Name: '+subname, font=('comic'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Type: '+subtype, font=('comic'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Faculty Initials: '+fini, font=('comic'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Sections: '+t, font=('comic'), anchor="w").pack(expand=1, fill=tk.X, padx=20)

    tk.Button(
        details,
        text="OK",
        font=('comic'),
        width=10,
        command=details.destroy
    ).pack(pady=10)

    details.mainloop()



def fac_tt_frame(tt, f):
    title_lab = tk.Label(
        tt,
        text='TIME TABLE',
        font=('comic', 20, 'bold'),
        pady=5
    )
    title_lab.pack()

    legend_f = tk.Frame(tt)
    legend_f.pack(pady=15)
    tk.Label(
        legend_f,
        text='Class Type: ',
        font=('comic', 10, 'italic')
    ).pack(side=tk.LEFT)

    tk.Label(
        legend_f,
        text='Theory Classes',
        bg='green',
        fg='white',
        relief='raised',
        font=('comic', 10, 'italic'),
        height=2
    ).pack(side=tk.LEFT, padx=10)

    tk.Label(
        legend_f,
        text='Practical Classes',
        bg='#ac9200',
        fg='white',
        relief='raised',
        font=('comic', 10, 'italic'),
        height=2
    ).pack(side=tk.LEFT, padx=10)

    global butt_grid
    global fini
    fini = f

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
        b.grid(row=i+1, column=0)

    for i in range(periods):
        if i < recess_break_aft:
            b = tk.Label(first_half)
            b.grid(row=0, column=i+1)
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
                bb.grid(row=i+1, column=j+1)
            else:
                bb = tk.Button(second_half)
                bb.grid(row=i+1, column=j)

            bb.config(
                text='No Class!',
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

    print(butt_grid[0][1], butt_grid[1][1])
    update_table(fini)



conn = sqlite3.connect(r'db/data.db')
if __name__ == "__main__":
    
    # connecting database

    tt = tk.Tk()
    tt.title('Faculty Timetable')

    fac_tt_frame(tt, fini)

    fac_select_f = tk.Frame(tt, pady=15)
    fac_select_f.pack()
    tk.Button(
        tt,
        text='< Back',
        font=('comic', 12, 'bold'), bg="#cca307", fg="#fff", width=5,
        command=tt.destroy
    ).place(x=0, y=0)

    tk.Label(
        fac_select_f,
        text='Select Faculty:  ',
        font=('comic', 12, 'bold')
    ).pack(side=tk.LEFT)

    conn = sqlite3.connect(r'db/data.db')
    cursor = conn.execute("SELECT DISTINCT INI FROM FACULTY")
    fac_li = [row[0] for row in cursor]
    print(fac_li)
    combo1 = ttk.Combobox(
        fac_select_f,
        values=fac_li,
    )
    combo1.pack(side=tk.LEFT)
    combo1.current(0)

    b = tk.Button(
        fac_select_f,
        text="OK",
        font=('comic', 12, 'bold'),
        padx=10,
        command=select_fac
    )
    b.pack(side=tk.LEFT, padx=10)
    b.invoke()


    tt.mainloop()