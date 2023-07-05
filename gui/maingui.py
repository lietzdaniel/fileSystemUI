import tkinter as tk
import os
from tkinter import ttk
from .folderinfo import returnItems
from .datatypes import Bytes
import webbrowser

class fileGui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Filesystem GUI")
        self.tree = ttk.Treeview(self.window)
        self.tree.bind("<Double-Button-1>", self.item_double_clicked)
        self.undoStack = []
        self.redoStack = []
        self.curDir = os.getcwd() #TODO: Update to root?
        self.back_button = tk.Button( self.window, text="Back", command=self.go_back)
        self.back_button.pack(side=tk.LEFT)
        self.back_button.configure(state='disabled')
        
        self.forward_button = tk.Button( self.window, text="Forward", command=self.go_forward)
        self.forward_button.pack(side=tk.LEFT)
        self.forward_button.configure(state='disabled')
        
    def buildTree(self):
        for file in returnItems(self.curDir):
            fileName, fileSize, lastModified = file[0], file[1], file[2]
            id = self.tree.insert("", tk.END, values=(fileName, fileSize, lastModified))



    def item_double_clicked(self,event):
        item = self.tree.focus()
        if item:
            item_text = self.tree.item(item,"values")
            newDir = os.path.join(self.curDir,item_text[0])
            if os.path.isfile(newDir):
                #TODO Does this work on Windows?
                webbrowser.open(newDir)
            else:
                
                self.undoStack.append((self.curDir,[self.tree.item(x) for x in self.tree.get_children()]))
                self.curDir = os.path.join(self.curDir,item_text[0])
                self.back_button.configure(state='active')
                self.forward_button.configure(state='disabled')
                self.redoStack = []
                self.reset_tree()
                self.buildTree()

                
            

    def sort_by_column(self, column, descending):
        data = [
            (self.tree.set(child, column), child)
            for child in self.tree.get_children("")
        ]
        if column == "file_size":
            data.sort(
                reverse=descending,
                key=lambda x: float(x[0].split(" ")[0])
                * (1000 ** (Bytes[x[0].split(" ")[1]].value)),
            )

        else:
            data.sort(reverse=descending)
        for index, (_, child) in enumerate(data):
            self.tree.move(child, "", index)

    def go_back(self):
        print(self.curDir)
        oldState = self.undoStack.pop()
        if len(self.undoStack) == 0:
            self.back_button.configure(state='disabled')
        self.redoStack.append((self.curDir,[self.tree.item(x) for x in self.tree.get_children()])) 
       
        self.reset_tree()
        for item in oldState[1]:
            self.tree.insert('', tk.END, **item)
        self.curDir = oldState[0]
        self.forward_button.config(state='active')  
        print(self.curDir)
        

    def go_forward(self):
        oldState = self.redoStack.pop()
        if len(self.redoStack) == 0:
            self.forward_button.config(state='disabled')
        self.undoStack.append((self.curDir,[self.tree.item(x) for x in self.tree.get_children()]))
        self.reset_tree()
        for item in oldState[1]:
            self.tree.insert('', tk.END, **item)
        self.curDir = oldState[0]
        self.back_button.config(state='active')
        
        print(self.curDir)

    def reset_tree(self):
        self.tree.delete(*self.tree.get_children())  # Delete all items
        
    def on_column_click(self, column):
        descending = False
        if column == self.tree.previous_sort_column:
            descending = not self.tree.previous_sort_descending

        self.sort_by_column(column, descending)
        self.tree.heading(column, command=lambda: self.on_column_click(column))
        self.tree.previous_sort_column = column
        self.tree.previous_sort_descending = descending

    def runGui(self):
        self.tree["columns"] = ("file_name", "file_size", "last_modified")
        self.tree.heading("#0", text="", anchor="w")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.heading(
            "file_name",
            text="File Name",
            command=lambda: self.on_column_click("file_name"),
        )
        self.tree.heading(
            "file_size",
            text="File Size",
            command=lambda: self.on_column_click("file_size"),
        )
        self.tree.heading(
            "last_modified",
            text="Last Modified",
            command=lambda: self.on_column_click("last_modified"),
        )
        self.tree.previous_sort_column = "#0"
        self.tree.previous_sort_descending = False
        scrollbar = ttk.Scrollbar(
            self.window, orient="vertical", command=self.tree.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        for file in returnItems(os.getcwd()):
            fileName, fileSize, lastModified = file[0], file[1], file[2]
            id = self.tree.insert("", tk.END, values=(fileName, fileSize, lastModified))

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.window.mainloop()
