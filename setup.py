from setuptools import setup, find_packages

setup(
    name="markov-ai",
    version="0.1.7",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
    author="Anant Chandra",
    author_email="anantchandra98@gmail.com",
    description="A Python SDK for interacting with Markov AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/markov-ai-xyz/markov-ai-python-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
