import os
import shutil
import sys
import Library
import logging as log

# Configure logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def organize_folder(path):
    '''

    :param:  path: takes a folder path ( must be folder not a file )
    :return: the same folder but after organizing:

    '''

    files:list = os.listdir(path) # this will list all the files inside the path folder

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////// if the organizing bags doesn't exist in the folder create them //////////////////////////////

    for folder in Library.folder_names: # here we iterate over the folder names to create folders
        folder_path:str = os.path.join(path, folder)
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        except PermissionError:
            log.error(f"Permission Error, Couldn't create folder {folder_path}")
        except Exception as e:
            log.error(f"Error creating {folder_path}: {e}")

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////// Now we Move the files inside the correct folder ////////////////////////////////////////

    for file in files:  # here we iterate through each file in the chosen folder
        file_path:str = os.path.join(path, file)

        # == if it's a directory skip it ==
        if os.path.isdir(file_path):
            continue
        # =================================

        moved:bool = False

        #trying to move the file to its respective folder
        for folder, ext in Library.extensions.items():
            if file.lower().endswith(tuple(ext)): # check if the file ends with any of the extensions in the list
                dest_folder = os.path.join(path, folder)

                #handel file name conflicts
                dest_path = os.path.join(dest_folder, file) # destination path for the file
                counter:int = 1

                while os.path.exists(dest_path):                                     # check if the file already exists in the destination folder
                    name, ext = os.path.splitext(file)                               # split the file name and extension
                    dest_path = os.path.join(dest_folder, f"{name}_[{counter}]{ext}")# create a new file name with a counter
                    counter += 1

                # attempt to move the file
                try:
                    shutil.move(file_path, dest_path)
                    log.info(f"Moving {file} to {dest_path}")
                    moved = True
                    break
                except PermissionError:
                    log.error(f"Permission denied to move {file}")
                    break
                except Exception as e:
                    log.error(f"Error moving {file}: {e}")
                    break

    # if the file didn't find a specific folder to fit its type then move to others folder
    if not moved:
        try:
            other_folder:str = os.path.join(path, "others")
            if not os.path.exists(other_folder):
                os.makedirs(other_folder)

            # handel the same conflict issue
            other_path = os.path.join(other_folder, file)
            counter:int = 1
            while os.path.exists(other_path):
                name, ext = os.path.splitext(file)
                other_path = os.path.join(other_folder, f"{name}_[{counter}]{ext}")
                counter += 1

            # now try to move
            shutil.move(file_path, other_path)
            log.info(f"Moving {file} to {other_path}")

        except Exception as e:
            log.error(f"Error moving {file}: {e}")


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////