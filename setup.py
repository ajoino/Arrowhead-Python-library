import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arrowhead-python-library",
    version="0.0.1",
    author="Emil Vidmark",
    author_email="emilvidmark@live.se",
    description="Arrowhead client library for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emilvidmark/Arrowhead-Python-library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
