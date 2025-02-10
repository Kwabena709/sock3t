from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter


def Login():
    if userentry.get()=="" or passwordentry.get()=="":
        messagebox.showerror("Error", "All fields are required", parent=window)
    elif userentry.get()=="admin" and passwordentry.get()=="admin":
        messagebox.showinfo("Success", "Welcome", parent=window)
        
        window.destroy()
        import sms
    else:
        messagebox.showerror("Error", "Invalid Username or Password", parent=window)
    
window=Tk()
window.title("Login")
window.geometry("911x500+200+100")
window.resizable(False, False)  
window.config(bg="purple4")


window.iconphoto(False, tkinter.PhotoImage(file='church logo.png'))
Frame_login=Frame(window, bg="purple3")
Frame_login.place(x=150, y=100, height=340, width=600)  

userlogo=ImageTk.PhotoImage(Image.open("student.png"))

userlogo_label=Label(Frame_login, image=userlogo, bg="purple3")
userlogo_label.pack(padx=10, pady=10)

userlabel=Label(Frame_login, text="Username:", font=("Goudy old style", 15, "bold"),width=20, bg="purple3", fg="white")
userlabel.pack(padx=10)

userentry=Entry(Frame_login, font=("times new roman", 15),width=20, bg="lightgray",bd=1)
userentry.pack(padx=10)

passwordlabel=Label(Frame_login, text="Password:", font=("Goudy old style", 15, "bold"),width=20, bg="purple3", fg="white")  
passwordlabel.pack(padx=10)

passwordentry=Entry(Frame_login, font=("times new roman", 15),width=20, bg=("lightgray"), show="*",bd=1)
passwordentry.pack(padx=10)

Button_login=Button(Frame_login, text="Login", font=("Goudy old style", 15, "bold"), bg="purple4", fg="white"
                    ,activebackground='purple4',activeforeground='white', width=20,cursor='hand2',command=Login) 
Button_login.pack(padx=10, pady=10)






window.mainloop()