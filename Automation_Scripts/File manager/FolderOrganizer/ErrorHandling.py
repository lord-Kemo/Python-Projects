import tkinter as tk
import logging
from tkinter import messagebox

class ErrorHandler:
    def __init__(self, log_widget=None):
        self.log_widget = log_widget

    def log(self, message):
        # Log to widget if provided
        if self.log_widget:
            self.log_widget.config(state='normal')
            self.log_widget.insert(tk.END, message + "\n")
            self.log_widget.see(tk.END)
            self.log_widget.config(state='disabled')
        # Also log to Python logger
        logging.error(message)

    def handle(self, error, user_message=None, popup=False):
        # Log the error detail
        self.log(f"ERROR: {error}")
        # Optionally show a popup with user-friendly message
        if popup:
            messagebox.showerror("Error", user_message or "An error occurred.")
        else:
            # Print user message to log widget or console
            if user_message:
                self.log(user_message)


# Redirect print to text widget
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget
    def write(self, message):
        self.widget.config(state='normal')
        self.widget.insert(tk.END, message)
        self.widget.see(tk.END)
        self.widget.config(state='disabled')
    def flush(self):
        pass