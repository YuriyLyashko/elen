import __main__
#from calc import calc_end
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
    date = __main__.ent10.get()
#    print(__main__.calc_end, len(__main__.calc_end))
    h = open('history.txt', 'a')
    if len(__main__.calc_end) < 2:
        exec(open('error.py').read())
    else:
        h.write(str(__main__.calc_end)+"s \n")
        h.close()
        s = open('saves.txt', 'a')
        #a - дозапис, 'w' - запис, 'r' - читання
        s.write(str(__main__.calc_end)+"\n")
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
