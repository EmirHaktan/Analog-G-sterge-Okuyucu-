#!/usr/bin/env python
# coding: utf-8

# In[3]:


import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from tkinter import*
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import ImageTk
from tkinter import Tk 
from tkinter import Label 
import time
import sys
from tkinter import messagebox
from skimage.morphology import skeletonize
import math 




# In[4]:


my_w = tk.Tk()
my_w.geometry("1000x700")
my_w.title("Gösterge seviyesi algılama programı")
my_font1=('times', 20, 'bold')
l1 = tk.Label(my_w,text="Yapımcılar:\n Metehan Yıldız\n Emir Haktan Ünal \n\n\n ⏰Lütfen Göstergenin Fotoğrafını Yükleyin⏰ \n ⏬⏬⏬⏬⏬⏬ "
              ,width=48,height=10,font=my_font1,fg="black")
l1.grid(row=1,column=1)

my_label=Label(my_w,text="",font=("Helvetica",48),fg="green")
my_label.grid(row=0,column=1)

clock = tk.Button(my_w, text="Saat ⏳",font=("Helvetica",10), fg="green",
   width=20, height=5, command = lambda:clock())
clock.grid(row=0,column=0)

b1 = tk.Button(my_w, text='Resim yükle',fg="brown", font=("times",12,"bold"),
   width=20, height=5,command = lambda:upload_file())
b1.grid(row=2,column=1) 

def upload_file():
    global img
    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = ImageTk.PhotoImage(file=filename)
    b2 =tk.Button(my_w,image=img) 
    b2.grid(row=3,column=1)
    img=cv2.imread(filename)
    cv2.imshow("merhaba",img)
    hh, ww = img.shape[:2]
    # Griye çevirme işlemi
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # threshold
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    # siyah zemin üzerine beyaz olacak şekilde tersine çevirmek
    thresh = 255 - thresh

    # Kontur oluşturma ve oluşan alanı koruma 
    cntrs_info = []
    contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    index=0
    for cntr in contours:
        area = cv2.contourArea(cntr)
        cntrs_info.append((index,area))
        index = index + 1

    # kontuları alana göre sıralama 
    def takeSecond(elem):
        return elem[1]
    cntrs_info.sort(key=takeSecond, reverse=True)

    # en büyük 3 konturu almak 
    arms = np.zeros_like(thresh)
    index_third = cntrs_info[2][0]
    cv2.drawContours(arms,[contours[index_third]],0,(1),-1)

    #armların inceliğini ayarlamak 
    arms_thin = skeletonize(arms)
    arms_thin = (255*arms_thin).clip(0,255).astype(np.uint8)

    # bir hough line çekmek ve görseli kopyalama işlemi 
    result = img.copy()
    lineThresh = 70
    minLineLength = 50
    maxLineGap = 70
    max
    lines = cv2.HoughLinesP(arms_thin, 1, np.pi/180, lineThresh, None, minLineLength, maxLineGap)
    
    for [line] in lines:
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]
        cv2.line(result, (x1,y1), (x2,y2), (0,0,255), 2)
        print(x1,x2,y1,y2)
    width, height = 800, 600
    x3, y3 = 0, y2
    x4, y4 =x2, y2
    line_thickness = 2
    cv2.line(result, (x3, y3), (x4, y4), (0, 255, 0), thickness=line_thickness)
    points_list=[]  
    slope1= (y2-y1) / (x2-x1)
    slope2= (y2-y3) / (x2-x3)
    tan_alfa = abs((slope1-slope2) / (1 + slope1*slope2)) 
    radyan_angle = math.atan(tan_alfa)
    angle = round(math.degrees(radyan_angle))
    print("acı",angle)
    if angle<50:
        messagebox.showwarning("Bilgi:",f"Gösterge derecesi: {angle} \t Göstergeniz düşük seviyededir.")
    elif 120>angle>=50:
        messagebox.showinfo("Bilgi:",f"Gösterge derecesi: {angle} \t Göstergeniz normal seviyededir.")
    else:
        messagebox.showwarning("Uyarı",f"Gösterge derecesi: {angle} \t Göstergeniz yüksek seviyededir")
    
    while True:
        cv2.imshow("sonuc",result)
        
        if cv2.waitKey() == 27:
            break
        else:
            cv2.waitKey()
            cv2.destroyAllWindows()
        
       
       

counter=0          
def clock():
    hour=time.strftime("%I")
    minute=time.strftime("%M")
    second=time.strftime("%S")
    day=time.strftime("%A")
    my_label.config(text= day+":"+hour+":"+minute+":"+second)
    my_label.after(1000,clock)
    global counter
    counter+=1
    if counter==1:
        messagebox.showinfo("Bildiri","Saat açılmıştır")
    
    elif counter==2:
        messagebox.showwarning("Uyarı","Saat göstergesi zaten açıktır")
        return
       
        
        
        
my_w.mainloop()


# In[ ]:





# In[ ]:




