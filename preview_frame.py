import tkinter as tk
import pathlib
from tkinter.constants import GROOVE


class PreviewFrame(tk.LabelFrame):
    def __init__(self, parentObject, background):
        tk.LabelFrame.__init__(
            self,
            parentObject,
            text="Preview",
            # background=background,
            relief=GROOVE,
            borderwidth=5,
        )
        # update this
        background = "white"
        self.grid(row=2, column=0, sticky="nsew", ipadx=10, pady=10, padx=10)
        self.canvas = tk.Canvas(
            self,
            borderwidth=0,
            background=background,
            highlightthickness=0,
        )
        self.internal_frame = tk.Frame(self.canvas, background=background)
        self.vsb = tk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview, background=background
        )

        self.internal_frame.grid_columnconfigure(0, weight=1)
        self.internal_frame.grid_columnconfigure(1, weight=1)

        self.lbl_original = tk.Label(master=self.internal_frame, text="Original")
        self.lbl_original.grid(row=0, column=0, sticky="ew")

        self.lbl_renamed = tk.Button(master=self.internal_frame, text="Renamed", bd=5)
        self.lbl_renamed.grid(row=0, column=1, sticky="ew")

        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=2, sticky="ns")
        self.window = self.canvas.create_window(
            0,
            0,
            window=self.internal_frame,
            anchor="nw",
            tags="self.internal_frame",
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)
        self.internal_frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

    def onMouseWheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def onFrameConfigure(self, event):
        # Reset the scroll region to encompass the inner internal_frame
        # print("onFrameConfigure")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event):
        # Resize the inner frame to match the canvas
        minWidth = self.internal_frame.winfo_reqwidth()
        minHeight = self.internal_frame.winfo_reqheight()

        if self.winfo_width() >= minWidth:
            newWidth = self.winfo_width()
            # Hide the scrollbar when not needed
            # self.hsb.grid_remove()
        else:
            newWidth = minWidth
            # Show the scrollbar when needed
            # self.hsb.grid()

        if self.winfo_height() >= minHeight:
            newHeight = self.winfo_height()
            # Hide the scrollbar when not needed
            self.vsb.grid_remove()
        else:
            newHeight = minHeight
            # Show the scrollbar when needed
            self.vsb.grid()

        self.canvas.itemconfig(self.window, width=newWidth, height=newHeight)


class ItemList(object):
    def __init__(self, scrollFrame, innerFrame):
        self.widget_list = []
        self.widget_list2 = []
        self.innerFrame = innerFrame
        self.scrollFrame = scrollFrame

        # Keep a dummy empty row if the list is empty
        self.placeholder = tk.Label(self.innerFrame, text=" ")
        self.placeholder.grid(row=0, column=0)

    # add new entry and update layout
    def add_item(self, text, level):
        self.placeholder.grid_remove()
        # create var to represent states
        int_var = tk.IntVar()

        cb = tk.Checkbutton(self.innerFrame, text=text, variable=int_var, bg="yellow")
        cb.grid(
            row=len(self.widget_list) + 1,
            column=0,
            ipadx=(20 * level,),
            pady=1,
            sticky="w",
        )

        cb2 = tk.Checkbutton(self.innerFrame, text=text, variable=int_var, bg="green")
        cb2.grid(
            row=len(self.widget_list2) + 1,
            column=1,
            ipadx=(20 * level,),
            pady=1,
            sticky="w",
        )
        # print(self.innerFrame.grid_size())

        self.widget_list.append(cb)
        self.widget_list2.append(cb2)

    def populate(self):
        self.recursive(pathlib.Path("."), 0)
        self.innerFrame.update_idletasks()
        self.scrollFrame.onCanvasConfigure(None)

    def recursive(self, path, level):
        dir_list = [x for x in path.iterdir() if x.is_dir()]
        for item in dir_list:
            self.add_item(str(item.name), level)
            new_path = pathlib.Path(f"{item.resolve()}")
            self.recursive(new_path, level + 1)

        path_list = [x for x in path.iterdir() if x.is_file()]
        for item in path_list:
            self.add_item(str(item.name), level)


if __name__ == "__main__":
    deviceBkgColor = "#FFFFFF"
    # deviceBkgColor = None
    root = tk()  # Makes the window
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.wm_title("Title")  # Makes the title that will appear in the top left
    root.config(background=deviceBkgColor)

    preview_frame = PreviewFrame(root, background=deviceBkgColor)
    preview_frame.grid(row=0, column=0, sticky="nsew")

    item_list = ItemList(preview_frame, preview_frame.internal_frame)
    item_list.populate()

    root.mainloop()
