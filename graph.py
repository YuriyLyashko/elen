#Для графіку
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.widgets import CheckButtons
mpl.rcParams['font.family'] = 'fantasy'
mpl.rcParams['font.fantasy'] = 'Arial'






#Функція, що викликається кнопкою "Показати графік навантаження"
def graph(event):
    s = open('saves.txt', 'r')
    all_lines = s.readlines()
    s.close()
    n = 1
    i = []
    grn = []
    kW = []
    dates = []
    while n < len(all_lines):
        line = all_lines[n]
        line = line[2:-3]
        line = line.split("', '")
#        print("\n", line, "\n", line[13],"\n", len(line), "\n", type(line[13]))
#        print(x)
#        print(y)
#        print(z)
        i_i = n # str(line[0])
        grn_i = line[13]
        kW_i = line[9]
        dates_i = line[0]
        i.append(i_i)
        grn.append(grn_i)
        kW.append(kW_i)
        dates.append(dates_i)
        n += 1

#    plt.xlabel("Час")    # обозначение оси абсцисс
#    plt.ylabel("Споживання, кВт.; Оплата, грн.")    # обозначение оси ординат
    plt.axes([0.06,0.17,0.9,0.72])#Розташування графіку у вікні
    plt.title("Графік споживання та оплат")
    
    kW_graph = plt.plot(i, kW, 'b', label="Споживання, кВт")
    grn_grsph = plt.plot(i, grn, 'r', label="Оплата, грн")



    plt.legend(loc=0)
    plt.grid(True)
    pos = np.arange(len(kW))
    xt = plt.xticks(pos + 1, dates, rotation=90)
    for i in pos:
        kW_text = plt.text(pos[i] + 1.1, kW[i], kW[i], color = 'blue')
    for i in pos:
        grn_text = plt.text(pos[i] + 1.1, grn[i], grn[i], color = 'red')

#    check = CheckButtons(plt.axes([0.74, 0.9, 0.22, 0.08]),
#                         ('Споживання, кВт','Оплата, грн'),                         
#                         (True, True))
#    def func(label):
#        if label == 'Споживання, кВт': kW_graph.set_visable(not kW_graph.get_visable())
#        if label == 'Оплата, грн': grn_graph.set_visable(not grn_graph.get_visable())
#        plt.draw()
#    check.on_clicked(func)

    
    plt.show()
