from tkinter import *
import pathlib


class PreviewFrame(Frame):
    def __init__(self, parentObject, background):
        Frame.__init__(self, parentObject, background=background, relief=RIDGE, borderwidth=10)
        self.canvas = Canvas(
            self, borderwidth=0, background=background, highlightthickness=0
        )
        self.internal_frame = Frame(self.canvas, background=background)
        self.vsb = Scrollbar(
            self, orient="vertical", command=self.canvas.yview, background=background
        )

        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)
        self.vsb.grid(row=0, column=1, sticky=N + S)
        self.window = self.canvas.create_window(
            0, 0, window=self.internal_frame, anchor="nw", tags="self.internal_frame"
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)
        self.internal_frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

    def onMouseWheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def onFrameConfigure(self, event):
        # Reset the scroll region to encompass the inner internal_frame
        print("onFrameConfigure")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event):
        # Resize the inner internal_frame to match the canvas
        print("onConvasConfigure")
        minHeight = self.internal_frame.winfo_reqheight()


        if self.winfo_height() >= minHeight:
            newHeight = self.winfo_height()
            # Hide the scrollbar when not needed
            self.vsb.grid_remove()
        else:
            newHeight = minHeight
            # Show the scrollbar when needed
            self.vsb.grid()

        self.canvas.itemconfig(self.window, height=newHeight)


class ItemList(object):
    def __init__(self, scrollFrame, innerFrame):
        self.widget_list = []
        self.innerFrame = innerFrame
        self.scrollFrame = scrollFrame

        # Keep a dummy empty row if the list is empty
        self.placeholder = Label(self.innerFrame, text=" ")
        self.placeholder.grid(row=0, column=0)

    # add new entry and update layout
    def add_item(self, text, level):
        self.placeholder.grid_remove()
        # create var to represent states
        int_var = IntVar()

        cb = Checkbutton(self.innerFrame, text=text, variable=int_var)
        cb.grid(
            row=self.innerFrame.grid_size()[1],
            column=0,
            ipadx=(20 * level,),
            pady=1,
            sticky="w",
        )
        self.widget_list.append(cb)

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
    root = Tk()  # Makes the window
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.wm_title("Title")  # Makes the title that will appear in the top left
    root.config(background=deviceBkgColor)

    preview_frame = PreviewFrame(root, background=deviceBkgColor)
    preview_frame.grid(row=0, column=0, sticky="nsew")

    item_list = ItemList(preview_frame, preview_frame.internal_frame)
    item_list.populate()


    root.mainloop()  