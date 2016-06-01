import tkinter
from datetime import * #tzinfo, date, timedelta
import pickle
import urllib.request
import re
import csv
#import threading #для багатопоточності
#def start():
#    t = threading.Thread(target=thred_func)

root = tkinter.Tk()
root.geometry('1000x550')
root.resizable(width=False, height=False)
root['bg'] = 'grey90'

#root.state("zoomed") #запускаэться у розгорнутому вікні

date_now = datetime.strftime(datetime.now(), "%d.%m.%Y") #%H:%M:%S

calc_end = []


print('tarifi_local')

limit_tariff_1 = tkinter.DoubleVar()
limit_tariff_2 = tkinter.DoubleVar()
tariff_1 = tkinter.DoubleVar()
tariff_2 = tkinter.DoubleVar()
tariff_3 = tkinter.DoubleVar()
date_fares = tkinter.StringVar()

previous_shows = tkinter.IntVar()
current_shows = tkinter.IntVar()
amount_of_electricity = tkinter.IntVar()

amount_of_electricity_in_tariff_1 = tkinter.IntVar()
amount_of_electricity_in_tariff_2 = tkinter.IntVar()
amount_of_electricity_in_tariff_3 = tkinter.IntVar()
amount_of_money_in_tariff_1 = tkinter.DoubleVar()
amount_of_money_in_tariff_2 = tkinter.DoubleVar()
amount_of_money_in_tariff_3 = tkinter.DoubleVar()

total_amount_of_money = tkinter.DoubleVar()

date_introduction_fares = tkinter.StringVar()
date_introduction_fares.set(date_now)

names_fares = limit_tariff_1, limit_tariff_2, tariff_1, tariff_2, tariff_3, date_fares

for name_tariff, value in zip(names_fares, pickle.load(open('fares_start', 'rb'))):
    name_tariff.set(value)


def save_fares(event):
    fares = read_fares()
    print('save_fares')
    pickle.dump(fares, open('fares_start', 'wb'))


def fares_inet(event):
    print('fares_inet')
    try:
        u_o = urllib.request.urlopen('http://kyivenergo.ua/odnozonni_lichilniki/')
        u_o = u_o.read().decode(encoding="utf-8", errors="ignore")
#        print(u_o)
        tarifi_all = [tar.replace(',', '.') for tar in re.findall
                   (r'<td>(\w+.\w+)\W+\w+\W+</tr>', u_o)]
#        print(tarifi_all)
        limit_tariff_1.set(re.findall(r'спожитий до (\w+)', u_o)[0])
        limit_tariff_2.set(re.findall(r'спожитий понад (\w+)', u_o)[1])
        tariff_1.set(float(tarifi_all[0])/100)# тариф 1
        tariff_2.set(float(tarifi_all[1])/100)# тариф 2
        tariff_3.set(float(tarifi_all[2])/100)# тариф 3

    except urllib.error.URLError:
        print('URLError')
        exec(open('error.py').read())
    except ValueError:
        print('ValueError')
        exec(open('error.py').read())

def calc(amount_of_electricity_in_tariff_1, amount_of_electricity_in_tariff_2, amount_of_electricity_in_tariff_3,
             amount_of_money_in_tariff_1, amount_of_money_in_tariff_2, amount_of_money_in_tariff_3,
             total_amount_of_money):
    print('calc')
    #Якщо кількість спожитої електроенергії входить в межі першого тарифу
    if 0 <= amount_of_electricity.get() <= limit_tariff_1.get():
        amount_of_electricity_in_tariff_1.set(amount_of_electricity.get())
        amount_of_electricity_in_tariff_2.set(0)
        amount_of_electricity_in_tariff_3.set(0)
        amount_of_money_in_tariff_1.set(tariff_1.get() * amount_of_electricity.get())
        amount_of_money_in_tariff_2.set(0)
        amount_of_money_in_tariff_3.set(0)
        total_amount_of_money.set(amount_of_money_in_tariff_1.get() + amount_of_money_in_tariff_2.get() +
                                  amount_of_money_in_tariff_3.get())

    #Якщо кількість спожитої електроенергії входить в межі другого тарифу
    elif limit_tariff_1.get() < amount_of_electricity.get() <= limit_tariff_2.get():
        amount_of_electricity_in_tariff_1.set(limit_tariff_1.get())
        amount_of_electricity_in_tariff_2.set(amount_of_electricity.get() - limit_tariff_1.get())
        amount_of_electricity_in_tariff_3.set(0)
        amount_of_money_in_tariff_1.set(tariff_1.get() * limit_tariff_1.get())
        amount_of_money_in_tariff_2.set((amount_of_electricity.get() - limit_tariff_1.get()) * tariff_2.get())
        amount_of_money_in_tariff_3.set(0)
        total_amount_of_money.set(amount_of_money_in_tariff_1.get() + amount_of_money_in_tariff_2.get() +
                                  amount_of_money_in_tariff_3.get())

    #Якщо кількість спожитої електроенергії входить в межі третього тарифу
    elif limit_tariff_2.get() < amount_of_electricity.get():
        amount_of_electricity_in_tariff_1.set(limit_tariff_1.get())
        amount_of_electricity_in_tariff_2.set(limit_tariff_2.get() - limit_tariff_1.get())
        amount_of_electricity_in_tariff_3.set(amount_of_electricity.get() - limit_tariff_2.get())
        amount_of_money_in_tariff_1.set(tariff_1.get() * limit_tariff_1.get())
        amount_of_money_in_tariff_2.set((limit_tariff_2.get() - limit_tariff_1.get()) * tariff_2.get())
        amount_of_money_in_tariff_3.set((amount_of_electricity.get() - limit_tariff_2.get()) * tariff_3.get())
        total_amount_of_money.set(amount_of_money_in_tariff_1.get() + amount_of_money_in_tariff_2.get() +
                                  amount_of_money_in_tariff_3.get())
        
    else:
        exec(open('error.py').read())

    get_history(limit_tariff_1.get(), limit_tariff_2.get(),
                tariff_1.get(), tariff_2.get(), tariff_3.get(),
                previous_shows.get(), current_shows.get(), amount_of_electricity.get(),
                amount_of_money_in_tariff_1.get(), amount_of_money_in_tariff_2.get(), amount_of_money_in_tariff_3.get(),
                total_amount_of_money.get()
                )


#Функція, що викликається кнопкою "Розрахувати"
def launch_calc(event):
    print('launch_calc')
    if previous_shows.get() < 0 or current_shows.get() < 0 or limit_tariff_1.get() > limit_tariff_2.get():
        exec(open('error.py').read())
    #Якщо показники лічильника не введені, то використовуємо введену кількість спожитої електроенергії
    elif previous_shows.get() == 0 and current_shows.get() == 0:
        calc(amount_of_electricity_in_tariff_1, amount_of_electricity_in_tariff_2, amount_of_electricity_in_tariff_3,
             amount_of_money_in_tariff_1, amount_of_money_in_tariff_2, amount_of_money_in_tariff_3,
             total_amount_of_money)
    else:
        amount_of_electricity.set(current_shows.get() - previous_shows.get())
        print(amount_of_electricity.get())
        calc(amount_of_electricity_in_tariff_1, amount_of_electricity_in_tariff_2, amount_of_electricity_in_tariff_3,
             amount_of_money_in_tariff_1, amount_of_money_in_tariff_2, amount_of_money_in_tariff_3,
             total_amount_of_money)


def get_history(limit_tariff_1, limit_tariff_2, tariff_1, tariff_2, tariff_3,
                previous_shows, current_shows, amount_of_electricity,
                amount_of_money_in_tariff_1, amount_of_money_in_tariff_2, amount_of_money_in_tariff_3,
                total_amount_of_money):
    print('get_history')
    calc_end =[date_introduction_fares.get(), date_now,
               '%.0f' % (limit_tariff_1), '%.0f' % (limit_tariff_2),
               '%.3f' % (tariff_1), '%.3f' % (tariff_2), '%.3f' % (tariff_3),
               '%.0f' % (previous_shows), '%.0f' % (current_shows), '%.0f' % (amount_of_electricity),
               '%.2f' % (amount_of_money_in_tariff_1), '%.2f' % (amount_of_money_in_tariff_2), '%.2f' % (amount_of_money_in_tariff_3), '%.2f' % (total_amount_of_money)
               ]
    h = open('history.txt', 'a')
    h.write(str(calc_end)+"r \n")
    h.close()
    global calc_end

#Функція, що викликається кнопкою "Зберегти в файл"
def sortByAlphabet_Day(inputStr):
#    print(inputStr[2:4])
    return inputStr[2:4]
def sortByAlphabet_Month(inputStr):
#    print(inputStr[5:7])
    return inputStr[5:7]
def sortByAlphabet_Year(inputStr):
#    print(inputStr[8:12])
    return inputStr[8:12]

def saves(event):
    print('saves')
    if len(calc_end) < 2:
        exec(open('error.py').read())
    else:
        h = open('history.txt', 'a')
        h.write(str(calc_end)+"s \n")
        h.close()
        s = open('saves.txt', 'a')
        #a - дозапис, 'w' - запис, 'r' - читання
        s.write(str(calc_end)+"\n")
        s.close()
        s = open('saves.txt', 'r')
        all_lines = s.readlines()
        all_lines.sort(key = sortByAlphabet_Day)
        all_lines.sort(key = sortByAlphabet_Month)
        all_lines.sort(key = sortByAlphabet_Year)
        n = 0
        while n < len(all_lines)-1:
            if all_lines[n][2:12] == all_lines[n+1][2:12]:
                all_lines.pop(n)
                n = n
            else:
                n += 1
        s = open('saves.txt', 'w')
        s.writelines(all_lines)
        s.close()


root.title("Розрахунок вартості спожитої електроенергії")

Central_title = tkinter.Label(root, text="Розрахунок вартості спожитої електроенергії для однозонного лічильника.",
                              font="Arial 16", bg='grey90')

#Опис блоку "Спожита електроенергія."
header_of_block_consumption = tkinter.Label(root, text="Спожита електроенергія.",
                                            font="Arial 14", bg='grey90')
lab_previous_shows = tkinter.Label(root, text="Введіть попередні значення лічильника електроенергії:",
                                   font="Arial 12", bg='grey90')
lab_current_shows = tkinter.Label(root, text="Введіть поточні значення лічильника електроенергії:",
                                  font="Arial 12", bg='grey90')
lab_or = tkinter.Label(root, text="АБО",
                       font="Arial 12", bg='grey90')
lab_amount_of_electricity = tkinter.Label(root, text="Введіть кількість спожитої електроенергії, кВт∙год:",
                                          font="Arial 12", bg='grey90')

ent_previous_shows = tkinter.Entry(root, width=20, bd=3, textvariable=previous_shows)
ent_current_shows = tkinter.Entry(root, width=20, bd=3, textvariable=current_shows)
ent_amount_of_electricity = tkinter.Entry(root, width=20, bd=3, textvariable=amount_of_electricity)


#Опис блоку "Діючі тарифи на електроенергію, грн. за 1 кВтгод."
header_of_block_fares = tkinter.Label(root, text="Діючі тарифи на електроенергію, грн. за 1 кВт∙год.",
                                      font="Arial 14", bg='grey90')
lab_pointer_date_saving_fares = tkinter.Label(root, text="Дата збереження тарифів:",
                                              font="Arial 10", bg='grey90')
lab_date_saving_fares = tkinter.Label(root, font="Arial 10", bg='grey90', textvariable=date_fares)
lab_pointer_tariff_1_in = tkinter.Label(root, text="за обсяг, спожитий до               кВт∙год "\
                                                   "електроенергії на місяць (включно):",
                                        font="Arial 12", bg='grey90')
lab_pointer_tariff_2_in = tkinter.Label(root, text="за обсяг, спожитий понад               кВт∙год "\
                                                   "до               кВт∙год електроенергії на місяць (включно):",
                                        font="Arial 12", bg='grey90')
lab_pointer_tariff_3_in = tkinter.Label(root, text="за обсяг, спожитий понад               кВт∙год "\
                                                   "електроенергії на місяць:",
                                        font="Arial 12", bg='grey90')

ent_tariff_1_in = tkinter.Entry(root, width=5, bd=3, textvariable=tariff_1)
ent_tariff_2_in = tkinter.Entry(root, width=5, bd=3, textvariable=tariff_2)
ent_tariff_3_in = tkinter.Entry(root, width=5, bd=3, textvariable=tariff_3)

ent_limit_tariff_1_in = tkinter.Entry(root, width=5, bd=3, textvariable=limit_tariff_1)
ent_limit_tariff_2_in = tkinter.Entry(root, width=5, bd=3, textvariable=limit_tariff_2)
lab_limit_tariff_1_in = tkinter.Label(root, font="Arial 12", bg='grey90', textvariable=limit_tariff_1)
lab_limit_tariff_2_in = tkinter.Label(root, font="Arial 12", bg='grey90', textvariable=limit_tariff_2)

#Опис кнопки "Оновити через інтернет"
but_update_via_internet = tkinter.Button(root,
                                         text="Оновити через інтернет", font="Arial 10",
                                         width=20, height=1,
                                         bg="grey85", fg="black")
but_update_via_internet.bind("<Button-1>", fares_inet)

#Опис кнопки "Зберегти тарифи"
but_save_fares = tkinter.Button(root,
                                text="Зберегти тарифи", font="Arial 10",
                                width=15, height=1,
                                bg="grey85", fg="black")
but_save_fares.bind("<Button-1>", save_fares)


#Опис блоку "Розрахунок вартості."
header_of_block_cost_calculation = tkinter.Label(root, text="Розрахунок вартості.",
                                                 font="Arial 14", bg='grey90')

lab_pointer_amount_of_electricity_in_tariff_1 = tkinter.Label(root, text="обсяг, спожитий до               кВт∙год електроенергії " \
                                                  "на місяць (включно):",
                                                              font="Arial 12", bg='grey90')
lab1_limit_tariff_1_out = tkinter.Label(root, font="Arial 12", bg='grey90', textvariable=limit_tariff_1)
lab_amount_of_electricity_in_tariff_1 = tkinter.Label(root, font="Arial 12", bg='grey90',
                                                      textvariable=amount_of_electricity_in_tariff_1)
lab1_mark_x = tkinter.Label(root, text="x                  =",
                            font="Arial 12", bg='grey90')
lab_tariff_1_out = tkinter.Label(root, font="Arial 12", bg='grey90', textvariable=tariff_1)
lab_amount_of_money_in_tariff_1 = tkinter.Label(root, font="Arial 12", bg='grey90',
                                                textvariable=amount_of_money_in_tariff_1)

lab_pointer_amount_of_electricity_in_tariff_2 = tkinter.Label(root, text="за обсяг, спожитий понад               кВт∙год "\
                                                          "до               кВт∙год електроенергії на місяць (включно):",
                                                              font="Arial 12", bg='grey90')
lab2_limit_tariff_1_out = tkinter.Label(root, font="Arial 12", bg='grey90', textvariable=limit_tariff_1)
lab1_limit_tariff_2_out = tkinter.Label(root, font="Arial 12", bg='grey90', textvariable=limit_tariff_2)
lab_amount_of_electricity_in_tariff_2 = tkinter.Label(root, font="Arial 12", bg='grey90', textvariable = amount_of_electricity_in_tariff_2)
lab2_mark_x = tkinter.Label(root, text="x                  =",
                            font="Arial 12", bg='grey90')
lab_tariff_2_out = tkinter.Label(root, font="Arial 12", bg='grey90', textvariable=tariff_2)
lab_amount_of_money_in_tariff_2 = tkinter.Label(root, font="Arial 12", bg='grey90',
                                                textvariable=amount_of_money_in_tariff_2)

lab_pointer_amount_of_electricity_in_tariff_3 = tkinter.Label(root, text="обсяг, спожитий понад               кВт∙год електроенергії на місяць:",
                                                              font="Arial 12", bg='grey90')
lab2_limit_tariff_2_out = tkinter.Label(root, font="Arial 12", bg='grey90', textvariable=limit_tariff_2)
lab_amount_of_electricity_in_tariff_3 = tkinter.Label(root, font="Arial 12", bg='grey90',
                                                      textvariable = amount_of_electricity_in_tariff_3)
lab3_mark_x = tkinter.Label(root, text="x                  =",
                            font="Arial 12", bg='grey90')
lab_tariff_3_out = tkinter.Label(root, font="Arial 12", bg='grey90', textvariable=tariff_3)
lab_amount_of_money_in_tariff_3 = tkinter.Label(root, font="Arial 12", bg='grey90',
                                                textvariable=amount_of_money_in_tariff_3)

lab_pointer_total_amount_of_money = tkinter.Label(root, text="Всього:                          грн.",
                                                  font="Arial 12", bg='grey90')
lab_total_amount_of_money = tkinter.Label(root, font="Arial 12", bg='grey90', textvariable=total_amount_of_money)

lab_date_introduction_fares = tkinter.Label(root, text="Дата занесення показів:",
                                            font="Arial 12", bg='grey90')
ent_date_introduction_fares = tkinter.Entry(root, width=10, bd=3, textvariable=date_introduction_fares)

#Опис кнопки "Розрахувати"
but_calculation = tkinter.Button(root,
                                 text="Розрахувати", font="Arial 18",
                                 width=15, height=3,
                                 bg="lightgreen", fg="blue")
but_calculation.bind("<Button-1>", launch_calc)

#Опис кнопки "Зберегти внесені дані в файл"
but_save_in_file = tkinter.Button(root,
                                  text="Зберегти в файл", font="Arial 10",
                                  width=15, height=1,
                                  bg="lightgreen", fg="blue")
but_save_in_file.bind("<Button-1>", saves)

#Опис кнопки "Показати графік"
#but2 = Button(root,
#          text="Показати графік споживання", font="Arial 10",
#          width=25,height=1,
#          bg="lightgreen",fg="blue")
#but2.bind("<Button-1>",graph)






Central_title.place(x=50, y=5)

#Розміщення блоку "Спожита електроенергія."
a = 150
b = 30
header_of_block_consumption.place(x = 70, y = a + b)
lab_previous_shows.place(x = 10, y = a + b * 2)
lab_current_shows.place(x = 10, y = a + b * 3)
lab_or.place(x = 300, y = a + b * 4)
lab_amount_of_electricity.place(x = 10, y = a + b * 5)

ent_previous_shows.place(x = 450, y = a + b * 2)
ent_current_shows.place(x = 450, y = a + b * 3)
ent_amount_of_electricity.place(x = 450, y = a + b * 5)


#Розміщення блоку "Діючі тарифи на електроенергію, грн. за 1 кВтгод."
c = 50
d = 30
header_of_block_fares.place(x = 70, y = c)
lab_pointer_date_saving_fares.place(x = 720, y = c)
lab_date_saving_fares.place(x = 880, y = c)
lab_pointer_tariff_1_in.place(x = 10, y = c + d)
lab_pointer_tariff_2_in.place(x = 10, y = c + d * 2)
lab_pointer_tariff_3_in.place(x = 10, y = c + d * 3)

ent_tariff_1_in.place(x = 720, y = c + d)
ent_tariff_2_in.place(x = 720, y = c + d * 2)
ent_tariff_3_in.place(x = 720, y = c + d * 3)

ent_limit_tariff_1_in.place(x = 180, y = c + d)
lab_limit_tariff_1_in.place(x = 205, y = c + d * 2)
ent_limit_tariff_2_in.place(x = 340, y = c + d * 2)
lab_limit_tariff_2_in.place(x = 205, y = c + d * 3)
#Розміщення кнопки "Оновити через інтернет"
but_update_via_internet.place(x = 820, y = c + d)
#Розміщення кнопки "Зберегти тарифи"
but_save_fares.place(x = 820, y = c + d * 2)

#Розміщення блоку "Розрахунок вартості."
e = 340
f = 30
header_of_block_cost_calculation.place(x = 70, y = e)

lab_pointer_amount_of_electricity_in_tariff_1.place(x = 10, y =e + f)
lab1_limit_tariff_1_out.place(x = 165, y = e + f)
lab_amount_of_electricity_in_tariff_1.place(x = 720, y =e + f)
lab1_mark_x.place(x = 780, y = e + f)
lab_tariff_1_out.place(x = 800, y = e + f)
lab_amount_of_money_in_tariff_1.place(x = 880, y = e + f)

lab_pointer_amount_of_electricity_in_tariff_2.place(x = 10, y =e + f * 2)
lab2_limit_tariff_1_out.place(x = 205, y = e + f * 2)
lab1_limit_tariff_2_out.place(x = 340, y = e + f * 2)
lab_amount_of_electricity_in_tariff_2.place(x = 720, y =e + f * 2)
lab2_mark_x.place(x = 780, y = e + f * 2)
lab_tariff_2_out.place(x = 800, y = e + f * 2)
lab_amount_of_money_in_tariff_2.place(x = 880, y = e + f * 2)

lab_pointer_amount_of_electricity_in_tariff_3.place(x = 10, y =e + f * 3)
lab2_limit_tariff_2_out.place(x = 185, y = e + f * 3)
lab_amount_of_electricity_in_tariff_3.place(x = 720, y =e + f * 3)
lab3_mark_x.place(x = 780, y = e + f * 3)
lab_tariff_3_out.place(x = 800, y = e + f * 3)
lab_amount_of_money_in_tariff_3.place(x = 880, y = e + f * 3)

lab_pointer_total_amount_of_money.place(x = 800, y = e + f * 4)
lab_total_amount_of_money.place(x = 880, y = e + f * 4)
#Розміщення блоку Дата, збереження
lab_date_introduction_fares.place(x = 500, y = e + f * 5)
ent_date_introduction_fares.place(x = 700, y = e + f * 5)

#Розміщення кнопки "Розрахувати"
but_calculation.place(x = 600, y = a + b * 2)

#Розміщення кнопки "Зберегти в файл"
but_save_in_file.place(x = 800, y = e + f * 5)

#Розміщення кнопки "Показати графік"
#but2.place(x=800,y=e+f*6)

 
#canv_1 = Canvas(width=1000,height=550, bg = "grey90:50")
#root.create_arc([300,30],[800,330],start=0,extent=140,
#          style=ARC,outline="darkgreen",width=2)
#canv_1.pack()
root.mainloop()

