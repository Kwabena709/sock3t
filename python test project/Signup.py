from tkinter import *
from PIL import ImageTk, Image
from tkinter.font import Font
from tkinter import messagebox
import tkinter

# Initialize main window
window = Tk()
window.title('Signup Page')
window.resizable(False, False)
window.geometry('900x600+250+50')
window.config(bg='#4E5069')

window.iconphoto(False, tkinter.PhotoImage(file='church logo.png'))

# Create left frame for background image
leftframe = Frame(window)
leftframe.place(x=10, y=20, width=410, height=560)

# Background image
background_image = ImageTk.PhotoImage(Image.open("img (5).jpg"))
background_label = Label(leftframe, image=background_image)
background_label.place(x=0, y=0)
# Create right frame for signup form
rightframe = Frame(window, bg='#F0F0F0')
rightframe.place(x=470, y=20, width=410, height=560)

# Login redirection
def open_login_page():
    window.destroy()
    import Login

# Validation functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)


# Create a StringVar for passwordEntry
password_var = StringVar()
confirm_password_var = StringVar()

# Define the password_length_check function to monitor the changes
def password_length_check(*args):
    password = password_var.get()  # Get the current password from the StringVar
    if len(password) > 8:  # If the password exceeds 8 characters
        messagebox.showwarning("Warning", "Password must be exactly 8 characters.")
        password_var.set(password[:8])  # Limit the password to 8 characters

# Create the passwordEntry widget with the StringVar bound to it
passwordEntry = Entry(rightframe, width=30, font=('Microsoft Yahei UI Light', 15), fg='cornflowerblue',
                      bd=2, show='*', textvariable=password_var)
passwordEntry.place(x=24, y=309)

# Trace the changes in the password variable
password_var.trace("w", password_length_check)

# Updated password validation function
def validate_password(password, confirm_password):
    if len(password) > 8:
        return "Password must be exactly 8 characters."
    if len(password) < 8:
        return "Password must be at least 8 characters."
    if not any(char.isdigit() for char in password):
        return "Password must include at least one number."
    if not any(char.isalpha() for char in password):
        return "Password must include at least one letter."
    if password != confirm_password:
        return "Passwords do not match."
    return None

def signup_action():
    email = EmailEntry.get()
    username = usernameEntry.get()
    phone = phoneEntry.get()  # Get phone number
    password = passwordEntry.get()
    confirm_password = ConfirmpasswordEntry.get()

    if not email or not username or not phone or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required.")
        return

    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format.")
        return

    password_error = validate_password(password, confirm_password)
    if password_error:
        messagebox.showerror("Error", password_error)
        return

    if not check.get():
        messagebox.showwarning("Warning", "Please agree to our Terms & Conditions to proceed.")
        return

    # Placeholder for saving user data (e.g., into a database)
    messagebox.showinfo("Success", "You have successfully signed up!")

# Form UI
Label(rightframe, text='CREATE AN ACCOUNT', font=('Microsoft Yahei UI Light', 20, 'bold'),
      bg='#F0F0F0', fg='#001C4E').pack(pady=15)

Label(rightframe, text='Email:', font=('Microsoft Yahei UI Light', 15, 'bold'),
      bg='#F0F0F0', fg='#001C4E').place(x=20, y=67)
EmailEntry = Entry(rightframe, width=30, font=('Microsoft Yahei UI Light', 15), fg='cornflowerblue', bd=2)
EmailEntry.place(x=24, y=95)

Label(rightframe, text='Username:', font=('Microsoft Yahei UI Light', 15, 'bold'),
      bg='#F0F0F0', fg='#001C4E').place(x=20, y=137)
usernameEntry = Entry(rightframe, width=30, font=('Microsoft Yahei UI Light', 15), fg='cornflowerblue', bd=2)
usernameEntry.place(x=24, y=165)

# Phone number entry
Label(rightframe, text='Phone:', font=('Microsoft Yahei UI Light', 15, 'bold'),
      bg='#F0F0F0', fg='#001C4E').place(x=20, y=207)
phoneEntry = Entry(rightframe, width=30, font=('Microsoft Yahei UI Light', 15), fg='cornflowerblue', bd=2)
phoneEntry.place(x=24, y=235)

Label(rightframe, text='Password:', font=('Microsoft Yahei UI Light', 15, 'bold'),
      bg='#F0F0F0', fg='#001C4E').place(x=22, y=280)
passwordEntry = Entry(rightframe, width=30, font=('Microsoft Yahei UI Light', 15), fg='cornflowerblue',
                      bd=2, show='*', textvariable=password_var)
passwordEntry.place(x=24, y=309)

Label(rightframe, text='Confirm Password:', font=('Microsoft Yahei UI Light', 15, 'bold'),
      bg='#F0F0F0', fg='#001C4E').place(x=22, y=359)
ConfirmpasswordEntry = Entry(rightframe, width=30, font=('Microsoft Yahei UI Light', 15), fg='cornflowerblue',
                             bd=2, show='*', textvariable=confirm_password_var)
ConfirmpasswordEntry.place(x=24, y=388)

# Password toggle
open_eye = ImageTk.PhotoImage(Image.open("eye.png").resize((20, 20)))
closed_eye = ImageTk.PhotoImage(Image.open("hide.png").resize((20, 20)))

def toggle_password(entry, button, state):
    if state[0]:
        entry.config(show='*')
        button.config(image=closed_eye)
    else:
        entry.config(show='')
        button.config(image=open_eye)
    state[0] = not state[0]

password_toggle_state = [True]
toggle_button_password = Button(
    rightframe, image=closed_eye, bg='#FFFFFF', bd=1, activebackground='#F0F0F0',
    cursor='hand2', command=lambda: toggle_password(passwordEntry, toggle_button_password, password_toggle_state)
)
toggle_button_password.place(x=335, y=313)

confirm_password_toggle_state = [True]
toggle_button_confirm = Button(
    rightframe, image=closed_eye, bg='#FFFFFF', bd=1, activebackground='#F0F0F0',
    cursor='hand2', command=lambda: toggle_password(ConfirmpasswordEntry, toggle_button_confirm, confirm_password_toggle_state)
)
toggle_button_confirm.place(x=335, y=392)

# Terms & Conditions
check = IntVar()
Checkbutton(rightframe, text='I agree to the Terms & Conditions',
            font=('Microsoft Yahei UI Light', 9, 'bold'), bg='#F0F0F0', fg='#001C4E',
            cursor='hand2', variable=check).place(x=24, y=430)

# Signup Button
Button(rightframe, text='Sign Up', font=('Microsoft Yahei UI Light', 15, 'bold'),
       bg='#001C4E', width=20, fg='white', command=signup_action).place(x=80, y=470)

# Login Link with additional text
Label(rightframe, text="Already having an account?", font=('Microsoft Yahei UI Light', 12),
      bg='#F0F0F0', fg='#001C4E').place(x=53, y=523)

login_font = Font(family="Microsoft Yahei UI Light", size=12, weight="bold", underline=True)
Button(rightframe, text="Login", font=login_font, bg='#F0F0F0', fg='dodger blue',
       bd=0, cursor='hand2', command=open_login_page).place(x=270, y=520)

window.mainloop()
