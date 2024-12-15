import os
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path = r"C:/Users/abo-k/Downloads/"
files = os.listdir(path)

# File names
file_names = [
    "Document Files",
    "Image Files",
    "Video Files",
    "Audio Files",
    "Compressed Files",
    "Executable Files",
    "Code Files",
    "Database Files",
    "Web Files",
    "System Files",
    "Miscellaneous Files",
    "Others"
]

# Extensions
extensions = {
    "Document Files": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".csv", ".ppt", ".pptx", ".xls", ".xlsx", ".ods", ".odp", ".odg", ".odf"],
    "Image Files": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".ico", ".psd", ".ai", ".eps", ".indd", ".cdr"],
    "Video Files": [".mp4", ".mkv", ".webm", ".avi", ".flv", ".mov", ".wmv", ".mpg", ".mpeg", ".3gp", ".vob", ".swf", ".m4v", ".rm", ".rmvb", ".asf", ".ts", ".divx", ".xvid"],
    "Audio Files": [".mp3", ".wav", ".flac", ".m4a", ".wma", ".aac", ".ogg", ".aiff", ".au", ".mka", ".mid", ".midi", ".mpa", ".ra", ".ram", ".spx", ".vox"],
    "Compressed Files": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".z", ".iso", ".dmg", ".pkg", ".deb", ".rpm"],
    "Executable Files": [".exe", ".msi", ".apk", ".bat", ".bin", ".cgi", ".pl", ".com", ".gadget", ".jar", ".wsf", ".app", ".vb", ".vbs", ".ws", ".msc"],
    "Code Files": [".py", ".java", ".c", ".cpp", ".html", ".css", ".js", ".php", ".json"],
    "Database Files": [".db", ".sqlite", ".sqlite3", ".dbf", ".mdb", ".accdb", ".sql", ".dbs", ".db3"],
    "Web Files": [".xml", ".asp", ".aspx", ".cer", ".cfm", ".htm", ".jsp", ".part", ".rss", ".xhtml"],
    "System Files": [".ini", ".dll", ".sys", ".log", ".reg", ".inf", ".conf", ".key"],
    "Miscellaneous Files": [".bak", ".tmp", ".crdownload"],
    "Others": []
}

# Creating folders if they do not exist
for folder in file_names:
    folder_path = os.path.join(path, folder)
    try:
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
    except PermissionError:
        logging.error(f"Permission denied to create folder: {folder_path}")
    except Exception as e:
        logging.error(f"Error creating folder {folder_path}: {e}")

# Moving files
for file in files:
    file_path = os.path.join(path, file)
    
    # Skip if it is a directory
    if os.path.isdir(file_path):
        continue
    
    moved = False
    
    # Try to move the file to its respective folder based on extensions
    for folder, exts in extensions.items():
        if file.lower().endswith(tuple(exts)):
            dest_folder = os.path.join(path, folder)
            
            # Handle filename conflicts
            dest_path = os.path.join(dest_folder, file)
            counter = 1
            while os.path.exists(dest_path):
                name, ext = os.path.splitext(file)
                dest_path = os.path.join(dest_folder, f"{name}_{counter}{ext}")
                counter += 1
            
            try:
                shutil.move(file_path, dest_path)
                logging.info(f"Moved {file} to {dest_path}")
                moved = True
                break
            except PermissionError:
                logging.error(f"Permission denied to move {file}")
                break
            except Exception as e:
                logging.error(f"Error moving {file}: {e}")
                break
    
    # If the file was not moved to a specific folder, move it to "Others"
    if not moved:
        try:
            other_folder = os.path.join(path, "Others")
            if not os.path.exists(other_folder):
                os.makedirs(other_folder)
            
            # Handle filename conflicts in Others folder
            other_path = os.path.join(other_folder, file)
            counter = 1
            while os.path.exists(other_path):
                name, ext = os.path.splitext(file)
                other_path = os.path.join(other_folder, f"{name}_{counter}{ext}")
                counter += 1
            
            shutil.move(file_path, other_path)
            logging.info(f"Moved {file} to Others folder")
        except Exception as e:
            logging.error(f"Error moving {file} to Others: {e}")