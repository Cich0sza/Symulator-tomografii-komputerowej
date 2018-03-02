from tkinter import *
from PIL import Image, ImageTk
from sinogram import Sinogram


class MainWindow:

    def __init__(self, image_name):
        self.sinogram = Sinogram(image_name, experimental=True)
        self.sinogram.prepare_animation()
        self.photo = None
        self.im = None

        self.root = Tk()
        self.root.resizable(0, 0)

        self.image = PhotoImage(file=image_name)
        self.original = Label(image=self.image).grid(row=0, column=0)

        self.sinogram_image = ImageTk.PhotoImage(image=Image.fromarray(self.sinogram.last_sinogram))
        self.sinogram_label = Label(image=self.sinogram_image).grid(row=0, column=1)

        self.canvas_output = Canvas(width=self.sinogram.width, height=self.sinogram.height)
        self.canvas_output.grid(row=0, column=2)

        self.mse_value = StringVar()
        mse_label = Label(textvariable=self.mse_value)
        mse_label.grid(row=1, column=1, sticky=W)

        self.root.after(0, self.start)
        self.root.mainloop()

    def start(self):
        if self.sinogram.animation_reverse():
            self.mse_value.set("RMSE: " + str(self.sinogram.calculate_mse()))
            self.im = Image.fromarray(self.sinogram.output_image)
            self.photo = ImageTk.PhotoImage(image=self.im)
            self.canvas_output.create_image(0, 0, image=self.photo, anchor=NW)
            self.root.update()
            self.root.after(50, self.start)


if __name__ == '__main__':
    x = MainWindow('Images_for_tests/test.png')
