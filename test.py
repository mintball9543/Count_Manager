import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import csv
import os
from tkcalendar import DateEntry
from datetime import date


file = "C:\count manager"
os.makedirs(file, exist_ok = True)

class ImageError(Exception):
    pass

#데이터 가져오기
def data_import():
    with open(file+"\project.csv","r",encoding="utf-8",newline='') as f:
        data = []
        for row in csv.reader(f):
            try:
                if row[5] != None: pass
            except: row.append(None)
            data.append(row)
        return data

#초기화
def data_all_delete():
    if os.path.isfile(file+"\project.csv") and tk.messagebox.askyesno("경고","기존 데이터가 전부 삭제됩니다. 정말 삭제하시겠습니까?"):
        os.remove(file+"\project.csv")
        entry_all_delete()
        tk.messagebox.showinfo("알림","기존 데이터 파일이 삭제되었습니다.")
    elif not os.path.isfile(file+"\project.csv"):
        tk.messagebox.showinfo("알림","기존 데이터 파일이 없습니다.")

#전체 데이터 목록 구현
def all_data():
    global new
    
    text = tk.Text(new,width=100,height=50)
    text.bind("<Key>", lambda a: "break")
    text.pack()
    text.insert("end","품번      고객 이름     고객 전화번호  수량\n\n")
    data = data_import()
    for row in data:
        for _ in range(4):
            row.pop()
        text.insert("end","       ".join(row))
        text.insert("end","\n")
    
#새로운 창
def new_window():
    global new
    new = tk.Toplevel(width=1000,height=500)
    new.geometry("900x600")
    all_data()

#데이터 편집
def data_edit():
    data = data_import()

    chk = False
    code = e_code.get()
    for idx in range(len(data)):
        if data[idx][0] == code:
            name = e_name.get()
            phone = e_phone_num.get()
            data[idx][3] = val.get()
            data[idx][4] = file_path
            data[idx][5] = text_memo.get(1.0,"end")
            money = e_money.get()
            data[idx][7] = str(e_date.get_date()).replace("-","/")
            if name == "" or phone == "": #고객명단 미입력시
                data[idx][1] = "Null"
                data[idx][2] = "Null"
            else:
                data[idx][1] = name
                data[idx][2] = phone

            if money == "":
                data[idx][6] = 0
            else:
                data[idx][6]
                
            entry_all_delete()
            chk = True
            break

    if not chk:
        tk.messagebox.showerror("에러","존재하지 않는 품번입니다.")
    else:
        if not tk.messagebox.askyesno("수정","정말 이대로 수정하시겠습니까?"): return
        with open(file+"\project.csv","w",encoding="utf-8",newline='') as f:
            data_csv = csv.writer(f)
            for row in data:
                data_csv.writerow(row)
            tk.messagebox.showinfo("확인","수정 완료!")

#데이터 삭제
def data_delete():
    data = data_import()

    chk = False
    code = e_code.get()
    for idx in range(len(data)):
        if data[idx][0] == code:
            del data[idx]
            entry_all_delete()
            chk = True
            break

    if not chk:
        tk.messagebox.showerror("에러","존재하지 않는 품번입니다.")
    else:
        if not tk.messagebox.askyesno("삭제","정말 삭제하시겠습니까?"): return
        with open(file+"\project.csv","w",encoding="utf-8",newline='') as f:
            data_csv = csv.writer(f)
            for row in data:
                data_csv.writerow(row)
            tk.messagebox.showinfo("확인","삭제 완료!")

#데이터 추가
def add_data():
    global file_path
    data = data_import()
    try:
        code = e_code.get()
        for row in data:
            if row[0] == code:
                tk.messagebox.showerror("오류","해당 품번은 이미 등록되어 있습니다.")
                return

        name = e_name.get()
        phone = e_phone_num.get()
        count = val.get()
        memo = text_memo.get(1.0,"end")
        money = e_money.get()
        date = str(e_date.get_date()).replace("-","/")
        if file_path == None: raise ImageError

    except ImageError:
        tk.messagebox.showerror("오류","이미지 등록 되어있지 않습니다.")
        return

    if name == "" or phone == "": #고객명단 미입력시
        name = "Null"
        phone = "Null"

    if money == "":
        money = 0

    with open(file+"\project.csv","a",encoding="utf-8",newline='') as f:
        data = csv.writer(f)
        data.writerow([code,name,phone,count,file_path,memo,money,date])
        tk.messagebox.showinfo("확인","데이터가 입력되었습니다.")

    file_path = None
    entry_all_delete()

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
                e_money.insert(0,row[6])
                e_date.set_date(row[7])
                if int(row[3]) == 1:
                    ch_sell.select()
                else:
                    ch_sell.deselect()
                file_path = row[4]
                image_input()
                try:
                    text_memo.insert("insert",row[5])
                    text_memo.delete('insert','end')
                except: pass
                chk = True
                break

        if not chk:
            tk.messagebox.showerror("에러","검색 결과를 찾을 수 없습니다.")

def entry_all_delete():
    """
    입력창 삭제
    """
    clear_entry()
    image_set()

def clear_entry():
    """
    엔트리 모두 삭제
    """
    e_code.delete(0,'end')
    ch_sell.deselect()
    e_name.delete(0,'end')
    e_phone_num.delete(0,'end')
    text_memo.delete(0.0,'end')
    e_money.delete(0,'end')
    e_date.set_date(date.today())

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
win.geometry("1400x900")
win.resizable(True,True)
image_set()
val = tk.IntVar()
header = ["품번","고객 이름","고객 전화번호","금액","판매여부"]

for i in range(len(header)):
    tk.Label(win,text = header[i], font = ("함초롬돋움",12,"bold")).grid(row=0,column=i*2)

for i in range(1,10,2):
    blank = tk.Label(win)
    blank.grid(row=1,column=i)

tk.Label(win,text="메모",font=("함초롬돋움",15,"bold")).place(x=750,y=130)

#엔트리 구현
e_code = tk.Entry(win,width = 15,font=("",15,""))
e_code.grid(row=1,column=0)

e_name = tk.Entry(win,width = 15,font=("",15,""))
e_name.grid(row=1,column=2)

e_phone_num = tk.Entry(win,width = 15,font=("",15,""))
e_phone_num.grid(row=1,column=4)

e_money = tk.Entry(win,width=10,font=("",15,""))
e_money.grid(row=1,column=6)
"""
e_amount = tk.Entry(win,width = 5,font=("",15,""))
e_amount.grid(row=1,column=6)
"""
#메모
text_memo = tk.Text(win,width=50,height = 33,font=("한초롬돋움",15,""))
text_memo.place(x=750 , y=155)

#판매여부 체크박스
ch_sell = tk.Checkbutton(win, variable=val)
ch_sell.grid(row=1,column=8)

#날짜
e_date = DateEntry(win, date_pattern='yyyy/MM/dd', firstweekday='sunday', width=12,
                   background='skyblue', foreground='white',borderwidth=4,font=("한초롬돋움",12,""))
e_date.grid(row=3,column=0)


#버튼 구현
tk.Button(win,text="저장", font=("함초롬돋움",12,"bold"),command = add_data).grid(row=1,column=50)
tk.Button(win,text="검색",font=("함초롬돋움",12,"bold"),command = search_data).grid(row=1,column=51)
tk.Button(win,text="전체 데이터",font=("함초롬돋움",12,"bold"),command = new_window).place(x=1230,y=25)
tk.Button(win, text="사진 등록", font=("함초롬돋움",12,"bold"),command = image_input).place(x=30,y=100)
tk.Button(win, text="취소", font=("함초롬돋움",12,"bold"),command = image_delete).place(x=120,y=100)
tk.Button(win, text="편집", font=("함초롬돋움",12,"bold"),command = data_edit).grid(row=1, column=52)
tk.Button(win, text="삭제", font=("함초롬돋움",12,"bold"),command = data_delete).grid(row=1, column=53)
tk.Button(win, text="입력창 삭제", font=("함초롬돋움",12,"bold"),command=entry_all_delete).place(x=1120,y=25)
tk.Button(win, text="초기화", font=("함초롬돋움",12,"bold"),command = data_all_delete).place(x=1340, y=25)

win.mainloop()
