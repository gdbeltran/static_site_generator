import os
import sys
import shutil

from copy_files import copy_files
from generate_page import generate_pages_recursive

if sys.argv[1]:
    basepath = sys.argv[1]
else:
    basepath = "/"

dir_path_static = "./static"
dir_path_docs = "./docs"

def main():
    print("Deleting docs directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to docs directory...")
    copy_files(dir_path_static, dir_path_docs)

    generate_pages_recursive(
        dir_path_content="./content",
        template_path="./template.html",
        dest_dir_path=dir_path_docs,
        basepath=basepath
    )
    
main()
