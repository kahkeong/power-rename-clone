import tkinter as tk
from preview_frame import PreviewFrame, ItemList

from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import Text


window = tk.Tk()
window.title("PowerRename Clone")

window.columnconfigure(0, minsize=300, weight=1)
window.rowconfigure(2, minsize=300, weight=1)

# search frame
frame_search = tk.Frame(
    master=window, bg="green", relief=tk.RIDGE, borderwidth=10, pady=10, padx=20
)
frame_search.columnconfigure(1, weight=1)
frame_search.grid(row=0, column=0, sticky="ew")

lbl_critera = tk.Label(
    master=frame_search, text="Enter the criteria below to rename the items"
)
lbl_critera.grid(row=0, column=0, sticky="w", columnspan=2)

lbl_search = tk.Label(master=frame_search, text="Search for:", bg="blue")
lbl_search.grid(row=1, column=0, sticky="e")

lbl_replace = tk.Label(master=frame_search, text="Replace with:", bg="red")
lbl_replace.grid(row=2, column=0, sticky="e")

entry_search = tk.Entry(master=frame_search)
entry_search.grid(row=1, column=1, sticky="ew")

entry_replace = tk.Entry(master=frame_search)
entry_replace.grid(row=2, column=1, sticky="ew")


# option frame
frame_option = tk.Frame(master=window, bg="purple", relief=tk.RIDGE, borderwidth=10)
frame_option.grid(row=1, column=0, sticky="ew")

lbl_options = tk.Label(master=frame_option, text="Options")
lbl_options.grid(row=0, column=0, columnspan=2, sticky="w")

alist = [
    "Use Regular Expressions",
    "Match All Occurences",
    "Case Sensitive",
    "Enumerate Items",
    "Item name Only",
    "Item Extension Only",
    "Exclude Folders",
    "Exclude Files",
    "Exclude Subfolder Items",
    "Make Uppercase",
    "Make Lowercase",
    "Make Titlecase",
]


def test():
    print("ha")
    # btn_new.


values = []
for index, name in enumerate(alist[:6]):
    value = tk.IntVar()
    btn_new = tk.Checkbutton(master=frame_option, text=name, variable=value)
    btn_new.grid(row=index + 1, column=0, sticky="w")
    values.append(value)


for index, name in enumerate(alist[6:]):
    value = tk.IntVar()
    btn_new = tk.Checkbutton(master=frame_option, text=name, variable=value)
    btn_new.grid(row=index + 1, column=1, sticky="w")
    values.append(value)

# preview frame
frame_preview1 = PreviewFrame(parentObject=window, background="brown")
frame_preview1.grid(row=2, column=0, sticky="nsew")
item_list = ItemList(frame_preview1, frame_preview1.internal_frame)
item_list.populate()

# frame_preview = tk.Frame(master=window, bg="pink", relief=tk.RIDGE, borderwidth=10)
# frame_preview.grid(row=2, column=0, sticky="nsew")


# lbl_preview = tk.Label(master=frame_preview, text="Preview")
# lbl_preview.grid(row=2, columnspan=2, sticky="w")

# scroll_bar = tk.Scrollbar(master=frame_preview)
# scroll_bar.grid(row=0, column=0, sticky="nsew")

# bottom bar frame
frame_bottom_bar = tk.Frame(master=window, bg="yellow", relief=tk.RIDGE, borderwidth=10)
frame_bottom_bar.grid(row=3, column=0, sticky="ew")
frame_bottom_bar.columnconfigure(0, weight=1)

lbl_items_selected = tk.Label(master=frame_bottom_bar, text="Items Selected:")
lbl_items_selected.grid(row=0, column=0, sticky="w")

lbl_items_renaming = tk.Label(master=frame_bottom_bar, text="Items Renaming:")
lbl_items_renaming.grid(row=1, column=0, sticky="w")


btn_rename = tk.Button(
    master=frame_bottom_bar,
    text="Rename",
    width=10,
)
btn_rename.grid(row=0, column=1, sticky="e", rowspan=2, padx=10)


def checking():
    for index, value in enumerate(values):
        print(alist[index], value.get())


btn_help = tk.Button(master=frame_bottom_bar, text="Help", width=10, command=checking)
btn_help.grid(row=0, column=2, sticky="e", rowspan=2, padx=10)

btn_cancel = tk.Button(master=frame_bottom_bar, text="Cancel", width=10)
btn_cancel.grid(row=0, column=3, sticky="e", rowspan=2, padx=10)

window.mainloop()