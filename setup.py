# setup.py
from setuptools import setup, find_packages

setup(
    name="graphhopper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests==2.31.0",
        "pytest==8.0.0",
    ],
)
