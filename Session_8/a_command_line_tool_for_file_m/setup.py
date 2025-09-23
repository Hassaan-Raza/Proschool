```python
# setup.py
import os
from setuptools import setup, find_packages

# Define the project metadata
NAME = 'file_manager'
VERSION = '1.0.0'
AUTHOR = 'Your Name'
EMAIL = 'your@email.com'
DESCRIPTION = 'A command-line tool for file management and batch processing'
LONG_DESCRIPTION = 'This is a long description of the project'
URL = 'https://github.com/your-username/file-manager'
DOWNLOAD_URL = f'https://github.com/your-username/file-manager/archive/v{VERSION}.tar.gz'
LICENSE = 'MIT'

# Define the dependencies
REQUIRES = [
    'click',
    'pathlib',
    'argparse',
    'pyyaml'
]

# Define the entry points
ENTRY_POINTS = {
    'console_scripts': [
        f'{NAME} = {NAME}.cli:cli',
    ],
}

# Define the setup function
def setup_package():
    try:
        # Create the MANIFEST.in file
        with open('MANIFEST.in', 'w') as f:
            f.write('include *.txt\n')
            f.write('recursive-include file_manager *.py\n')
            f.write('recursive-include file_manager *.yaml\n')

        # Run the setup
        setup(
            name=NAME,
            version=VERSION,
            author=AUTHOR,
            author_email=EMAIL,
            description=DESCRIPTION,
            long_description=LONG_DESCRIPTION,
            url=URL,
            download_url=DOWNLOAD_URL,
            license=LICENSE,
            packages=find_packages(),
            install_requires=REQUIRES,
            entry_points=ENTRY_POINTS,
            include_package_data=True,
            zip_safe=False,
        )
    except Exception as e:
        print(f'Error: {e}')

# Run the setup function
if __name__ == '__main__':
    setup_package()
```

```python
# MANIFEST.in
include *.txt
recursive-include file_manager *.py
recursive-include file_manager *.yaml
```

```python
# file_manager/__init__.py
from pathlib import Path

# Define the root directory
ROOT_DIR = Path(__file__).parent

# Define the config file
CONFIG_FILE = ROOT_DIR / 'config.yaml'
```

```python
# file_manager/cli.py
import click
from pathlib import Path
import yaml

# Define the config
config = None

# Define the cli function
@click.group()
def cli():
    global config
    config = yaml.safe_load(open('config.yaml', 'r'))

# Define the commands
@cli.command()
@click.argument('path', type=click.Path(exists=True))
def ls(path):
    """List the files in the given path"""
    print(Path(path).glob('*'))

@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.argument('pattern', type=click.STRING)
def find(path, pattern):
    """Find the files matching the given pattern in the given path"""
    for file in Path(path).glob(pattern):
        print(file)

# Run the cli function
if __name__ == '__main__':
    cli()
```

```python
# file_manager/config.yaml
# Define the config
config:
  root_dir: /path/to/root/dir
  file_pattern: *.txt
```

```python
# requirements.txt
click==8.1.3
pathlib==1.0.1
argparse==1.4.0
pyyaml==6.0
```