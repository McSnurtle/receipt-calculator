#src/utils/widgets.py
# imports
import platform
import tkinter as tk
from typing import Any
from .models import Receipt


class ReceiptPreview(tk.Frame):    
    def __init__(self, receipt: Receipt, edit_func: callable, del_func: callable, *args, **kwargs):
        """A horizontal tk.Frame widget showing a preview of a receipt"""
        super().__init__(*args, **kwargs)
        
        # vars
        self.receipt: Receipt = receipt
        self.delete: callable = del_func
        self.edit: callable = edit_func
        
        # layout
        info_frame: tk.Frame = tk.Frame(self)
        info_frame.pack(padx=5, pady=5, side=tk.LEFT)
        title_label: tk.Label = tk.Label(info_frame, text=self.receipt.name, font=("Arial", 18))
        title_label.pack(padx=5, pady=5, side=tk.TOP, anchor=tk.NW) # top left
        date_label: tk.Label = tk.Label(info_frame, text=self.receipt.date, font=("Arial", 10))
        date_label.pack(padx=5, pady=5, side=tk.BOTTOM, anchor=tk.SW)   # top left subheader
        
        control_frame: tk.Frame = tk.Frame(self)
        control_frame.pack(padx=5, pady=5, side=tk.RIGHT)
        delete_button: tk.Button = tk.Button(control_frame, text="🗑", command=self.delete)
        delete_button.pack(padx=5, pady=5, side=tk.RIGHT, anchor=tk.E)
        edit_button: tk.Button = tk.Button(control_frame, text="🖉", command=self.edit)
        edit_button.pack(padx=5, pady=5, side=tk.RIGHT, anchor=tk.E)


class PlaceholderEntry(tk.Entry):
    def __init__(self, master: tk.Widget | Any, placeholder: str = "", primary_colour: str = "#FFFFFF", secondary_colour: str = "#666666", *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        
        self._focused: bool = False
        self._placeholder: str = placeholder
        self._primary_colour: str = primary_colour
        self._secondary_colour: str = secondary_colour
        
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        
    def on_focus_in(self, callback: Any) -> None:
        """Removes the placeholder text and colour, or 'resets' the widget for typing in."""
        if self.get() is self._placeholder:
            self.delete(1.0, tk.END)
            self.config(fg=self._primary_colour)
            
    def on_focus_out(self, callback: Any) -> None:
        """If nothing has been written, shows the placeholder text and colour."""
        if self.get() is None:
            self.insert(1.0, self._placeholder)
            self.config(fg=self._secondary_colour)


class PopupEntry(tk.Toplevel):
    def __init__(self, master: tk.Widget | Any, title: str, message: str, placeholder: str, parent: tk.Widget, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        
        self.title(title)
        self.resizable(False, False)
        
        message: tk.Label = tk.Label(self, text=message)
        message.pack(padx=10, pady=10, anchor=tk.CENTER)
        
        entry_frame: tk.Frame = tk.Frame(self)
        entry_frame.pack(padx=10, pady=5, fill=tk.X, expand=True)
        self.entry: tk.Entry = PlaceholderEntry(master=self, placeholder=placeholder)
        self.entry.pack(padx=5, pady=5, side=tk.LEFT)
        submit: tk.Button = tk.Button(self, text="Submit", command=submit)
        submit.pack(padx=5, pady=5, side=tk.RIGHT)

    def submit(self) -> str:
        self.destroy()
        return self.entry.get()
        
    def __str__(self) -> str:
        return self.entry.get()



# ********************
# NOTICE
# ********************
# The following code was taken from user mp035 on GitHub from [this gist](<https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01>).
# The following Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
class ScrollableFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the canvas frame changes.
            
        self.viewPort.bind('<Enter>', self.onEnter)                                 # bind wheel events when the cursor enters the control
        self.viewPort.bind('<Leave>', self.onLeave)                                 # unbind wheel events when the cursorl leaves the control

        self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.

    def onMouseWheel(self, event):                                                  # cross platform scroll wheel event
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll( -1, "units" )
            elif event.num == 5:
                self.canvas.yview_scroll( 1, "units" )
    
    def onEnter(self, event):                                                       # bind wheel events when the cursor enters the control
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, event):                                                       # unbind wheel events when the cursorl leaves the control
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")
            