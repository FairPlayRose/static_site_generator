from markdown import extract_title, markdown_to_html_node
import os
import shutil
import sys

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

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_content = open(os.path.abspath(from_path)).read()
    template = open(os.path.abspath(template_path)).read()

    html_node = markdown_to_html_node(from_content)
    html_from_content = html_node.to_html()
    title = extract_title(from_content)

    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_from_content).replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')

    with open(os.path.abspath(dest_path), "w") as t:
        t.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    dir_path_content_abs = os.path.abspath(dir_path_content)
    dest_dir_path_abs = os.path.abspath(dest_dir_path)

    for newpath in os.listdir(dir_path_content_abs):
        dir_path_content_abs_new = os.path.join(dir_path_content_abs, newpath)
        if os.path.isfile(dir_path_content_abs_new):
            filename, filetype = os.path.splitext(newpath)
            if filetype != ".md":
                continue
            dest_dir_path_abs_new = os.path.join(dest_dir_path_abs, filename + ".html")
            generate_page(dir_path_content_abs_new, template_path, dest_dir_path_abs_new, base_path)
        
        else:
            dest_dir_path_new = os.path.join(dest_dir_path, newpath)
            dir_path_content_new = os.path.join(dir_path_content, newpath)
            os.mkdir(os.path.join(dest_dir_path_abs, newpath))
            generate_pages_recursive(dir_path_content_new, template_path, dest_dir_path_new, base_path)

def main():
    args = sys.argv
    basepath = "/"
    if len(args) > 1:
        basepath = sys.argv[1]
    static_to_public()
    generate_pages_recursive("content/", "template.html", "docs/", basepath)

main()