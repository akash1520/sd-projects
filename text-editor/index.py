
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror

filename = None

def newFile():
    global filename
    filename = "Untitled"
    text.delete('1.0', END)

def saveFile():
    global filename
    t = text.get('1.0', END)
    if filename is None:
        saveAs()
    else:
        with open(filename, 'w') as f:
            f.write(t)

def saveAs():
    global filename
    f = asksaveasfilename(defaultextension='.txt', filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if f:
        filename = f
        t = text.get('1.0', END)
        with open(filename, 'w') as file:
            file.write(t.rstrip())

def openFile():
    global filename
    f = askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if f:
        filename = f
        with open(filename, 'r') as file:
            t = file.read()
            text.delete('1.0', END)
            text.insert('1.0', t)

root = Tk()
root.title("My Python Text Editor")
root.minsize(width=500, height=500)
root.maxsize(width=600, height=600)

text = Text(root, width=500, height=500)
text.pack()

menubar = Menu(root)
filemenu = Menu(menubar)
filemenu.add_command(label="New", command=newFile)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_command(label="Save As", command=saveAs)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)

root.mainloop()

