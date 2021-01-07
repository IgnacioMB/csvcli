from setuptools import setup, find_packages
from io import open
from os import path
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# automatically captured required modules for install_requires in requirements.txt and as well as configure dependency links
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]


setup(
 name='csvcli',
 description ='A light-weight command-line tool to browse and query CSV, Excel and Apache Parquet files, regardless of their size.',
 version = '1.0.2',
 packages=find_packages(), # list of all packages
 install_requires=install_requires,
 python_requires='>=3.7', # any python greater than 3.7
 entry_points='''
     [console_scripts]
     csvcli=csvcli.cli:cli
     ''',
 author="Ignacio Marin",
 keyword="csv,parquet,excel, table, tabular, cli, command-line, read, convert, query",
 long_description=README,
 long_description_content_type="text/markdown",
 license='GNU GPLv3',
 url='https://github.com/IgnacioMB/csvcli',
 download_url='https://github.com/IgnacioMB/csvcli/archive/main.tar.gz',
  dependency_links=dependency_links,
  author_email='ignacio.marin@holidu.com',
  classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.7",
    ]
)