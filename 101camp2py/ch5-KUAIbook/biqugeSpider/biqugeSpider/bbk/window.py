from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import os
import sys
import random

BOOK = ''
search_ety = None

WIDTH = 800
HEIGHT = 600

BUTTON_x = 530
BUTTON_y = 205

ENTRY_x = 150
ENTRY_y = 210
ENTRY_width = 30

txt_HEIGHT = 10

font_style = 'Calibri 18 bold'

def create_window():
    window = Tk()
    window.title('Welcome to BITEBOOK - by RIS - 101camp2py')
    # 禁止拉伸窗口大小
    window.resizable(height=False, width=False)
    window.geometry('800x600')
    canvas = Canvas(window, bg='white', height=HEIGHT, width=WIDTH)
    canvas.place(x=0, y=0)
    pic = ['blue_min.gif', 'pic2.gif', 'pic.gif']
    image_bg = PhotoImage(file=random.choice(pic))
    canvas.create_image(0, 0, anchor='nw', image=image_bg)

    lab = Label(window,
                text='Bite\nBook\n\n渣耀队',  # 标签的文字
                bg='lightgray',  # 背景颜色
                font=('consolas 16'),  # 字体和字体大小
                width=5, height=8,  # 标签长宽
                justify='center',  # 文本居中
                borderwidth=0
                ).place(x=2, y=20)

    global search_ety
    search_ety = Entry(window,
                            bg='white',
                            justify='center',
                            font=font_style,
                            bd=5,
                            show=None,
                            width=ENTRY_width)

    search_ety.place(x=ENTRY_x, y=ENTRY_y)
    search_ety.insert(50, '请输入你要下载的小说名')

    while True:
        search_btn = Button(window,
                            text="搜 索",
                            bg='white',
                            justify='center',
                            font=font_style,
                            command=click_search).place(x=BUTTON_x, y=BUTTON_y)
        mainloop()


def click_search():
    global search_ety
    global BOOK
    BOOK = search_ety.get()
    print('*' + BOOK + '*')
    if len(BOOK) > 0 and BOOK.isspace() is False and BOOK != '请输入你要下载的小说名':
        current_path = sys.path
        os.chdir(current_path[0])
        print('*'+BOOK)
        os.popen('scrapy crawl biquge')
        print('*'+BOOK)
        tkinter.messagebox.showwarning('警告', '小说正在下载中...请勿瞎**点')
    else:
        tkinter.messagebox.showinfo('提示', '请输入正确的小说名')


if __name__ == '__main__':
    create_window()
