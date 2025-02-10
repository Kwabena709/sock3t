from tkinter import *
import time
import ttkthemes
import tkinter
import pymysql
from tkinter import ttk, messagebox,filedialog
import pandas


# Global variables for database connection
con = None
mycursor = None
date = time.strftime('%d/%m/%Y')
currenttime = time.strftime('%H:%M:%S')

# Function to exit the application
def Exit():
    result = messagebox.askyesno('Confirm Exit', 'Do you want to exit the application?', parent=window)
    if result:
        window.destroy()
    else:
        return

# Function to export data to a text file
def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')  
    indexing = churchmemberTabel.get_children()
    newlist = []
    for index in indexing:
        content=churchmemberTabel.item(index)
        datalist=content['values']
        newlist.append(datalist)
        
        table=pandas.DataFrame(newlist, columns=['Id', 'Name', 'Mobile No', 'Email Address', 'Location','gender', 'D.O.B', 'Added Date', 'Added Time'])
        table.to_csv(url, index=False)
        messagebox.showinfo('Success', 'Data exported successfully', parent=window) 
        
   
def toplevel_data(title, button_text, command):
    global idEntry, nameEntry, mobileEntry, EmailEntry, LocationEntry, GenderEntry, DOBEntry, screen
    screen = Toplevel()
    screen.grab_set()
    screen.title(title)
    screen.resizable(False, False)
    
    # Create and place all the labels and entry widgets
    idLabel = Label(screen, text='Id:', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, padx=10, pady=15)

    nameLabel = Label(screen, text='Name:', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, padx=10, pady=15)

    mobileLabel = Label(screen, text='Mobile No:', font=('times new roman', 20, 'bold'))
    mobileLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    mobileEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    mobileEntry.grid(row=2, column=1, padx=10, pady=15)

    EmailLabel = Label(screen, text='Email Address:', font=('times new roman', 20, 'bold'))
    EmailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    EmailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    EmailEntry.grid(row=3, column=1, padx=10, pady=15)

    LocationLabel = Label(screen, text='Location:', font=('times new roman', 20, 'bold'))
    LocationLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    LocationEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    LocationEntry.grid(row=4, column=1, padx=10, pady=15)

    GenderLabel = Label(screen, text='Gender:', font=('times new roman', 20, 'bold'))
    GenderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    GenderEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    GenderEntry.grid(row=5, column=1, padx=10, pady=15)

    DOBLabel = Label(screen, text='D.O.B:', font=('times new roman', 20, 'bold'))
    DOBLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    DOBEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    DOBEntry.grid(row=6, column=1, padx=10, pady=15)

    # Submit Button to add data
    Search_member_button = ttk.Button(screen, text=button_text, cursor='hand2', command=command)
    Search_member_button.grid(row=7, columnspan=2, pady=10)

    screen.iconphoto(False, tkinter.PhotoImage(file='church logo.png'))

    if title == 'Update Member':
        indexing = churchmemberTabel.focus()
        content = churchmemberTabel.item(indexing)

        # Ensure there's a valid selection
        if not content['values']:
            messagebox.showerror("Error", "Please select a member to update", parent=screen)
            screen.destroy()  # Close the screen if no row is selected
            return

        listdata = content['values']
        # Now safely insert values into entry fields
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        mobileEntry.insert(0, listdata[2])
        EmailEntry.insert(0, listdata[3])
        LocationEntry.insert(0, listdata[4])
        GenderEntry.insert(0, listdata[5])
        DOBEntry.insert(0, listdata[6])

# Function to show all members in the database
def Show_member():
    query = 'SELECT * FROM church'
    mycursor.execute(query)
    rows = mycursor.fetchall()
    churchmemberTabel.delete(*churchmemberTabel.get_children())
    for row in rows:
        churchmemberTabel.insert('', END, values=row)

# Function to update a member in the database
def update_data():
    query = 'UPDATE church SET name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s WHERE id=%s'
    mycursor.execute(query, (nameEntry.get(), mobileEntry.get(), EmailEntry.get(), LocationEntry.get(), GenderEntry.get(), DOBEntry.get(), date, currenttime, idEntry.get()))
    con.commit()
    messagebox.showinfo('Success', 'Member updated successfully', parent=screen)
    screen.destroy()
    Show_member()

# Function to delete a member from the database
def delete_member():
    indexing = churchmemberTabel.focus()
    content = churchmemberTabel.item(indexing)
    row = content['values']
    if not row:
        messagebox.showerror('Error', 'Please select a member to delete', parent=window)
    else:
        result = messagebox.askyesno('Confirm', 'Do you want to delete this member?', parent=window)
        if result:
            query = 'DELETE FROM church WHERE id=%s'
            mycursor.execute(query, (row[0],))
            con.commit()
            messagebox.showinfo('Success', 'Member deleted successfully', parent=window)
            query = 'SELECT * FROM church'
            mycursor.execute(query)
            rows = mycursor.fetchall()
            churchmemberTabel.delete(*churchmemberTabel.get_children())
            for row in rows:
                churchmemberTabel.insert('', END, values=row)
        else:
            return

# Function to search for a member in the database
def Search_data():
    query = 'SELECT * FROM church WHERE id=%s OR name=%s OR mobile=%s OR email=%s OR address=%s OR gender=%s OR dob=%s'
    mycursor.execute(query, (idEntry.get(), nameEntry.get(), mobileEntry.get(), EmailEntry.get(), LocationEntry.get(), GenderEntry.get(), DOBEntry.get()))
    churchmemberTabel.delete(*churchmemberTabel.get_children())
    rows = mycursor.fetchall()
    if not rows:
        messagebox.showerror('Error', 'Member not found', parent=screen)
    else:
        for row in rows:
            churchmemberTabel.insert('', END, values=row)
        messagebox.showinfo('Success', 'Member found', parent=screen)

# Function to add a new member to the database
def add_data():
    if (idEntry.get() == '' or nameEntry.get() == '' or mobileEntry.get() == '' or
        EmailEntry.get() == '' or LocationEntry.get() == '' or GenderEntry.get() == '' or
        DOBEntry.get() == ''):
        messagebox.showerror("Error", 'Fields cannot be empty', parent=screen)
    else:
        try:
            # Insert data into the database
            query = 'INSERT INTO church (id, name, mobile, email, address, gender, dob, date, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            mycursor.execute(query, (idEntry.get(), nameEntry.get(), mobileEntry.get(),
                                    EmailEntry.get(), LocationEntry.get(), GenderEntry.get(),
                                    DOBEntry.get(), date, currenttime))
            con.commit()

            result = messagebox.askyesno('Confirm','Data added successfully, Do you want to clean the form?', parent=screen)
            if result:
                # Clear the form after successful submission
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                mobileEntry.delete(0, END)
                EmailEntry.delete(0, END)
                LocationEntry.delete(0, END)
                GenderEntry.delete(0, END)
                DOBEntry.delete(0, END)
            else:
                pass
        except Exception as e:
            messagebox.showerror('Error','Id cannot be repeated', parent=screen)
            return

        # Display the data in the Treeview widget
        query = 'SELECT * FROM church'
        mycursor.execute(query)
        rows = mycursor.fetchall()
        churchmemberTabel.delete(*churchmemberTabel.get_children())
        for row in rows:
            churchmemberTabel.insert('', END, values=row)
        messagebox.showinfo('Success', 'Data added successfully', parent=screen)

# Function to connect to the MySQL database
def connect_database():
    def connect():
        global mycursor, con
        try:
            # Connect to the database
            con = pymysql.connect(host=hostEntry.get(), user=usernameEntry.get(), password=PasswordEntry.get())
            mycursor = con.cursor()

            messagebox.showinfo('Success', 'Database connection is successful', parent=connectwindow)
            connectwindow.destroy()

            # Enable buttons after successful connection
            AddmemberButton.config(state=NORMAL)
            SearchmemberButton.config(state=NORMAL)
            DeletememberButton.config(state=NORMAL)
            UpdatememberButton.config(state=NORMAL)
            ShowmemberButton.config(state=NORMAL)
            ExportdataButton.config(state=NORMAL)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to connect: {str(e)}', parent=connectwindow)
            return

        try:
            # Create database and table if they don't exist
            query = 'CREATE DATABASE IF NOT EXISTS churchmanagementsystem'
            mycursor.execute(query)
            query = 'USE churchmanagementsystem'
            mycursor.execute(query)
            query = '''CREATE TABLE IF NOT EXISTS church (
                        id INT NOT NULL PRIMARY KEY,
                        name VARCHAR(30),
                        mobile VARCHAR(10),
                        email VARCHAR(30),
                        address VARCHAR(100),
                        gender VARCHAR(20),
                        dob VARCHAR(20),
                        date VARCHAR(50),
                        time VARCHAR(50)
                    )'''
            mycursor.execute(query)
        except Exception as e:
            messagebox.showerror('Error', f'Error creating table: {str(e)}', parent=connectwindow)

    # Create the connection window
    connectwindow = Toplevel()
    connectwindow.grab_set()
    connectwindow.geometry('470x250+730+230')
    connectwindow.title("Database Connection")
    connectwindow.resizable(False, False)
    
    connectwindow.iconphoto(False, tkinter.PhotoImage(file='church logo.png'))

    # UI elements for database connection
    hostnameLabel = Label(connectwindow, text='Host Name:', font=('times new roman', 20, 'bold'))
    hostnameLabel.grid(row=0, column=0, padx=20, sticky=W)

    hostEntry = Entry(connectwindow, font=('times new roman', 15, 'bold'), bd=2)
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    usernameLabel = Label(connectwindow, text='User Name:', font=('times new roman', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20, sticky=W)

    usernameEntry = Entry(connectwindow, font=('times new roman', 15, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    PasswordLabel = Label(connectwindow, text='Password:', font=('times new roman', 20, 'bold'))
    PasswordLabel.grid(row=2, column=0, padx=20, sticky=W)

    PasswordEntry = Entry(connectwindow, font=('times new roman', 15, 'bold'), bd=2, show='*')
    PasswordEntry.grid(row=2, column=1, padx=40, pady=20)

    connect_button = ttk.Button(connectwindow, text='Connect', cursor='hand2', command=connect)
    connect_button.grid(row=3, columnspan=2, pady=20)
    
    
# Main window setup
window = ttkthemes.ThemedTk()
window.get_themes()
window.set_theme('radiance')
window.title('Church Management System')
window.geometry('1174x680+90+7')
window.resizable(False, False)
window.iconphoto(False, tkinter.PhotoImage(file='church logo.png'))

# Display the date and time on the window
datetimeLabel = Label(window, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)


def clock():
    global date, currenttime
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'    Date:{date}\nTime:{currenttime}')
    datetimeLabel.after(1000, clock)


clock()

# Creating the slider text
s = 'Church Management System'
sliderLabel = Label(window, font=('times new roman', 28, 'italic bold'), width=35)
sliderLabel.place(x=200, y=0)

count = 0
text = ''


def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(300, slider)


slider()

# Connect button for database
connectButton = ttk.Button(window, text='CONNECT TO DATABASE', command=connect_database, cursor='hand2')
connectButton.place(x=945, y=10)

# Frames setup
leftframe = Frame(window)
leftframe.place(x=50, y=10, width=300, height=600)

# Logo
logo_image = PhotoImage(file='member1.png')
logoLabel = Label(leftframe, image=logo_image)
logoLabel.grid(row=0, column=0)

# Buttons in the left panel
AddmemberButton = ttk.Button(leftframe, text='Add Member', cursor='hand2', width=25, state=DISABLED, command=lambda :toplevel_data('Add Member','ADD MEMBER',add_data))
AddmemberButton.grid(row=1, column=0, pady=15)

SearchmemberButton = ttk.Button(leftframe, text='Search Member', cursor='hand2', width=25, state=DISABLED,command=lambda :toplevel_data('Search Member','SEARCH MEMBER',Search_data))
SearchmemberButton.grid(row=2, column=0, pady=15)

DeletememberButton = ttk.Button(leftframe, text='Delete Member', cursor='hand2', width=25, state=DISABLED,command=delete_member)
DeletememberButton.grid(row=3, column=0, pady=15)

UpdatememberButton = ttk.Button(leftframe, text='Update Member', cursor='hand2', width=25, state=DISABLED,command=lambda :toplevel_data('Update Member','UPDATE MEMBER',update_data))
UpdatememberButton.grid(row=4, column=0, pady=15)

ShowmemberButton = ttk.Button(leftframe, text='Show Member', cursor='hand2', width=25, state=DISABLED,command=Show_member)
ShowmemberButton.grid(row=5, column=0, pady=15)

ExportdataButton = ttk.Button(leftframe, text='Export Data', cursor='hand2', width=25, state=DISABLED,command=export_data)
ExportdataButton.grid(row=6, column=0, pady=15)

ExitButton = ttk.Button(leftframe, text='Exit', cursor='hand2', width=25,command=Exit)
ExitButton.grid(row=7, column=0, pady=15)
 
# Right frame for data display
rightFrame = Frame(window)
rightFrame.place(x=350, y=80, width=820, height=600)

# Scrollbars for the Treeview widget
scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

# Treeview for displaying members
churchmemberTabel = ttk.Treeview(rightFrame, columns=('Id', 'Name', 'Mobile No', 'Email Address', 'Location', 'Gender', 'D.O.B', 'Added Date', 'Added Time'),
                                 xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)
scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

scrollBarX.config(command=churchmemberTabel.xview)
scrollBarY.config(command=churchmemberTabel.yview)

churchmemberTabel.pack(fill=BOTH, expand=1)

# Setting up columns headings
churchmemberTabel.heading('Id', text='Id')
churchmemberTabel.heading('Name', text='Name')
churchmemberTabel.heading('Mobile No', text='Mobile No')
churchmemberTabel.heading('Email Address', text='Email Address')
churchmemberTabel.heading('Location', text='Location')
churchmemberTabel.heading('Gender', text='Gender')
churchmemberTabel.heading('D.O.B', text='D.O.B')
churchmemberTabel.heading('Added Date', text='Added Date')
churchmemberTabel.heading('Added Time', text='Added Time')

churchmemberTabel.column('Id', width=90, anchor=CENTER)
churchmemberTabel.column('Name', width=400, anchor=CENTER)
churchmemberTabel.column('Mobile No', width=300, anchor=CENTER)
churchmemberTabel.column('Email Address', width=300, anchor=CENTER)
churchmemberTabel.column('Location', width=300, anchor=CENTER)
churchmemberTabel.column('Gender', width=150, anchor=CENTER)
churchmemberTabel.column('D.O.B', width=200, anchor=CENTER)
churchmemberTabel.column('Added Date', width=200, anchor=CENTER)
churchmemberTabel.column('Added Time', width=200, anchor=CENTER)

style = ttk.Style()
style.configure('Treeview.Heading', font=('times new roman', 15, 'bold'))
style.configure('Treeview', font=('times new roman', 15), rowheight=35, bd=2,foreground='red4')

churchmemberTabel.config(show='headings')

window.mainloop()
