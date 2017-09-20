# coding: utf-8

"""命令行火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""
#from docopt import docopt
import requests
import urllib.request
from prettytable import PrettyTable
from tkinter import *
from tkinter import ttk

def cli(_from,_to,_date):
    """command-line interface"""
    #arguments = docopt(__doc__)
    from_station = urllib.request.quote(str(_from))
    to_station = urllib.request.quote(str(_to))
    date = urllib.request.quote(str(_date))
    url = ('https://train.qunar.com/dict/open/s2s.do?\
&dptStation={}\
&arrStation={}\
&date={}\
&type=normal\
&user=neibu\
&source=site\
&start=1\
&num=500\
&sort=3').format(from_station,to_station,date)
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Connection':'keep-alive',
              'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
              'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'
              }
    #request = urllib.request.Request(url=url,headers=headers
    r = requests.get(url,verify=False)
    #print(r.status_code)
    print(url)
    available_trains = r.json()["data"]["s2sBeanList"]
    return available_trains

def seat(seat_name,tain_inf):
	if tain_inf["seats"].get(seat_name):
		return '\n'.join(map(str,(tain_inf["seats"][seat_name]["count"],tain_inf["seats"][seat_name]["price"])))+'元'
	else:
		return "--"

def colored(color, text):
    table = {
        'red': '\033[91m',
        'green': '\033[92m',
        # no color
        'nc': '\033[0'
    }
    cv = table.get(color)
    nv = table.get('nc')
    return ''.join([cv, text, nv])


def tain(tains_inf):
	title = PrettyTable(["车次","车站","时间","历时","商务座","一等座","二等座","动卧","无座","硬座","硬卧","软卧"])
	title.align = "c"
	title.valign = "m"
	for tain_inf in tains_inf:
		title.add_row([tain_inf["trainNo"],'\n'.join([tain_inf["dptStationName"],tain_inf["arrStationName"]]),\
			'\n'.join([tain_inf["dptTime"],tain_inf["arrTime"]]),\
			str(int(tain_inf["lishiValue"])//60)+'小时'+str(int(tain_inf["lishiValue"])%60)+'分钟',\
			seat("商务座",tain_inf),seat("一等座",tain_inf),seat("二等座",tain_inf),seat("动卧",tain_inf),\
			seat("无座",tain_inf),seat("硬座",tain_inf),seat("硬卧",tain_inf),seat("软卧",tain_inf)])
	return title

def clickme():

    t.insert(1.0,tain(cli(e1.get(),e2.get(),year.get()+'-'+month.get()+'-'+day.get())))

def clearme():
    t.delete(1.0,END)

master=Tk() #生成root主窗口
Label(master,text='shekelin').grid(row=0,columnspan=3)
Label(master,text='起点').grid(row=1,sticky=E)
Label(master,text='终点').grid(row=2,sticky=E)


e1=Entry(master)
e1.grid(row=1,column=1,sticky=W)

e2=Entry(master)
e2.grid(row=2,column=1,sticky=W)

t=Text(master,width=150)
t.grid(row=4,columnspan=3)



Button(master,text='查询',command=clickme).grid(row=1,column=2)
Button(master,text='清空',command=clearme).grid(row=2,column=2)

number_year=StringVar(master)
number_year.set("2017")
year=ttk.Combobox(master,width=12,textvariable=number_year,values=["2016","2017"])
year.grid(row=3,column=0)
number_month=StringVar(master)
number_month.set("01")
month=ttk.Combobox(master,width=12,textvariable=number_month,values=['01','02','03','04','05','06','07','08','09','10','11','12'])
month.grid(row=3,column=1)
number_day=StringVar(master)
number_day.set("01")
day=ttk.Combobox(master,width=12,textvariable=number_day,values=['01','02','03','04','05','06','07','08','09','10','11','12']+list(range(13,32)))
day.grid(row=3,column=2)



master.mainloop() 

#if __name__ == '__main__':
#   print(tain(cli()))