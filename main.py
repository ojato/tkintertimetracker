#!/usr/bin/python3

import tkinter # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
top = tkinter.Tk()
# Code to add widgets will go here...
top.mainloop()

def output(l):
    with open("output.csv","w") as f:
        for x in l:
            f.write(",".join(x)+"\n")
        

#design:
#question:
#radio buttons
#other, freefrom text
#produces csv with question,answer
