"""Get all JPEG images from a folder given on the command line.
The user copies each image to a different folder using a UI."""

import sys, os, glob, re
import tkinter as tk
from PIL import ImageTk, Image
from shutil import copy


class ImageSort(tk.Frame):
    """
    Takes a Tkinter Frame object and a folder given in command line.
    Builds the UI and allows user to copy images to new folders.
    """
    def __init__(self, *args, **kwargs):
        """
        Sets up the class for the user.
        """
        tk.Frame.__init__(self, *args, **kwargs)
        self.input_dir = self.check_input_dir(sys.argv)
        self.make_output_dirs(self.input_dir)
        self.index = -1
        self.file_list, self.f = self.get_images(self.input_dir)
        self.lbl = tk.Label(self)
        self.setup_grid()
        self.display_next(self.file_list)

    def check_input_dir(self, argv):
        """
        Takes an argument and checks if it's a folder that exists.
        """
        if len(argv) == 1:
            raise ValueError("Must provide a folder!")
        elif len(argv) > 2:
            raise ValueError("Only one folder allowed!")
        elif not os.path.exists(argv[1]):
            raise ValueError("Image folder does not exist: " + argv[1])
        else:
            print("Status: Input folder confirmed")
        return argv[1]

    def make_output_dirs(self, input_dir):
        """
        Create 3 output folders: bad, good, and neutral.
        """
        self.bad_dir = input_dir + '/bad'
        self.good_dir = input_dir + '/good'
        self.neutral_dir = input_dir + '/neutral'
        all_dirs = [self.bad_dir, self.good_dir, self.neutral_dir]
        
        for sdir in all_dirs:
            if not os.path.exists(sdir):
                os.makedirs(sdir)
        print("Status: Output folders confirmed")
    
    def get_images(self, input_dir):
        """
        Takes a folder path and returns a list of JPEG images.
        """
        flist = []
        for f in os.listdir(input_dir):
            if f.endswith(".jpg"):
                flist.append(os.path.join(input_dir, f))
        if not flist:
            print("Could not find JPEG images in input folder!")
            sys.exit(0)
        flist.sort(key=natural_keys)
        f = flist[self.index]
        print("Status: Got images from input folder")
        return flist, f

    def setup_grid(self):
        """
        Setup Tkinter grid.
        """
        self.bind('<KeyPress-f>', lambda event: self.keypress(output_dir=self.bad_dir))
        self.bind('<KeyPress-j>', lambda event: self.keypress(output_dir=self.good_dir))
        self.bind('<space>', lambda event: self.keypress(output_dir=self.neutral_dir))
        self.lbl.grid(row = 0, column = 0)
        self.key1 = tk.Button(self, text = "f = bad", command = self.keypress)
        self.key1.grid(row = 1, column = 0, sticky = "w")
        self.key2 = tk.Button(self, text = "j = good", command = self.keypress)
        self.key2.grid(row = 1, column = 2)
        self.key3 = tk.Button(self, text = "spacebar = neutral", command = self.keypress)
        self.key3.grid(row = 1, column = 1)
        self.focus_set()

    def keypress(self, output_dir, *args):
        """Button action."""
        try:
            dest = output_dir
            copy(self.f, dest)
            print(self.f + " copied to: " + dest)
            self.display_next(self.file_list)
        except ValueError:
            pass

    def display_next(self, file_list):
        """
        Display next image.
        """
        self.index += 1
        try:
            self.f = self.file_list[self.index]
        except IndexError:
            self.index = -1
            self.display_next(self.file_list)
            return

        self.img = Image.open(self.f)
        self.resize_image(self)
        self.im = ImageTk.PhotoImage(self.img)
        self.lbl.config(image = self.im)
        self.lbl.image = self.im
    
    def resize_image(self, *args):
        """
        If image is larger than 1080x720, reduce its size by half for display.
        """
        width, height = self.img.size
        if width > 1080 or height > 720:
            width, height = int(width / 2), int(height / 2)
            self.img = self.img.resize((width, height), Image.ANTIALIAS)
            self.resize_image(self)
        else:
            return


def atoi(text):
    """
    Takes a string which represents an integer and returns its value.

    Arguments:
        text: A string.

    Returns:
        An integer or a string.
    """
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    Takes a list and performs a natural alphanumeric sort.

    Arguments:
        text: A list.

    Returns:
        A sorted list.
    """
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


if __name__ == "__main__":
    root = tk.Tk()
    my_app = ImageSort(root)
    my_app.grid(row = 0, column = 0)
    root.mainloop()