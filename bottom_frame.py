import tkinter as tk

class BottomFrame(tk.Frame):
    def __init__(self, parentObject, background):
        tk.Frame.__init__(
            self, parentObject, background=background, relief=tk.RIDGE, borderwidth=10
        )
        self.grid(row=4, column=0, sticky="ew")
        self.grid_columnconfigure(0, weight=1)

        self.lbl_items_selected = tk.Label(master=self, text="Items Selected:")
        self.lbl_items_selected.grid(row=0, column=0, sticky="w")

        self.lbl_items_renaming = tk.Label(master=self, text="Items Renaming:")
        self.lbl_items_renaming.grid(row=1, column=0, sticky="w")

        self.btn_rename = tk.Button(
            master=self,
            text="Rename",
            width=10,
        )
        self.btn_rename.grid(row=0, column=1, sticky="e", rowspan=2, padx=10)

        self.btn_help = tk.Button(
            master=self, text="Help", width=10, command=self.go_online
        )
        self.btn_help.grid(row=0, column=2, sticky="e", rowspan=2, padx=10)

        self.btn_cancel = tk.Button(master=self, text="Cancel", width=10)
        self.btn_cancel.grid(row=0, column=3, sticky="e", rowspan=2, padx=10)

    def go_online(self):
        print("go online")
        pass