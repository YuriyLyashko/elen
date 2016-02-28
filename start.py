from tkinter import *

from datetime import * #tzinfo, date, timedelta

from tarifi import *
from calc import *
from saves import *
#from graph import *


root = Tk()
root.geometry('1000x550')
root['bg'] = 'grey90'
#root.state("zoomed") #запускаэться у розгорнутому вікні

date_now = datetime.strftime(datetime.now(), "%d.%m.%Y") #%H:%M:%S

calc_end = []
date_tarifiv = date_tarifiv
mt1 = mt1
mt2 = mt2
t1 = t1
t2 = t2
t3 = t3


   
root.title("Розрахунок вартості спожитої електроенергії")


#canv = Canvas(width=1000,height=550,bg='grey90')
#canv.grid(row=0, column=0)#pack()

lab = Label(root, text="Розрахунок вартості спожитої електроенергії для однозонного лічильника.",\
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
lab6_2 = Label(root, text=date_tarifiv,\
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
but4.bind("<Button-1>",tarifi_inet)
#Опис кнопки "Зберегти тарифи"
but3 = Button(root,
          text="Зберегти тарифи", font="Arial 10",
          width=15,height=1,
          bg="grey85",fg="black")
but3.bind("<Button-1>",save_tarifi)


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
but.bind("<Button-1>",calc)

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









lab.place(x=50,y=5)

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
but2.place(x=800,y=e+f*6)

 
#canv_1 = Canvas(width=1000,height=550, bg = "grey90:50")
#root.create_arc([300,30],[800,330],start=0,extent=140,
#          style=ARC,outline="darkgreen",width=2)
#canv_1.pack()
root.mainloop()

