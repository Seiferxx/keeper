#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import ascii_lowercase, digits, punctuation
# from shutil import copyfile
from os import listdir
from datetime import date
from hashlib import md5
from random import choice
from tkinter import Listbox, Tk, Frame, Text, Toplevel, Label, ttk, Menu
from tkinter import Button, StringVar, Entry
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
        self.modified = False


class UI:

    def __init__(self):
        self.notes = []
        self.init_ui()
        self.load_notes_from_directory()
        self.window.after(5000, self.save_notes_to_files)
        self.window.mainloop()

    def add_note(self):
        note = Note()
        note.id = get_md5_hash(get_random_string(4))
        note.title = 'New note'
        note.date = date.today()
        note.content = 'Sample content'
        with open(note.id + '.keeper', 'w') as file:
            file.write(note.title + '\n')
            file.write(str(note.date) + '\n')
            file.write(note.content)
        self.notes.append(note)
        self.note_title.set(note.title)
        self.listbox.insert(END, note.title + ' ' + str(note.date))
        self.listbox.selection_clear(0, END)
        self.listbox.select_set(END)
        self.listbox.event_generate("<<ListboxSelect>>")

    def save_notes_to_files(self):
        index = 0
        for note in self.notes:
            if note.modified:
                with open(note.id + '.keeper', 'w') as file:
                    file.write(note.title + '\n')
                    file.write(str(note.date) + '\n')
                    file.write(note.content)
                note.modified = False
                if(self.listbox.curselection()[0] == index):
                    self.textbox_label_var.set(str(note.date) + ' (Saved)')
            index += 1
        self.window.after(5000, self.save_notes_to_files)

    def load_notes_from_directory(self):
        for file_name in listdir('.'):
            if file_name.endswith(".keeper"):
                with open(file_name, 'r') as file:
                    note = Note()
                    note.id = file_name.split('.')[0]
                    note.title = file.readline().replace('\n', '')
                    note.date = date.fromisoformat(file.readline().replace('\n', ''))
                    note.content = ''
                    for line in file:
                        note.content += line
                    self.notes.append(note)
                    self.listbox.insert(END, note.title + ' ' + str(note.date))

    def select_note(self, event):
        if self.notes:
            note = self.notes[self.listbox.curselection()[0]]
            self.note_title.set(note.title)
            self.textbox_label_var.set(str(note.date) + (' (Modified)' if note.modified else ' (Saved)'))
            self.textbox.delete('0.0', END)
            self.textbox.insert('0.0', note.content)

    def update_note_content(self, event):
        if self.notes:
            note = self.notes[self.listbox.curselection()[0]]
            self.textbox_label_var.set(str(note.date) + ' (Modified)')
            note.content = self.textbox.get('0.0', END)
            note.modified = True

    def update_note_title(self, event):
        if self.notes:
            index = self.listbox.curselection()[0]
            note = self.notes[index]
            self.textbox_label_var.set(str(note.date) + ' (Modified)')
            note.modified = True
            note.title = self.note_title.get()
            self.listbox.delete(index)
            self.listbox.insert(index, note.title + ' ' + str(note.date))
            self.listbox.select_set(index)

    def create_password_window(self):
        passwords_window = Toplevel()
        passwords_window.wm_title("Paswords")

        lx = Label(passwords_window, text="Input")
        lx.grid(row=0, column=0)

        b = ttk.Button(passwords_window, text="Okay", command=passwords_window.destroy)
        b.grid(row=1, column=0)

    def init_ui(self):
        self.window = Tk()
        self.window.title('Keeper')
        self.window.configure(background='#33312e')

        self.main_menu = Menu(self.window)
        self.window.config(menu=self.main_menu)

        self.file_menu = Menu(self.main_menu)
        self.main_menu.add_cascade(label="Tools", menu=self.file_menu)
        self.file_menu.add_command(label="Passwords", command=self.create_password_window)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.window.quit)

        self.note_title = StringVar()
        self.textbox_label_var = StringVar()

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

        self.notes_title_container = Frame(self.note_content)
        self.notes_title_container.configure(bg='#33312e')

        self.textbox_label = Label(self.notes_title_container)
        self.textbox_label.configure(textvariable=self.textbox_label_var)
        self.textbox_label.configure(font=SYS_FONT)
        self.textbox_label.configure(bg='#f5e6c6')
        self.textbox_label.configure(fg='#494642')
        self.textbox_label.configure(width=23)

        self.note_title_entry = Entry(self.notes_title_container)
        self.note_title_entry.configure(width=65)
        self.note_title_entry.configure(font=SYS_FONT)
        self.note_title_entry.configure(textvariable=self.note_title)
        self.note_title_entry.bind('<KeyRelease>', self.update_note_title)

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
        self.textbox.bind('<KeyRelease>', self.update_note_content)

        self.button_add_note = Button(self.notes_panel)
        self.button_add_note.configure(text='+')
        self.button_add_note.configure(command=self.add_note)

        self.note_title_entry.pack(side=LEFT)
        self.textbox_label.pack(side=RIGHT)
        self.notes_title_container.pack(side=TOP, fill=X, pady=5)
        self.textbox.pack()

        self.listbox.pack(padx=10, pady=5)
        self.button_add_note.pack(side=BOTTOM, fill=X, padx=10)

        self.notes_panel.pack(side=LEFT)
        self.note_content.pack()
        self.container.pack(padx=20, pady=20, fill=BOTH)


ui = UI()
