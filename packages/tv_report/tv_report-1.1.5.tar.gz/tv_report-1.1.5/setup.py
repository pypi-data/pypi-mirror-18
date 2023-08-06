#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="tv_report",
    version="1.1.5",
    author="Justin Dray",
    author_email="justin@dray.be",
    url="https://github.com/justin8/tv_report",
    description="A parser for tv show episode files of various formats",
    packages=find_packages(),
    license="MIT",
    install_requires=[
        "colorama",
        "pymediainfo",
        "tqdm",
        "video_utils",
    ],
    tests_require=["nose",
        "coverage",
    ],
    test_suite="nose.collector",
    entry_points={
        "console_scripts": [
            "tv-report=tv_report:main",
            "tv_report=tv_report:main",
            ],
        },
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
    ],
)
