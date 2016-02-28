import __main__
#Функція, що викликається кнопкою "Розрахувати"
def calc(event):
    #Зчитуємо дані введених тарифних меж
    mt1 = int(__main__.ent7.get())
    mt2 = int(__main__.ent9.get())
    #Коригуємо значення тарифних меж у відповідності до введених даних
    __main__.lab32.config(text = mt1)
    __main__.lab33.config(text = mt2)
    __main__.lab12.config(text = mt1)
    __main__.lab18.config(text = mt1)
    __main__.lab19.config(text = mt2)
    __main__.lab25.config(text = mt2)
    #Зчитуємо дані введених тарифів
    t1 = float(__main__.ent4.get())
    t2 = float(__main__.ent5.get())
    t3 = float(__main__.ent6.get())
    #Коригуємо значення тарифів у відповідності до введених даних
    __main__.lab15.config(text = t1)
    __main__.lab22.config(text = t2)
    __main__.lab28.config(text = t3)
    #Зчитуємо дані введених показників або к-ть спожитої електроенергії
    l1 = int(__main__.ent1.get())
    l2 = int(__main__.ent2.get())
    k = int(__main__.ent3.get())
    #Якщо показники лічильника не введені, то використовуємо введену кількість
    #спожитої електроенергії
    if l1 < 0 or l2 < 0:
        exec(open('error.py').read())
    elif l1 == 0 and l2 == 0 :
        #Якщо кількість спожитої електроенергії входить в межі першого тарифу
        if 0 <= k <= mt1:
            #Змінюємо значення в поля
            __main__.lab13.config(text = k)
            __main__.lab20.config(text = 0)
            __main__.lab26.config(text = 0)

            t1k = t1 * k
            __main__.lab16.config(text = '%.2f'%(t1k))
            t2k = 0
            __main__.lab23.config(text = '%.2f'%(t2k))
            t3k = 0
            __main__.lab29.config(text = '%.2f'%(t3k))

            tk = t1k + t2k + t3k
            __main__.lab31.config(text = '%.2f'%(tk))

        #Якщо кількість спожитої електроенергії входить в межі другого тарифу
        elif mt1 < k <= mt2:
            __main__.lab13.config(text = mt1)
            __main__.lab20.config(text = k-mt1)
            __main__.lab26.config(text = 0)

            t1k = t1 * mt1
            __main__.lab16.config(text = '%.2f'%(t1k))
            t2k = (k-mt1)*t2
            __main__.lab23.config(text = '%.2f'%(t2k))
            t3k = 0
            __main__.lab29.config(text = '%.2f'%(t3k))

            tk = t1k + t2k + t3k
            __main__.lab31.config(text = '%.2f'%(tk))
        #Якщо кількість спожитої електроенергії входить в межі третього тарифу
        elif mt2 < k:
            __main__.lab13.config(text = mt1)
            __main__.lab20.config(text = mt2-mt1)
            __main__.lab26.config(text = k - mt2)

            t1k = t1 * mt1
            __main__.lab16.config(text = '%.2f'%(t1k))
            t2k = (mt2-mt1)*t2
            __main__.lab23.config(text = '%.2f'%(t2k))
            t3k = (k-mt2)*t3
            __main__.lab29.config(text = '%.2f'%(t3k))

            tk = t1k + t2k + t3k
            __main__.lab31.config(text = '%.2f'%(tk))
        else:
            exec(open('error.py').read())
    else:
        k = l2 - l1
        __main__.ent3.delete(0,100)#0,END
        __main__.ent3.insert(0,k)#END,k
        #Якщо кількість спожитої електроенергії входить в межі першого тарифу
        if 0 <= k <= mt1:
            #Змінюємо значення в поля
            __main__.lab13.config(text = k)
            __main__.lab20.config(text = 0)
            __main__.lab26.config(text = 0)

            t1k = t1 * k
            __main__.lab16.config(text = '%.2f'%(t1k))
            t2k = 0
            __main__.lab23.config(text = '%.2f'%(t2k))
            t3k = 0
            __main__.lab29.config(text = '%.2f'%(t3k))

            tk = t1k + t2k + t3k
            __main__.lab31.config(text = '%.2f'%(tk))

        #Якщо кількість спожитої електроенергії входить в межі другого тарифу
        elif mt1 < k <= mt2:
            __main__.lab13.config(text = mt1)
            __main__.lab20.config(text = k-mt1)
            __main__.lab26.config(text = 0)

            t1k = t1 * mt1
            __main__.lab16.config(text = '%.2f'%(t1k))
            t2k = (k-mt1)*t2
            __main__.lab23.config(text = '%.2f'%(t2k))
            t3k = 0
            __main__.lab29.config(text = '%.2f'%(t3k))

            tk = t1k + t2k + t3k
            __main__.lab31.config(text = '%.2f'%(tk))
        #Якщо кількість спожитої електроенергії входить в межі третього тарифу
        elif mt2 < k:
            __main__.lab13.config(text = mt1)
            __main__.lab20.config(text = mt2-mt1)
            __main__.lab26.config(text = k - mt2)

            t1k = t1 * mt1
            __main__.lab16.config(text = '%.2f'%(t1k))
            t2k = (mt2-mt1)*t2
            __main__.lab23.config(text = '%.2f'%(t2k))
            t3k = (k-mt2)*t3
            __main__.lab29.config(text = '%.2f'%(t3k))

            tk = t1k + t2k + t3k
            __main__.lab31.config(text = '%.2f'%(tk))
        else:
            exec(open('error.py').read())
    date = __main__.ent10.get()
    __main__.calc_end =[date, __main__.date_now,
               '%.0f'%(mt1), '%.0f'%(mt2),
               '%.3f'%(t1), '%.3f'%(t2), '%.3f'%(t3),
               '%.0f'%(l1), '%.0f'%(l2), '%.0f'%(k),
               '%.2f'%(t1k), '%.2f'%(t2k), '%.2f'%(t3k), '%.2f'%(tk)]
#    print(__main__.calc_end, len(__main__.calc_end))
    h = open('history.txt', 'a')
    h.write(str(__main__.calc_end)+"r \n")
    h.close()
#    return calc_end
