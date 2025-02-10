import random

# Rock
Rock ="""
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
"""

# Paper
paper ="""
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
"""

# Scissors
scissors ="""
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""

computer=[Rock,paper,scissors]

user_input=int(input("\nChoose 0 for rock, 1 for paper and 2 for scissors\n"))

if user_input==0:
    print(f"You chose:\n{user_input}")
    print(Rock)

if user_input==1:
    print(f"You chose:\n{user_input}")
    print(paper)

if user_input==2:
    print(f"You chose:\n{user_input}")
    print(scissors)

computer_choice=random.randint(0,2)

if computer_choice==0:
    print(f"Computer chose:\n {computer_choice}")
    print(Rock)
if computer_choice==1:
    print(f"Computer chose:\n {computer_choice}")
    print(paper)
if computer_choice==2:
    print(f"Computer chose:\n {computer_choice}")
    print(scissors)

if user_input==computer_choice:
    print("It's a draw please try again next time")

if user_input==0 and computer_choice==1:
    print("You win!!!")

elif computer_choice==0 and user_input==1:
    print("You loose!!!")

elif user_input==1 and computer_choice==2:
    print("You loose!!!")
elif computer_choice==1 and user_input==2:
    print("You win!!!")
elif user_input==2 and computer_choice==0:
    print("You win!!!")
elif computer_choice==2 and user_input==0:
    print("You loose!!!")
if user_input>2:
    print("You entered an invalid choice you loose ---GAME OVER!!!---")


from tkinter import *
from PIL import ImageTk, Image
from tkinter.font import Font
from tkinter import messagebox
import re
import tkinter

# Initialize main window
window = Tk()
window.title('Signup Page')
window.resizable(False, False)
window.geometry('900x600+250+50')
window.config(bg='#4E5069')

window.iconphoto(False,tkinter.PhotoImage(file='purple-logo (1).png'))
# Create left frame for background image
leftframe = Frame(window)
leftframe.place(x=10, y=20, width=410, height=560)

# Image carousel
images = [ImageTk.PhotoImage(file=f'img ({i}).jpg') for i in range(1, 8)]
label = Label(leftframe, font='bold')
label.pack()
x = 0

def move():
    global x
    label.config(image=images[x])  # Update the image label with the new image
    x = (x + 1) % len(images)  # Update the index to the next image (looping around)
    if window.winfo_exists():  # Ensure the window still exists before scheduling the next call
        window.after(2500, move)  # Call move again in 2.5 seconds

move()  # Start the image carousel


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

def validate_password(password, confirm_password):
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
    password = passwordEntry.get()
    confirm_password = ConfirmpasswordEntry.get()

    if not email or not username or not password or not confirm_password:
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

Label(rightframe, text='Password:', font=('Microsoft Yahei UI Light', 15, 'bold'),
      bg='#F0F0F0', fg='#001C4E').place(x=22, y=210)
passwordEntry = Entry(rightframe, width=30, font=('Microsoft Yahei UI Light', 15), fg='cornflowerblue',
                      bd=2, show='*')
passwordEntry.place(x=24, y=239)

Label(rightframe, text='Confirm Password:', font=('Microsoft Yahei UI Light', 15, 'bold'),
      bg='#F0F0F0', fg='#001C4E').place(x=22, y=289)
ConfirmpasswordEntry = Entry(rightframe, width=30, font=('Microsoft Yahei UI Light', 15), fg='cornflowerblue',
                             bd=2, show='*')
ConfirmpasswordEntry.place(x=24, y=318)

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
toggle_button_password.place(x=335, y=243)

confirm_password_toggle_state = [True]
toggle_button_confirm = Button(
    rightframe, image=closed_eye, bg='#FFFFFF', bd=1, activebackground='#F0F0F0',
    cursor='hand2', command=lambda: toggle_password(ConfirmpasswordEntry, toggle_button_confirm, confirm_password_toggle_state)
)
toggle_button_confirm.place(x=335, y=322)

# Terms & Conditions
check = IntVar()
Checkbutton(rightframe, text='I agree to the Terms & Conditions',
            font=('Microsoft Yahei UI Light', 9, 'bold'), bg='#F0F0F0', fg='#001C4E',
            cursor='hand2', variable=check).place(x=24, y=360)

# Signup Button
Button(rightframe, text='Sign Up', font=('Microsoft Yahei UI Light', 15, 'bold'),
       bg='#001C4E', width=20, fg='white', command=signup_action).place(x=80, y=400)

# Login Link with additional text
Label(rightframe, text="Already having an account?", font=('Microsoft Yahei UI Light', 12),
      bg='#F0F0F0', fg='#001C4E').place(x=53, y=453)

login_font = Font(family="Microsoft Yahei UI Light", size=12, weight="bold", underline=True)
Button(rightframe, text="Login", font=login_font, bg='#F0F0F0', fg='dodger blue',
       bd=0, cursor='hand2', command=open_login_page).place(x=270, y=450)

window.mainloop()
