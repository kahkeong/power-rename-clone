import tkinter as tk
import webbrowser


class BottomFrame(tk.Frame):
    def __init__(self, item_list, parent_object):
        tk.Frame.__init__(self, parent_object, borderwidth=5)
        self.parent_object = parent_object
        self.item_list = item_list

        self.grid(row=4, column=0, sticky="ew")
        self.grid_columnconfigure(0, weight=1)

        self.lbl_items_selected = tk.Label(master=self, text="Items Selected: -")
        self.lbl_items_selected.grid(row=0, column=0, sticky="w")

        self.lbl_items_renaming = tk.Label(master=self, text="Items Renaming: -")
        self.lbl_items_renaming.grid(row=1, column=0, sticky="w")

        self.btn_rename = tk.Button(
            master=self, text="Rename", width=10, command=self.rename
        )
        self.btn_rename.grid(row=0, column=1, sticky="e", rowspan=2, padx=10)

        self.btn_help = tk.Button(
            master=self,
            text="Help",
            width=10,
            command=self.open_power_rename_documentation,
        )
        self.btn_help.grid(row=0, column=2, sticky="e", rowspan=2, padx=10)

        self.btn_cancel = tk.Button(
            master=self, text="Cancel", width=10, command=self.close_application
        )
        self.btn_cancel.grid(row=0, column=3, sticky="e", rowspan=2, padx=10)
        self.update_btn_rename_state(0)

    def update_btn_rename_state(self, count):
        if count > 0:
            state = "normal"
        else:
            state = "disable"
        self.btn_rename["state"] = state

    def rename(self):
        self.item_list.rename()
        self.parent_object.destroy()

    def close_application(self):
        self.parent_object.destroy()

    def open_power_rename_documentation(self):
        webbrowser.open(
            "https://docs.microsoft.com/en-us/windows/powertoys/powerrename"
        )
