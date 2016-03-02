import tkinter
from datetime import * #tzinfo, date, timedelta
import pickle
import urllib.request
import re
import csv

root = tkinter.Tk()
root.geometry('1000x550')
root['bg'] = 'grey90'
#root.state("zoomed") #запускаэться у розгорнутому вікні

date_now = datetime.strftime(datetime.now(), "%d.%m.%Y") #%H:%M:%S

calc_end = []


print('tarifi_local')
fares_start = pickle.load(open('fares_start', 'rb'))

limit_tariff_1, limit_tariff_2, tariff_1, tariff_2, tariff_3, date_fares = fares_start


def read_fares():
    print('read_fares')
    #Зчитуємо дані введених тарифних меж
    limit_tariff_1 = int(ent_limit_tariff_1_in.get())#__main__.ent7.get()
    limit_tariff_2 = int(ent_limit_tariff_2_in.get())
    #Зчитуємо дані введених тарифів
    tariff_1 = float(ent_tariff_1_in.get())
    tariff_2 = float(ent_tariff_2_in.get())
    tariff_3 = float(ent_tariff_3_in.get())
    return [limit_tariff_1, limit_tariff_2, tariff_1, tariff_2, tariff_3, date_now]


def read_counter():
    print('read_counter')
    #Зчитуємо дані введених показників або к-ть спожитої електроенергії
    previous_shows = int(ent_previous_shows.get())
    current_shows = int(ent_current_shows.get())
    amount_of_electricity = int(ent_amount_of_electricity.get())
    return [previous_shows, current_shows, amount_of_electricity]


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
                   (r'<td>(\w+.\w+)\W+\w+\W+</tr>', u_o)
                    ]
#        print(tarifi_all)
        limit_tariff_1 = re.findall(r'спожитий до (\w+)', u_o)[0]
        limit_tariff_2 = re.findall(r'спожитий понад (\w+)', u_o)[1]
        tariff_1 = float(tarifi_all[0])/100# тариф 1
        tariff_2 = float(tarifi_all[1])/100# тариф 2
        tariff_3 = float(tarifi_all[2])/100# тариф 3
        
        write_labs_in(limit_tariff_1, limit_tariff_2, tariff_1, tariff_2, tariff_3)
        write_ents_in(limit_tariff_1, limit_tariff_2, tariff_1, tariff_2, tariff_3)
        
    except urllib.error.URLError:
        print('URLError')
        exec(open('error.py').read())
    except ValueError:
        print('ValueError')
        exec(open('error.py').read())


def write_labs_in(limit_tariff_1, limit_tariff_2, tariff_1, tariff_2, tariff_3):
    print('write_labs_in')
    #Коригуємо значення тарифних меж у відповідності до введених даних
    lab_limit_tariff_1_in.config(text = limit_tariff_1)
    lab_limit_tariff_2_in.config(text = limit_tariff_2)
    lab1_limit_tariff_1_out.config(text = limit_tariff_1)
    lab2_limit_tariff_1_out.config(text = limit_tariff_1)
    lab1_limit_tariff_2_out.config(text = limit_tariff_2)
    lab2_limit_tariff_2_out.config(text = limit_tariff_2)
    #Коригуємо значення тарифів у відповідності до введених даних
    lab_tariff_1_out.config(text = tariff_1)
    lab_tariff_2_out.config(text = tariff_2)
    lab_tariff_3_out.config(text = tariff_3)

    lab_date_saving_fares.config(text = date_now)


def write_ents_in(limit_tariff_1, limit_tariff_2, tariff_1, tariff_2, tariff_3):
    print('write_ents_in')
    ent_limit_tariff_1_in.delete(0, 100)#0,END
    ent_limit_tariff_1_in.insert(0, limit_tariff_1)#END,k
    ent_limit_tariff_2_in.delete(0, 100)#0,END
    ent_limit_tariff_2_in.insert(0, limit_tariff_2)#END,k

    ent_tariff_1_in.delete(0, 100)#0,END
    ent_tariff_1_in.insert(0, tariff_1)#END,k
    ent_tariff_2_in.delete(0, 100)#0,END
    ent_tariff_2_in.insert(0, tariff_2)#END,k
    ent_tariff_3_in.delete(0, 100)#0,END
    ent_tariff_3_in.insert(0, tariff_3)#END,k


def write_labs_out(mt1k, mt2k, mt3k, t1k, t2k, t3k, tk):
    #Змінюємо значення в поляx виводу
    lab_amount_on_tariff_1.config(text = mt1k)
    lab_amount_on_tariff_2.config(text = mt2k)
    lab_amount_on_tariff_3.config(text = mt3k)

    lab_amount_of_money_in_tariff_1.config(text ='%.2f' % (t1k))
    lab_amount_of_money_in_tariff_2.config(text ='%.2f' % (t2k))
    lab_amount_of_money_in_tariff_3.config(text ='%.2f' % (t3k))

    lab_total_amount_of_money.config(text ='%.2f' % (tk))


def calc(limit_tariff_1, limit_tariff_2, tariff_1, tariff_2, tariff_3,
         previous_shows, current_shows, amount_of_electricity
         ):
    print('calc')
    #Якщо кількість спожитої електроенергії входить в межі першого тарифу
    if 0 <= amount_of_electricity <= limit_tariff_1:
        amount_of_electricity_in_tariff_1= amount_of_electricity
        amount_of_electricity_in_tariff_2 = 0
        amount_of_electricity_in_tariff_3 = 0
        amount_of_money_in_tariff_1 = tariff_1 * amount_of_electricity
        amount_of_money_in_tariff_2 = 0
        amount_of_money_in_tariff_3 = 0
        total_amount_of_money = amount_of_money_in_tariff_1 + amount_of_money_in_tariff_2 + amount_of_money_in_tariff_3
        
        write_labs_out(amount_of_electricity_in_tariff_1, amount_of_electricity_in_tariff_2, amount_of_electricity_in_tariff_3,
                       amount_of_money_in_tariff_1, amount_of_money_in_tariff_2, amount_of_money_in_tariff_3, total_amount_of_money
                       )
            
    #Якщо кількість спожитої електроенергії входить в межі другого тарифу
    elif limit_tariff_1 < amount_of_electricity <= limit_tariff_2:
        amount_of_electricity_in_tariff_1 = limit_tariff_1
        amount_of_electricity_in_tariff_2 = amount_of_electricity - limit_tariff_1
        amount_of_electricity_in_tariff_3 = 0
        amount_of_money_in_tariff_1 = tariff_1 * limit_tariff_1
        amount_of_money_in_tariff_2 = (amount_of_electricity - limit_tariff_1) * tariff_2
        amount_of_money_in_tariff_3 = 0
        total_amount_of_money = amount_of_money_in_tariff_1 + amount_of_money_in_tariff_2 + amount_of_money_in_tariff_3
        
        write_labs_out(amount_of_electricity_in_tariff_1, amount_of_electricity_in_tariff_2, amount_of_electricity_in_tariff_3,
                       amount_of_money_in_tariff_1, amount_of_money_in_tariff_2, amount_of_money_in_tariff_3, total_amount_of_money
                       )

    #Якщо кількість спожитої електроенергії входить в межі третього тарифу
    elif limit_tariff_2 < amount_of_electricity:
        amount_of_electricity_in_tariff_1 = limit_tariff_1
        amount_of_electricity_in_tariff_2 = limit_tariff_2 - limit_tariff_1
        amount_of_electricity_in_tariff_3 = amount_of_electricity - limit_tariff_2
        amount_of_money_in_tariff_1 = tariff_1 * limit_tariff_1
        amount_of_money_in_tariff_2 = (limit_tariff_2 - limit_tariff_1) * tariff_2
        amount_of_money_in_tariff_3 = (amount_of_electricity - limit_tariff_2) * tariff_3
        total_amount_of_money = amount_of_money_in_tariff_1 + amount_of_money_in_tariff_2 + amount_of_money_in_tariff_3
        
        write_labs_out(amount_of_electricity_in_tariff_1, amount_of_electricity_in_tariff_2, amount_of_electricity_in_tariff_3,
                       amount_of_money_in_tariff_1, amount_of_money_in_tariff_2, amount_of_money_in_tariff_3, total_amount_of_money
                       )

    else:
        exec(open('error.py').read())

    get_history(limit_tariff_1, limit_tariff_2,
                tariff_1, tariff_2, tariff_3,
                previous_shows, current_shows, amount_of_electricity,
                amount_of_money_in_tariff_1, amount_of_money_in_tariff_2, amount_of_money_in_tariff_3, total_amount_of_money
                )


#Функція, що викликається кнопкою "Розрахувати"
def launch_calc(event):
    #Зчитуємо дані введених тарифних меж та тарифів
    limit_tariff_1, limit_tariff_2, tariff_1, tariff_2, tariff_3, date_fares = read_fares()
    print(limit_tariff_1, limit_tariff_2, tariff_1, tariff_2, tariff_3, date_fares)

    #Коригуємо значення тарифних меж та тарифів у відповідності до введених даних
    write_labs_in(limit_tariff_1, limit_tariff_2, tariff_1, tariff_2, tariff_3)

    #Зчитуємо дані введених показників або к-ть спожитої електроенергії
    previous_shows, current_shows, amount_of_electricity = read_counter()
    print(previous_shows, current_shows, amount_of_electricity)

    print('launch_calc')
    if previous_shows < 0 or current_shows < 0 or limit_tariff_1 > limit_tariff_2:
        exec(open('error.py').read())
    #Якщо показники лічильника не введені, то використовуємо введену кількість
    #спожитої електроенергії
    elif previous_shows == 0 and current_shows == 0 :
        calc(limit_tariff_1, limit_tariff_2, tariff_1, tariff_2, tariff_3, previous_shows, current_shows, amount_of_electricity)
    else:
        amount_of_electricity = current_shows - previous_shows
        ent_amount_of_electricity.delete(0, 100)#0,END
        ent_amount_of_electricity.insert(0, amount_of_electricity)#END,amount_of_electricity
        calc(limit_tariff_1, limit_tariff_2,
             tariff_1, tariff_2, tariff_3,
             previous_shows, current_shows, amount_of_electricity)


def get_history(limit_tariff_1, limit_tariff_2, tariff_1, tariff_2, tariff_3,
                previous_shows, current_shows, amount_of_electricity,
                amount_of_money_in_tariff_1, amount_of_money_in_tariff_2, amount_of_money_in_tariff_3, total_amount_of_money
                ):
    date = ent_date_introduction_fares.get()
    calc_end =[date, date_now,
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
    date = ent_date_introduction_fares.get()
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
#canv = Canvas(width=1000,height=550,bg='grey90')
#canv.grid(row=0, column=0)#pack()

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

ent_previous_shows = tkinter.Entry(root, width=20, bd=3)
ent_current_shows = tkinter.Entry(root, width=20, bd=3)
ent_amount_of_electricity = tkinter.Entry(root, width=20, bd=3)


#Опис блоку "Діючі тарифи на електроенергію, грн. за 1 кВтгод."
header_of_block_fares = tkinter.Label(root, text="Діючі тарифи на електроенергію, грн. за 1 кВт∙год.",
                                      font="Arial 14", bg='grey90')
lab_pointer_date_saving_fares = tkinter.Label(root, text="Дата збереження тарифів:",
                                              font="Arial 10", bg='grey90')
lab_date_saving_fares = tkinter.Label(root, text=date_fares,
                                      font="Arial 10", bg='grey90')
lab_pointer_tariff_1_in = tkinter.Label(root, text="за обсяг, спожитий до               кВт∙год "\
                                                   "електроенергії на місяць (включно):",
                                        font="Arial 12", bg='grey90')
lab_pointer_tariff_2_in = tkinter.Label(root, text="за обсяг, спожитий понад               кВт∙год "\
                                                   "до               кВт∙год електроенергії на місяць (включно):",
                                        font="Arial 12", bg='grey90')
lab_pointer_tariff_3_in = tkinter.Label(root, text="за обсяг, спожитий понад               кВт∙год "\
                                                   "електроенергії на місяць:",
                                        font="Arial 12", bg='grey90')

ent_tariff_1_in = tkinter.Entry(root, width=5, bd=3)
ent_tariff_2_in = tkinter.Entry(root, width=5, bd=3)
ent_tariff_3_in = tkinter.Entry(root, width=5, bd=3)

ent_limit_tariff_1_in = tkinter.Entry(root, width=5, bd=3)
ent_limit_tariff_2_in = tkinter.Entry(root, width=5, bd=3)
lab_limit_tariff_1_in = tkinter.Label(root, text=limit_tariff_1,
                                      font="Arial 12", bg='grey90')
lab_limit_tariff_2_in = tkinter.Label(root, text=limit_tariff_2,
                                      font="Arial 12", bg='grey90')

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

lab_pointer_amount_on_tariff_1 = tkinter.Label(root, text="обсяг, спожитий до               кВт∙год електроенергії " \
                                                  "на місяць (включно):",
                                               font="Arial 12", bg='grey90')
lab1_limit_tariff_1_out = tkinter.Label(root, text=limit_tariff_1,
                                        font="Arial 12", bg='grey90')
lab_amount_on_tariff_1 = tkinter.Label(root, text="99",
                                       font="Arial 12", bg='grey90')
lab1_mark_x = tkinter.Label(root, text="x                  =",
                            font="Arial 12", bg='grey90')
lab_tariff_1_out = tkinter.Label(root, text="0.456",
                                 font="Arial 12", bg='grey90')
lab_amount_of_money_in_tariff_1 = tkinter.Label(root, text="123",
                                                font="Arial 12", bg='grey90')

lab_pointer_amount_on_tariff_2 = tkinter.Label(root, text="за обсяг, спожитий понад               кВт∙год "\
                                                          "до               кВт∙год електроенергії на місяць (включно):",
                                               font="Arial 12", bg='grey90')
lab2_limit_tariff_1_out = tkinter.Label(root, text=limit_tariff_1,
                                        font="Arial 12", bg='grey90')
lab1_limit_tariff_2_out = tkinter.Label(root, text=limit_tariff_2,
                                        font="Arial 12", bg='grey90')
lab_amount_on_tariff_2 = tkinter.Label(root, text="599",
                                       font="Arial 12", bg='grey90')
lab2_mark_x = tkinter.Label(root, text="x                  =",
                            font="Arial 12", bg='grey90')
lab_tariff_2_out = tkinter.Label(root, text="0.789",
                                 font="Arial 12", bg='grey90')
lab_amount_of_money_in_tariff_2 = tkinter.Label(root, text="456",
                                                font="Arial 12", bg='grey90')

lab_pointer_amount_on_tariff_3 = tkinter.Label(root, text="обсяг, спожитий понад               кВт∙год електроенергії на місяць:",
                                               font="Arial 12", bg='grey90')
lab2_limit_tariff_2_out = tkinter.Label(root, text=limit_tariff_2,
                                        font="Arial 12", bg='grey90')
lab_amount_on_tariff_3 = tkinter.Label(root, text="999",
                                       font="Arial 12", bg='grey90')
lab3_mark_x = tkinter.Label(root, text="x                  =",
                            font="Arial 12", bg='grey90')
lab_tariff_3_out = tkinter.Label(root, text="1.479",
                                 font="Arial 12", bg='grey90')
lab_amount_of_money_in_tariff_3 = tkinter.Label(root, text="798",
                                                font="Arial 12", bg='grey90')

lab_pointer_total_amount_of_money = tkinter.Label(root, text="Всього:                          грн.",
                                                  font="Arial 12", bg='grey90')
lab_total_amount_of_money = tkinter.Label(root, text="88888",
                                          font="Arial 12", bg='grey90')

lab_date_introduction_fares = tkinter.Label(root, text="Дата занесення показів:",
                                            font="Arial 12", bg='grey90')
ent_date_introduction_fares = tkinter.Entry(root, width=10, bd=3)

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



#Внесення в поля значень за умовчуванням
ent_previous_shows.insert(tkinter.END, 0)
ent_current_shows.insert(tkinter.END, 0)
ent_amount_of_electricity.insert(tkinter.END, 0)
#ent4,ent5,ent6 вносяться з модуля tarifi

ent_tariff_1_in.insert(tkinter.END, tariff_1)#0.456
ent_tariff_2_in.insert(tkinter.END, tariff_2)#0.789
ent_tariff_3_in.insert(tkinter.END, tariff_3)#1.479
ent_limit_tariff_1_in.insert(tkinter.END, limit_tariff_1)#100
ent_limit_tariff_2_in.insert(tkinter.END, limit_tariff_2)#600
ent_date_introduction_fares.insert(tkinter.END, date_now)





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

lab_pointer_amount_on_tariff_1.place(x = 10, y = e + f)
lab1_limit_tariff_1_out.place(x = 165, y = e + f)
lab_amount_on_tariff_1.place(x = 720, y = e + f)
lab1_mark_x.place(x = 780, y = e + f)
lab_tariff_1_out.place(x = 800, y = e + f)
lab_amount_of_money_in_tariff_1.place(x = 880, y = e + f)

lab_pointer_amount_on_tariff_2.place(x = 10, y = e + f * 2)
lab2_limit_tariff_1_out.place(x = 205, y = e + f * 2)
lab1_limit_tariff_2_out.place(x = 340, y = e + f * 2)
lab_amount_on_tariff_2.place(x = 720, y = e + f * 2)
lab2_mark_x.place(x = 780, y = e + f * 2)
lab_tariff_2_out.place(x = 800, y = e + f * 2)
lab_amount_of_money_in_tariff_2.place(x = 880, y = e + f * 2)

lab_pointer_amount_on_tariff_3.place(x = 10, y = e + f * 3)
lab2_limit_tariff_2_out.place(x = 185, y = e + f * 3)
lab_amount_on_tariff_3.place(x = 720, y = e + f * 3)
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

