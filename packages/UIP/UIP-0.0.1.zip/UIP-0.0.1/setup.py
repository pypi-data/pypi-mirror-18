from setuptools import setup
from uiplib.settings import (HOME_DIR,
                             DEFAULT_PICS_FOLDER,
                             NUMBER_OF_IMAGES_TO_PARSE,
                             settings_file_path)
import sys
import os
import json

def get_contents(filename):
    file = open(filename, 'r').readlines()
    out = []
    for a in file:
        out.append(a.strip())
    return out

#Make Home Directory
if not os.path.exists(HOME_DIR):
    os.makedirs(HOME_DIR)

if not os.path.isfile(settings_file_path):
    file_data = {'timeout' : 30*60,
                 'no-of-images': NUMBER_OF_IMAGES_TO_PARSE,
                 'pics-folder' : DEFAULT_PICS_FOLDER,
                 'website' : ['https://www.reddit.com/r/wallpapers/']}
    with open(settings_file_path,"w") as settings_file:
        settings_file.write(json.dumps(file_data))

requirements = []
requirements += get_contents('requirements.txt')
if sys.platform.startswith('darwin'):
    requirements += get_contents('mac-requirements.txt')

setup(
    #Name of application:
    name="UIP",

    #Version (initial)
    version="0.0.1",

    #author details:
    author="uip-dev",
    author_email="uip.developers@gmail.com",

    #packages:
    packages=["uiplib"],

    license="LICENSE",

    url="https://www.github.com/NIT-dgp/UIP",

    #description
    description="A library to get new wallpapers.",
    long_description=open("README.md").read(),

    #dependencies
    install_requires=requirements,

    #scripts to be run
    scripts=[
        "UIP"
    ],

    #binaries that can be called from anywhere
    entry_points = {
        "console_scripts": [
                  "UIP = uiplib.UIP:main"]}


)
