from tkinter import *

root = Tk()

# Creating a Label Widget
myLabel1 = Label(root, text="Hello World").grid(row=1, column=0)
myLabel2 = Label(root, text="Nice to meet you").grid(row=1, column=5)

# Shoving it onto the screen
#myLabel1.grid(row=1, column=0)
#myLabel2.grid(row=1, column=5)

root.mainloop()
