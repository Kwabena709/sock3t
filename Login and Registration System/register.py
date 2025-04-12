from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import pymysql
import bcrypt
from customtkinter import CTkLabel
import re

def is_valid_phone(phone):
    """
    Validates the phone number.
    Accepts formats like: +2348012345678 or 08012345678
    """
    pattern = re.compile(r"^\+?\d{10,15}$")
    return bool(pattern.match(phone))

def clean_phone(phone):
    """
    Removes all characters except digits and '+' (for country code)
    """
    return re.sub(r"[^\d+]", "", phone)


def create_database_and_table():
    try:
        con = pymysql.connect(host='localhost', user='root', password='1989')
        cur = con.cursor()

        cur.execute('CREATE DATABASE IF NOT EXISTS welfare_contribution_db')
        cur.execute('USE welfare_contribution_db')

        cur.execute('''CREATE TABLE IF NOT EXISTS contributors (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        first_name VARCHAR(255),
                        last_name VARCHAR(255),
                        phone VARCHAR(255),  # Ensure this is the correct column for contact
                        email VARCHAR(255) UNIQUE,
                        security_question VARCHAR(255),
                        security_answer VARCHAR(255),
                        password TEXT
                        
                    )''')

        con.commit()
        con.close()
    except Exception as e:
        showerror('Error', f"Error creating database or table: {e}", parent=root)


def login_window():
    root.destroy()
    import login


def clear():
    entryemail.delete(0, END)
    entrypassword.delete(0, END)
    entryconfirmpassword.delete(0, END)
    entryfirstname.delete(0, END)
    entrylastname.delete(0, END)
    entryanswer.delete(0, END)
    comboquestion.current(0)
    entryphone.delete(0, END)
    check.set(0)


def register():
    if entryfirstname.get() == '' or entrylastname.get() == '' or entryemail.get() == '' or \
            entrypassword.get() == '' or entryconfirmpassword.get() == '' or comboquestion.get() == 'Select' or entryanswer.get() == '' or entryphone.get() == '':
        showerror('Error', "All Fields Are Required", parent=root)

    elif entrypassword.get() != entryconfirmpassword.get():
        showerror('Error', "Password Mismatch", parent=root)

    elif check.get() == 0:
        showerror('Error', "Please Agree To Our Terms & Conditions", parent=root)

    else:
        try:
            # Clean and validate phone number
            raw_phone = entryphone.get()
            phone = clean_phone(raw_phone)

            if not is_valid_phone(phone):
                showerror("Error", "Invalid phone number format. Use +233XXXXXXXXXX or 080XXXXXXXX", parent=root)
                return

            # Validate email format
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', entryemail.get()):
                showerror("Error", "Invalid email format", parent=root)
                return

            # Hash password
            hashed_password = bcrypt.hashpw(entrypassword.get().encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            con = pymysql.connect(host='localhost', user='root', password='1989', database='welfare_contribution_db')
            cur = con.cursor()

            # Check if user already exists
            cur.execute('SELECT * FROM contributors WHERE email=%s', (entryemail.get(),))
            row = cur.fetchone()

            if row:
                showerror('Error', "User Already Exists", parent=root)
            else:
                # Insert using the correct order and cleaned phone
                cur.execute('''INSERT INTO contributors 
                               (first_name, last_name, phone, email, security_question, security_answer, password) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                            (entryfirstname.get(), entrylastname.get(), phone, entryemail.get(),
                             comboquestion.get(), entryanswer.get(), hashed_password))

                con.commit()
                con.close()

                showinfo('Success', "Registration Successful", parent=root)
                clear()
                root.destroy()
                import login

        except Exception as e:
            showerror('Error', f"Error due to: {e}", parent=root)

def check_password(email, entered_password):
    try:
        con = pymysql.connect(host='localhost', user='root', password='1989', database='welfare_contribution_db')
        cur = con.cursor()

        cur.execute('SELECT password FROM contributors WHERE email=%s', (email,))
        row = cur.fetchone()

        if row and bcrypt.checkpw(entered_password.encode('utf-8'), row[0].encode('utf-8')):
            return True
        else:
            return False

    except Exception as e:
        showerror('Error', f"Error due to: {e}", parent=root)
        return False


# GUI Start
root = Tk()
root.geometry('1350x710+0+10')
root.title('Registration Form')
root.resizable(False, False)
root.iconbitmap("church_logo.ico")

create_database_and_table()

try:
    bg = PhotoImage(file='bg.png')
except:
    bg = None

if bg:
    bgLabel = Label(root, image=bg)
    bgLabel.place(x=0, y=0)

registerFrame = Frame(root, bg='white', width=650, height=670)
registerFrame.place(x=630, y=20)

titleLabel = Label(registerFrame, text='Registration Form', font=('arial', 22, 'bold'), bg='white', fg='Black')
titleLabel.place(x=200, y=5)

firstnameLabel = Label(registerFrame, text='First Name', font=('times new roman', 18, 'bold'), bg='white', fg='gray20')
firstnameLabel.place(x=20, y=60)
entryfirstname = Entry(registerFrame, font=('times new roman', 18), bg='lightgray')
entryfirstname.place(x=20, y=90, width=250)

lastnameLabel = Label(registerFrame, text='Last Name', font=('times new roman', 18, 'bold'), bg='white', fg='gray20')
lastnameLabel.place(x=370, y=60)
entrylastname = Entry(registerFrame, font=('times new roman', 18), bg='lightgray')
entrylastname.place(x=370, y=90, width=250)

phoneLabel = Label(registerFrame, text='Phone with country code', font=('times new roman', 18, 'bold'), bg='white', fg='gray20')
phoneLabel.place(x=370, y=140)
entryphone = Entry(registerFrame, font=('times new roman', 18), bg='lightgray')
entryphone.place(x=370, y=170, width=250)

emailLabel = Label(registerFrame, text='Email', font=('times new roman', 18, 'bold'), bg='white', fg='gray20')
emailLabel.place(x=20, y=220)
entryemail = Entry(registerFrame, font=('times new roman', 18), bg='lightgray')
entryemail.place(x=20, y=250, width=600)

questionLabel = Label(registerFrame, text='Security Question', font=('times new roman', 18, 'bold'), bg='white', fg='gray20')
questionLabel.place(x=20, y=300)
comboquestion = ttk.Combobox(registerFrame, font=('times new roman', 16), state='readonly', justify=CENTER)
comboquestion['values'] = ('Select', 'Your First Pet Name?', 'Your Place Of Birth?', 'Your Best Friend Name?', 'Your Favourite Teacher?', 'Your Favourite Food?')
comboquestion.place(x=20, y=330, width=250)
comboquestion.current(0)

answerLabel = Label(registerFrame, text='Answer', font=('times new roman', 18, 'bold'), bg='white', fg='gray20')
answerLabel.place(x=370, y=300)
entryanswer = Entry(registerFrame, font=('times new roman', 18), bg='lightgray')
entryanswer.place(x=370, y=330, width=250)

passwordLabel = Label(registerFrame, text='Password', font=('times new roman', 18, 'bold'), bg='white', fg='gray20')
passwordLabel.place(x=20, y=380)
entrypassword = Entry(registerFrame, font=('times new roman', 18), bg='lightgray', show='*')
entrypassword.place(x=20, y=410, width=250)

confirmpasswordLabel = Label(registerFrame, text='Confirm Password', font=('times new roman', 18, 'bold'), bg='white', fg='gray20')
confirmpasswordLabel.place(x=370, y=380)
entryconfirmpassword = Entry(registerFrame, font=('times new roman', 18), bg='lightgray', show='*')
entryconfirmpassword.place(x=370, y=410, width=250)

check = IntVar()
checkButton = Checkbutton(registerFrame, text='I Agree To All The Terms & Conditions', variable=check, onvalue=1, offvalue=0,
                          font=('times new roman', 14, 'bold'), bg='white')
checkButton.place(x=20, y=470)

try:
    button = PhotoImage(file="button.png")
    registerbutton = Button(registerFrame, image=button, bd=0, cursor='hand2', bg='white',
                            activebackground='white', activeforeground='white', command=register)
except:
    registerbutton = Button(registerFrame, text="Register", font=('times new roman', 18), command=register)
registerbutton.place(x=250, y=520)

try:
    loginimage = PhotoImage(file="login.png")
    loginbutton1 = Button(root, image=loginimage, bd=0, cursor='hand2', bg='gold',
                          activebackground='gold', activeforeground='gold', command=login_window)
except:
    loginbutton1 = Button(root, text="Login", font=('times new roman', 18), command=login_window)
loginbutton1.place(x=240, y=330)

root.mainloop()
