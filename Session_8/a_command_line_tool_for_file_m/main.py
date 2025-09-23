```python
import argparse
import os
import shutil
import glob
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_directory(directory):
    """
    Create a new directory if it does not exist.
    
    Args:
        directory (str): Path to the directory to be created.
    """
    try:
        os.makedirs(directory)
    except FileExistsError:
        logging.warning(f"Directory '{directory}' already exists.")

def delete_directory(directory):
    """
    Delete a directory and all its contents.
    
    Args:
        directory (str): Path to the directory to be deleted.
    """
    try:
        shutil.rmtree(directory)
    except FileNotFoundError:
        logging.warning(f"Directory '{directory}' does not exist.")

def copy_file(src, dst):
    """
    Copy a file from source to destination.
    
    Args:
        src (str): Path to the source file.
        dst (str): Path to the destination file.
    """
    try:
        shutil.copy2(src, dst)
    except FileNotFoundError:
        logging.warning(f"File '{src}' does not exist.")

def move_file(src, dst):
    """
    Move a file from source to destination.
    
    Args:
        src (str): Path to the source file.
        dst (str): Path to the destination file.
    """
    try:
        shutil.move(src, dst)
    except FileNotFoundError:
        logging.warning(f"File '{src}' does not exist.")

def process_files(directory, extension, action):
    """
    Process files in a directory based on the specified action.
    
    Args:
        directory (str): Path to the directory containing files to be processed.
        extension (str): File extension to be processed.
        action (str): Action to be performed on files (copy, move, delete).
    """
    for file in glob.glob(f"{directory}/*.{extension}"):
        if action == "copy":
            copy_file(file, f"{directory}/processed_{os.path.basename(file)}")
        elif action == "move":
            move_file(file, f"{directory}/processed_{os.path.basename(file)}")
        elif action == "delete":
            delete_directory(os.path.dirname(file))
        else:
            logging.warning(f"Invalid action '{action}' specified.")

def main():
    # Create a parser for command-line arguments
    parser = argparse.ArgumentParser(description="File management and batch processing tool")
    
    # Add subparsers for different actions
    subparsers = parser.add_subparsers(dest="action")
    
    # Create a parser for create action
    create_parser = subparsers.add_parser("create", help="Create a new directory")
    create_parser.add_argument("directory", help="Path to the directory to be created")
    
    # Create a parser for delete action
    delete_parser = subparsers.add_parser("delete", help="Delete a directory and all its contents")
    delete_parser.add_argument("directory", help="Path to the directory to be deleted")
    
    # Create a parser for copy action
    copy_parser = subparsers.add_parser("copy", help="Copy a file from source to destination")
    copy_parser.add_argument("src", help="Path to the source file")
    copy_parser.add_argument("dst", help="Path to the destination file")
    
    # Create a parser for move action
    move_parser = subparsers.add_parser("move", help="Move a file from source to destination")
    move_parser.add_argument("src", help="Path to the source file")
    move_parser.add_argument("dst", help="Path to the destination file")
    
    # Create a parser for process action
    process_parser = subparsers.add_parser("process", help="Process files in a directory based on the specified action")
    process_parser.add_argument("directory", help="Path to the directory containing files to be processed")
    process_parser.add_argument("extension", help="File extension to be processed")
    process_parser.add_argument("action", choices=["copy", "move", "delete"], help="Action to be performed on files")
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    # Perform the specified action
    if args.action == "create":
        create_directory(args.directory)
    elif args.action == "delete":
        delete_directory(args.directory)
    elif args.action == "copy":
        copy_file(args.src, args.dst)
    elif args.action == "move":
        move_file(args.src, args.dst)
    elif args.action == "process":
        process_files(args.directory, args.extension, args.action)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```