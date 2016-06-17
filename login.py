from tkinter import *
import hashlib

import administration_db

message_name_is_not_entered = 'Логін не введено.'
message_name_is_to_long = 'Довжена логіну маєбути меншим, ніж 20 символів.'
message_name_is_not_alnum = "Логін повинен складатися тільки з буквенно-цифренних символів."
message_password_is_not_entered = 'Пароль не введено.'
message_password_is_to_long = 'Довжена паролю маєбути меншим, ніж 20 символів.'
message_password_is_not_alnum = 'Пароль повинен складатися тільки з буквенно-цифренних символів.'
message_sing_uo_to_enter = 'Необхідно зареєструватися, щоб увійти.'
message_name_alredy_exists = 'Користувач із вказаним логіном вже існує.'
message_registration_successful = 'Реєстрація успішна!'

report_title = 'report_title'


class Login:
    flag = 1
    def __init__(self):
        self.login_window = Tk()
        self.login_window.geometry('500x300')
        self.login_window.resizable(width=False, height=False)
        self.login_window['bg'] = 'grey90'
        self.login_window.title('Аунтефікація користувача')

        self.login = StringVar()
        self.password = StringVar()
        self.report_message = StringVar()

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
        but_logged.bind("<Button-1>", self.sing_in)

        but_registrate = Button(self.login_window,
                                    text="{}".format('Зареєструватися'), font="Arial 10",
                                    width=15, height=1,
                                    bg="grey85", fg="black")
        but_registrate.bind("<Button-1>", self.create_user)

        lab_report = Label(self.login_window, font="Arial 10", bg='grey90', textvariable=self.report_message)


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

        lab_report.place(relx=0.5, rely=0.7, anchor="center")

        self.login_window.mainloop()


    def close_login_window(self):
        print('close_login_window')
        self.flag = 0
        self.login_window.destroy()

    def create_user(self, value):
        print('create_user')
        if self.check_entered_name(self.login.get()) and self.check_entered_password(self.password.get()):
            adm_db = administration_db.AdminDB()
            if not adm_db.check_user(self.login.get()):
                adm_db.create_user(self.login.get(), self.encrypt(self.password.get()))
                adm_db.create_table('history_{}'.format(self.login.get()))
                adm_db.create_table('log_{}'.format(self.login.get()))
                adm_db.close_connection()
                self.show_report('{}, {}'.format(self.login.get(), message_registration_successful))
                return True
            self.show_report(message_name_alredy_exists)

    def encrypt(self, string):
        return hashlib.md5('{}'.format(string).encode('cp1251')).hexdigest()

    def sing_in(self, value):
        print('sing_in')
        if self.check_entered_name(self.login.get()) and self.check_entered_password(self.password.get()):
            adm_db = administration_db.AdminDB()
            if adm_db.check_user(self.login.get()) and adm_db.check_password(self.login.get(), self.encrypt(self.password.get())):
                self.close_login_window()
                return True
            self.show_report(message_sing_uo_to_enter)

    def check_entered_name(self, entered_name):
        print('check_entered_name')
        if len(entered_name) < 1:
            self.show_report('{}'.format(message_name_is_not_entered))
            return False
        elif len(entered_name) > 20:
            self.show_report('{}'.format(message_name_is_to_long))
            return False
        elif not entered_name.isalnum():
            self.show_report('{}'.format(message_name_is_not_alnum))
            return False
        else:
            return True

    def check_entered_password(self, entered_password):
        print('check_entered_password')
        if len(entered_password) < 1:
            self.show_report('{}'.format(message_password_is_not_entered))
            return False
        elif len(entered_password) > 20:
            self.show_report('{}'.format(message_password_is_to_long))
            return False
        elif not entered_password.isalnum():
            self.show_report('{}'.format(message_password_is_not_alnum))
            return False
        else:
            return True

    def show_report(self, message):
        print('show_report', message)
        self.report_message.set(message)
