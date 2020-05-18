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
    def __init__(self, question_fn=None):
        self.questions = []
        self.question_index = 0
        self.root = tkinter.Tk()
        self.MenuBar = tkinter.Menu(self.root)
        self.FileMenu = tkinter.Menu(self.MenuBar, tearoff=0)
        self.MenuBar.add_cascade(label="File", menu=self.FileMenu)

        self.active_var = None

        width = 600
        height = 400
        # center the window
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()

        left = (screenWidth / 2) - (width / 2)
        top = (screenHeight / 2) - (height / 2)

        self.root.geometry('%dx%d+%d+%d' % (width, height, left, top))
        self.root.config(menu=self.MenuBar)

        self.root.title("Surveytool")
        self.FileMenu.add_command(label="Open", command=self.openFile)
        if question_fn is not None:
            with open(question_fn, "r") as f:
                string = f.read()
            self.load_questions_from_text(string)
            self.question_index = 0
            self.load_next_question()

    def run(self):
        self.root.mainloop()

    def load_questions_from_text(self, string):
        """
        input format is
        question?,answer,answer,answer

        other is always added at the end automatically.
        """

        string = string.split("\n")
        for line in string:
            if line == '':
                continue
            line = line.split(",")
            if len(line) <= 1:
                raise TypeError(
                    "I don't think that's a valid question:" + str(line))

            self.questions.append(Question(line[0], line[1:]))

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

    def build_question_window(self, question):
        #zero everything
        length = len(question.option_list)
        c = 0
        var = tkinter.IntVar()
        self.active_var = var
        self.active_stuff = []
        
        #this is the question
        w = tkinter.Label(self.root, text=question.question_text)
        w.pack()
        self.active_stuff.append(w)

        for option in question.option_list:
            # radiobutton
            w = tkinter.Radiobutton(
                self.root,
                text=option,
                variable=var,
                value=c,
            )
            
            w.pack()
            self.active_stuff.append(w)
            c += 1
        #another one for "other"
        w = tkinter.Radiobutton(
            self.root,
            text="other",
            variable=var,
            value=c,
        )
        w.pack()
        self.active_stuff.append(w)
        
        
        w = tkinter.Button(self.root, text="continue", command=self.done)
        w.pack()
        self.active_stuff.append(w)

    def done(self):
        value = self.active_var.get()
        answer = self.questions[self.question_index].option_list[value]
        self.questions[self.question_index].selected_answer = answer
        self.question_index += 1
        
        #this deletes the UI elements for the current question
        for x in self.active_stuff:
            x.pack_forget()
        self.load_next_question()

    def load_next_question(self):

        if self.question_index >= len(self.questions):
            # all done, collect outputs and zero everything
            self.output_answers()
            self.questions = []
            self.active_var = None
            self.question_index = 0
            w = tkinter.Label(self.root, text="all done")
            w.pack()
            self.active_stuff.append(w)
            return

        self.build_question_window(self.questions[self.question_index])

    def output_answers(self):
        """output format is
        question, given answer
        
        obviously only makes sense in connection with the input form
        """
        
        # append it, for easier data collection
        with open("output.csv", "a") as f:
            f.write("new entry," + datetime.datetime.now().isoformat() + "\n")
            for question in self.questions:
                f.write(
                    ",".join(
                        (question.question_text,
                         question.selected_answer)) +
                    "\n")


if __name__ == "__main__":
    M = myApp("test_question.txt")
    M.run()
