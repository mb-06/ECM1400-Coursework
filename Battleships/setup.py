import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
name="battleships-pkg-mb", 
version="0.0.1",
author="Matthew Bright",
author_email="mb1345@exeter.ac.uk",
description="A simulation of the battleships with ASCII and web implementation",
long_description=long_description,
long_description_content_type="text/markdown",
url="https://github.com/mb-06/ECM1400-Coursework",
packages=setuptools.find_packages(),
classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: BSD License",
"Operating System :: OS Independent",
],
python_requires='>=3.6',
)