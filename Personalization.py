
from ttkbootstrap import *


class Entry_Placeholder(Entry):
    def __init__(self, *args, **kwargs):
        self.placeholder = kwargs.pop("placeholder", "")
        super().__init__(*args, **kwargs)

        self.insert("end", self.placeholder)
        self.bind("<FocusIn>", self.remove_placeholder)
        self.bind("<FocusOut>", self.add_placeholder)

    def remove_placeholder(self, event):
        if self.get() == self.placeholder:
            self.delete(0, "end")

    def add_placeholder(self, event):
        if self.placeholder and self.get() == "":
            self.config(show="")
            self.insert(0, self.placeholder)


class Entry_Placeholder_password(Entry):
    def __init__(self, master: Frame, *args, **kwargs):
        self.placeholder = kwargs.pop("placeholder", "")
        self.showpath = kwargs.pop("show_image", "")
        self.hidepath = kwargs.pop("hide_image", "")
        self.sw = True

        super().__init__(master=master, *args, **kwargs)
        self.show_im = ImageTk.PhotoImage(Image.open(self.showpath).resize((20, 20)))
        self.hide_im = ImageTk.PhotoImage(Image.open(self.hidepath).resize((20, 20)))

        self.grid_configure(row=0, column=0)
        self.b1 = Button(master=self.master, image=self.show_im, command=self.passcheck)
        self.b1.grid(row=0, column=1)

        self.insert("end", self.placeholder)
        self.bind("<FocusIn>", self.remove_placeholder)
        self.bind("<FocusOut>", self.add_placeholder)

    def remove_placeholder(self, event):
        if self.get() == self.placeholder:
            self.b1.config(image=self.show_im)
            self.delete(0, "end")
            self.config(show="*")
            self.sw = True

    def add_placeholder(self, event):
        if self.placeholder and self.get() == "":
            self.config(show="")
            self.insert(0, self.placeholder)
            self.sw = False

    def passcheck(self):
        if self.get() != self.placeholder:
            if self.sw:
                self.b1.config(image=self.hide_im)
                self.config(show="")
                self.sw = False
            elif not self.sw:
                self.b1.config(image=self.show_im)
                self.config(show="*")
                self.sw = True


if __name__ == "__main__":
    root = Window()

    password_entry = Entry_Placeholder(
        master=root,
        placeholder="Username",
    )
    password_entry.pack()

    f2 = Frame(root)
    password_entry = Entry_Placeholder_password(
        master=f2,
        placeholder="Password",
        show_image="image/show.png",
        hide_image="image/hide.png",
    )
    f2.pack()

    root.geometry("500x500")
    root.mainloop()
