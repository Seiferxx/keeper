#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import ascii_lowercase, digits, punctuation
# from shutil import copyfile
from hashlib import md5
from random import choice
from tkinter import Listbox, Tk, Frame, Text, Toplevel, Label, ttk
from tkinter import GROOVE, BOTH, LEFT, RIGHT, END, WORD
from tkinter import NONE, FALSE


SYS_FONT = ('Consolas', '10')


def get_random_string(str_length):
    characters = ascii_lowercase + digits + punctuation
    return ''.join(choice(characters) for i in range(str_length))


def get_md5_hash(str):
    return md5(str.encode()).hexdigest()


class Note:
    def __init__(self):
        self.id = ''
        self.title = ''
        self.date = ''
        self.content = ''

    def serialize(self):
        return self.id + '~' + self.title + '~' + self.date + '~' + self.content

    def deserialize(self, string):
        content = string.split('~')
        self.id = content[0]
        self.title = content[1]
        self.date = content[2]
        self.content = content[3]


class UI:

    def __init__(self):
        self.notes = []
        self.load_notes_from_files()
        self.init_ui()

    def handle_note_select(self, event):
        if(self.listbox.size() > 0):
            index = int(event.widget.curselection()[0])
            print(index)
            self.textbox.delete('0.0', END)
            self.textbox.insert('0.0', self.tasks[index-1].content)

    def popup_test(self, event):
        print('something')
        win = Toplevel()
        win.wm_title("Window")

        lx = Label(win, text="Input")
        lx.grid(row=0, column=0)

        b = ttk.Button(win, text="Okay", command=win.destroy)
        b.grid(row=1, column=0)

    def init_ui(self):
        self.window = Tk()
        self.window.title('Keeper')
        self.window.configure(background='#33312e')

        self.container = Frame(self.window)
        self.container.configure(bg='#33312e')

        self.listbox = Listbox(self.container)

        self.listbox.configure(font=SYS_FONT)
        self.listbox.configure(height=20)
        self.listbox.configure(width=25)
        self.listbox.configure(bg='#33312e')
        self.listbox.configure(fg='#aeaaa3')
        self.listbox.configure(selectbackground='#353844')
        self.listbox.configure(relief=GROOVE)
        self.listbox.configure(selectforeground='#b7c3db')
        self.listbox.configure(exportselection=FALSE)
        self.listbox.configure(activestyle=NONE)

        self.listbox.bind('<<ListboxSelect>>', self.handle_note_select)

        self.textbox = Text(self.container)

        self.textbox.configure(font=SYS_FONT)
        self.textbox.configure(height=20)
        self.textbox.configure(width=75)
        self.textbox.configure(bg='#f5e6c6')
        self.textbox.configure(fg='#494642')
        self.textbox.configure(insertbackground='#494642')
        self.textbox.configure(relief=GROOVE)
        self.textbox.configure(spacing1=1)
        self.textbox.configure(wrap=WORD)

        self.textbox.bind('<KeyPress>', self.popup_test)

        self.listbox.pack(side=LEFT, padx=10)
        self.textbox.pack(side=RIGHT)

        self.container.pack(padx=20, pady=20, fill=BOTH)

        self.window.mainloop()

    def load_notes_from_files(self):
        pass


ui = UI()
