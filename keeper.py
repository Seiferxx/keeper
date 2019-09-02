#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import ascii_lowercase, digits, punctuation
# from shutil import copyfile
from datetime import date
from hashlib import md5
from random import choice
from tkinter import Listbox, Tk, Frame, Text, Toplevel, Label, ttk
from tkinter import Button, StringVar
from tkinter import GROOVE, BOTH, LEFT, RIGHT, END, WORD, BOTTOM, X
from tkinter import NONE, FALSE, TOP


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


class UI:

    def __init__(self):
        self.notes = []
        self.init_ui()

    def add_note(self):
        note = Note()
        note.id = get_md5_hash(get_random_string(4))
        note.title = ''
        note.date = date.today()
        note.content = ''
        self.notes.append(note)
        self.listbox.insert(END, note.id + ' ' + str(note.date))
        self.listbox.selection_clear(0, END)
        self.listbox.select_set(END)
        self.listbox.event_generate("<<ListboxSelect>>")

    def select_note(self, event):
        note = self.notes[self.listbox.curselection()[0]]
        self.textbox_label_var.set(note.id + ' ' + str(note.date) + ' ' + note.title)
        self.textbox.delete('0.0', END)
        self.textbox.insert('0.0', note.content)

    def update_note_content(self, event):
        if self.notes:
            note = self.notes[self.listbox.curselection()[0]]
            note.content = self.textbox.get('0.0', END)

    def init_ui(self):
        self.window = Tk()
        self.window.title('Keeper')
        self.window.configure(background='#33312e')

        self.container = Frame(self.window)
        self.container.configure(bg='#33312e')

        self.note_content = Frame(self.container)
        self.note_content.configure(bg='#33312e')

        self.notes_panel = Frame(self.container)
        self.notes_panel.configure(bg='#33312e')

        self.listbox = Listbox(self.notes_panel)
        self.listbox.configure(font=SYS_FONT)
        self.listbox.configure(height=20)
        self.listbox.configure(width=30)
        self.listbox.configure(bg='#33312e')
        self.listbox.configure(fg='#aeaaa3')
        self.listbox.configure(selectbackground='#353844')
        self.listbox.configure(relief=GROOVE)
        self.listbox.configure(selectforeground='#b7c3db')
        self.listbox.configure(exportselection=FALSE)
        self.listbox.configure(activestyle=NONE)
        self.listbox.bind('<<ListboxSelect>>', self.select_note)

        self.textbox_label = Label(self.note_content)
        self.textbox_label_var = StringVar()
        self.textbox_label.configure(textvariable=self.textbox_label_var)
        self.textbox_label.configure(font=SYS_FONT)
        self.textbox_label.configure(bg='#f5e6c6')
        self.textbox_label.configure(fg='#494642')

        self.textbox = Text(self.note_content)
        self.textbox.configure(font=SYS_FONT)
        self.textbox.configure(height=20)
        self.textbox.configure(width=90)
        self.textbox.configure(bg='#f5e6c6')
        self.textbox.configure(fg='#494642')
        self.textbox.configure(insertbackground='#494642')
        self.textbox.configure(relief=GROOVE)
        self.textbox.configure(spacing1=1)
        self.textbox.configure(wrap=WORD)
        self.textbox.bind('<KeyPress>', self.update_note_content)

        self.button_add_note = Button(self.notes_panel)
        self.button_add_note.configure(text='+')
        self.button_add_note.configure(command=self.add_note)

        self.textbox_label.pack(side=TOP, fill=X, pady=5)
        self.textbox.pack()

        self.listbox.pack(padx=10)
        self.button_add_note.pack(side=BOTTOM, fill=X, padx=10, pady=5)

        self.notes_panel.pack(side=LEFT)
        self.note_content.pack()
        self.container.pack(padx=20, pady=20, fill=BOTH)

        self.window.mainloop()


ui = UI()
