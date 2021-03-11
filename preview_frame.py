import tkinter as tk
import logging


class PreviewFrame(tk.LabelFrame):
    def __init__(self, item_list, parent_object):
        tk.LabelFrame.__init__(
            self,
            parent_object,
            text="Preview",
            relief=tk.GROOVE,
            borderwidth=5,
        )
        background = "white"

        self.item_list = item_list
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

        self.lbl_original = tk.Button(
            master=self.internal_frame,
            text="Original",
            bd=5,
            command=self.on_click_original,
        )
        self.lbl_original.grid(row=0, column=0, sticky="ew")

        self.lbl_renamed = tk.Button(
            master=self.internal_frame,
            text="Renamed",
            bd=5,
            command=self.on_click_renamed,
        )
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

        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.internal_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def on_click_original(self):
        logging.debug("called")
        self.item_list.update_show_checked_only()

    def on_click_renamed(self):
        logging.debug("called")
        self.item_list.update_show_renamed_only()

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_frame_configure(self, _event):
        # Reset the scroll region to encompass the inner internal_frame
        # print("on_frame_configure")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, _event):
        # Resize the inner frame to match the canvas
        min_width = self.internal_frame.winfo_reqwidth()
        min_height = self.internal_frame.winfo_reqheight()

        if self.winfo_width() >= min_width:
            new_width = self.winfo_width()
            # Hide the scrollbar when not needed
            # self.hsb.grid_remove()
        else:
            new_width = min_width
            # Show the scrollbar when needed
            # self.hsb.grid()

        if self.winfo_height() >= min_height:
            new_height = self.winfo_height()
            # Hide the scrollbar when not needed
            self.vsb.grid_remove()
        else:
            new_height = min_height
            # Show the scrollbar when needed
            self.vsb.grid()

        self.canvas.itemconfig(self.window, width=new_width, height=new_height)
