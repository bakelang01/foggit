# This Python file uses the following encoding: utf-8
# 作者：black_lang
# 创建时间：2022/5/19 21:59
# 文件名：root.py.py

"""
json文件中是老师的邮箱，要运行先更改json中的邮箱地址，不可乱来！
"""

"""
这个小程序用到了tkinter模块进行gui编写，用到了自动发邮箱的模块，也用到了处理表格的openpyxl模块，算是一次小综合的实践运用了
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename
import json
import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart  #  用于发送邮件的附件
import openpyxl as ex
import pandas as pd
import os
from openpyxl.styles import Font
import time
from tkinter.messagebox import showwarning,askyesno,showinfo


def smtplib_faunction(file, item):
    global data
    email = smtplib.SMTP(host='smtp.163.com', port=25, )
    #  host : 一般要指定。SMTP服务器主机，可以指定主机ip地址或域名，如 smtp.qq.com、smtp.163.com 等。
    #  port : 可选。host指定了就需要指定端口号，一般端口号为25，QQ邮箱的ssl端口为465。
    #   local_hostname : 可选。如果SMTP服务器设置在了本机上，就指定服务器地址为localhost。

    # step2: 登录smtp服务器
    from_mail = 'dwyzuzhibu@163.com'  # 发件人的邮箱地址
    mail_pass = 'WZWVJCYWAWTNAQHA'  # smtp服务授权码
    login_code = email.login(from_mail, mail_pass)  # 返回一个元组，包含登录状态码和登录结果。eg：(235, 'Authentication successful')

    # step3 : 发送邮件
    who = data["email_to"][item]  # 收件人邮箱地址
    msg=MIMEMultipart()   # 创建一个带附件的邮件
    t = time.strftime('%w', time.localtime()) # 确定周几
    if t == '0':
        t='周日'
    elif t == '1':
        t='周一'
    elif t == '2':
        t='周二'
    elif t == '3':
        t='周三'
    elif t == '4':
        t='周四'
    elif t == '5':
        t='周五'
    elif t == '6':
        t='周六'
    ti = time.strftime(f'（%m-%d，{t}）', time.localtime())
    zhwen = data["email_main"] % (item,ti)
    msg.attach(MIMEText(str(zhwen),'plain','utf-8')) #正文

    #构造附件
    path = './统计表分表/'+file
    att1=MIMEApplication(open(path,'rb').read())
    att1['Content_Type']='application/octet-stream'
    att1["Content-Disposition"] = f'attachment; filename="statistical_table.xlsx"'  # filename 是附件的文件名，可以自定义
    msg.attach(att1)

    msg['From'] = from_mail  # 邮件内容中的发送方
    msg['To'] = who  # 邮件内容中的接收方
    title = data["email_title"] % (file.replace('.xlsx',''),ti)
    msg['Subject'] = Header(title, 'utf-8')  # 邮件内容的标题
    try:
        email.sendmail(from_mail, who, msg.as_string())   #发送邮件
        email.quit()
        text.insert('end','send email successful!!!\n')
    except:
        text.insert('end','发送失败!\n')

def creat_excel(di,file):
    global data
    excels = [file.replace('.xlsx', '%s') % i for i in data["excels"]]
    text.insert('end',excels)
    data["excels"] = excels
    try:
        with open('./统计表分表/data.json','w',encoding='utf-8') as fp:
            json.dump(data,fp=fp,ensure_ascii=False)
    except:
        text.insert('end','没有对应json数据\n')

    for key,name in zip(di.keys(),excels):
        name = './统计表分表/'+name
        if os.path.exists(name):
            os.remove(name)
        df = pd.DataFrame()
        df.to_excel(name)
        wb = ex.load_workbook(name)
        sheet = wb.active

        sheet.append(['姓名', '班级'])
        bold_itatic_24_font = Font(name='等线', size=13,bold=True)
        sheet['A1'].font = bold_itatic_24_font
        sheet['B1'].font = bold_itatic_24_font
        for n in di[key]:
            sheet.append(n)
        sheet.column_dimensions['A'].width = 30
        sheet.column_dimensions['B'].width = 30
        wb.save(name)
        text.insert('end',name+' 生成成功！\n')

def pare_excel(file):
    global e
    try:
        wb = ex.load_workbook(file, data_only=True)
        sheet = wb.get_sheet_by_name("参与率")
        one_two = []
        three=[]
        four = []
        yan = []
        t=[] # 临时变量，用于存储上一个同学的班级，对比下一次班级，达到判断的目的
        for row in sheet.rows:
            if '计数' in row[0].value:
                t.append([row[0].value,row[1].value])
                text.insert('end',row[0].value+'\t'+str(row[1].value)+'\n')
                continue
            # 筛选18级，也就是大四的
            if '18' in row[1].value and '硕' not in row[1].value and '博' not in row[1].value:
                four.append([row[0].value,row[1].value])
                t=four
                continue
            # 筛选19级，也就是大三的
            if '19' in row[1].value and '硕' not in row[1].value and '博' not in row[1].value:
                three.append([row[0].value, row[1].value])
                t = three
                continue
            # 筛选20级，21级，也就是大一大二的
            if '20' in row[1].value or '21' in row[1].value  :
                if '硕' not in row[1].value and '博' not in row[1].value:
                    one_two.append([row[0].value, row[1].value])
                    t = one_two
                    continue
            # 筛选研究生的班级
            if '硕' in row[1].value or '博' in row[1].value:
                yan.append([row[0].value, row[1].value])
                t = yan
                continue
        di={
            'one_two':one_two,
            'three':three,
            'four':four,
            'yan':yan,
        }
        text.insert('end','分类完成！\n')
        # 生成表格
        file = file.rsplit(r'/')[-1]
        e = True
        creat_excel(di,file)
    except:
        text.insert('end','选择的文件错误>>\n\t可能是格式不对，或者空文件'
                          '\n\t请选择处理后的统计报表\n')
        e = False

    # print(
    #     '大一大二：\n',one_two,
    #     '\n大三\n',three,
    #     '\n大四\n',four,
    #     '\n研究生\n',yan,
    # )

def main():
    global text
    # with open('./统计表分表/data.json','r',encoding='utf-8') as f:
    #     data = json.load(f)
    global data
    global file_path
    global e


    # print(file_path.get())
    pare_excel(file_path.get())
    if e:
        con = askyesno(message='表格已生成，请检查表格准确性(检查后需要关闭文件)，再选择是否发送邮件...')
        if con:
            for file,who in zip(data["excels"],data["email_to"].keys()):
                smtplib_faunction(file,who)
                text.insert("end",f'{file}\n')
                text.insert('end',f'{who}\n')
        else:
            showinfo(message='已取消发送邮件')
            text.insert('end','发送取消\n')
    else:
        pass
    # 恢复json数据
    with open('./统计表分表/data.json', 'r', encoding='utf-8') as fp:
        excel = json.load(fp)
        ti = [
            "（大一和大二统计表）.xlsx",
            "（大三统计表）.xlsx",
            "（大四统计表）.xlsx",
            "（研究生统计表）.xlsx"
        ]
    excel['excels'] = ti
    with open('./统计表分表/data.json', 'w', encoding='utf-8') as fp:
        json.dump(excel, fp, ensure_ascii=False)
        text.insert('end', 'json recover\n')

def file_chose():
    global file_path
    file = askopenfilename(title='选择表格')
    text.insert('end',file)
    file_path.set(file)

if __name__ =='__main__':
    e=True
    root = tk.Tk()
    root.geometry('800x600+100+100')
    root.title('浪浪小面条')
    root.resizable(0, 0)

    # 文件选择
    file_path = tk.StringVar()
    file_path.set('excel文档')
    en = tk.Label(
        root,
        textvariable=file_path,
        font=('楷体', 13),
        width=30,
        height=4,
        # bg='green',
        anchor="w",
        justify="left",
        wraplength=500,
    )
    en.pack(anchor='n',pady=10)
    bu_file = tk.Button(
        root,
        text='文件选择',
        command=file_chose
    )
    bu_file.pack(anchor='n',pady=20)

    # 文本框
    text = tk.Text(
        root,
        height=20,
        width=20,
        bg='black',
        font=['宋体', 13],
        fg='white',
        insertbackground='white',
        relief='groove'
    )
    text.pack(side='bottom',fill='x')
    try:
        with open('./统计表分表/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        showwarning(
            message='没有检测到“./统计表分表/data.json”文件\n请创建好信息文件后再打开'
        )
        exit(0)
    main_bu = tk.Button(
        text='开始',
        command=main
    )
    main_bu.pack(anchor='n',pady=20)
    root.mainloop()
