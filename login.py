from tkinter import *
import hashlib

import administration_db


class Login:
    flag = 1

    def __init__(self):
        while self.flag:
            self.login_window = Tk()
            self.login_window.geometry('500x300')
            self.login_window.resizable(width=False, height=False)
            self.login_window['bg'] = 'grey90'
            self.login_window.title('Аунтефікація користувача')

            self.login = StringVar()
            self.password = StringVar()

            canv = Canvas(self.login_window, width=500, height=300)
            canv['bg'] = 'grey90'

            central_title = Label(self.login_window,
                                  text="{}"
                                  .format("Розрахунок вартості спожитої електроенергії для однозонного лічильника."),
                                  font="Arial 10", bg='grey90')

            lab_login = Label(self.login_window, text="{}".format("Логін:"), font="Arial 10", bg='grey90')
            lab_password = Label(self.login_window, text="{}".format("Пароль:"), font="Arial 10", bg='grey90')

            ent_login = Entry(self.login_window, width=20, bd=3, textvariable=self.login)
            ent_password = Entry(self.login_window, width=20, bd=3, textvariable=self.password)

            but_logged = Button(self.login_window,
                                text="{}".format("Вхід"), font="Arial 10",
                                width=15, height=1,
                                bg="grey85", fg="black")
            but_logged.bind("<Button-1>", self.close_login_window)

            but_registrate = Button(self.login_window,
                                    text="{}".format('Зареєструватися'), font="Arial 10",
                                    width=15, height=1,
                                    bg="grey85", fg="black")
            but_registrate.bind("<Button-1>", self.create_user)


            central_title.place(x=20, y=10)

            a = 50
            b = 50
            lab_login.place(x=a, y=b)
            ent_login.place(x=a+60, y=b)

            lab_password.place(x=a, y=b+30)
            ent_password.place(x=a+60, y=b+30)

            but_logged.place(x=a+60, y=b+60)
            but_registrate.place(x=a+300, y=b+12)

            canv.create_line(245, 60, 350, 70, width=2, arrow=LAST)
            canv.create_line(245, 90, 350, 80, width=2, arrow=LAST)
            canv.place(x=0, y=0)

            self.login_window.mainloop()


    def close_login_window(self, value):
        self.flag = 0
        self.login_window.destroy()

    def create_user(self, value):
        adm_db = administration_db.AdminDB()
        adm_db.create_user(self.login.get(), self.encrypt(self.password.get()))

    def encrypt(self, string):
        return hashlib.md5('{}'.format(string).encode('cp1251')).hexdigest()

    def show_report(self, message):
        pass
