#  This Python file uses the following encoding: utf-8
import datetime
import os.path
import time
import tkinter as tk
import pygame as py
import random
import threading
import inspect
import ctypes
from PIL import Image,ImageTk


def love_time_01():

    '''
    计算时间的函数
    '''

    last = datetime.datetime(2019, 12, 4, 20, 00)  # 高二的那天晚上
    now = datetime.datetime.now()  # 现在的时间
    cha = now - last
    day = cha.days  # 得到天数
    data_list = str(cha).split(' ')[-1].split(':')  # 将cha拆分，获得小时，分钟和秒
    hour = int(data_list[0]) + day * 24  # 总小时
    minter = int(data_list[1]) + hour * 60  # 总分钟
    ms = minter * 60 + float(data_list[2])  # 总秒速
    data = f'{day}天{data_list[0]}小时{data_list[1]}分钟{data_list[2]}秒' # 整合时间
    times = {
        'day': day,
        'hour': hour,
        'minter': minter,
        'ms': ms,
        'data': data,
    }
    return times  # 返回整理好的时间字典

def love_hua():  #设置动态的浪漫的语句，显示在界面
    pass

def love_music():
    musics = os.listdir(r'./data/music')
    global music
    py.mixer.init()
    time.sleep(5)
    while True:  # 达到循环播放的效果
            if not py.mixer.music.get_busy():  # 检测声卡是否被占用，意思就是看看有没有再播放的音乐
                music = random.choice(musics)
                py.mixer.music.load(rf'.\data\music\{music}')
                py.mixer.music.play(1, 1)
                py.mixer.fadeout(2000)
            else:
                time.sleep(1)

def change_shi():
    with open('./data/诗句.txt', 'r', encoding='utf-8') as f:
        shi=random.choice(f.readlines()).split(',')
        var06.set(shi[0])
        var07.set(shi[1])


def love_time():
    '''
    主要的浮窗控间
    显示时间窗口
    '''

    #窗口属性设置
    root_love=tk.Tk()
    root_love.title('依 · 恋 · 忆')
    root_love.geometry('670x390+350+100')
    root_love['bg']='white'
    root_love.resizable(0, 0)
    
    #设置参数
    color='white'
    #下面是关于lable标签的一些显示
    times=love_time_01()
    la1=tk.Label(root_love,text='浮世三千，吾爱有三：日，月，与卿\n日为朝\n月为暮\n卿为朝朝暮暮',justify='left',bg=color,font=('楷体',15))
    la1['fg']='darkblue'
    la1.place(x=20,y=20)
    la2=tk.Label(root_love,text='愿岁月静好，浅笑安然，一切美好如约而至。\n',bg=color,font=('楷体',15))
    la2.place(x=20,y=120)
    la2['fg']='darkblue'
    la3=tk.Label(root_love, text='我们一起经历了：', bg=color, font=('楷体', 15))
    la3.place(x=20,y=155)
    la3['fg']='blue'
    var01 = tk.StringVar()
    var01.set(value=f'共计{times["day"]}天  {times["hour"]}小时  {times["minter"]}分钟  {times["ms"]}秒！')
    lb4=tk.Label(root_love, textvariable=var01, bg=color, font=('algerian', 18))
    lb4.place(x=20,y=180)
    lb4['fg']='deepskyblue'
    lb5 = tk.Label(root_love, text='到现在，我们走过了', bg=color, font=('楷体', 16))
    lb5['fg']='red'
    lb5.place(x=20,y=240)
    var05 = tk.StringVar()
    var05.set(value=f"{times['data']}")
    lb6 = tk.Label(root_love, textvariable=var05, bg=color, justify='left',font=('algerian', 21))
    lb6.place(x=230,y=230)
    lb6['fg']='orangered'
    
    im = Image.open('./data/lang_yi.jpg').resize((100, 100))
    img = ImageTk.PhotoImage(im)
    lb8=tk.Button(root_love,image=img)
    lb8.place(x=480,y=50)

    global var06
    global var07
    var06=tk.StringVar()
    var07=tk.StringVar()
    with open('./data/诗句.txt','r',encoding='utf-8') as f:
        shi=random.choice(f.readlines()).split(',')
        var06.set(shi[0])
        lb7=tk.Label(root_love, textvariable=var06, bg=color, justify='center',font=('楷体', 18))
        var07.set(shi[1])
        lb8 = tk.Button(root_love, textvariable=var07, bg=color, font=('楷体', 16),justify='center',command=change_shi)
        lb8.place(x=190,y=330)
        lb8['fg']='black'
        lb7.place(x=50,y=290)
    var_music = tk.StringVar()
    var_music.set(music)
    bu_music = tk.Label(root_love, textvariable=var_music, bg=color,fg='black')
    bu_music.place(x=500,y=20)
    while True :
        # 实现动态加载数据
        root_love.update()  # 不断进行更新
        root_love.after(1000)  # 更新间隔时间1秒
        times = love_time_01()
        var_music.set(music[:-4])
        var01.set(value=f'共计{times["day"]}天  {times["hour"]}小时  {times["minter"]}分钟  {times["ms"]}秒！')
        var05.set(value=f"{times['data']}")
        try:   # 赋值状态码，如果报错，就推出，达到关闭线程的目的
            a=root_love.state()
        except:
            break




def _async_raise(tid, exctype):   #停止线程
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
def stop_thread(thread):  #停止线程
    _async_raise(thread.ident, SystemExit)

if __name__ == '__main__':
    '''
    创建多线程的方式，同时播放音乐和显示窗口
    '''
    music = 'music    '
    th_music = threading.Thread(target=love_music)
    th_time=threading.Thread(target=love_time)
    th_time.start()
    th_music.start()
    th_time.join()
    statue=th_time.is_alive()   #获取窗口线程的状态
    if  statue== False:   #当窗口关闭时，同时也关闭音乐线程
            stop_thread(th_music)
            th_music.join()




