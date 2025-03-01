from tkinter import ttk, messagebox
from tkinter import *
import webbrowser
import time
import speech_recognition
from pygame import mixer
from tkinter import Tk, PhotoImage
import os,sys

currenttime = time.strftime('%H:%M:%S')

def clock():
    global currenttime
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'    Time:{currenttime}')
    datetimeLabel.after(1000, clock)  # Updates every second

# Function to open WhatsApp Web
def Click():
    webbrowser.open('https://web.whatsapp.com/')

# Initialize the mixer for sound (music files should be in the same directory or provide full path)
mixer.init()

# Function to search based on selected option
def search():
    query = queryEntry.get()
    if query != '':
        if temp.get() == 'google':
            webbrowser.open(f'https://www.google.com/search?q={query}')
        elif temp.get() == 'tiktok':
            webbrowser.open(f'https://www.google.com/search?q=tiktok={query}')
        elif temp.get() == 'amazon':
            webbrowser.open(f'https://www.amazon.com/s?k={query}&ref=nb_sb_noss_1')
        elif temp.get() == 'kickass torrent':
            webbrowser.open(f'https://kickasstorrent.cr/usearch/={query}')
        elif temp.get() == 'alibaba':
            webbrowser.open(f'https://www.alibaba.com/trade/search?SearchText={query}')
        elif temp.get() == 'youtube':
            webbrowser.open(f'https://www.youtube.com/results?search_query={query}')
    else:
        messagebox.showerror('Warning', 'Sorry! There is nothing to be searched')

# Function to handle voice input and perform the search
def voice():
    mixer.music.load('music1.mp3')
    mixer.music.play()
    sr = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as m:
        try:
            sr.adjust_for_ambient_noise(m, duration=0.2)
            audio = sr.listen(m)
            message = sr.recognize_google(audio)
            mixer.music.load('music2.mp3')
            mixer.music.play()
            queryEntry.delete(0, END)
            queryEntry.insert(0, message)
            search()
        except Exception as e:
            messagebox.showerror('Error', f"An error occurred: {str(e)}")

# Initialize Tkinter root window
root = Tk()
root.geometry('680x100+200+200')
root.title('Deep Sight Universal Search Bar')
root.resizable(False, False)

# Setting an icon for the window (make sure the file is available in your directory)
icon_image = PhotoImage(file="mic.png")
root.iconphoto(True, icon_image)
root.config(bg='green4')

# Variable to store the selected search engine
temp = StringVar()

# Setting up styles for ttk widgets
style = ttk.Style()
style.theme_use('default')

# Title label
label = Label(root, text='Python Search Bar', font=('arial', 20, 'bold'), bg='green4')
label.place(x=220)

# Date and Time label (for displaying current time and date)
datetimeLabel = Label(root, font=('arial', 12, 'bold'), bg='green4', fg='white')
datetimeLabel.place(x=530, y=8)

# Connect label for WhatsApp
connectlabel = Label(root, text='Connect to WhatsApp', font=('arial', 10, 'bold'), bg='green4')
connectlabel.place(x=45, y=9)

# Query label
querylabel = Label(root, text='Query', font=('arial', 20, 'bold'), bg='green4')
querylabel.grid(row=0, column=0, pady=35)

# Entry for user query
queryEntry = Entry(root, width=45, font=('arial', 14, 'bold'), bd=2, relief=SUNKEN)
queryEntry.grid(row=0, column=1)

# Mic button
mic_icon = PhotoImage(file='mic.png') # Ensure this file exists in the same directory
mic_icon_btn = Button(root, image=mic_icon, bg='green4', bd=0, cursor='hand2', activebackground='green4', command=voice)
mic_icon_btn.grid(row=0, column=2, padx=5)

# Search button
search_image = PhotoImage(file='search.png')  # Ensure this file exists
searchbtn = Button(root, image=search_image, bg='green4', bd=0, cursor='hand2', activebackground='green4', command=search)
searchbtn.grid(row=0, column=3)

# WhatsApp button
whatspp_icon = PhotoImage(file='whatsapp-logo.png')  # Ensure this file exists
whatsappbtn = Button(root, image=whatspp_icon, font=('arial', 15, 'bold'), bg='green4', bd=0, activebackground='green4', cursor='hand2', command=Click)
whatsappbtn.place(x=10, y=2)

# Radio buttons for search engine selection
googleRadioButton = ttk.Radiobutton(root, text='Google', value='google', variable=temp, cursor='hand2')
googleRadioButton.place(x=85, y=75)

TiktokRadioButton = ttk.Radiobutton(root, text='Tiktok', value='tiktok', variable=temp, cursor='hand2')
TiktokRadioButton.place(x=160, y=75)

AmazonRadioButton = ttk.Radiobutton(root, text='Amazon', value='amazon', variable=temp, cursor='hand2')
AmazonRadioButton.place(x=230, y=75)

AlibabaRadioButton = ttk.Radiobutton(root, text='Alibaba', value='alibaba', variable=temp, cursor='hand2')
AlibabaRadioButton.place(x=310, y=75)

Kickass_TorrentRadioButton = ttk.Radiobutton(root, text='Softwares/Movies', value='kickass torrent', variable=temp, cursor='hand2')
Kickass_TorrentRadioButton.place(x=390, y=75)

YoutubeRadioButton = ttk.Radiobutton(root, text='Youtube', value='youtube', variable=temp, cursor='hand2')
YoutubeRadioButton.place(x=518, y=75)

# Binding Enter key to search
def enter_function(value):
    searchbtn.invoke()

root.bind('<Return>', enter_function)

# Default search engine
temp.set('google')

# Start clock function to display date and time
clock()

# Main loop to run the application
root.mainloop()
