import sys
from utils import copy_contents_to_folder, generate_pages_recursive

basepath = '/'

args = sys.argv

if len(args) > 1:
    basepath = args[1]

def main():
    copy_contents_to_folder("static", "docs")
    generate_pages_recursive('content', 'template.html', 'docs', basepath)

main()