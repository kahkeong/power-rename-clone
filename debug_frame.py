import tkinter as tk


class DebugFrame(tk.Frame):
    def __init__(self, item_list, parent_object, background):
        tk.Frame.__init__(
            self, parent_object, background=background, relief=tk.RIDGE, borderwidth=10
        )
        self.item_list = item_list
        self.grid(row=5, column=0, sticky="ew")

        btn_debug = tk.Button(
            master=self, text="Debug", width=10, command=self.debugging
        )
        btn_debug.grid(row=0, column=4, sticky="e", rowspan=2, padx=10)

    def debugging(self):
        for item in self.item_list.widget_list:
            print(item["text"])