from tkinter import *

from datetime import * #tzinfo, date, timedelta

#from tarifi import *
#from launch_calc import *
from saves import *
#from graph import *

import pickle
import urllib.request
import re


root = Tk()
root.geometry('1000x550')
root['bg'] = 'grey90'
#root.state("zoomed") #запускаэться у розгорнутому вікні

date_now = datetime.strftime(datetime.now(), "%d.%m.%Y") #%H:%M:%S

calc_end = []


print('tarifi_local')
fares_start = pickle.load(open('fares_start', 'rb'))

mt1 = fares_start[0]
mt2 = fares_start[1]    
t1 = float(fares_start[2])
t2 = float(fares_start[3])
t3 = float(fares_start[4])
date_fares = fares_start[5]


def read_fares():
    print('read_fares')
    #Зчитуємо дані введених тарифних меж
    mt1 = int(ent7.get())#__main__.ent7.get()
    mt2 = int(ent9.get())
    #Зчитуємо дані введених тарифів
    t1 = float(ent4.get())
    t2 = float(ent5.get())
    t3 = float(ent6.get())
    return [mt1, mt2, t1, t2, t3, date_now]


def read_counter():
    print('read_counter')
    #Зчитуємо дані введених показників або к-ть спожитої електроенергії
    l1 = int(ent1.get())
    l2 = int(ent2.get())
    k = int(ent3.get())    
    return [l1, l2, k]


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
        tar_meg_1 = re.findall(r'спожитий до (\w+)', u_o)
        tar_meg_2 = re.findall(r'спожитий понад (\w+)', u_o)
        mt1 = tar_meg_1[0]# верхня межа тарифу 1
        mt2 = tar_meg_2[1]# верхня межа тарифу 2
        t1 = float(tarifi_all[0])/100# тариф 1
        t2 = float(tarifi_all[1])/100# тариф 2
        t3 = float(tarifi_all[2])/100# тариф 3
        
        write_labs_in(mt1, mt2, t1, t2, t3)
        write_ents_in(mt1, mt2, t1, t2, t3)
        
    except urllib.error.URLError:
        print('URLError')
        exec(open('error.py').read())
    except ValueError:
        print('ValueError')
        exec(open('error.py').read())


def write_labs_in(mt1, mt2, t1, t2, t3):
    print('write_labs_in')
    #Коригуємо значення тарифних меж у відповідності до введених даних
    lab32.config(text = mt1)
    lab33.config(text = mt2)
    lab12.config(text = mt1)
    lab18.config(text = mt1)
    lab19.config(text = mt2)
    lab25.config(text = mt2)
    #Коригуємо значення тарифів у відповідності до введених даних
    lab15.config(text = t1)
    lab22.config(text = t2)
    lab28.config(text = t3)

    lab6_2.config(text = date_now)


def write_ents_in(mt1, mt2, t1, t2, t3):
    print('write_ents_in')
    ent7.delete(0,100)#0,END
    ent7.insert(0,mt1)#END,k
    ent9.delete(0,100)#0,END
    ent9.insert(0,mt2)#END,k

    ent4.delete(0,100)#0,END
    ent4.insert(0,t1)#END,k
    ent5.delete(0,100)#0,END
    ent5.insert(0,t2)#END,k
    ent6.delete(0,100)#0,END
    ent6.insert(0,t3)#END,k


def write_labs_out(mt1k, mt2k, mt3k, t1k, t2k, t3k, tk):
    #Змінюємо значення в поляx виводу
    lab13.config(text = mt1k)
    lab20.config(text = mt2k)
    lab26.config(text = mt3k)

    lab16.config(text = '%.2f'%(t1k))
    lab23.config(text = '%.2f'%(t2k))
    lab29.config(text = '%.2f'%(t3k))

    lab31.config(text = '%.2f'%(tk))


def calc(mt1, mt2, t1, t2, t3, l1, l2, k):
    print('calc')
    #Якщо кількість спожитої електроенергії входить в межі першого тарифу
    if 0 <= k <= mt1:
        mt1k = k
        mt2k = 0
        mt3k = 0
        t1k = t1 * k
        t2k = 0
        t3k = 0
        tk = t1k + t2k + t3k
        
        write_labs_out(mt1k, mt2k, mt3k, t1k, t2k, t3k, tk)
            
    #Якщо кількість спожитої електроенергії входить в межі другого тарифу
    elif mt1 < k <= mt2:
        mt1k = mt1
        mt2k = k-mt1
        mt3k = 0
        t1k = t1 * mt1
        t2k = (k-mt1)*t2
        t3k = 0   
        tk = t1k + t2k + t3k
        
        write_labs_out(mt1k, mt2k, mt3k, t1k, t2k, t3k, tk)

    #Якщо кількість спожитої електроенергії входить в межі третього тарифу
    elif mt2 < k:
        mt1k = mt1
        mt2k = mt2-mt1
        mt3k = k - mt2
        t1k = t1 * mt1
        t2k = (mt2-mt1)*t2
        t3k = (k-mt2)*t3   
        tk = t1k + t2k + t3k
        
        write_labs_out(mt1k, mt2k, mt3k, t1k, t2k, t3k, tk)

    else:
        exec(open('error.py').read())
    get_history(mt1, mt2, t1, t2, t3, l1, l2, k, t1k, t2k, t3k, tk)

def get_history(mt1, mt2, t1, t2, t3, l1, l2, k, t1k, t2k, t3k, tk):
    date = ent10.get()
    calc_end =[date, date_now,
               '%.0f'%(mt1), '%.0f'%(mt2),
               '%.3f'%(t1), '%.3f'%(t2), '%.3f'%(t3),
               '%.0f'%(l1), '%.0f'%(l2), '%.0f'%(k),
               '%.2f'%(t1k), '%.2f'%(t2k), '%.2f'%(t3k), '%.2f'%(tk)
               ]
    h = open('history.txt', 'a')
    h.write(str(calc_end)+"r \n")
    h.close()


#Функція, що викликається кнопкою "Розрахувати"
def launch_calc(event):
    #Зчитуємо дані введених тарифних меж та тарифів
    fares = read_fares()
    mt1 = fares[0]
    mt2 = fares[1]
    t1 = fares[2]
    t2 = fares[3]
    t3 = fares[4]
    print(fares)
    #Коригуємо значення тарифних меж та тарифів у відповідності до введених даних
    write_labs_in(mt1, mt2, t1, t2, t3)
    #Зчитуємо дані введених показників або к-ть спожитої електроенергії
    counter_reads = read_counter()
    print(counter_reads)
    l1 = counter_reads[0]
    l2 = counter_reads[1]
    k = counter_reads[2]
    print('launch_calc')
    if l1 < 0 or l2 < 0 or mt1 > mt2:
        exec(open('error.py').read())
    #Якщо показники лічильника не введені, то використовуємо введену кількість
    #спожитої електроенергії
    elif l1 == 0 and l2 == 0 :
        calc(mt1, mt2, t1, t2, t3, l1, l2, k)
    else:
        k = l2 - l1
        ent3.delete(0,100)#0,END
        ent3.insert(0,k)#END,k
        calc(mt1, mt2, t1, t2, t3, l1, l2, k)
        
    

   
root.title("Розрахунок вартості спожитої електроенергії")
#canv = Canvas(width=1000,height=550,bg='grey90')
#canv.grid(row=0, column=0)#pack()

Central_title = Label(root, text="Розрахунок вартості спожитої електроенергії для однозонного лічильника.", \
                      font="Arial 16", bg='grey90')


#Опис блоку "Спожита електроенергія."
lab1 = Label(root, text="Спожита електроенергія.",\
             font="Arial 14", bg='grey90')
lab2 = Label(root, text="Введіть попередні значення лічильника електроенергії:",\
             font="Arial 12", bg='grey90')
lab3 = Label(root, text="Введіть поточні значення лічильника електроенергії:",\
             font="Arial 12", bg='grey90')
lab4 = Label(root, text="АБО",\
             font="Arial 12", bg='grey90')
lab5 = Label(root, text="Введіть кількість спожитої електроенергії, кВт∙год:",\
             font="Arial 12", bg='grey90')

ent1 = Entry(root,width=20,bd=3)
ent2 = Entry(root,width=20,bd=3)
ent3 = Entry(root,width=20,bd=3)


#Опис блоку "Діючі тарифи на електроенергію, грн. за 1 кВтгод."
lab6 = Label(root, text="Діючі тарифи на електроенергію, грн. за 1 кВт∙год.",\
             font="Arial 14", bg='grey90')
lab6_1 = Label(root, text="Дата оновлення тарифів:",\
             font="Arial 10", bg='grey90')
lab6_2 = Label(root, text=date_fares,\
             font="Arial 10", bg='grey90')
lab7 = Label(root, text="за обсяг, спожитий до               кВт∙год електроенергії на місяць (включно):",\
             font="Arial 12", bg='grey90')
lab8 = Label(root, text="за обсяг, спожитий понад               кВт∙год до               кВт∙год електроенергії на місяць (включно):",\
             font="Arial 12", bg='grey90')
lab9 = Label(root, text="за обсяг, спожитий понад               кВт∙год електроенергії на місяць:",\
             font="Arial 12", bg='grey90')

ent4 = Entry(root,width=5,bd=3)
ent5 = Entry(root,width=5,bd=3)
ent6 = Entry(root,width=5,bd=3)

ent7 = Entry(root,width=5,bd=3)
ent9 = Entry(root,width=5,bd=3)
lab32 = Label(root, text=mt1,\
             font="Arial 12", bg='grey90')
lab33 = Label(root, text=mt2,\
             font="Arial 12", bg='grey90')

#Опис кнопки "Оновити через інтернет"
but4 = Button(root,
          text="Оновити через інтернет", font="Arial 10",
          width=20,height=1,
          bg="grey85",fg="black")
but4.bind("<Button-1>",fares_inet)

#Опис кнопки "Зберегти тарифи"
but3 = Button(root,
          text="Зберегти тарифи", font="Arial 10",
          width=15,height=1,
          bg="grey85",fg="black")
but3.bind("<Button-1>", save_fares)


#Опис блоку "Розрахунок вартості."
lab10 = Label(root, text="Розрахунок вартості.",\
             font="Arial 14", bg='grey90')

lab11 = Label(root, text="обсяг, спожитий до               кВт∙год електроенергії на місяць (включно):",\
             font="Arial 12", bg='grey90')
lab12 = Label(root, text=mt1,\
             font="Arial 12", bg='grey90')
lab13 = Label(root, text="99",\
             font="Arial 12", bg='grey90')
lab14 = Label(root, text="x                  =",\
             font="Arial 12", bg='grey90')
lab15 = Label(root, text="0.456",\
             font="Arial 12", bg='grey90')
lab16 = Label(root, text="123",\
             font="Arial 12", bg='grey90')

lab17 = Label(root, text="за обсяг, спожитий понад               кВт∙год до               кВт∙год електроенергії на місяць (включно):",\
             font="Arial 12", bg='grey90')
lab18 = Label(root, text=mt1,\
             font="Arial 12", bg='grey90')
lab19 = Label(root, text=mt2,\
             font="Arial 12", bg='grey90')
lab20 = Label(root, text="599",\
             font="Arial 12", bg='grey90')
lab21 = Label(root, text="x                  =",\
             font="Arial 12", bg='grey90')
lab22 = Label(root, text="0.789",\
             font="Arial 12", bg='grey90')
lab23 = Label(root, text="456",\
             font="Arial 12", bg='grey90')

lab24 = Label(root, text="обсяг, спожитий понад               кВт∙год електроенергії на місяць:",\
             font="Arial 12", bg='grey90')
lab25 = Label(root, text=mt2,\
             font="Arial 12", bg='grey90')
lab26 = Label(root, text="999",\
             font="Arial 12", bg='grey90')
lab27 = Label(root, text="x                  =",\
             font="Arial 12", bg='grey90')
lab28 = Label(root, text="1.479",\
             font="Arial 12", bg='grey90')
lab29 = Label(root, text="798",\
             font="Arial 12", bg='grey90')

lab30 = Label(root, text="Всього:                          грн.",\
             font="Arial 12", bg='grey90')
lab31 = Label(root, text="88888",\
             font="Arial 12", bg='grey90')

lab34 = Label(root,text="Дата занесення показів:",\
             font="Arial 12", bg='grey90')
ent10 = Entry(root,width=10,bd=3)

#Опис кнопки "Розрахувати"
but = Button(root,
          text="Розрахувати", font="Arial 18",
          width=15,height=3,
          bg="lightgreen",fg="blue")
but.bind("<Button-1>",launch_calc)

#Опис кнопки "Зберегти внесені дані в файл"
but1 = Button(root,
          text="Зберегти в файл", font="Arial 10",
          width=15,height=1,
          bg="lightgreen",fg="blue")
but1.bind("<Button-1>",saves)

#Опис кнопки "Показати графік"
#but2 = Button(root,
#          text="Показати графік споживання", font="Arial 10",
#          width=25,height=1,
#          bg="lightgreen",fg="blue")
#but2.bind("<Button-1>",graph)



#Внесення в поля значень за умовчуванням
ent1.insert(END,0)
ent2.insert(END,0)
ent3.insert(END,0)
#ent4,ent5,ent6 вносяться з модуля tarifi

ent4.insert(END,t1)#0.456
ent5.insert(END,t2)#0.789
ent6.insert(END,t3)#1.479
ent7.insert(END,mt1)#100
ent9.insert(END,mt2)#600
ent10.insert(END,date_now)





Central_title.place(x=50, y=5)

#Розміщення блоку "Спожита електроенергія."
a = 150
b = 30
lab1.place(x=70,y=a+b)
lab2.place(x=10,y=a+b*2)
lab3.place(x=10,y=a+b*3)
lab4.place(x=300,y=a+b*4)
lab5.place(x=10,y=a+b*5)

ent1.place(x=450,y=a+b*2)
ent2.place(x=450,y=a+b*3)
ent3.place(x=450,y=a+b*5)


#Розміщення блоку "Діючі тарифи на електроенергію, грн. за 1 кВтгод."
c = 50
d = 30
lab6.place(x=70,y=c)
lab6_1.place(x=720,y=c)
lab6_2.place(x=880,y=c)
lab7.place(x=10,y=c+d)
lab8.place(x=10,y=c+d*2)
lab9.place(x=10,y=c+d*3)

ent4.place(x=720,y=c+d)
ent5.place(x=720,y=c+d*2)
ent6.place(x=720,y=c+d*3)

ent7.place(x=180,y=c+d)
lab32.place(x=205,y=c+d*2)
ent9.place(x=340,y=c+d*2)
lab33.place(x=205,y=c+d*3)
#Розміщення кнопки "Оновити через інтернет"
but4.place(x=820,y=c+d)
#Розміщення кнопки "Зберегти тарифи"
but3.place(x=820,y=c+d*2)

#Розміщення блоку "Розрахунок вартості."
e = 340
f = 30
lab10.place(x=70,y=e)

lab11.place(x=10,y=e+f)
lab12.place(x=165,y=e+f)
lab13.place(x=720,y=e+f)
lab14.place(x=780,y=e+f)
lab15.place(x=800,y=e+f)
lab16.place(x=880,y=e+f)

lab17.place(x=10,y=e+f*2)
lab18.place(x=205,y=e+f*2)
lab19.place(x=340,y=e+f*2)
lab20.place(x=720,y=e+f*2)
lab21.place(x=780,y=e+f*2)
lab22.place(x=800,y=e+f*2)
lab23.place(x=880,y=e+f*2)

lab24.place(x=10,y=e+f*3)
lab25.place(x=185,y=e+f*3)
lab26.place(x=720,y=e+f*3)
lab27.place(x=780,y=e+f*3)
lab28.place(x=800,y=e+f*3)
lab29.place(x=880,y=e+f*3)

lab30.place(x=800,y=e+f*4)
lab31.place(x=880,y=e+f*4)
#Розміщення блоку Дата, збереження
lab34.place(x=500,y=e+f*5)
ent10.place(x=700,y=e+f*5)

#Розміщення кнопки "Розрахувати"
but.place(x=600,y=a+b*2)

#Розміщення кнопки "Зберегти в файл"
but1.place(x=800,y=e+f*5)

#Розміщення кнопки "Показати графік"
#but2.place(x=800,y=e+f*6)

 
#canv_1 = Canvas(width=1000,height=550, bg = "grey90:50")
#root.create_arc([300,30],[800,330],start=0,extent=140,
#          style=ARC,outline="darkgreen",width=2)
#canv_1.pack()
root.mainloop()

