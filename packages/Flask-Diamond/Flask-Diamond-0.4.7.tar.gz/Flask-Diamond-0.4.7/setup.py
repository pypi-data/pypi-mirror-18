# -*- coding: utf-8 -*-
# Flask-Diamond (c) Ian Dennis Miller

import re
import os
from setuptools import setup
from distutils.dir_util import copy_tree


# mimicking flask-admin setup.py
# https://github.com/flask-admin/flask-admin/blob/master/setup.py
def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return open(fpath(fname)).read()


file_text = read(fpath('flask_diamond/__meta__.py'))


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


setup(
    version=grep('__version__'),
    name='Flask-Diamond',
    description="Flask-Diamond is a batteries-included Flask framework.",
    packages=[
        "flask_diamond",
        "flask_diamond.facets",
        "flask_diamond.mixins",
        "flask_diamond.models",
        "flask_diamond.views",
        "flask_diamond.views.diamond",
    ],
    scripts=[
        "bin/flask-diamond",
    ],
    long_description=read('Readme.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet :: WWW/HTTP",
    ],
    include_package_data=True,
    keywords='',
    author=grep('__author__'),
    author_email=grep('__email__'),
    url=grep('__url__'),
    install_requires=read('requirements.txt'),
    license='MIT',
    zip_safe=False,
)

venv_path = os.environ.get("VIRTUAL_ENV")
if venv_path:
    try:
        copy_tree("skels", os.path.join(venv_path, "share/skels"))
    except:
        print("WARN: failed to install skels.")
        print("flask-diamond may not work correctly as a result.")
else:
    print("WARN: did not install skels.  This was not installed in a virtual environment")
    print("flask-diamond may not work correctly as a result.")
