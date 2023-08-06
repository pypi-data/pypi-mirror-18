"""For distribution.
"""

from setuptools import setup, find_packages

setup(
    name="deepmodels",
    version="0.1.1",
    description="framework for build, train and test deep learning models",
    url="https://github.com/flyfj/deepmodels",
    author="Jie Feng",
    author_email="jiefengdev@gmail.com",
    license="MIT",
    packages=find_packages(exclude=["docs"]),
    install_requires=["tensorflow", "lasagne"])
