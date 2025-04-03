from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="reverbed",
    version="0.1.0",
    author="Param Patel",
    author_email="your.email@example.com",
    description="A Python package for creating slowed and reverbed versions of videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paramp07/reverbed",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pytube",
        "moviepy",
        "yt-dlp",
        "soundfile",
        "pedalboard",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "reverbed=reverbed.core:main",
        ],
    },
) 