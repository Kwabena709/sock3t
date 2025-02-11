from tkinter import *
from PIL import Image, ImageTk
from Employees import employee_form




# GUI Part
window = Tk()
window.title("Dashboard")
window.geometry('1270x668+40+15')
window.resizable(False, False)
window.configure(bg='white')

Logoimg = ImageTk.PhotoImage(Image.open("icon.png"))

# Title
titlelabel = Label(window, image=Logoimg, compound=LEFT, text="  Inventory Management System", font=("Times new roman", 40), bg='#010c48', fg='white', anchor='w', padx=20)
titlelabel.place(x=0, y=0, relwidth=1)

logoutbtn = Button(window, text="Logout", width=10, font=("Times new roman", 17), bg='#0f4d7d', fg='white', cursor='hand2', activebackground='#0f4d7d', activeforeground='white')
logoutbtn.place(x=1080, y=14)

subtitlelabel = Label(window, text='Welcome Admin\t\t Date: 08-07-2025\t\t Time 12:36:17 pm', font=('times new roman', 15), bg='#4d636d', fg='white')
subtitlelabel.place(x=0, y=70, relwidth=1)

leftframe = Frame(window)
leftframe.place(x=0, y=102, width=200, height=555)

imagelogo = ImageTk.PhotoImage(Image.open('logo.png'))

imagelabel = Label(leftframe, image=imagelogo)
imagelabel.pack()

menulabel = Label(leftframe, text='Menu', font=('times new roman', 20), bg='#009688')
menulabel.pack(fill=X)

employee_icon = PhotoImage(file='employee.png')

employee_btn = Button(leftframe, image=employee_icon, compound=LEFT, text=' Employees', font=('Times new roman', 20, 'bold'), bd=2, anchor='w', padx=10, cursor='hand2', command=lambda :employee_form(window))
employee_btn.pack(fill=X)

Supplier_icon = PhotoImage(file='Supplier.png')

Supplier_btn = Button(leftframe, image=Supplier_icon, compound=LEFT, text=' Supplier', font=('Times new roman', 20, 'bold'), bd=2, anchor='w', padx=10, cursor='hand2')
Supplier_btn.pack(fill=X)


Category_icon=PhotoImage(file='Category.png')

Category_btn=Button(leftframe,image=Category_icon,compound=LEFT,text=' Category',font=('Times new roman',20,'bold'),bd=2,anchor='w',padx=10,cursor='hand2')
Category_btn.pack(fill=X)

Product_icon=PhotoImage(file='Product.png')

Product_btn=Button(leftframe,image=Product_icon,compound=LEFT,text=' Product',font=('Times new roman',20,'bold'),bd=2,anchor='w',padx=10,cursor='hand2')
Product_btn.pack(fill=X)

Sales_icon=PhotoImage(file='Sales.png')

Sales_btn=Button(leftframe,image=Sales_icon,compound=LEFT,text=' Sales',font=('Times new roman',20,'bold'),bd=2,anchor='w',padx=10,cursor='hand2')
Sales_btn.pack(fill=X)

Exit_icon=PhotoImage(file='Exit.png')

Exit_btn=Button(leftframe,image=Exit_icon,compound=LEFT,text=' Exit',font=('Times new roman',20,'bold'),bd=2,anchor='w',padx=10,cursor='hand2')
Exit_btn.pack(fill=X)

emp_frame=Frame(window,bg='#2C3E50',bd=3,relief=RIDGE)
emp_frame.place(x=400,y=125,width=280,height=170)

Total_emp_icon=ImageTk.PhotoImage(Image.open('total_emp.png'))

Total_Emp_icon_label=Label(emp_frame,image=Total_emp_icon,bg='#2C3E50')
Total_Emp_icon_label.pack(pady=3)

Total_Emp_label=Label(emp_frame,text='Total Employees',font=("times new roman",20,'bold'),bg='#2C3E50',fg='white')
Total_Emp_label.pack()

Total_Emp_count_label=Label(emp_frame,text='0',font=("times new roman",40,'bold'),bg='#2C3E50',fg='white')
Total_Emp_count_label.pack()


Sup_frame=Frame(window,bg='#8E44AD',bd=3,relief=RIDGE)
Sup_frame.place(x=800,y=125,width=280,height=170)

Total_Sup_icon=ImageTk.PhotoImage(Image.open('total_sup.png'))

Total_Sup_icon_label=Label(Sup_frame,image=Total_Sup_icon,bg='#8E44AD')
Total_Sup_icon_label.pack(pady=3)

Total_Sup_label=Label(Sup_frame,text='Total Suppliers',font=("times new roman",20,'bold'),bg='#8E44AD',fg='white')
Total_Sup_label.pack()

Total_Sup_count_label=Label(Sup_frame,text='0',font=("times new roman",40,'bold'),bg='#8E44AD',fg='white')
Total_Sup_count_label.pack()



Cat_frame=Frame(window,bg='#27AE60',bd=3,relief=RIDGE)
Cat_frame.place(x=400,y=310,width=280,height=170)

Total_Cat_icon=ImageTk.PhotoImage(Image.open('total_cat.png'))

Total_Cat_icon_label=Label(Cat_frame,image=Total_Cat_icon,bg='#27AE60')
Total_Cat_icon_label.pack(pady=3)

Total_Cat_label=Label(Cat_frame,text='Total Categories',font=("times new roman",20,'bold'),bg='#27AE60',fg='white')
Total_Cat_label.pack()

Total_Cat_count_label=Label(Cat_frame,text='0',font=("times new roman",40,'bold'),bg='#27AE60',fg='white')
Total_Cat_count_label.pack()



Prod_frame=Frame(window,bg='#2C3E50',bd=3,relief=RIDGE)
Prod_frame.place(x=800,y=310,width=280,height=170)

Total_Prod_icon=ImageTk.PhotoImage(Image.open('total_Prod.png'))

Total_Prod_icon_label=Label(Prod_frame,image=Total_Prod_icon,bg='#2C3E50')
Total_Prod_icon_label.pack(pady=3)

Total_Prod_label=Label(Prod_frame,text='Total Products',font=("times new roman",20,'bold'),bg='#2C3E50',fg='white')
Total_Prod_label.pack()

Total_Prod_count_label=Label(Prod_frame,text='0',font=("times new roman",40,'bold'),bg='#2C3E50',fg='white')
Total_Prod_count_label.pack()


Sales_frame=Frame(window,bg='#E74C3C',bd=3,relief=RIDGE)
Sales_frame.place(x=600,y=495,width=280,height=170)

Total_Sales_icon=ImageTk.PhotoImage(Image.open('total_Sales.png'))

Total_Sales_icon_label=Label(Sales_frame,image=Total_Sales_icon,bg='#E74C3C')
Total_Sales_icon_label.pack(pady=3)

Total_Sales_label=Label(Sales_frame,text='Total Sales',font=("times new roman",20,'bold'),bg='#E74C3C',fg='white')
Total_Sales_label.pack()

Total_Sales_count_label=Label(Sales_frame,text='0',font=("times new roman",40,'bold'),bg='#E74C3C',fg='white')
Total_Sales_count_label.pack()





window.mainloop()