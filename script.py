from tkinter import *
from screeninfo import get_monitors
from dragonfly import Window
import json
import math
from subprocess import call
import os

data = []

def setup_file():
	if not os.path.exists("D:\\win-collection\\collections.dat"):
		f = open("D:\\win-collection\\collections.dat", "w+")
		f.write("[]")
		f.close()
	f = open("D:\\win-collection\\collections.dat", "r")
	data = json.load(f)
	f.close()

def window_main():
    master = Tk()
    master.title("")

    Label(master, text="Select Collection To Open:").grid(row=0, columnspan=2)
    listbox = Listbox(master)
    listbox.focus_set()
    for collection in data:
        listbox.insert(END, collection["name"])
    listbox.grid(row=1, columnspan=2)

    def launch():
        if listbox.curselection():
            selection = listbox.curselection()[0]

            collection = data[selection]
            print("Launching %s" % collection["name"])
            for process in collection["content"]:
                call(process)

    def create():
        master.destroy()
        window_create()

    def edit():
        if listbox.curselection():
            selection = listbox.curselection()[0]
            collection = data[selection]
            print("Editing %s" % collection["name"])
            master.destroy()
            window_edit(selection)

    def remove():
        if listbox.curselection():
            selection = listbox.curselection()[0]
            collection = data[selection]

            if(collection["content"] == []):
                listbox.delete(selection)

                data.remove(collection)
                save_state()

    Button(master, text="Launch Collection", command=launch).grid(row=2, columnspan=2, sticky="news")
    master.bind("<r>", (lambda event: launch()))
    Button(master, text="Create Collection", command=create).grid(row=3, column=0, sticky="news")
    master.bind("<+>", (lambda event: create()))
    Button(master, text="Edit Collection", command=edit).grid(row=3, column=1, sticky="news")
    master.bind("<Return>", (lambda event: edit()))
    master.bind("<Delete>", (lambda event: remove()))

    master.bind("<Escape>", (lambda event: master.destroy()))

    set_position(master)
    master.focus_force()
    master.mainloop()

def window_edit(id):
    collection = data[id]
    
    master = Tk()
    master.title("")

    Label(master, text="Select Collection To Open:\nIf No Processes Are Entered, Press Remove To Delete Collecion").grid(row=0, columnspan=2)
    listbox = Listbox(master)
    listbox.focus_set()
    listbox.config(width=0)
    for process in collection["content"]:
        listbox.insert(END, process)
    listbox.grid(row=1, columnspan=2)

    def add():
        master.destroy()
        window_add(id)

    def remove():
        if listbox.size() > 0:
            if listbox.curselection():
                selection = listbox.curselection()[0]
                process = collection["content"][selection]
                listbox.delete(selection)

                data[id]["content"].remove(process)
                save_state()
        else:
            data.remove(collection)
            save_state()

            master.destroy()
            window_main()

    def cancel():
        master.destroy()
        window_main()

    Button(master, text="Add", command=add).grid(row=2, column=0, sticky="news")
    master.bind("<+>", (lambda event: add()))
    Button(master, text="Remove", command=remove).grid(row=2, column=1, sticky="news")
    master.bind("<Delete>", (lambda event: remove()))
    Button(master, text="Cancel", command=cancel).grid(row=3, columnspan=2, sticky="news")
    master.bind("<Escape>", (lambda event: cancel()))

    set_position(master)
    master.focus_force()
    master.mainloop()

def window_add(id):
    master = Tk()

    Label(master, text="Select Process To Add:").grid(row=0, columnspan=2)

    listbox = Listbox(master)
    listbox.focus_set()

    arr = []
    for window in Window.get_all_windows():
        if window.title != "" and window.is_visible:
            arr.append(window)

    for window in arr:
        listbox.insert(END, window.title)
        
    listbox.grid(row=1, columnspan=2)

    def add():
        if listbox.curselection():
            window = arr[listbox.curselection()[0]]

            data[id]["content"].append(window.executable)
            save_state()
            master.destroy()
            window_edit(id)

    def cancel():
        master.destroy()
        window_edit(id)

    Button(master, text="Add", command=add).grid(row=2, columnspan=2, sticky="news")
    master.bind("<Return>", (lambda event: add()))
    Button(master, text="Cancel", command=cancel).grid(row=3, columnspan=2, sticky="news")
    master.bind("<Escape>", (lambda event: cancel()))

    set_position(master)
    master.focus_force()
    master.mainloop()

def window_create():
    master = Tk()
    master.title("")

    name = Entry(master)
    name.focus_set()
    name.grid(row=0)

    def create():
        if name.get():
            data.append({"name": name.get(), "content":[]})
            save_state()

            master.destroy()
            window_main()
    def cancel():
        master.destroy()
        window_main()

    Button(master, text="Create", command=create).grid(row=1, sticky="news")
    master.bind("<Return>", (lambda event: create()))
    Button(master, text="Cancel", command=cancel).grid(row=2, sticky="news")
    master.bind("<Escape>", (lambda event: cancel()))

    set_position(master)
    master.focus_force()
    master.mainloop()

def save_state():
    f = open("D:\\win-collection\\collections.dat", "w")
    f.write(json.dumps(data))
    f.close()

def set_position(window):
    w = window.winfo_reqwidth()
    h = window.winfo_reqheight()
    W = get_monitors()[0].width
    H = get_monitors()[0].height

    window.geometry("+%s+%s" % (
        math.floor((W - w) / 2),
        math.floor((H - h) / 2)
    ))

if __name__ == "__main__":
	setup_file()
	window_main()