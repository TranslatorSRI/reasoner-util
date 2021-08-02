"""Setup reasoner-util package."""
from setuptools import setup

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name="reasoner-util",
    version="1.0.0",
    author="Patrick Wang",
    author_email="patrick@covar.com",
    url="https://github.com/TranslatorSRI/reasoner-util",
    description="Utilities for manipulating for TRAPI JSON components",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["reasoner_util"],
    package_data={},
    include_package_data=True,
    install_requires=[
        "reasoner-validator>=2.1,<3.0",
        "bmt-lite-1.8.2>=1.0.2",
    ],
    zip_safe=False,
    license="MIT",
    python_requires=">=3.6",
)
