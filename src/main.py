from utils import copy_contents_to_folder, generate_pages_recursive


def main():
    copy_contents_to_folder("static", "public")
    generate_pages_recursive('content', 'template.html', 'public')

main()