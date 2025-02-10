from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk


def employee_form():
    global back_logo
    employee_frame=Frame(window,width=1070,height=567,bg='white')
    employee_frame.place(x=200,y=100)
    headingLabel=Label(employee_frame,text='Manage Employee Details',font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    headingLabel.place(x=0,y=0,relwidth=1)
    
    back_logo=ImageTk.PhotoImage(file='back.png')
    back_btn=Button(employee_frame,image=back_logo,bd=0,cursor='hand2',command=lambda: employee_frame.place_forget(),bg='white')
    back_btn.place(x=10,y=30)
    
    Topframe=Frame(employee_frame,bg='white')
    Topframe.place(x=0,y=60,relwidth=1,height=235)
    
    search_frame=Frame(Topframe,bg='white')
    search_frame.pack()
    Search_combo=ttk.Combobox(search_frame,values=('Id','Name','Email'),font=('times new roman',15),state='readonly')
    Search_combo.set("Search By")
    Search_combo.grid(row=0,column=0,padx=20)
    
    search_Entry=Entry(search_frame,font=('times new roman',15),bg='lightyellow')
    search_Entry.grid(row=0,column=1)
    
    search_btn=Button(search_frame,text='SEARCH',font=('times new roman',15),width=10,cursor='hand2',bg='#0f4d7d',fg='white',activebackground='#0f4d7d',activeforeground='white')
    search_btn.grid(row=0,column=2,padx=20)
    
    show_btn=Button(search_frame,text='SHOW ALL',font=('times new roman',15),width=10,cursor='hand2',bg='#0f4d7d',fg='white',activebackground='#0f4d7d',activeforeground='white')
    show_btn.grid(row=0,column=3)
    
    horizontal_scrollbar=Scrollbar(Topframe,orient=HORIZONTAL)
    Vertical_scrollbar=Scrollbar(Topframe,orient=VERTICAL)
    employee_treeview=ttk.Treeview(Topframe,columns=('empid','name','email','location','phone','gender','dob','employment_type','education','work_shift','doj','salary','user type'),show='headings',
                                   yscrollcommand=Vertical_scrollbar.set,xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM,fill=X)
    Vertical_scrollbar.pack(side=RIGHT,fill=Y,pady=(10,0))
    horizontal_scrollbar.config(command=employee_treeview.xview)
    Vertical_scrollbar.config(command=employee_treeview.yview)
    employee_treeview.pack(pady=(10,0))
    
    employee_treeview.heading('empid',text='EmpId')
    employee_treeview.heading('name',text='Name')
    employee_treeview.heading('email',text='Email')
    employee_treeview.heading('location',text='Location')
    employee_treeview.heading('phone',text='Phone')
    employee_treeview.heading('gender',text='Gender')
    employee_treeview.heading('dob',text='Date of Birth')
    employee_treeview.heading('employment_type',text='Employment Type')
    employee_treeview.heading('education',text='Education')
    employee_treeview.heading('work_shift',text='Work Shift')
    employee_treeview.heading('doj',text='Date of Joining')
    employee_treeview.heading('salary',text='Salary')
    employee_treeview.heading('user type',text='User Type')
    
    employee_treeview.column('empid',width=60)
    employee_treeview.column('name',width=140)
    employee_treeview.column('email',width=180)
    employee_treeview.column('location',width=200)
    employee_treeview.column('phone',width=80)
    employee_treeview.column('gender',width=80)
    employee_treeview.column('dob',width=100)
    employee_treeview.column('employment_type',width=120)
    employee_treeview.column('education',width=120)
    employee_treeview.column('work_shift',width=100)
    employee_treeview.column('doj',width=100)
    employee_treeview.column('salary',width=140)
    employee_treeview.column('user type',width=120)
    
    detail_frame=Frame(employee_frame)
    detail_frame.place(x=0,y=300)
    
    
#GUI Part
window=Tk()
window.title("Dashboard")
window.geometry('1270x668+40+15')
window.resizable(False, False)
window.configure(bg='white')

Logoimg=ImageTk.PhotoImage(Image.open("icon.png"))

# Title
titlelabel = Label(window,image=Logoimg,compound=LEFT, text="  Inventory Management System", font=("Times new roman", 40), bg='#010c48',fg='white',anchor='w',padx=20)
titlelabel.place(x=0,y=0,relwidth=1)

logoutbtn = Button(window, text="Logout",width=10, font=("Times new roman", 20), bg='#010c48',fg='white',cursor='hand2',activebackground='#010c48',activeforeground='white')    
logoutbtn.place(x=1080,y=6)

subtitlelabel=Label(window,text='Welcome Admin\t\t Date: 08-07-2025\t\t Time 12:36:17 pm',font=('times new roman',15),bg='#4d636d',fg='white')
subtitlelabel.place(x=0,y=70,relwidth=1)

leftframe=Frame(window)
leftframe.place(x=0,y=102, width=200,height=555)

imagelogo=ImageTk.PhotoImage(Image.open('logo.png'))

imagelabel=Label(leftframe,image=imagelogo)
imagelabel.pack()

menulabel=Label(leftframe,text='Menu',font=('times new roman',20),bg='#009688')
menulabel.pack(fill=X)

employee_icon=PhotoImage(file='employee.png')

employee_btn=Button(leftframe,image=employee_icon,compound=LEFT,text=' Employees',font=('Times new roman',20,'bold'),bd=2,anchor='w',padx=10,cursor='hand2',command=employee_form)
employee_btn.pack(fill=X)

Supplier_icon=PhotoImage(file='Supplier.png')

Supplier_btn=Button(leftframe,image=Supplier_icon,compound=LEFT,text=' Supplier',font=('Times new roman',20,'bold'),bd=2,anchor='w',padx=10,cursor='hand2')
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

Total_emp_icon=ImageTk.PhotoImage(file='total_emp.png')

Total_Emp_icon_label=Label(emp_frame,image=Total_emp_icon,bg='#2C3E50')
Total_Emp_icon_label.pack(pady=3)

Total_Emp_label=Label(emp_frame,text='Total Employees',font=("times new roman",20,'bold'),bg='#2C3E50',fg='white')
Total_Emp_label.pack()

Total_Emp_count_label=Label(emp_frame,text='0',font=("times new roman",40,'bold'),bg='#2C3E50',fg='white')
Total_Emp_count_label.pack()


Sup_frame=Frame(window,bg='#8E44AD',bd=3,relief=RIDGE)
Sup_frame.place(x=800,y=125,width=280,height=170)

Total_Sup_icon=ImageTk.PhotoImage(file='total_sup.png')

Total_Sup_icon_label=Label(Sup_frame,image=Total_Sup_icon,bg='#8E44AD')
Total_Sup_icon_label.pack(pady=3)

Total_Sup_label=Label(Sup_frame,text='Total Suppliers',font=("times new roman",20,'bold'),bg='#8E44AD',fg='white')
Total_Sup_label.pack()

Total_Sup_count_label=Label(Sup_frame,text='0',font=("times new roman",40,'bold'),bg='#8E44AD',fg='white')
Total_Sup_count_label.pack()



Cat_frame=Frame(window,bg='#27AE60',bd=3,relief=RIDGE)
Cat_frame.place(x=400,y=310,width=280,height=170)

Total_Cat_icon=ImageTk.PhotoImage(file='total_cat.png')

Total_Cat_icon_label=Label(Cat_frame,image=Total_Cat_icon,bg='#27AE60')
Total_Cat_icon_label.pack(pady=3)

Total_Cat_label=Label(Cat_frame,text='Total Categories',font=("times new roman",20,'bold'),bg='#27AE60',fg='white')
Total_Cat_label.pack()

Total_Cat_count_label=Label(Cat_frame,text='0',font=("times new roman",40,'bold'),bg='#27AE60',fg='white')
Total_Cat_count_label.pack()



Prod_frame=Frame(window,bg='#2C3E50',bd=3,relief=RIDGE)
Prod_frame.place(x=800,y=310,width=280,height=170)

Total_Prod_icon=ImageTk.PhotoImage(file='total_Prod.png')

Total_Prod_icon_label=Label(Prod_frame,image=Total_Prod_icon,bg='#2C3E50')
Total_Prod_icon_label.pack(pady=3)

Total_Prod_label=Label(Prod_frame,text='Total Products',font=("times new roman",20,'bold'),bg='#2C3E50',fg='white')
Total_Prod_label.pack()

Total_Prod_count_label=Label(Prod_frame,text='0',font=("times new roman",40,'bold'),bg='#2C3E50',fg='white')
Total_Prod_count_label.pack()


Sales_frame=Frame(window,bg='#E74C3C',bd=3,relief=RIDGE)
Sales_frame.place(x=600,y=495,width=280,height=170)

Total_Sales_icon=ImageTk.PhotoImage(file='total_Sales.png')

Total_Sales_icon_label=Label(Sales_frame,image=Total_Sales_icon,bg='#E74C3C')
Total_Sales_icon_label.pack(pady=3)

Total_Sales_label=Label(Sales_frame,text='Total Sales',font=("times new roman",20,'bold'),bg='#E74C3C',fg='white')
Total_Sales_label.pack()

Total_Sales_count_label=Label(Sales_frame,text='0',font=("times new roman",40,'bold'),bg='#E74C3C',fg='white')
Total_Sales_count_label.pack()






window.mainloop()