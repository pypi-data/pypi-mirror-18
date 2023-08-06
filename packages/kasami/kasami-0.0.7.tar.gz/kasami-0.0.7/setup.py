import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def requirements(fname):
    return [line.strip()
            for line in open(os.path.join(os.path.dirname(__file__), fname))]

about_path = os.path.join(os.path.dirname(__file__), "kasami/about.py")
exec(compile(open(about_path).read(), about_path, "exec"))


setup(
    name="kasami",
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    license=__license__,
    url=__url__,
    packages=find_packages(),
    include_package_data=True,
    long_description=read('README.md'),
    install_requires=requirements('requirements.txt'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
