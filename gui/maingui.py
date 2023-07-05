import tkinter as tk
import os
from tkinter import ttk
from .folderinfo import returnItems
from .datatypes import Bytes


class fileGui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Filesystem GUI")
        self.tree = ttk.Treeview(self.window)

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

    def reset_tree(self):
        self.tree.delete(*self.tree.get_children())  # Delete all items
        columns = self.tree["columns"]
        for column in columns:
            self.tree.column(column, width=0)

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

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.window.mainloop()
