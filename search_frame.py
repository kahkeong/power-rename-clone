import tkinter as tk

class SearchFrame(tk.Frame):
    def __init__(self, parentObject, background):
        tk.Frame.__init__(
            self, parentObject, background=background, relief=tk.RIDGE, borderwidth=10
        )
        self.grid(row=0, column=0, sticky="ew")
        self.columnconfigure(1, weight=1)

        self.lbl_critera = tk.Label(
            master=self, text="Enter the criteria below to rename the items"
        )
        self.lbl_critera.grid(row=0, column=0, sticky="w", columnspan=2)

        self.lbl_search = tk.Label(master=self, text="Search for:", bg="blue")
        self.lbl_search.grid(row=1, column=0, sticky="e")

        self.lbl_replace = tk.Label(master=self, text="Replace with:", bg="red")
        self.lbl_replace.grid(row=2, column=0, sticky="e")

        self.search_value = tk.StringVar()
        self.replace_value = tk.StringVar()

        self.search_value.trace_add("write", self.search_callback)
        self.replace_value.trace_add("write", self.replace_callback)

        entry_search = tk.Entry(master=self, textvariable=self.search_value)
        entry_search.grid(row=1, column=1, sticky="ew")

        entry_replace = tk.Entry(master=self, textvariable=self.replace_value)
        entry_replace.grid(row=2, column=1, sticky="ew")

    def search_callback(self,*args):
        print(self.search_value.get())


    def replace_callback(self,*args):
        print(self.replace_value.get())