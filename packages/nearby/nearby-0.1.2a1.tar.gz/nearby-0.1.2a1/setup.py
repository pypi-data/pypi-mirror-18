import codecs
import os
import re
from setuptools import setup, find_packages


PACKAGE_NAME = "nearby"
SCRIPT_DIR = os.path.join(os.path.dirname(__file__), "bin")


def read(fname):
    with codecs.open(fname, 'r', encoding="utf-8") as f:
        return f.read()


def get_version(package):
    init_py_path = os.path.join(package, '__init__.py')
    init_py = read(init_py_path)
    # if __version__ isn't set, this will error out
    # #featurenotabug
    version = re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)
    return version


def get_script_path(name):
    return os.path.join(SCRIPT_DIR, name)


setup(
    name="nearby",
    version=get_version(PACKAGE_NAME),
    author="Chuck Bassett",
    author_email="iamchuckb@gmail.com",
    description="Simple, dumb interface to remote files",
    license="MIT",
    url="Https://github.com/chucksmash/nearby.git",
    keywords="sshfs fusemount remote nearby",
    packages=find_packages(exclude=["tests"]),
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[],
    scripts=[
        get_script_path('nearby')
    ],
    zip_safe=True
)
