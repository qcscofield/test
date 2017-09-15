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
    print(r.status_code)
    print(url)
    available_trains = r.json()["data"]
    print(available_trains)

if __name__ == '__main__':
    cli()