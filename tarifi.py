import __main__
from datetime import *
import urllib.request

date_now = datetime.strftime(datetime.now(), "%d.%m.%Y") #%H:%M:%S

def save_tarifi(event):
    print('save_tarifi')
    #Зчитуємо дані введених тарифних меж
    mt1 = int(__main__.ent7.get())
    mt2 = int(__main__.ent9.get())
    #Зчитуємо дані введених тарифів
    t1 = float(__main__.ent4.get())
    t2 = float(__main__.ent5.get())
    t3 = float(__main__.ent6.get())
    tarifi = [mt1, mt2, t1, t2, t3, date_now]
    tar = open('tarifi.txt', 'w')
    tar.write(str(tarifi))
    tar.close()

def tarifi_inet(event):
    print('tarifi_inet')
    try:
        u_o = urllib.request.urlopen('http://kyivenergo.ua/odnozonni_lichilniki/')
        u_o = u_o.read().decode(encoding="utf-8", errors="ignore")
        #print(u_o[7881:8500], len(u_o), u_o.index(str("147,90")))

        mt1 = int(u_o[7784:7787])# верхня межа тарифу 1
        #print(mt1)
        mt2 = int(u_o[8122:8125])# верхня межа тарифу 2
        #print(mt2)
        
        t1_1 = u_o[7881:7883]# цифри перед комою тарифу 1
        t1_2 = u_o[7884:7886]# цифри після коми тарифу 1
        #print(t1_1, t1_2)
        t1 =(int(t1_1)+int(t1_2)/100)/100
        t2_1 = u_o[8061:8063]# цифри перед комою тарифу 2
        t2_2 = u_o[8064:8066]# цифри після коми тарифу 2
        #print(t2_1, t2_2)
        t2 = (int(t2_1)+int(t2_2)/100)/100
        t3_1 = u_o[8211:8214]
        t3_2 = u_o[8215:8217]
        #print(t3_1, t3_2)
        t3 = (int(t3_1)+int(t3_2)/100)/100
        #Коригуємо значення тарифних меж у відповідності до введених даних
        __main__.lab32.config(text = mt1)
        __main__.lab33.config(text = mt2)
        __main__.lab12.config(text = mt1)
        __main__.lab18.config(text = mt1)
        __main__.lab19.config(text = mt2)
        __main__.lab25.config(text = mt2)

        __main__.lab15.config(text = t1)
        __main__.lab22.config(text = t2)
        __main__.lab28.config(text = t3)

        __main__.ent7.delete(0,100)#0,END
        __main__.ent7.insert(0,mt1)#END,k
        __main__.ent9.delete(0,100)#0,END
        __main__.ent9.insert(0,mt2)#END,k

        __main__.ent4.delete(0,100)#0,END
        __main__.ent4.insert(0,t1)#END,k
        __main__.ent5.delete(0,100)#0,END
        __main__.ent5.insert(0,t2)#END,k
        __main__.ent6.delete(0,100)#0,END
        __main__.ent6.insert(0,t3)#END,k

        __main__.lab6_2.config(text = date_now)
        date_tarifiv = date_now
        tarifi = [mt1, mt2, t1, t2, t3, date_tarifiv]
        print(tarifi)
        tar = open('tarifi.txt', 'w')
        tar.write(str(tarifi))
        tar.close()
    except urllib.error.URLError:
        exec(open('error.py').read())
    except ValueError:
        exec(open('error.py').read())
    
print ('tarifi_local')
tar = open('tarifi.txt', 'r').readline()
mt1 = tar[1:4]
mt2 = tar[6:9]    
t1 = float(tar[11:16])
t2 = float(tar[18:23])
t3 = float(tar[25:30])
#    print(mt1, mt2, t1, t2, t3)
date_tarifiv = tar[33:43]
__main__.mt1 = mt1
__main__.mt2 = mt2
__main__.t1 = t1
__main__.t2 = t2
__main__.t3 = t3
__main__.date_tarifiv = date_tarifiv
#    print(t1, t2, t3, date_tarifiv)
