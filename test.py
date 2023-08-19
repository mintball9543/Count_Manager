import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import csv
import os

file = "C:\count manager"

def add_data():
    global file_path
       
    try:
        code = int(e_code.get())
        name = e_name.get()
        phone = e_phone_num.get()
        count = e_amount.get()
        
    except ValueError:
        tk.messagebox.showerror("오류","품번은 숫자만 입력할 수 있습니다.")
        return
    except:
        tk.messagebox.showerror("오류","데이터가 입력되지 않았습니다.")
        return
    
    os.makedirs(file, exist_ok = True)

    with open(file+"\project.csv","a",encoding="utf-8",newline='') as f:
        data = csv.writer(f)
        data.writerow([code,name,phone,count,file_path])
        tk.messagebox.showinfo("확인","데이터가 입력되었습니다.")

    file_path = None
    image_set()
    clear_entry()

def search_data():
    global file_path
    
    code = e_code.get()
    chk = False
    with open(file+"\project.csv","r",encoding="utf-8",newline='') as f:
        data = csv.reader(f)
        
        for row in data:
            if row[0] == code:
                e_name.insert(0,row[1])
                e_phone_num.insert(0,row[2])
                e_amount.insert(0,row[3])
                file_path = row[4]
                image_input()
                chk = True
                break

        if not chk:
            tk.messagebox.showerror("에러","검색 결과를 찾을 수 없습니다.")

        chk = False
        
def clear_entry():
    """
    엔트리 모두 삭제
    """
    e_code.delete(0,'end')
    e_amount.delete(0,'end')
    e_name.delete(0,'end')
    e_phone_num.delete(0,'end')

def image_set():
    """
    이미지 백지로 세팅
    """
    global img
    global canvas
    global file_path

    canvas = tk.Canvas(win,width=1000,height=600)
    canvas.place(x=30,y=155)
    img = None
    file_path = None

def image_input():
    """
    이미지 구현
    """
    global img
    global file_path
    global canvas
    
    if file_path == None:    
        file_path = filedialog.askopenfilename()
    img = Image.open(file_path)
    img = ImageTk.PhotoImage(img)
    canvas.create_image(0,0,anchor=tk.NW,image = img)


#pillow 쓰지 않았을 시 (이미지 첨부가 잘 안됨)
"""
    img = ImageTk.PhotoImage(file=file_path)
    canvas.create_image(20,20,anchor=NW,image = img)
"""

#메인부분
win = tk.Tk()

win.title("재고관리 프로그램")
win.geometry("1000x800+400+200")
win.resizable(True,True)
image_set()
header = ["품번","고객 이름","고객 전화번호","수량"]

for i in range(len(header)):
    l = tk.Label(win,text = header[i])
    l.grid(row=0,column=i*2)

for i in range(1,6,2):
    blank = tk.Label(win)
    blank.grid(row=1,column=i)

#엔트리 구현
e_code = tk.Entry(win,width = 20)
e_code.grid(row=1,column=0)

e_name = tk.Entry(win,width = 20)
e_name.grid(row=1,column=2)

e_phone_num = tk.Entry(win,width = 20)
e_phone_num.grid(row=1,column=4)

e_amount = tk.Entry(win,width = 5)
e_amount.grid(row=1,column=6)

#버튼 구현
add = tk.Button(win,text="추가",command = add_data)
add.grid(row=1,column=50)

search = tk.Button(win,text="검색",command = search_data)
search.grid(row=1,column=51)

image = tk.Button(win, text="사진 등록", command = image_input)
image.place(x=30,y=100)



win.mainloop()

