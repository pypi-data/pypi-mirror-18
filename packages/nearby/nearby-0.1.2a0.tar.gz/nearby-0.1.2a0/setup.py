from setuptools import setup, find_packages


VERSION = "0.1.2-alpha"


def read(fname):
    with open(fname, 'r') as f:
        return f.read()


setup(
    name="nearby",
    version=VERSION,
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
    zip_safe=True
)
