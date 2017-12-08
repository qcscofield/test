# -*- coding:utf-8 -*-

import xlsxwriter
import re
import numpy
from tkinter import *
from tkinter.filedialog import askopenfilename


pattern_time = re.compile(r'\d{2}-\d{2}-\d{2}_\d{2}:{1}\d{2}:{1}\d{2}')
pattern_MemTotal = re.compile(r'MemTotal')
pattern_MemFree = re.compile(r'MemFree')
pattern_Buffers = re.compile(r'Buffers')
pattern_Cached = re.compile(r'Cached')

def judges(keykeyword,content,liste,time_input):
    if keykeyword.match(content) and time_input:
        content = content.strip()
        return liste.append(content)
    elif keykeyword.match(content):
        content = int(re.findall(r'\d+',content)[0])
        return liste.append(content)

def get_data(file_name):
    time_stamp = []
    MemTotal_List = []
    MemFree_List = []
    Buffers_List = []
    Cached_List = []
    with open(file_name) as f:
        for line in f.readlines():
            judges(pattern_time,line,time_stamp,time_input = True)
            judges(pattern_MemTotal,line,MemTotal_List,time_input = False)
            judges(pattern_MemFree,line,MemFree_List,time_input = False)
            judges(pattern_Buffers,line,Buffers_List,time_input = False)
            judges(pattern_Cached,line,Cached_List,time_input = False)
    numpy_MemFree = numpy.array(MemFree_List)
    numpy_Cached = numpy.array(Cached_List)
    numpy_Buffers = numpy.array(Buffers_List)
    MemFree_Cached = numpy_MemFree + numpy_Cached
    MemFree_Cached_Buffers = numpy_MemFree + numpy_Cached + numpy_Buffers
    global MemTotal_num
    MemTotal_num = MemTotal_List[0]

    return time_stamp,MemTotal_List,MemFree_List,Buffers_List,Cached_List,MemFree_Cached,MemFree_Cached_Buffers

def write_chart(*datas):
    workbook = xlsxwriter.Workbook('Meminfo.xlsx')
    worksheet = workbook.add_worksheet(name = 'Meminfo')
    titles = ['time_stamp','MemTotal','MemFree','Buffers','Cached','MemFree+Cached','MemFree+Cached+Buffers']
    col = 0
    format_title = workbook.add_format({'fg_color':'#0066CC',\
                                        'font_color':'#FFFFFF',\
                                        'align':'center',\
                                        'valign':'vcenter',\
                                        'bold':True})
    format_content = workbook.add_format({'fg_color':'#FFFFCC',\
                                          'align':'left',\
                                          'valign':'vcenter',\
                                          'border':1,\
                                          'border_color':'#696969'})
    format_content.set_text_wrap()
    worksheet.set_row(0,18,format_title)
    worksheet.set_column('A:A',18,format_content)
    worksheet.set_column('F:F',18)
    worksheet.set_column('G:G',25)
    for title in titles:
        worksheet.write(0,col,title)
        col += 1
    col = -1
    for data in datas[0]:
        row = 1
        col += 1
        for value in data:
            worksheet.write(row,col,value)
            row += 1
        count = row

    chart = workbook.add_chart({'type':'line'})
    chart.add_series({'name':      ['Meminfo',0,2],
                      'categories':['Meminfo',1,0,count-1,0],
                      'values':    ['Meminfo',1,2,count-1,2],
                      'line':      {'width': 2.0}})
    chart.add_series({'name':      ['Meminfo',0,5],
                      'categories':['Meminfo',1,0,count-1,0],
                      'values':    ['Meminfo',1,5,count-1,5],
                      'line':      {'width': 2.0}})
    chart.add_series({'name':      ['Meminfo',0,6],
                      'categories':['Meminfo',1,0,count-1,0],
                      'values':    ['Meminfo',1,6,count-1,6],
                      'line':      {'width': 2.0}})
    chart.set_title ({'name': 'MemTotal('+str(MemTotal_num)+'KB)'})
    chart.set_x_axis({'name': 'Time'})
    chart.set_y_axis({'name': 'Value(KB)'})
    chart.set_style(10)
    chart.set_size({'width': 1600, 'height': 900})
    worksheet.insert_chart(0,0, chart)

    chart2 = workbook.add_chart({'type':'line'})
    chart2.add_series({'name':      ['Meminfo',0,2],
                      'categories':['Meminfo',1,0,count-1,0],
                      'values':    ['Meminfo',1,2,count-1,2],
                      'line':      {'width': 2.0}})
    chart2.set_title ({'name': 'MemFree'})
    chart2.set_x_axis({'name': 'Time'})
    chart2.set_y_axis({'name': 'Value(KB)'})
    chart2.set_style(6)
    chart2.set_size({'width': 1600, 'height': 900})
    worksheet.insert_chart(50,0, chart2)
    workbook.close()

def main(file_name):
    write_chart(get_data(file_name))


def selectPath():
    path_ = askopenfilename()
    file_path.set(path_)

def clickme():
    if main(e1.get()) != 1:
        message = 'Success!!'
        t.insert(1.0,message)
    else:
        t.insert(1.0,'Fail!!')


root = Tk()
file_path = StringVar()
Label(root,text = "目标路径:").grid(row = 0, column = 0)
e1 = Entry(root, textvariable = file_path)
e1.grid(row = 0, column = 1)
Button(root, text = "选择文件", command = selectPath).grid(row = 0, column = 2)
Label(root,text = "运行结果:").grid(row = 1, column = 0)
t=Text(root,width=20,height=5)
t.grid(row=2,columnspan=3)
Button(root, text = "生成excel", command = clickme).grid(row = 1, column = 2)

root.mainloop()





