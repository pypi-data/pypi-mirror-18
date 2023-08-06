from setuptools import setup
import ast

from lilypad import __version__


with open('lilypad/lilypad.py') as f:
    lilypad_contents = f.read()

module = ast.parse(lilypad_contents)
readme_docstring = ast.get_docstring(module)

setup(
    name='lilypad',
    version=__version__,
    description='markdown + jinja, static site generator',
    long_description=readme_docstring,
    author='Lily Seabreeze',
    author_email='lillian.gardenia.seabreeze@gmail.com',
    keywords='cli',
    install_requires=['jinja2', 'bs4', 'docopt', 'markdown',],
    packages=['lilypad',],
    entry_points = {
        'console_scripts': [
            'lilypad=lilypad.lilypad:main',
        ],
    },
    package_dir={'lilypad': 'lilypad'},
)
