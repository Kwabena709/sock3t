import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3


window=tk.Tk()
window.title("User information management system")  
window.geometry("700x500")
window.resizable(width=False, height=False)
frame_form=tk.Frame(window,padx=20,pady=10)   
frame_form.pack(side=tk.TOP,fill=tk.X) 
frame_form.config(bg="cornflower blue")

tk.Label(frame_form,text="First Name:",bg='cornflower blue',font=('times new roman',17,'bold')).grid(row=0,column=0,pady=5,sticky="w")
entry_fname=tk.Entry(frame_form,width=20)
entry_fname.grid(row=0,column=1,pady=5,padx=5)

tk.Label(frame_form,text="Last Name:").grid(row=0,column=2,pady=5,sticky="w")
entry_lname=tk.Entry(frame_form,width=20)
entry_lname.grid(row=0,column=3,pady=5,padx=5)

tk.Label(frame_form,text="Gender:").grid(row=1,column=0,pady=5,sticky="w")
combo_gender=ttk.Combobox(frame_form,values=['male','Female'],state='readonly', width=18)
combo_gender.grid(row=1,column=1,pady=5,padx=5)

tk.Label(frame_form,text="Address:").grid(row=1,column=2,pady=5,sticky="w")
entry_address=tk.Entry(frame_form,width=20)
entry_address.grid(row=1,column=3,pady=5,padx=5)

tk.Label(frame_form,text="Phone:").grid(row=2,column=0,pady=5,sticky="w")
entry_phone=tk.Entry(frame_form,width=20)
entry_phone.grid(row=2,column=1,pady=5,padx=5)

tk.Label(frame_form,text="Email:").grid(row=2,column=2,pady=5,sticky="w")
entry_email=tk.Entry(frame_form,width=20)
entry_email.grid(row=2,column=3,pady=5,padx=5)











window.mainloop()