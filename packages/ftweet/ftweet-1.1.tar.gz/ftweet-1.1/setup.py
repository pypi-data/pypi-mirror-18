import os
import setuptools

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE = os.path.join(BASE_DIR, "ftweet", "version.py")
README_FILE  = os.path.join(BASE_DIR, "README.rst")

def get_version():
    with open(VERSION_FILE) as f:
        version = next(line for line in f if line.startswith("__version__"))
        return version.split("=")[-1].replace('"', '').strip()

with open(README_FILE) as f:
    readme = f.read()

setuptools.setup(
    name='ftweet',
    description='A simple python script to tweet status updates from the command line.',
    license='MIT',
    version=get_version(),
    packages=setuptools.find_packages(),
    scripts=['scripts/ftweet'],
    url='https://gitlab.com/srfilipek/ftweet',
    author='Stefan R. Filipek',
    author_email='srfilipek@gmail.com',
    keywords=['twitter', 'tweet', 'commandline','file'],
    long_description=readme,
    classifiers=[],
    install_requires=['tweepy',],
)
