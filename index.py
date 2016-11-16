from Tkinter import *

class App:
    def __init__(self, win):
        win.minsize(width=750, height=500)
        win.maxsize(width=500, height=500)

        #main frame
        f = Frame(win, width=500, height=500, bd=1, relief=SUNKEN)

        #topbar frame
        topbar = Frame(f, width=499, bd=1, relief=SUNKEN)

        topbar.columnconfigure(0, weight=1)
        topbar.columnconfigure(1, weight=1)
        topbar.columnconfigure(2, weight=1)
        topbar.columnconfigure(3, weight=1)


        #frame for buttons in the left and right of the topbar
        leftbuttons = Frame(topbar, bd=1, relief=SUNKEN)
        rightbuttons = Frame(topbar, bd=1, relief=SUNKEN)

        #leftbuttons
        back = Button(leftbuttons, text="<", padx=5)
        forward = Button(leftbuttons, text=">", padx=5)
        up = Button(leftbuttons, text="up", padx=5)

        #rightbuttons
        index = Button(rightbuttons, text="?")
        maincontents = Button(rightbuttons, text="M")
        exit = Button(rightbuttons, text="X")

        rightbuttons.columnconfigure(0, weight=1)
        rightbuttons.columnconfigure(1, weight=1)
        rightbuttons.columnconfigure(2, weight=1)

        leftbuttons.columnconfigure(0, weight=1)
        leftbuttons.columnconfigure(1, weight=1)
        leftbuttons.columnconfigure(2, weight=1)

        #add buttons to leftbuttons frame
        back.grid(row=0, column=0)
        forward.grid(row=0, column=2)
        up.grid(row=0, column=1)

        #add buttons to rightbuttons frame
        index.grid(row=0, column=0)
        maincontents.grid(row=0, column=2)
        exit.grid(row=0, column=1)


        #end leftbuttons
        leftbuttons.grid(row=0, column=0)
        #end rightbuttons
        rightbuttons.grid(row=0, column=3)

        #end topbar
        topbar.pack(side=TOP)

        #end main frame
        f.pack()
        win.mainloop()

top = Tk()
app = App(top)
top.mainloop()
