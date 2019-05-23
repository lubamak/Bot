import pandas as pd
import random
import win32com.client
import pythoncom
import numpy as np
dictionary={0:1, 2:1}

def ap(chat_id, x, dictionary):
    if chat_id in dictionary.keys():
        dictionary[chat_id]=x
    else:
        dictionary.update({chat_id: x})
    return dictionary

def number(chat_id, dictionary):
    return dictionary[chat_id]


def category(y):
    data = pd.read_excel('anekdot.xls')
    a = data.as_matrix()
    x = random.randrange(1, 150, 1)

    while a[x - 1][1] != y:
        x = random.randrange(1, 150, 1)

    t = a[x - 1][2]

    return [t, x]

def category_B():
    data = pd.read_excel('anekdot_B.xlsx')
    a = data.as_matrix()
    x = random.randrange(1, 31, 1)
    return a[x-1][1]
print(category_B())

print(category('о жизни'))
#Проверка функции category

#Меняет рейтинг выбранного анекдота. Принимает анекдот и оценку.
def ranking(q,x):
    data = pd.read_excel('anekdot.xls')
    a = data.as_matrix()
    
    if a[x-1][3]==0:
        a[x-1][3]=q
    else:
        a[x-1][3]=(a[x-1][3]+q)/2
    # Сразу перед инициализацией DCOM
    pythoncom.CoInitializeEx(0)

    Excel = win32com.client.Dispatch("Excel.Application")
    wb = Excel.Workbooks.Open(u'C:\\Users\\Luba\\PycharmProjects\\Bot\\anekdot.xls')
    sheet = wb.ActiveSheet
    
    sheet.Cells(x+1,4).value = a[x-1][3]

    wb.Save()
    wb.Close()
    Excel.Quit()
    return a[x-1][2]

ranking(2,4)

def top():
    data = pd.read_excel('anekdot.xls')
    a = data.as_matrix()
    c = []
    b = data.as_matrix()
    c = sorted(b, key = lambda s: s[3])
    x=random.randrange(141,151,1)
    rep = c[x][2]

    return [rep,x]

top()



