from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkcalendar import DateEntry
import pymysql
from tkinter import messagebox

def connect_database():
    try:
        connection=pymysql.connect(host='localhost',user='root',password='1989')
        cursor=connection.cursor()

    except:
        messagebox.showerror('Error','Database connectivity issue try again, open mysql command line client')
        return

def employee_form(window):
    global back_logo
    employee_frame = Frame(window, width=1070, height=567, bg='white')
    employee_frame.place(x=200, y=100)
    headinglabel = Label(employee_frame, text='Manage Employee Details', font=('times new roman', 16, 'bold'),
                         bg='#0f4d7d', fg='white')
    headinglabel.place(x=0, y=0, relwidth=1)

    Topframe = Frame(employee_frame, bg='white')
    Topframe.place(x=0, y=40, relwidth=1, height=235)

    back_logo = ImageTk.PhotoImage(file='back.png')
    back_btn = Button(Topframe, image=back_logo, bd=0, cursor='hand2', command=lambda: employee_frame.place_forget(),
                      bg='white')
    back_btn.place(x=10, y=0)

    search_frame = Frame(Topframe, bg='white')
    search_frame.pack()
    Search_combo = ttk.Combobox(search_frame, values=('Id', 'Name', 'Email'), font=('times new roman', 12),
                                state='readonly')
    Search_combo.set("Search By")
    Search_combo.grid(row=0, column=0, padx=20)

    search_entry = Entry(search_frame, font=('times new roman', 15), bg='lightyellow')
    search_entry.grid(row=0, column=1)

    search_btn = Button(search_frame, text='SEARCH', font=('times new roman', 15), width=10, cursor='hand2',
                        bg='#0f4d7d',
                        fg='white', activebackground='#0f4d7d', activeforeground='white')
    search_btn.grid(row=0, column=2, padx=20)

    show_btn = Button(search_frame, text='SHOW ALL', font=('times new roman', 15), width=10, cursor='hand2',
                      bg='#0f4d7d',
                      fg='white', activebackground='#0f4d7d', activeforeground='white')
    show_btn.grid(row=0, column=3)

    horizontal_scrollbar = Scrollbar(Topframe, orient=HORIZONTAL)
    Vertical_scrollbar = Scrollbar(Topframe, orient=VERTICAL)
    employee_treeview = ttk.Treeview(Topframe, columns=(
    'empid', 'name', 'email', 'location', 'phone', 'gender', 'dob', 'employment_type', 'education', 'work_shift', 'doj',
    'salary', 'user type'),
                                     show='headings', yscrollcommand=Vertical_scrollbar.set,
                                     xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    Vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10, 0))
    horizontal_scrollbar.config(command=employee_treeview.xview)
    Vertical_scrollbar.config(command=employee_treeview.yview)
    employee_treeview.pack(fill=BOTH, expand=True, pady=(10, 0))

    employee_treeview.heading('empid', text='EmpId')
    employee_treeview.heading('name', text='Name')
    employee_treeview.heading('email', text='Email')
    employee_treeview.heading('location', text='Location')
    employee_treeview.heading('phone', text='Phone')
    employee_treeview.heading('gender', text='Gender')
    employee_treeview.heading('dob', text='Date of Birth')
    employee_treeview.heading('employment_type', text='Employment Type')
    employee_treeview.heading('education', text='Education')
    employee_treeview.heading('work_shift', text='Work Shift')
    employee_treeview.heading('doj', text='Date of Joining')
    employee_treeview.heading('salary', text='Salary')
    employee_treeview.heading('user type', text='User Type')

    employee_treeview.column('empid', width=60)
    employee_treeview.column('name', width=140)
    employee_treeview.column('email', width=180)
    employee_treeview.column('location', width=200)
    employee_treeview.column('phone', width=80)
    employee_treeview.column('gender', width=80)
    employee_treeview.column('dob', width=100)
    employee_treeview.column('employment_type', width=120)
    employee_treeview.column('education', width=120)
    employee_treeview.column('work_shift', width=100)
    employee_treeview.column('doj', width=100)
    employee_treeview.column('salary', width=140)
    employee_treeview.column('user type', width=120)

    detail_frame = Frame(employee_frame, bg='white')
    detail_frame.place(x=20, y=280)

    empid_label = Label(detail_frame, text='EmpId', bg='white', font=('times new roman', 12))
    empid_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')

    emp_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    emp_entry.grid(row=0, column=1, padx=20, pady=10)

    Name_label = Label(detail_frame, text='Name', bg='white', font=('times new roman', 12))
    Name_label.grid(row=0, column=2, padx=20, pady=10, sticky='w')

    Name_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    Name_entry.grid(row=0, column=3, padx=20, pady=10)

    Email_label = Label(detail_frame, text='Email', bg='white', font=('times new roman', 12))
    Email_label.grid(row=0, column=4, padx=20, pady=10, sticky='w')

    Email_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    Email_entry.grid(row=0, column=5, padx=20, pady=10)

    gender_label = Label(detail_frame, text='Gender', bg='white', font=('times new roman', 12))
    gender_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')

    gender_combobox = ttk.Combobox(detail_frame, values=('Male', 'Female'), font=('times new roman', 12), width=18,
                                   state='readonly')
    gender_combobox.set('Select Gender')
    gender_combobox.grid(row=1, column=1, padx=20, pady=10)

    dob_label = Label(detail_frame, text='Date of Birth', bg='white', font=('times new roman', 12))
    dob_label.grid(row=1, column=2, padx=20, pady=10, sticky='w')

    # DateEntry widget with calendar popup behavior
    dob_date_entry = DateEntry(detail_frame, font=('times new roman', 12), width=18, state='readonly',
                               date_pattern='dd/mm/yyyy', showweeknumbers=False)
    dob_date_entry.grid(row=1, column=3)

    Contact_label = Label(detail_frame, text='Contact', bg='white', font=('times new roman', 12))
    Contact_label.grid(row=1, column=4, padx=20, pady=10, sticky='w')

    contact_Entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    contact_Entry.grid(row=1, column=5)

    Emp_type_label = Label(detail_frame, text='Employment Type', font=('times new roman', 12), bg='white')
    Emp_type_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')

    emp_type_Combobox = ttk.Combobox(detail_frame, values=('Full Time', 'Part Time', 'Casual', 'Contract', 'Intern'),
                                     font=('times new roman', 12), width=18, state='readonly')
    emp_type_Combobox.set('Select Type')
    emp_type_Combobox.grid(row=2, column=1)

    education_option = ['University', 'Polytechnic', 'Technical Institutes', 'Special Education', 'Shs', 'Jhs']
    Education_label = Label(detail_frame, text='Education', font=('times new roman', 12), bg='white')
    Education_label.grid(row=2, column=2, padx=20, pady=10, sticky='w')

    education_Combobox = ttk.Combobox(detail_frame, values=(education_option), font=('times new roman', 12), width=18,
                                      state='readonly')
    education_Combobox.set('Select Education')
    education_Combobox.grid(row=2, column=3)

    Work_Shift_label = Label(detail_frame, text='Work Shift', font=('times new roman', 12), bg='white')
    Work_Shift_label.grid(row=2, column=4, padx=20, pady=10, sticky='w')

    Work_Shift_Combobox = ttk.Combobox(detail_frame, values=('Morning', 'Night', 'Afternoon'),
                                       font=('times new roman', 12), width=18, state='readonly')
    Work_Shift_Combobox.set('Shift Type')
    Work_Shift_Combobox.grid(row=2, column=5)

    Location_label = Label(detail_frame, text='Address', font=('times new roman', 12), bg='white')
    Location_label.grid(row=3, column=0, padx=20, pady=10, sticky='w')
    address_text = Text(detail_frame, width=20, height=3, bg='lightyellow', font=('times new roman', 12))
    address_text.grid(row=3, column=1, rowspan=2)

    Doj_label = Label(detail_frame, text='Date of Joining', font=('times new roman', 12), bg='white')
    Doj_label.grid(row=3, column=2, padx=20, pady=10, sticky='w')

    Doj_label_combobox = DateEntry(detail_frame, font=('times new roman', 12), width=18, state='readonly',
                                   date_pattern='dd/mm/yyyy', showweeknumbers=False)
    Doj_label_combobox.grid(row=3, column=3)

    Salary_label = Label(detail_frame, text='Salary', font=('times new roman', 12), bg='white')
    Salary_label.grid(row=3, column=4, padx=20, pady=10, sticky='w')

    Salary_Entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    Salary_Entry.grid(row=3, column=5)

    User_type_label = Label(detail_frame, text='User Type', font=('times new roman', 12), bg='white')
    User_type_label.grid(row=4, column=2, padx=20, pady=10, sticky='w')

    User_type_Combobox = ttk.Combobox(detail_frame, values=('Admin', 'Employee'), font=('times new roman', 12),
                                      width=18, state='readonly')
    User_type_Combobox.set('Select User Type')
    User_type_Combobox.grid(row=4, column=3)

    Password_label = Label(detail_frame, text='Password', font=('times new roman', 12), bg='white')
    Password_label.grid(row=4, column=4, padx=20, pady=10, sticky='w')

    Password_Entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    Password_Entry.grid(row=4, column=5)

    button_frame = Frame(employee_frame, bg='white')
    button_frame.place(x=200, y=520)

    Save_button = Button(button_frame, text='Save', font=('times new roman', 15), width=10, cursor='hand2',
                         bg='#0f4d7d',
                         fg='white', activebackground='#0f4d7d', activeforeground='white')
    Save_button.grid(row=0, column=2, padx=20)

    Update_button = Button(button_frame, text='Update', font=('times new roman', 15), width=10, cursor='hand2',
                           bg='#0f4d7d',
                           fg='white', activebackground='#0f4d7d', activeforeground='white')
    Update_button.grid(row=0, column=3, padx=20)

    Delete_button = Button(button_frame, text='Delete', font=('times new roman', 15), width=10, cursor='hand2',
                           bg='#0f4d7d',
                           fg='white', activebackground='#0f4d7d', activeforeground='white')
    Delete_button.grid(row=0, column=4, padx=20)

    Clear_button = Button(button_frame, text='Clear', font=('times new roman', 15), width=10, cursor='hand2',
                          bg='#0f4d7d',
                          fg='white', activebackground='#0f4d7d', activeforeground='white')
    Clear_button.grid(row=0, column=5, padx=20)
