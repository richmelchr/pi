from tkinter import *

root = Tk()

topFrame = Frame(root)
botFrame = Frame(root)

topFrame.pack(side=TOP)
botFrame.pack(side=BOTTOM)

button1 = Button(topFrame, text="one")
button2 = Button(topFrame, text="two")
button3 = Button(botFrame, text="three")
button4 = Button(botFrame, text="four")

button1.config(height=10, width=30)
button2.config(height=10, width=30)
button3.config(height=10, width=30)
button4.config(height=10, width=30)

button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=LEFT)

root.mainloop()
