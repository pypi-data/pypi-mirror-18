import os
from setuptools import setup

# Set external files
try:
    from pypandoc import convert
    README = convert('README.md', 'rst')
except ImportError:
    README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
    print("warning: pypandoc module not found, could not convert Markdown to RST")

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='harser',
    version='0.0.1',
    packages=['harser'],
    install_requires=required,
    include_package_data=True,
    license='MIT License',
    description='Easy way for HTML parsing and building XPath.',
    long_description=README,
    url='https://github.com/sihaelov/harser',
    author='Michael Sinov',
    author_email='sihaelov@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
