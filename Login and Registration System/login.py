from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
import pymysql
import bcrypt
import subprocess
import os
import re



def forget_password():
    email = mailentry.get().strip()
    if email == '':
        showerror('Error', 'Please enter your email address first.', parent=root)
        return

    try:
        with pymysql.connect(host='localhost', user='root', password='1989', database='welfare_contribution_db') as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM contributors WHERE email=%s', (email,))
            row = cur.fetchone()
    except Exception as e:
        showerror('Error', f'Connection Error: {e}', parent=root)
        return

    if row is None:
        showerror('Error', 'Email not found. Please enter a valid email.', parent=root)
        return

    # Create reset password window
    root2 = Toplevel()
    root2.title('Reset Password')
    root2.geometry('500x570+420+70')
    root2.config(bg='white')
    root2.focus_force()
    root2.grab_set()
    root2.resizable(False, False)

    if os.path.exists("church_logo.ico"):
        root2.iconbitmap("church_logo.ico")

    Label(root2, text='Reset Password', font=('times new roman', 24, 'bold'), fg='green', bg='white').pack(pady=10)

    if os.path.exists("pass.png"):
        passwordimage = PhotoImage(file='pass.png')
        forgetimageLabel = Label(root2, image=passwordimage, bg='white')
        forgetimageLabel.image = passwordimage
        forgetimageLabel.pack(pady=5)

    form_frame = Frame(root2, bg='white')
    form_frame.pack(pady=15)

    field_font = ('arial', 22)
    entry_width = 22

    # Security Question
    Label(form_frame, text='Security Question', font=('arial', 16, 'bold'), bg='white').pack(anchor='w', padx=10, pady=(10, 0))
    securityquescombo = ttk.Combobox(form_frame, font=('arial', 16), state='readonly', justify=CENTER, width=entry_width)
    securityquescombo['values'] = (
        'Select', 'Your First Pet Name?', 'Your Place Of Birth?', 'Your Best Friend Name?', 'Your Favourite Teacher?', 'Your Favourite Food?')
    securityquescombo.current(0)
    securityquescombo.pack(pady=5)

    # Answer
    Label(form_frame, text='Answer', font=('arial', 16, 'bold'), bg='white').pack(anchor='w', padx=10, pady=(15, 0))
    answerEntry = Entry(form_frame, font=field_font, width=entry_width, bg='white')
    answerEntry.pack(pady=5)

    # New Password
    Label(form_frame, text='New Password', font=('arial', 16, 'bold'), bg='white').pack(anchor='w', padx=10, pady=(15, 0))
    newpassEntry = Entry(form_frame, font=field_font, width=entry_width, bg='white', show='*')
    newpassEntry.pack(pady=5)

    def reset_password():
        question = securityquescombo.get()
        answer = answerEntry.get().strip()
        newpass = newpassEntry.get().strip()

        if not all([question != 'Select', answer, newpass]):
            showerror('Error', 'All fields are required.', parent=root2)
            return

        try:
            with pymysql.connect(host='localhost', user='root', password='1989', database='welfare_contribution_db') as con:
                cur = con.cursor()
                cur.execute('SELECT * FROM contributors WHERE email=%s', (email,))
                row = cur.fetchone()

                db_question = row[5]
                db_answer = row[6]
                stored_hashed_password = row[7]

                if question != db_question or answer.lower().strip() != db_answer.lower().strip():
                    showerror('Error', 'Security question or answer is incorrect.', parent=root2)
                    return

                if bcrypt.checkpw(newpass.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    showerror('Error',
                              'For new password, Use a more Sophisticated Password!.',
                              parent=root2)
                    return

                hashed_password = bcrypt.hashpw(newpass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                cur.execute(
                    'UPDATE contributors SET security_question=%s, security_answer=%s, password=%s WHERE email=%s',
                    (question, answer, hashed_password, email)
                )
                con.commit()

            showinfo('Success', 'Password updated successfully.', parent=root2)
            root2.destroy()

        except Exception as e:
            showerror('Error', f'Error: {e}', parent=root2)

    Button(root2, text='Reset Password', font=('arial', 18, 'bold'), bg='green', fg='white',
           command=reset_password, cursor='hand2').pack(pady=20)



def register_window():
    root.destroy()
    try:
        import register
    except ImportError as e:
        showerror("Error", f"Cannot open register window: {e}")


def signin():
    email = mailentry.get()
    password = passentry.get()

    if email == '' or password == '':
        showerror('Error', 'All Fields Are Required')
        return

    try:
        with pymysql.connect(host='localhost', user='root', password='1989', database='welfare_contribution_db') as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM contributors WHERE email=%s', (email,))
            row = cur.fetchone()

            if row is None:
                showerror('Error', 'Invalid Email or Password')
            else:
                stored_hashed_password = row[7]
                if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    showinfo('Success', 'Welcome!')
                    root.quit()
                    root.destroy()
                    subprocess.run(["python", "App.py"])
                else:
                    showerror('Error', 'Invalid Email or Password')

    except Exception as e:
        showerror('Error', f"Error due to: {e}", parent=root)


# GUI Setup
root = Tk()
root.geometry('900x600+250+50')
root.title('Login Page')
root.resizable(False, False)

try:
    if os.path.exists("church_logo.ico"):
        root.iconbitmap("church_logo.ico")
except Exception as e:
    print(f"Failed to load icon: {e}")

try:
    if os.path.exists("loginbg.png"):
        bglogin = PhotoImage(file='loginbg.png')
        bgloginLabel = Label(root, image=bglogin)
        bgloginLabel.place(x=0, y=0)
except Exception as e:
    print(f"Background image not loaded: {e}")

frame = Frame(root, bg='white', width=560, height=320)
frame.place(x=180, y=140)

try:
    if os.path.exists("user.png"):
        userimage = PhotoImage(file='user.png')
        userimageLabel = Label(frame, image=userimage, bg='white')
        userimageLabel.image = userimage
        userimageLabel.place(x=10, y=50)
except Exception:
    pass

Label(frame, text='Email', font=('arial', 22, 'bold'), bg='white', fg='black').place(x=220, y=32)
email_var = StringVar()
mailentry = Entry(frame, font=('arial', 22), bg='white', fg='black', textvariable=email_var)
mailentry.place(x=220, y=70)

email_feedback = Label(frame, font=('arial', 10), bg='white', fg='red')
email_feedback.place(x=220, y=105)

def validate_email(*args):
    email = email_var.get()
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        email_feedback.config(text='Valid Email ✔', fg='green')
    else:
        email_feedback.config(text='Invalid Email ✖', fg='red')

email_var.trace('w', validate_email)

Label(frame, text='Password', font=('arial', 22, 'bold'), bg='white', fg='black').place(x=220, y=120)
password_var = StringVar()
passentry = Entry(frame, font=('arial', 22), bg='white', fg='black', show='*', textvariable=password_var)
passentry.place(x=220, y=160)

# Toggle show/hide password
def toggle_password():
    if passentry.cget('show') == '':
        passentry.config(show='*')
        toggle_btn.config(text='Show')
    else:
        passentry.config(show='')
        toggle_btn.config(text='Hide')

toggle_btn = Button(frame, text='Show', font=('arial', 10), command=toggle_password)
toggle_btn.place(x=490, y=165)

# Password strength indicator
strength_label = Label(frame, text='', font=('arial', 10), bg='white', fg='black')
strength_label.place(x=220, y=195)

def check_strength(*args):
    pwd = password_var.get()
    if len(pwd) < 6:
        strength = 'Weak'
        color = 'red'
    elif re.search(r"[A-Za-z]", pwd) and re.search(r"\d", pwd) and len(pwd) >= 8:
        strength = 'Strong'
        color = 'green'
    else:
        strength = 'Medium'
        color = 'orange'
    strength_label.config(text=f'Password Strength: {strength}', fg=color)

password_var.trace('w', check_strength)


Button(frame, text='Register New Account?', font=('arial', 12), bd=0, fg='gray20', bg='white',
       cursor='hand2', command=register_window).place(x=220, y=200)

Button(frame, text='Forget Password?', font=('arial', 12), bd=0, fg='red', bg='white',
       cursor='hand2', command=forget_password).place(x=410, y=200)

Button(frame, text='Login', font=('arial', 18, 'bold'), fg='white', bg='gray20',
       cursor='hand2', command=signin).place(x=450, y=240)


def toggle_theme():
    if root['bg'] == 'white':
        root.config(bg='#2e2e2e')
        frame.config(bg='#2e2e2e')
        for widget in frame.winfo_children():
            if isinstance(widget, Label):
                widget.config(bg='#2e2e2e', fg='white')
            elif isinstance(widget, Entry):
                widget.config(bg='#3e3e3e', fg='white', insertbackground='white')
        theme_btn.config(text='☀ Light Mode')
    else:
        root.config(bg='white')
        frame.config(bg='white')
        for widget in frame.winfo_children():
            if isinstance(widget, Label):
                widget.config(bg='white', fg='black')
            elif isinstance(widget, Entry):
                widget.config(bg='white', fg='black', insertbackground='black')
        theme_btn.config(text='🌙 Dark Mode')

theme_btn = Button(root, text='🌙 Dark Mode', font=('arial', 10), bg='gray20', fg='white', command=toggle_theme)
theme_btn.place(x=10, y=10)

if __name__ == '__main__':
    root.mainloop()
