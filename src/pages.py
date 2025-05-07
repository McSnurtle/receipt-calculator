#src/pages.py
# imports
import tkinter as tk
from .utils.models import Receipt
from .utils.widgets import ScrollableFrame, ReceiptPreview, PlaceholderEntry
from .utils.platform import get_receipts


class Page(tk.Frame):
    def __init__(self, master: tk.Widget, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        
        self.title_label: tk.Label = tk.Label(self, font=("Helvetica", 24))
        self.body_frame: ScrollableFrame = ScrollableFrame(self)
        
    def draw(self) -> None:
        """Draws all of the default page elements """
        self.title_label.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        self.body_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True, side=tk.BOTTOM, anchor=tk.S)
        

class Editor(Page):
    def __init__(self, master: tk.Widget, receipt: Receipt, save_func: callable, del_func: callable, calc_func: callable, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        
        self.title_label.config(text=receipt)

        # body frame
        self.name_label: tk.Label = tk.Label(self.body_frame.viewPort, text="Name:")
        self.name_label.pack(side=tk.TOP, padx=5, pady=5)
        self.name_entry: PlaceholderEntry = PlaceholderEntry(self.body_frame.viewPort, placeholder=receipt)
        self.name_entry.pack(padx=5, pady=5, side=tk.TOP, fill=tk.X, expand=True)

        control_frame: tk.Frame = tk.Frame(self.body_frame.viewPort)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=10, pady=10)       
        save_button: tk.Button = tk.Button(control_frame, text="Save", bg="#00FF00", command=save_func)
        save_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH)
        del_button: tk.Button = tk.Button(control_frame, text="Delete", bg="#FF0000", command=del_func)
        del_button.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.BOTH)
        calc_button: tk.Button = tk.Button(control_frame, text="CALCULATE!", bg="#0000FF", command=calc_func)
        calc_button.pack(side=tk.BOTTOM, padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        self.draw()


class Overview(Page):
    def __init__(self, master: tk.Widget, edit_func: callable, del_func: callable, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        
        self.title_label.config(text="Receipts")

        for receipt in get_receipts():
            receipt_frame: tk.Frame = ReceiptPreview(receipt=receipt, edit_func=lambda r=receipt: edit_func(r), del_func=lambda r=receipt: del_func(r), master=self.body_frame.viewPort)
            receipt_frame.pack(padx=10, pady=10, side=tk.TOP, anchor=tk.N, fill=tk.X, expand=True)

        self.draw()
        