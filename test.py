import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import csv
import os

file = "C:\count manager"
os.makedirs(file, exist_ok = True)

class ImageError(Exception):
    pass

#전체 데이터 목록 구현
def all_data():
    global new
    
    text = tk.Text(new,width=100,height=50)
    text.bind("<Key>", lambda a: "break")
    text.pack()
    
    with open(file+"\project.csv","r",encoding="utf-8",newline='') as f:
        data = csv.reader(f)
        text.insert("end","품번      고객 이름     고객 전화번호  수량\n\n")
        for row in data:
            row.pop()
            text.insert("end","       ".join(row))
            text.insert("end","\n")
    
#새로운 창
def new_window():
    global new
    new = tk.Toplevel(width=1000,height=500)
    new.geometry("900x600+600+300")
    all_data()

#데이터 추가
def add_data():
    global file_path
       
    try:
        code = int(e_code.get())
        name = e_name.get()
        phone = e_phone_num.get()
        count = e_amount.get()
        if file_path == None: raise ImageError
    except ValueError:
        tk.messagebox.showerror("오류","품번은 숫자만 입력할 수 있습니다.")
        return
    except ImageError:
        tk.messagebox.showerror("오류","이미지 등록 되어있지 않습니다.")
        return
    except:
        tk.messagebox.showerror("오류","데이터가 입력되지 않았습니다.")
        return
    


    with open(file+"\project.csv","a",encoding="utf-8",newline='') as f:
        data = csv.writer(f)
        data.writerow([code,name,phone,count,file_path])
        tk.messagebox.showinfo("확인","데이터가 입력되었습니다.")

    file_path = None
    image_set()
    clear_entry()

#데이터 검색
def search_data():
    global file_path
    
    code = e_code.get()
    chk = False
    with open(file+"\project.csv","r",encoding="utf-8",newline='') as f:
        data = csv.reader(f)
        
        for row in data:
            if row[0] == code:
                clear_entry()
                image_set()
                e_code.insert(0,row[0])
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

    canvas = tk.Canvas(win,width=700,height=600)
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
        file_path = filedialog.askopenfilename(filetypes=[("이미지 파일","*.jpg;*.jpeg;*.png")])

    img = Image.open(file_path)
    img = ImageTk.PhotoImage(img)
    canvas.create_image(0,0,anchor=tk.NW,image = img)

#이미지 등록 취소
def image_delete():
    global file_path

    file_path = None
    image_set()

#pillow 쓰지 않았을 시 (이미지 첨부가 잘 안됨)
"""
    img = ImageTk.PhotoImage(file=file_path)
    canvas.create_image(20,20,anchor=NW,image = img)
"""

#메인부분
win = tk.Tk()

win.title("재고관리 프로그램")
win.geometry("1400x900+400+200")
win.resizable(True,True)
image_set()
header = ["품번","고객 이름","고객 전화번호","수량"]

for i in range(len(header)):
    l = tk.Label(win,text = header[i])
    l.grid(row=0,column=i*2)

for i in range(1,10,2):
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

#메모 기능구현 x
text_memo = tk.Text(win,width=50,height = 33,font=("",15,""))
text_memo.place(x=750 , y=155)

#버튼 구현
add = tk.Button(win,text="추가",command = add_data)
add.grid(row=1,column=50)

search = tk.Button(win,text="검색",command = search_data)
search.grid(row=1,column=51)

all_button = tk.Button(win,text="전체 데이터",command = new_window)
all_button.grid(row=1,column=52)

image = tk.Button(win, text="사진 등록", command = image_input)
image.place(x=30,y=100)

image_cancel = tk.Button(win, text="취소", command = image_delete)
image_cancel.place(x=100,y=100)





win.mainloop()

