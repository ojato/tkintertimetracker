import tkinter 
from tkinter.filedialog import askopenfilename

import os
import datetime

class Question:
    def __init__(self, question, option_list):
        self.question_text = question
        self.option_list = option_list
        self.selected_answer = None


class myApp:
    def __init__(self, ):
        self.times=[]
        self.root = tkinter.Tk()
        self.MenuBar = tkinter.Menu(self.root)
        self.FileMenu = tkinter.Menu(self.MenuBar, tearoff=0)
        self.MenuBar.add_cascade(label="File", menu=self.FileMenu)
        self.active_stuff = []
        self.tracking=False
        
        w = tkinter.Button(self.root, text="time", command=self.time)
        w.pack()
        #self.active_stuff.append(w)
        
        width = 600
        height = 400
        # center the window
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()

        left = (screenWidth / 2) - (width / 2)
        top = (screenHeight / 2) - (height / 2)

        self.root.geometry('%dx%d+%d+%d' % (width, height, left, top))
        self.root.config(menu=self.MenuBar)

        self.root.title("timetracker")
        self.root.wm_iconbitmap("Iconsmind-Outline-Stopwatch-2.ico")
        self.FileMenu.add_command(label="Open", command=self.openFile)
        
    def time(self):
        for x in self.active_stuff:
            x.pack_forget()
        self.times.append(datetime.datetime.now())
        #print()
        
        self.tracking = not self.tracking
        w = tkinter.Label(self.root, text="tracking - "+str(self.tracking)+" - since - "+self.times[-1].isoformat())
        w.pack()
        self.active_stuff.append(w)
        #I always start not tracking, so
        c = 0
        while c < len(self.times)-1:
            message = ""
            
            tracking_start=self.times[c]
            c += 1
            
            tracking_end=self.times[c]
            tracking_diff= tracking_end-tracking_start
            
            w = tkinter.Label(self.root, text="tracker was on for "+str(tracking_diff)+"\n start "+ tracking_start.isoformat()+"\n end "+tracking_end.isoformat())
            w.pack()
            self.active_stuff.append(w)
            c += 1
            
        
    def run(self):
        self.root.mainloop()

    def openFile(self):

        self.filename = askopenfilename(
            defaultextension=".txt", filetypes=[
                ("All Files", "*.*"), ("Text Documents", "*.txt")])

        if self.filename == "":
            self.filename = None
        else:
            # try to open the file
            # set the window title
            self.root.title(os.path.basename(self.filename) + "- Survey")
            
            with open(self.filename, "r") as f:
                text = f.read()
                
            self.load_questions_from_text(text)
            self.load_next_question()


if __name__ == "__main__":
    M = myApp()
    M.run()
