import os, glob
import tkinter as tk
from PIL import ImageTk, Image
from shutil import copy

class ImageSort(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self,*args,**kwargs)

        self.image_dir = "images"
        self.script_dir = os.path.dirname(os.path.realpath('__file__'))
        self.my_dir = os.path.join(self.script_dir, self.image_dir)
        os.chdir(self.my_dir)

        self.file_list = []

        for f in os.listdir(self.my_dir):
            if f.endswith(".jpg"):
                self.file_list.append(os.path.join(self.my_dir, f))
            
        self.index = -1
        self.setup()
        self.display_next()

    def setup(self):
        self.bind('<KeyPress-f>', self.btn1_clicked)
        self.bind('<KeyPress-j>', self.btn2_clicked)

        self.lbl = tk.Label(self)
        self.lbl.grid(row = 0, column = 0)

        self.btn1 = tk.Button(self, text = "f = bad", command = self.btn1_clicked)
        self.btn1.grid(row = 1, column = 0, sticky = "w")
        self.btn2 = tk.Button(self, text = "j = good", command = self.btn2_clicked)
        self.btn2.grid(row = 1, column = 1)


    def btn1_clicked(self):
        try:
            self.dest = self.my_dir + '/output/bad'
            copy(self.f, self.dest)
            self.display_next()
        except ValueError:
            pass

    def btn2_clicked(self):
        try:
            self.dest = self.my_dir + '/output/good'
            copy(self.f, self.dest)
            self.display_next()
        except ValueError:
            pass

    def display_next(self):
        self.index += 1
        try:
            self.f = self.file_list[self.index]
        except IndexError:
            self.index = -1
            self.display_next()
            return

        self.img = Image.open(self.f)
        self.im = ImageTk.PhotoImage(self.img)
        self.lbl.config(image = self.im)
        self.lbl.image = self.im


if __name__ == "__main__":
    root = tk.Tk()
    my_app = ImageSort(root)
    my_app.grid(row = 0, column = 0)
    root.mainloop()