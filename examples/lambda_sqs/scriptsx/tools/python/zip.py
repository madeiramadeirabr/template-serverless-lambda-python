import argparse
import os
import logging
from zipfile import ZipFile

logger = logging.getLogger("zip")


def add_to_zip():
    pass


def create_zip(zip_file, source_dir, verbose):
    try:
        with ZipFile(zip_file, 'w') as zip_obj:
            # Iterate over all the files in directory
            for folder_name, sub_folders, file_names in os.walk(source_dir):
                for file_name in file_names:
                    # create complete filepath of file in directory
                    file_path = os.path.join(folder_name, file_name)
                    # Add file to zip
                    zip_obj.write(file_path)
                    if verbose:
                        logger.info("Added: {}".format(file_path))
    except Exception as err:
        logger.info("Added: {}".format(file_path))
    finally:
        if zip_obj:
            zip_obj.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='count')
    parser.add_argument("--zip_file", help="Name of the file to be created")
    parser.add_argument("--source_dir", help="Source directory")

    args = parser.parse_args()
    create_zip(args.zip_file, args.source_dir, args.v)
