import tkinter as tk
import Logic
import sys
import logging
import ErrorHandling as Er

# Configure logging (optional, also logs to console/file)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




root = tk.Tk()
root.title("Folder Organizer")
root.geometry("600x350")

# UI elements
message = tk.Label(root, text="Hello \\User : >", font=("Arial", 14))
message.grid(row=0, column=0, columnspan=3, pady=10)

entry = tk.Entry(root, width=50, fg='grey')
entry.insert(0, "Enter absolute folder path here...")
entry.grid(row=1, column=0, padx=10, pady=10, sticky="w")

log_text = tk.Text(root, height=10, width=70, state='disabled', bg='black', fg='lime', font=('Consolas', 10))
log_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)



sys.stdout = Er.TextRedirector(log_text)
sys.stderr = Er.TextRedirector(log_text)

# Entry placeholder behavior
def on_entry_click(event):
    if entry.get() == "Enter absolute folder path here...":
        entry.delete(0, tk.END)
        entry.config(fg='black')

def on_focusout(event):
    if entry.get() == "":
        entry.insert(0, "Enter absolute folder path here...")
        entry.config(fg='grey')

entry.bind('<FocusIn>', on_entry_click)
entry.bind('<FocusOut>', on_focusout)

# Instantiate error handler with the log widget
error_handler = Er.ErrorHandler(log_text)

def on_organize_click():
    folder_path = entry.get()
    if folder_path == "Enter absolute folder path here..." or folder_path.strip() == "":
        print("Please enter a valid folder path.\n")
        return
    print(f"Organizing folder: {folder_path}\n")

    try:
        Logic.organize_folder(folder_path)
        print("Done organizing.\n")
    except FileNotFoundError:
        error_handler.handle("Folder not found.", "The specified folder does not exist.", popup=True)
    except PermissionError:
        error_handler.handle("Permission denied.", "You do not have permission to organize this folder.", popup=True)
    except Exception as e:
        error_handler.handle(str(e), "An unexpected error occurred. Check logs for details.", popup=True)

button = tk.Button(root, text="Organize", command=on_organize_click, width=10)
button.grid(row=1, column=1, padx=10, pady=10, sticky="w")

root.mainloop()
