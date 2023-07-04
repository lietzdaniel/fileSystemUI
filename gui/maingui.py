import tkinter as tk
import os



from ..getinfo.folderinfo import returnItems



if __name__ == "__main__":  

    window = tk.Tk()
    window.title("Filesystem GUI")

    label = tk.Label(window, text="Welcome to the Filesystem GUI", fg="white", bg="#1E1E1E")
    label.pack()
    
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox = tk.Listbox(window, yscrollcommand=scrollbar.set)
    
    for file in returnItems(os.getcwd()):
        listbox.insert(tk.END,file[0])
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)
    window.configure(bg="#1E1E1E") 
    scrollbar.config(command=listbox.yview)
    window.mainloop()