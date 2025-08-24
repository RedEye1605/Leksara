import os
from setuptools import setup, find_packages

setup(
    name="[Project_Name]",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        # For example:
        # "numpy>=1.18.0",
        # "pandas>=1.0.0",
    ],
    author="",
    author_email="your.email@example.com",
    description="A short description of your package",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/RedEye1605/laplace.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)