import tkinter as tk


class SearchFrame(tk.LabelFrame):
    def __init__(self, parentObject, background):
        tk.LabelFrame.__init__(
            self,
            parentObject,
            text="Enter the criteria below to rename the items",
            # background=background,
            relief=tk.GROOVE,
            borderwidth=5,
        )
        self.grid(row=0, column=0, sticky="ew", pady=10, padx=10)
        self.columnconfigure(1, weight=1)

        self.lbl_search = tk.Label(master=self, text="Search for:")
        self.lbl_search.grid(row=1, column=0, sticky="e", ipady=5, padx=(10, 0))

        self.lbl_replace = tk.Label(master=self, text="Replace with:")
        self.lbl_replace.grid(row=2, column=0, sticky="e", ipady=5, padx=(10, 0))

        self.search_value = tk.StringVar()
        self.replace_value = tk.StringVar()

        self.search_value.trace_add("write", self.search_callback)
        self.replace_value.trace_add("write", self.replace_callback)

        entry_search = tk.Entry(master=self, textvariable=self.search_value)
        entry_search.grid(row=1, column=1, sticky="ew", padx=(0, 10))

        entry_replace = tk.Entry(master=self, textvariable=self.replace_value)
        entry_replace.grid(row=2, column=1, sticky="ew", padx=(0, 10))

    def search_callback(self, *args):
        print(self.search_value.get())

    def replace_callback(self, *args):
        print(self.replace_value.get())