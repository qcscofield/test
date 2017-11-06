# -*- coding: utf-8 -*-

#导入os模块，askdirectory是获取文件夹路径的函数
import os
from tkinter import *
from tkinter.filedialog import askdirectory


def main(work_dir,old_suffix,new_suffix):
    os.chdir(work_dir)
    for file_name in os.listdir():
        prefix_name=file_name[::-1].split('.',1)[1][::-1]
        suffix_name=file_name[::-1].split('.',1)[0][::-1]
        new_filename=prefix_name+'.'+new_suffix
        if suffix_name == old_suffix:
            os.rename(file_name,new_filename)
#选择文件路径
def selectPath():
    path_ = askdirectory()
    file_path.set(path_)
#触发按钮
def clickme():
    main(e1.get(),e2.get(),e3.get())

root = Tk()
file_path = StringVar()
#获取文件所在路径
Label(root,text = "工作目录:").grid(row = 0, column = 0)
e1 = Entry(root, textvariable = file_path)
e1.grid(row = 0, column = 1)
Button(root, text = "选择目录", command = selectPath).grid(row = 0, column = 2)
#需要修改的后缀
Label(root,text = "原后缀:").grid(row = 1, column = 0)
e2 = Entry(root)
e2.grid(row = 1,column = 1)
#目标后缀
Label(root,text = "目标后缀:").grid(row = 2, column = 0)
e3 = Entry(root)
e3.grid(row = 2,column = 1)
#运行按钮
Button(root,text = "运行",command = clickme).grid(row = 3,column = 1)

root.mainloop()


