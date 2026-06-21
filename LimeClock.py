from tkinter import *
from time import *

def update():
        time_string = strftime('%I:%M:%S %p')
        time_label.config(text=time_string)
        window.after(1000, update)

        day_strig = strftime('%A')
        day_label.config(text=day_strig)

        date_string = strftime('%d/%B/%Y')
        date_label.config(text=date_string)
window = Tk()
window.configure(background="black")
time_label = Label(window, font=("Times New Roman", 50),fg="lime",bg="black")
time_label.pack()
day_label = Label(window, font=("Times New Roman", 45),fg="white",bg="black")
day_label.pack()
date_label = Label(window, font=("Times New Roman", 40),fg="white",bg="black")
date_label.pack()
update()
window.mainloop()