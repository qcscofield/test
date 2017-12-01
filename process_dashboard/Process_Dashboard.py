# -*- coding:utf-8 -*-

import xlsxwriter
import xlrd
import re

workbook = xlsxwriter.Workbook('Process_Dashboard.xlsx')
worksheet = workbook.add_worksheet('init_data')
work_list = []

def get_data():
    with open('procrank.txt') as f:
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
    dataset()
    workbook.close()

def get_stru():
    data = xlrd.open_workbook('Process_Dashboard.xlsx')
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

    for i in range(len(time_index)-1):
        content_row1 = list(time_index[i].keys())[0]+2
        content_row2 = list(time_index[i+1].keys())[0]-5
        for j in range(content_row1,content_row2):
            process_name = table.cell(j,process_index).value
            time_data = {list(time_index[i].values())[0]:table.row_values(j)}
            if process_name not in work_list:
                work_list.append(process_name)
                work_list.append([time_data])
            else:
                work_list[work_list.index(process_name)+1].append(time_data)
    print(work_list)





get_data()











