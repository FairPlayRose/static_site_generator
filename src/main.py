from textnode import TextNode, TextType
from markdown import extract_title
import re
import os
import shutil

def find_file_paths(path: str):
    if not os.path.exists(path):
        raise Exception("Encountered invalid path during recurtion")
    
    files: list[str] = []
    for newpath in os.listdir(path):
        if os.path.isfile(os.path.join(path, newpath)):
            files.append(os.path.join(path, newpath))
        else:
            files.extend(find_file_paths(os.path.join(path, newpath)))
    
    return files

def copy_files_to_different_dir(source_path, target_path):
    if not os.path.exists(source_path) or not os.path.exists(target_path):
        raise Exception("Encountered invalid path during recurtion")
    
    for newpath in os.listdir(source_path):
        file_or_dir_path = os.path.join(source_path, newpath)
        if os.path.isfile(file_or_dir_path):
            shutil.copy(file_or_dir_path, target_path)
            print(os.path.join(source_path, newpath))
        else:
            os.mkdir(os.path.join(target_path, newpath))
            copy_files_to_different_dir(file_or_dir_path, os.path.join(target_path, newpath))

def delete_files_and_paths(path: str):
    if not os.path.exists(path):
        raise Exception("Encountered invalid path during recurtion")
    
    for newpath in os.listdir(path):
        if os.path.isfile(os.path.join(path, newpath)):
            os.remove(os.path.join(path, newpath))
        else:
            delete_files_and_paths(os.path.join(path, newpath))

    os.rmdir(path)

def static_to_public():
    public_path = os.path.abspath("public/")
    static_path = os.path.abspath("static/")

    delete_files_and_paths(public_path)

    os.mkdir(public_path)

    copy_files_to_different_dir(static_path, public_path)



def main():
    static_to_public()

main()