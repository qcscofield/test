# -*- coding:utf-8 -*-

import xlsxwriter
import xlrd
import re
from tkinter import *
from tkinter.filedialog import askopenfilename

workbook = xlsxwriter.Workbook('init_data.xlsx')
worksheet = workbook.add_worksheet(name = 'init_data')
work_list = []

def get_data(filename):
    with open(filename) as f:
        #if 'PID' in f.readline():
        #    title = f.readline().split()
        #    break
        row = 0
        for line in f.readlines():
            list_line = line.split()
            col = 0
            for element in list_line:
                worksheet.write(row,col,element)
                col += 1
            row += 1
    workbook.close()
    print_pic()



def get_stru():
    data = xlrd.open_workbook('init_data.xlsx')
    table = data.sheet_by_name(u'init_data')
    nrows = table.nrows
    ncols = table.ncols
    pattern = re.compile(r'\d{2}-\d{2}-\d{2}_\d{2}:{1}\d{2}:{1}\d{2}')
    time_index = []
    for row in range(nrows):
        for col in range(ncols):
            if pattern.match(table.cell(row,col).value):
                time_index.append({row:table.cell(row,col).value})


    for row in range(nrows):
        for col in range(ncols):
            if pattern.match(table.cell(row,col).value):
                title = table.row_values(row+1)
                process_index = title.index('cmdline')
                get_it = True
        if get_it:
            break
    return title,process_index,time_index,data,table

def dataset():
    key_values = get_stru()
    title = key_values[0]
    process_index = key_values[1]
    time_index = key_values[2]
    data = key_values[3]
    table = key_values[4]
    pattern_num = re.compile(r'\d\+')

    for i in range(len(time_index)-1):
        content_row1 = list(time_index[i].keys())[0]+2
        content_row2 = list(time_index[i+1].keys())[0]-5
        for j in range(content_row1,content_row2):
            process_name = table.cell(j,process_index).value
            li = []
            for k in table.row_values(j)[:9]:
                li.append(int(k.split('K')[0]))
            li.append(table.row_values(j)[9])
            time_data = {list(time_index[i].values())[0]:li}
            if process_name not in work_list:
                work_list.append(process_name)
                work_list.append([time_data])
            else:
                work_list[work_list.index(process_name)+1].append(time_data)
    return work_list,title

def print_pic():
    key_values = dataset()
    work_list = key_values[0]
    title = key_values[1]
    workbook = xlsxwriter.Workbook('Process_Dashboard.xlsx')
    worksheet = workbook.add_worksheet(name = 'Dashboard')
    worksheet2 = workbook.add_worksheet(name = 'Chart')
    row = 0
    init_row = 0
    chart2_row = 0
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
    for i in range(0,len(work_list),2):
        print(work_list[i])

        init_row += row
        col = 1
        for title_name in title:
            worksheet.set_row(init_row,18,format_title)
            worksheet.write(init_row,col,title_name)

            col += 1
        row = 1
        for element0 in work_list[i+1]:
            col = 0
            worksheet.set_column('A:A',18,format_content)
            worksheet.write(init_row+row,col,list(element0.keys())[0])
            for element1 in list(element0.values())[0]:
                worksheet.write(init_row+row,col+1,element1)
                col += 1
            row += 1
        process_name = list(element0.values())[0][-1]
        #chart1
        '''chart = workbook.add_chart({'type':'line'})
        chart.add_series({'name':      ['Dashboard',init_row,3],
                          'categories':['Dashboard',init_row+1,0,init_row+row-1,0],
                          'values':    ['Dashboard',init_row+1,3,init_row+row-1,3],
                          'line':      {'width': 2.0}})
        chart.add_series({'name':      ['Dashboard',init_row,4],
                          'categories':['Dashboard',init_row+1,0,init_row+row-1,0],
                          'values':    ['Dashboard',init_row+1,4,init_row+row-1,4]})
        chart.add_series({'name':      ['Dashboard',init_row,5],
                          'categories':['Dashboard',init_row+1,0,init_row+row-1,0],
                          'values':    ['Dashboard',init_row+1,5,init_row+row-1,5]})
        chart.add_series({'name':      ['Dashboard',init_row,6],
                          'categories':['Dashboard',init_row+1,0,init_row+row-1,0],
                          'values':    ['Dashboard',init_row+1,6,init_row+row-1,6]})
        chart.add_series({'name':      ['Dashboard',init_row,7],
                          'categories':['Dashboard',init_row+1,0,init_row+row-1,0],
                          'values':    ['Dashboard',init_row+1,7,init_row+row-1,7]})
        chart.add_series({'name':      ['Dashboard',init_row,8],
                          'categories':['Dashboard',init_row+1,0,init_row+row-1,0],
                          'values':    ['Dashboard',init_row+1,8,init_row+row-1,8]})
        chart.add_series({'name':      ['Dashboard',init_row,9],
                          'categories':['Dashboard',init_row+1,0,init_row+row-1,0],
                          'values':    ['Dashboard',init_row+1,9,init_row+row-1,9]})
        chart.set_title ({'name': process_name})
        chart.set_x_axis({'name': 'Time'})
        chart.set_y_axis({'name': 'Value(KB)'})
        chart.set_style(10)
        worksheet.insert_chart(init_row+2,11, chart)'''

        #chart2
        chart2 = workbook.add_chart({'type':'line'})
        chart2.add_series({'name':      ['Dashboard',init_row,3],
                          'categories':['Dashboard',init_row+1,0,init_row+row-1,0],
                          'values':    ['Dashboard',init_row+1,3,init_row+row-1,3],
                           'line':      {'width': 2.0}})
        chart2.add_series({'name':      ['Dashboard',init_row,4],
                          'categories':['Dashboard',init_row+1,0,init_row+row-1,0],
                          'values':    ['Dashboard',init_row+1,4,init_row+row-1,4],
                           'line':      {'width': 2.0}})
        chart2.add_series({'name':      ['Dashboard',init_row,5],
                          'categories':['Dashboard',init_row+1,0,init_row+row-1,0],
                          'values':    ['Dashboard',init_row+1,5,init_row+row-1,5],
                           'line':      {'width': 2.0}})
        chart2.add_series({'name':      ['Dashboard',init_row,6],
                          'categories':['Dashboard',init_row+1,0,init_row+row-1,0],
                          'values':    ['Dashboard',init_row+1,6,init_row+row-1,6],
                           'line':      {'width': 2.0}})
        chart2.add_series({'name':      ['Dashboard',init_row,7],
                          'categories':['Dashboard',init_row+1,0,init_row+row-1,0],
                          'values':    ['Dashboard',init_row+1,7,init_row+row-1,7],
                           'line':      {'width': 2.0}})
        chart2.add_series({'name':      ['Dashboard',init_row,8],
                          'categories':['Dashboard',init_row+1,0,init_row+row-1,0],
                          'values':    ['Dashboard',init_row+1,8,init_row+row-1,8],
                           'line':      {'width': 2.0}})
        chart2.add_series({'name':      ['Dashboard',init_row,9],
                          'categories':['Dashboard',init_row+1,0,init_row+row-1,0],
                          'values':    ['Dashboard',init_row+1,9,init_row+row-1,9],
                           'line':      {'width': 2.0}})
        chart2.set_title ({'name': process_name})
        chart2.set_x_axis({'name': 'Time'})
        chart2.set_y_axis({'name': 'Value(KB)'})
        chart2.set_style(10)
        chart2.set_size({'width': 1600, 'height': 900})
        worksheet2.set_row(chart2_row,18,format_title)
        worksheet2.write(chart2_row,12,process_name)
        worksheet2.insert_chart(chart2_row+1,0, chart2)
        chart2_row += 50
    workbook.close()



def selectPath():
    path_ = askopenfilename()
    file_path.set(path_)

def clickme():
    if get_data(e1.get()) != 1:
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











