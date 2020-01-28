from setuptools import setup, find_packages

setup(
    name="format_converter",
    version="0.1.0",
    packages=find_packages(),
    url="",
    license="MIT",
    author="Jean-Denis VIDOT",
    author_email="contact@jdevelop.io",
    description="",
    entry_points={
        "console_scripts": [
            "format_converter = format_converter.cli:convert"
        ]
    }
)
