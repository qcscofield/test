# -*- coding:UTF-8 -*-
# Author:qiuchen
# Date:2017-09-27

import linecache
import xlsxwriter
from tkinter import *
from tkinter.filedialog import askopenfilename




ANR_keyword = 'ANR in'
CRASH_keyword = '// CRASH'


def readfile(filename,keyword,rows):
    with open(filename,'r',encoding='UTF-8') as f:
        lines = enumerate(f)
        for num,line in lines:
            if keyword in line:
                yield num,line,linecache.getline(filename,num+2),linecache.getline(filename,num+3),\
                      tuple(linecache.getlines(filename)[num+4:num+rows])

def get_data(type,database):
    new_database = []
    temp = []
    temp_crash = []
    if type == 'ANR':
        for texts in list(database):
            if texts[1] not in temp:
                new_database.append(texts)
                temp.append(texts[1])
    if type == 'CRASH':
        for texts in list(database):
            texts = list(texts)
            if texts[1].split('(pid')[0] not in temp and texts[2] not in temp_crash:
                temp.append(texts[1])
                temp_crash.append(texts[2])
                texts[1] = texts[1].split(r'// ')[1]
                texts[2] = texts[2].split(r'// ')[1]
                texts[3] = texts[3].split(r'// ')[1]
                new_database.append(texts)
    return new_database

def init_excel(*type,**content):
    workbook = xlsxwriter.Workbook('monkeysyslog.xlsx')
    format_title = workbook.add_format({'fg_color':'#0066CC',\
                                        'font_color':'#FFFFFF',\
                                        'align':'center',\
                                        'valign':'vcenter',\
                                        'bold':True})
    format_content = workbook.add_format({'fg_color':'#FFFFCC',\
                                          'align':'left',\
                                          'valign':'vcenter',\
                                          'border':1,\
                                          'font_name':'Microsoft YaHei',\
                                          'border_color':'#696969'})
    format_content.set_text_wrap()
    if 'ANR' in type:
        worksheet = workbook.add_worksheet(name = 'ANR')
        worksheet.set_row(0,18,format_title)
        worksheet.set_column('A:A',40,format_content)
        worksheet.set_column('B:B',13,format_content)
        worksheet.set_column('C:C',60,format_content)
        worksheet.set_column('D:D',90,format_content)
        worksheet.write('A1','Name')
        worksheet.write('B1','PID')
        worksheet.write('C1','Reason')
        worksheet.write('D1','Detail Info')
        write_content(worksheet,content['content_anr'])
    if 'CRASH' in type:
        worksheet = workbook.add_worksheet(name = 'CRASH')
        worksheet.set_row(0,18,format_title)
        worksheet.set_column('A:A',40,format_content)
        worksheet.set_column('B:B',28,format_content)
        worksheet.set_column('C:C',68,format_content)
        worksheet.set_column('D:D',90,format_content)
        worksheet.write('A1','Name')
        worksheet.write('B1','Short MSG')
        worksheet.write('C1','Long MSG')
        worksheet.write('D1','Detail Info')
        write_content(worksheet,content['content_crash'])
    workbook.close()

def write_content(worksheet,content):
    row_num = 1
    for texts in content:
        col_num = 0
        for text in texts[1:]:
            if type(text) is type(('tuple',)):
                allline = ''
                for eachline in text:
                    allline += eachline
                worksheet.write(row_num,col_num,allline)
            else:
                worksheet.write(row_num,col_num,text)
            col_num += 1
        row_num += 1

def main(filename):
    try:
        ANR_info = get_data('ANR',readfile(filename,ANR_keyword,100))
        CRASH_info = get_data('CRASH',readfile(filename,CRASH_keyword,30))
        init_excel('ANR','CRASH',content_anr=ANR_info,content_crash=CRASH_info)
    except:
        return 1

def clickme():
    if main(e1.get()) != 1:
        t.insert(1.0,'Success!!')
    else:
        t.insert(1.0,'Fail!!')

def selectPath():
    path_ = askopenfilename()
    file_path.set(path_)

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
