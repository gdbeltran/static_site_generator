import logging
import shutil
import os

logger = logging.getLogger(__name__)
logging.basicConfig(filename='copied_files.log', level=logging.INFO, filemode='w', format='%(asctime)s:%(levelname)s:%(message)s')

def copy_files(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        raise Exception(f"Source directory {source_dir} does not exist.")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)

    items = os.listdir(source_dir)
    for item in items:
        logger.info(item)
        source_item = os.path.join(source_dir, item)
        dest_item = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_item):
            shutil.copy(source_item, dest_item)
            logger.info(f"Copied file {source_item} to {dest_item}")
        else:
            copy_files(source_item, dest_item)