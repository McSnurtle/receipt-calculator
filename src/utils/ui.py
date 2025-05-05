#src/utils/ui.py
# imports
import tkinter as tk
from typing import Any


class PlaceholderEntry(tk.Entry):
    def __init__(self, placeholder: str = "", primary_colour: str = "#FFFFFF", secondary_colour: str = "#666666", *args, **kwargs):
        super().__init__(*args, **kwargs)
        
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
            