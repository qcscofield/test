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
from docopt import docopt
import requests
import urllib.request
from prettytable import PrettyTable

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    from_station = urllib.request.quote(arguments['<from>'])
    to_station = urllib.request.quote(arguments['<to>'])
    date = urllib.request.quote(arguments['<date>'])
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
    #print(url)
    available_trains = r.json()["data"]["s2sBeanList"]
    return available_trains

def seat(seat_name,tain_inf):
	if tain_inf["seats"].get(seat_name):
		return '\n'.join(map(str,(tain_inf["seats"][seat_name]["count"],tain_inf["seats"][seat_name]["price"])))+'元'
	else:
		return "--"

def colored(color, text):
    table = {
        'red':'\033[91m',
        'green':'\033[92m',
        # no color
        'nc':'\033[0'
    }
    cv = table.get(color)
    nv = table.get('nc')
    return ''.join([cv, text, nv])


def tain(tains_inf):
	title = PrettyTable(["车次","车站","时间","历时","商务座(余票/价格)","一等座(余票/价格)","二等座(余票/价格)","动卧(余票/价格)","无座(余票/价格)","硬座(余票/价格)","硬卧(余票/价格)","软卧(余票/价格)"])
	title.align = "c"
	title.valign = "m"
	for tain_inf in tains_inf:
		title.add_row([tain_inf["trainNo"],'\n'.join([tain_inf["dptStationName"],tain_inf["arrStationName"]]),\
			'\n'.join([tain_inf["dptTime"],tain_inf["arrTime"]]),\
			str(int(tain_inf["lishiValue"])//60)+'小时'+str(int(tain_inf["lishiValue"])%60)+'分钟',\
			seat("商务座",tain_inf),seat("一等座",tain_inf),seat("二等座",tain_inf),seat("动卧",tain_inf),\
			seat("无座",tain_inf),seat("硬座",tain_inf),seat("硬卧",tain_inf),seat("软卧",tain_inf)])
	return title

if __name__ == '__main__':
    print(tain(cli()))