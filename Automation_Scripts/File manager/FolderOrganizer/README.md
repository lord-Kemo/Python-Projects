# Folder Organizer

A simple Python GUI application to help you organize files inside any folder by automatically sorting them into categorized subfolders (e.g., Documents, Images, Videos). Built with Tkinter for the interface and Python’s standard libraries for file operations.

---

## 🖥️ Project Overview

This app allows users to enter an **absolute folder path**, then organizes all files inside that folder into appropriate subfolders based on file extensions. It handles common file types like documents, images, videos, audio, code files, and more.  

The interface features:  
- A clear message greeting the user  
- A large input box to enter the folder path  
- An "Organize" button to start sorting files  
- A log area showing real-time status and error messages  

---

## 🖼️ Visualization
+---------------------------------------------------+
| Hello \User : > | <-- Top centered greeting label
+---------------------------------------------------+
| [ C:\Users\Example\Downloads\ ] [ Organize ] | <-- Input box + button side by side
+---------------------------------------------------+
| Logs: | <-- Scrollable text area showing logs
| > Moving file1.pdf to Document Files |
| > Moving image1.jpg to Image Files |
| > Error: Permission denied to move secret.txt |
| ... |
+---------------------------------------------------+

---

## ⚙️ How to Download and Setup

### 1. Clone or Download the Repository

```bash
git clone https://github.com/yourusername/folder-organizer.git
cd folder-organizer
```

Alternatively, download the ZIP and extract it.

### 2. Create and Activate a Virtual Environment (Recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
(Currently includes watchdog if used, otherwise standard libraries only)

### 4. Run the App
```bash
python App.py
```
Enter the absolute path of the folder you want to organize and click Organize.


##🛠️ How to Build an Executable (Optional)
To generate a Windows executable:

### 1-Install PyInstaller:
```bash
pip install pyinstaller
```
### 2-Build the executable:
```bash
pyinstaller --onefile --windowed App.py
```

### 3-Find your .exe inside the dist folder.


## 🚀 How to Help Evolve This Project
This is an ongoing passion project, and contributions are very welcome! Here are some ways you could help:

Add support for more file types and custom categories

Improve the UI/UX, maybe add drag-and-drop support

Add undo/redo functionality for file moves

Enhance error handling and reporting

Create versions for other platforms (macOS, Linux)

Add scheduled or automatic folder organization

Integrate with cloud storage or sync tools

Feel free to fork the repo, open issues, or submit pull requests. Together we can make organizing files effortless!


---

You can save this content as `README.md` in your project root. Let me know if you want me to generate the `requirements.txt` or other setup files!

