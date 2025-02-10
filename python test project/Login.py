from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import tkinter

# Validation function
def validate_inputs(username, password):
    if not username or username == "Username":
        return "Please enter a username!"
    if not password or password == "Password":
        return "Please enter a password!"
    return None

# Authentication function
def authenticate(username, password):
    error = validate_inputs(username, password)
    if error:
        error_label.config(text=error, fg="red")
        return

    valid_username = "admin"
    valid_password = "1234"

    if username == valid_username and password == valid_password:
        messagebox.showinfo('Success', 'Login Successful!')
    else:
        messagebox.showerror('Warning', "Invalid Username or Password!")

# Toggle Password Visibility
def toggle_password():
    if passwordEntry.cget("show") == "*":
        passwordEntry.config(show="")
        eye_button.config(image=open_eye)
    else:
        passwordEntry.config(show="*")
        eye_button.config(image=closed_eye)

# Event when password typing starts
def on_password_type(event):
    if passwordEntry.cget("show") != "*":
        passwordEntry.config(show="*")
    error_label.config(text="")

# Forgot Password Functionality
def forgot_password():
    error_label.config(text="Forgot Password?", fg="blue")

# Show message when password exceeds 18 characters
def check_max_length(event):
    if len(passwordEntry.get()) > 18:
        messagebox.showwarning("Password Length", "Password cannot exceed 18 characters.")
        passwordEntry.delete(18, END)

# Open social media links
def open_social_media(url):
    import webbrowser
    webbrowser.open(url)

# Open Create Account Window
def create_account_window():
    window.destroy()
    import Signup

# Main Window Setup
window = Tk()
window.title('Login Page')
window.resizable(False, False)
window.geometry('990x660+175+20')
window.config(bg='#4E5069')

window.iconphoto(False, tkinter.PhotoImage(file='church logo.png'))
backgroundimage = ImageTk.PhotoImage(file='bg (1).jpg')
imagelabel = Label(window, image=backgroundimage)
imagelabel.place(x=0, y=0)

# Login Label
loginlabel = Label(window, text='USER LOGIN', font=('Times new roman', 20, 'bold'), bg='white', fg='red')
loginlabel.place(x=620, y=105)

# Username Field
usernameEntry = Entry(window, highlightthickness=0, relief=FLAT, width=19,
                      font=('Microsoft Yahei UI Light', 15, 'bold'), bg='white', fg='red')
usernameEntry.place(x=570, y=180)
usernameEntry.insert(0, "Username")

def on_focus_in(event):
    if usernameEntry.get() == "Username":
        usernameEntry.delete(0, END)

usernameEntry.bind("<FocusIn>", on_focus_in)
usernameEntry.bind("<FocusOut>",
                   lambda event: usernameEntry.insert(0, "Username") if usernameEntry.get() == "" else None)
usernameline = Canvas(window, width=250, height=2.0, bg='red', highlightthickness=0)
usernameline.place(x=570, y=215)

# Password Field
passwordEntry = Entry(window, highlightthickness=0, relief=FLAT, width=19,
                      font=('Microsoft Yahei UI Light', 15, 'bold'), bg='white', fg='red')
passwordEntry.place(x=570, y=250)
passwordEntry.insert(0, "Password")
passwordEntry.bind("<FocusIn>",
                   lambda event: passwordEntry.delete(0, END) if passwordEntry.get() == "Password" else None)
passwordEntry.bind("<FocusOut>",
                   lambda event: passwordEntry.insert(0, "Password") if passwordEntry.get() == "" else None)
passwordEntry.bind("<Key>", on_password_type)
passwordEntry.bind("<KeyRelease>", check_max_length)
passwordline = Canvas(window, width=250, height=2.0, bg='red', highlightthickness=0)
passwordline.place(x=570, y=285)

# Forgot Password Label
forgot_password_label = Label(window, text="Forgot Password?", font=('Microsoft Yahei UI Light', 10, 'bold'),
                              bg='white', fg='red', cursor="hand2")
forgot_password_label.place(x=697, y=290)
forgot_password_label.bind("<Button-1>", lambda event: forgot_password())

# Open and Closed Eye Images
open_eye = ImageTk.PhotoImage(Image.open("openeye.png").resize((20, 20)))
closed_eye = ImageTk.PhotoImage(Image.open("closeye.png").resize((20, 20)))

# Show/Hide Password Button
eye_button = Button(window, image=closed_eye, bg='white', relief=FLAT, cursor="hand2", command=toggle_password)
eye_button.place(x=790, y=250)

# Login Button
login_button = Button(window, text="Login", font=('Microsoft Yahei UI Light', 15, 'bold'), bg='red', fg='white',
                      width=20,
                      cursor="hand2", activebackground='red', activeforeground='white', bd=2,
                      command=lambda: authenticate(usernameEntry.get(), passwordEntry.get()))
login_button.place(x=575, y=350)

Orlabel = Label(window, text='---------- OR ----------', font=('Microsoft Yahei UI Light', 12, 'bold'), bg='#FFFFFF',
                fg='red')
Orlabel.place(x=598, y=405)

# Social Media Icons
facebook_icon = ImageTk.PhotoImage(Image.open("facebook.png").resize((25, 25)))
google_icon = ImageTk.PhotoImage(Image.open("google.png").resize((25, 25)))
youtube_icon = ImageTk.PhotoImage(Image.open("youtube.png").resize((25, 25)))

facebook_button = Button(window, image=facebook_icon, bg='white', relief=FLAT, cursor="hand2",activebackground='white',
                         command=lambda: open_social_media("https://www.facebook.com"))
facebook_button.place(x=605, y=440)

google_button = Button(window, image=google_icon, bg='white', relief=FLAT, cursor="hand2",activebackground='white',
                       command=lambda: open_social_media("https://www.google.com"))
google_button.place(x=680, y=440)

youtube_button = Button(window, image=youtube_icon, bg='white', relief=FLAT, cursor="hand2",
                        command=lambda: open_social_media("https://www.youtube.com"))
youtube_button.place(x=760, y=440)

# "Don't have an account?" and "Create New Account" Link
dont_have_account_label = Label(window, text="Don't have an account?", font=('Microsoft Yahei UI Light', 10), bg='white', fg='red')
dont_have_account_label.place(x=565, y=490)

create_account_label = Label(window, text="Create New Account", font=('Microsoft Yahei UI Light', 10, 'underline'), bg='white', fg='blue', cursor="hand2")
create_account_label.place(x=715, y=490)
create_account_label.bind("<Button-1>", lambda event: create_account_window())

# Error Label
error_label = Label(window, text="", font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='red')
error_label.place(x=610, y=320)

# Bind Enter Key
window.bind("<Return>", lambda event: authenticate(usernameEntry.get(), passwordEntry.get()))

window.mainloop()
