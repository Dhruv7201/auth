# setup.py
from setuptools import setup, find_packages

setup(
    name="jwt_auth_provider",
    version="0.2.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "pyjwt",
        "passlib",
        "python-dotenv",
    ],
    description="JWT authentication package for FastAPI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Dhruv Modi",
    author_email="dhruv.modi2345@gmail.com",
    url="https://github.com/Dhruv7201/auth",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
