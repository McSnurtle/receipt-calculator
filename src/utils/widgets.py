#src/utils/widgets.py
# imports
import platform
import tkinter as tk
from typing import Any, Union, Callable
from .models import Receipt # type: ignore


class ReceiptPreview(tk.Frame):
    """A horizontal tk.Frame widget showing a preview of a receipt

    Args:
        receipt (Union[Receipt, object]): The receipt object to preview.
        edit_func (Callable): The function to run if the user clicks "edit".
        del_func (Callable): The function to run if the user clicks "delete".

    Raises:
        TypeError: _description_
    """

    def __init__(self, receipt: Union[Receipt, object], calc_func: Callable, del_func: Callable,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        # vars
        if not isinstance(receipt, Receipt):
            raise TypeError("receipt must be of type Receipt!")
        self.receipt: Receipt = receipt

        # layout
        info_frame: tk.Frame = tk.Frame(self)
        info_frame.pack(padx=5, pady=5, side=tk.LEFT)
        title_label: tk.Label = tk.Label(info_frame, text=self.receipt.name, font=("Arial", 18))
        title_label.pack(padx=5, pady=5, side=tk.TOP, anchor=tk.NW) # top left
        date_label: tk.Label = tk.Label(info_frame, text=str(self.receipt.date), font=("Arial", 10))
        date_label.pack(padx=5, pady=5, side=tk.BOTTOM, anchor=tk.SW)   # top left subheader

        control_frame: tk.Frame = tk.Frame(self)
        control_frame.pack(padx=5, pady=5, side=tk.RIGHT)
        delete_button: tk.Button = tk.Button(control_frame, text="🗑", command=del_func)
        delete_button.pack(padx=5, pady=5, side=tk.RIGHT, anchor=tk.E)
        calc_button: tk.Button = tk.Button(control_frame, text="🖩", command=calc_func)
        calc_button.pack(padx=5, pady=5, side=tk.RIGHT, anchor=tk.E)


class PlaceholderEntry(tk.Entry):
    """A tk.Entry widget that shows placeholder text when inactive / nothing is being done with it.

    Args:
        master (tk.Widget | Any): The parent widget.
        placeholder (str, optional): The text to be displayed upon inactivity.
        Defaults to "".
        primary_colour (str, optional): The colour of the text when active.
        Defaults to "#FFFFFF".
        secondary_colour (str, optional): The colour of the text when inactive.
        Defaults to "#666666".
    """

    def __init__(self, *args, master: tk.Widget | Any = None, placeholder: str = "",
                 primary_colour: str = "#FFFFFF", secondary_colour: str = "#666666"):
        super().__init__(master=master, *args)

        self._focused: bool = False
        self._placeholder: str = placeholder
        self._primary_colour: str = primary_colour
        self._secondary_colour: str = secondary_colour
        
        self.callback: Any = None   # why did I install pylint again? Pain? Oh right.

        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def on_focus_in(self, callback: Any = None) -> None:
        """Removes the placeholder text and colour, or 'resets' the widget for typing in."""
        self.callback = callback
        if self.get() is self._placeholder:
            self.delete(1, tk.END)
            self.config(fg=self._primary_colour)

    def on_focus_out(self, callback: Any = None) -> None:
        """If nothing has been written, shows the placeholder text and colour."""
        if self.get() is None:
            self.insert(1, self._placeholder)
            self.config(fg=self._secondary_colour)
        return callback


class PopupEntry(tk.Toplevel):
    """A mock-popup that allows the user to input custom text.

    Args:
        master (tk.Widget | Any): The parent window that holds the mainloop.
        title (str): The title of the popup.
        message (str): The message / body contents of the popup.
        placeholder (str): What the input / entry widget should say by default.
    """

    def __init__(self, master: tk.Widget | Any, title: str, message: str, placeholder: str, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.title(title)
        self.resizable(False, False)

        message_label: tk.Label = tk.Label(self, text=message)
        message_label.pack(padx=10, pady=10, anchor=tk.CENTER)

        entry_frame: tk.Frame = tk.Frame(self)
        entry_frame.pack(padx=10, pady=5, fill=tk.X, expand=True)
        self.entry: tk.Entry = PlaceholderEntry(master=self, placeholder=placeholder)
        self.entry.pack(padx=5, pady=5, side=tk.LEFT)
        submit: tk.Button = tk.Button(self, text="Submit", command=self.submit)
        submit.pack(padx=5, pady=5, side=tk.RIGHT)

    def submit(self) -> str:
        """Destroys the popup and returns the user's (string) entry.

        Returns:
            str: The user content of the entry.
        """
        self.destroy()
        return self.entry.get()

    def __str__(self) -> str:
        return self.entry.get()



# ********************
# NOTICE
# ********************
# The following code was taken from user mp035 on GitHub from:
# [this gist](<https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01>).
# The following Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
class ScrollableFrame(tk.Frame):
    """A customized tkinter Frame that allows for vertical scrolling. Made by mp035 on GitHub.

    Args:
        tk (tk.Frame): _description_
    """
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
        self.viewport = tk.Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.event: Any = None

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewport, anchor="nw",
                                  tags="self.viewPort") # add view port frame to canvas

        self.viewport.bind("<Configure>", self.on_frame_configure)  # bind an event whenever the
        # size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.on_frame_configure)    # bind an event whenever the
        # size of the canvas frame changes.

        self.viewport.bind('<Enter>', self.on_enter)    # bind wheel events when the cursor enters
        # the control
        self.viewport.bind('<Leave>', self.on_leave)    # unbind wheel events when the cursorl
        # leaves the control

        self.on_frame_configure(None)   # perform an initial stretch on render, otherwise the
        # scroll region has a tiny border until the first resize

    def on_frame_configure(self, event: Any = None) -> None:
        '''Reset the scroll region to encompass the inner frame'''
        self.event = event
        self.canvas.configure(scrollregion=self.canvas.bbox("all")) # whenever the size of the frame
        # changes, alter the scroll region respectively.

    def on_canvas_configure(self, event: Any = None) -> None:
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)    # whenever the size of
        # the canvas changes alter the window region respectively.

    def on_mouse_wheel(self, event: Any = None) -> Union[int, float]:
        """cross platform scroll wheel event

        Args:
            event (Any, optional): callback of the binding process. Defaults to None.

        Returns:
            Union[int, float]: the amount scrolled.
        """
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll( -1, "units" )
            elif event.num == 5:
                self.canvas.yview_scroll( 1, "units" )
        return event.delta

    def on_enter(self, event: Any = None) -> None:
        """bind wheel events when the cursor enters thecontrol

        Args:
            event (Any, optional): callback of the binding process. Defaults to None.
        """
        self.event = event
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)
            self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def on_leave(self, event: Any = None):
        """unbind wheel events when the cursor leaves the control

        Args:
            event (Any, optional): the callback from the binding process. Defaults to None.
        """

        self.event = event
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")
