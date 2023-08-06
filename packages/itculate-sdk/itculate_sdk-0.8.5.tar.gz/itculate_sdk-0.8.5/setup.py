from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="itculate_sdk",
    version="0.8.5",
    description="ITculate SDK",
    url="https://bitbucket.org/itculate/itculate-sdk",
    author="Ophir",
    author_email="opensource@itculate.io",
    license="MIT",
    keywords=["ITculate", "sdk", "graph", "topology"],
    package_data={'itculate_sdk/*': ['*.csv']},
    packages=find_packages(),
)
