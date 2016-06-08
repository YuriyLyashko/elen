from tkinter import *
import pymysql

def close_login_window(value):
    flag = 0
    global flag
    login_window.destroy()

def create_user():
        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='123456',
                               db='elen_db')
        cur = conn.cursor()
        #cur.execute('SELECT ')
        print(cur.description)



flag = 1
while flag:
    login_window = Tk()
    login_window.geometry('500x300')
    login_window.resizable(width=False, height=False)
    login_window['bg'] = 'grey90'
    login_window.title('Аунтефікація користувача')

    login = StringVar()
    password = StringVar()


    canv = Canvas(login_window, width=500, height=300)
    canv['bg'] = 'grey90'


    central_title = Label(login_window,
                          text="{}".format("Розрахунок вартості спожитої електроенергії для однозонного лічильника."),
                          font="Arial 10", bg='grey90')

    lab_login = Label(login_window, text="{}".format("Логін:"), font="Arial 10", bg='grey90')
    lab_password = Label(login_window, text="{}".format("Пароль:"), font="Arial 10", bg='grey90')

    ent_login = Entry(login_window, width=20, bd=3, textvariable=login)
    ent_password = Entry(login_window, width=20, bd=3, textvariable=password)

    but_logged = Button(login_window,
                        text="{}".format("Вхід"), font="Arial 10",
                        width=15, height=1,
                        bg="grey85", fg="black")
    but_logged.bind("<Button-1>", close_login_window)

    but_registrate = Button(login_window,
                            text="{}".format('Зареєструватися'), font="Arial 10",
                            width=15, height=1,
                            bg="grey85", fg="black")
    but_registrate.bind("<Button-1>", create_user())



    central_title.place(x=20, y=10)

    a = 50
    b = 50
    lab_login.place(x=a, y=b)
    ent_login.place(x=a+60, y=b)

    lab_password.place(x=a, y=b+30)
    ent_password.place(x=a+60, y=b+30)

    but_logged.place(x=a + 60, y=b + 60)
    but_registrate.place(x=a + 300, y=b + 12)

    canv.create_line(245,60,350,70,width=2,arrow=LAST)
    canv.create_line(245,90,350,80,width=2,arrow=LAST)
    canv.place(x=0, y=0)

    login_window.mainloop()