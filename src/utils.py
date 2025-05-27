import os
import shutil
from transformers import markdown_to_html_node

def copy_files_and_folders(src_path, dst_path):
    if os.path.isfile(src_path):
        shutil.copy(src_path, dst_path)
    entries = os.listdir(src_path)
    if len(entries) == 0:
        return
    for item in entries:
        new_path = os.path.join(dst_path, item)
        old_path = os.path.join(src_path, item)
        if os.path.isfile(old_path):
            shutil.copy(old_path, new_path)
        elif os.path.isdir(old_path):
            if not os.path.exists(new_path):
                os.mkdir(new_path)
            copy_files_and_folders(old_path, new_path)


def copy_contents_to_folder(src_path, dst_path):
    if not os.path.exists(src_path) or not os.path.isdir(src_path):
        raise ValueError("Source path doesn't exists or isn't a directory")
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)
    os.mkdir(dst_path)
    copy_files_and_folders(src_path, dst_path)

def extract_title(markdown):
    lines = markdown.split("\n")
    heading_line = next((line for line in lines if line[:2] == "# "), None)
    if heading_line == None:
        raise ValueError("Markdown doesn't have a valid title")
    return heading_line[2:]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as markdown:
        content = markdown.read()
    with open(template_path, "r") as template:
        html_template = template.read()
    html_node = markdown_to_html_node(content)
    html_string = html_node.to_html()
    title = extract_title(content)
    html_template = html_template.replace('{{ Title }}', title)
    html_template = html_template.replace('{{ Content }}', html_string)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as dest_file:
        dest_file.write(html_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise ValueError('Cannot found the content folder')
    if os.path.isfile(dir_path_content) and dir_path_content[-3:] == '.md':
        generate_page(dir_path_content, template_path, f"{dest_dir_path[:-3]}.html")
    entries = os.listdir(dir_path_content)
    if len(entries) == 0:
        return
    for item in entries:
        new_path = os.path.join(dest_dir_path, item)
        old_path = os.path.join(dir_path_content, item)
        if os.path.isfile(old_path) and old_path[-3:] == '.md':
            generate_page(old_path, template_path, f"{new_path[:-3]}.html")
        elif os.path.isdir(old_path):
            if not os.path.exists(new_path):
                os.mkdir(new_path)
            generate_pages_recursive(old_path, template_path, new_path)