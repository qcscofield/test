# -*- coding:utf-8 -*-

import requests
import os
from bs4 import BeautifulSoup

url = 'http://trend.caipiao.163.com/cqssc/zuxuan-3xing.html'

def getdata(url):
    r = requests.get(url)
    with open('basedata.txt','w') as f:
        f.write(r.text)
    soup = BeautifulSoup(open('basedata.txt'),'html.parser')
    cpdata = soup.find_all(id="cpdata")[0].find_all(attrs={"class":"c_ba2636"})
    with open('current_data.txt','w') as f:
        for i in cpdata:
            f.write(i.string+'\n')

def calculate():
    a = ''
    b = ''
    c = ''
    with open('current_data.txt','r') as f:
        for i in f:
            print(i)
            a += i[0]
            b += i[1]
            c += i[2]
        s = {'A':a,
             'B':b,
             'C':c}
        S0,S1,S2,S3,S4,S5,S6,S7,S8,S9 = 0,0,0,0,0,0,0,0,0,0
        for i in s:
            print(i)
            S0 += int(s[i].count('0'))//0.3
            print('0:  '+str(int(s[i].count('0'))//0.3)+'%')
            S1 += int(s[i].count('1'))//0.3
            print('1:  '+str(int(s[i].count('1'))//0.3)+'%')
            S2 += int(s[i].count('2'))//0.3
            print('2:  '+str(int(s[i].count('2'))//0.3)+'%')
            S3 += int(s[i].count('3'))//0.3
            print('3:  '+str(int(s[i].count('3'))//0.3)+'%')
            S4 += int(s[i].count('4'))//0.3
            print('4:  '+str(int(s[i].count('4'))//0.3)+'%')
            S5 += int(s[i].count('5'))//0.3
            print('5:  '+str(int(s[i].count('5'))//0.3)+'%')
            S6 += int(s[i].count('6'))//0.3
            print('6:  '+str(int(s[i].count('6'))//0.3)+'%')
            S7 += int(s[i].count('7'))//0.3
            print('7:  '+str(int(s[i].count('7'))//0.3)+'%')
            S8 += int(s[i].count('8'))//0.3
            print('8:  '+str(int(s[i].count('8'))//0.3)+'%')
            S9 += int(s[i].count('9'))//0.3
            print('9:  '+str(int(s[i].count('9'))//0.3)+'%')
            if i == 'C':
                zong = {'S0':S0,'S1':S1,'S2':S2,'S3':S3,'S4':S4,'S5':S5,'S6':S6,'S7':S7,'S8':S8,'S9':S9}
                for i in zong:
                    print('\n\n'+i+'  :  '+str(zong[i])+'%')




getdata(url)
calculate()