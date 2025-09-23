```python
"""
File Management and Batch Processing Tool

Usage:
    file_manager.py <command> [<args>]

Commands:
    list        List all files in the current directory
    copy        Copy files from source to destination
    move        Move files from source to destination
    delete      Delete files
    rename      Rename files
    batch       Run batch commands on files

Options:
    -h --help   Show this help message and exit
    -v --verbose Print debug messages
"""

import os
import shutil
import glob
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def list_files():
    """List all files in the current directory"""
    files = glob.glob('*')
    for file in files:
        print(file)

def copy_files(src, dst):
    """Copy files from source to destination"""
    try:
        shutil.copytree(src, dst)
        logging.info(f"Files copied successfully from {src} to {dst}")
    except Exception as e:
        logging.error(f"Error copying files: {e}")

def move_files(src, dst):
    """Move files from source to destination"""
    try:
        shutil.move(src, dst)
        logging.info(f"Files moved successfully from {src} to {dst}")
    except Exception as e:
        logging.error(f"Error moving files: {e}")

def delete_files(files):
    """Delete files"""
    for file in files:
        try:
            os.remove(file)
            logging.info(f"File {file} deleted successfully")
        except Exception as e:
            logging.error(f"Error deleting file {file}: {e}")

def rename_files(src, dst):
    """Rename files"""
    try:
        os.rename(src, dst)
        logging.info(f"File {src} renamed to {dst}")
    except Exception as e:
        logging.error(f"Error renaming file: {e}")

def batch_commands(commands):
    """Run batch commands on files"""
    for command in commands:
        if command['type'] == 'copy':
            copy_files(command['src'], command['dst'])
        elif command['type'] == 'move':
            move_files(command['src'], command['dst'])
        elif command['type'] == 'delete':
            delete_files(command['src'])
        elif command['type'] == 'rename':
            rename_files(command['src'], command['dst'])

def main():
    parser = argparse.ArgumentParser(description='File Management and Batch Processing Tool')
    parser.add_argument('command', help='Command to execute')
    parser.add_argument('args', nargs='*', help='Arguments for the command')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print debug messages')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if args.command == 'list':
        list_files()
    elif args.command == 'copy':
        copy_files(args.args[0], args.args[1])
    elif args.command == 'move':
        move_files(args.args[0], args.args[1])
    elif args.command == 'delete':
        delete_files(args.args)
    elif args.command == 'rename':
        rename_files(args.args[0], args.args[1])
    elif args.command == 'batch':
        batch_commands(args.args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
```