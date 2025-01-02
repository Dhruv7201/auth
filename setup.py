# setup.py
from setuptools import setup, find_packages

setup(
    name="jwt_auth",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "pyjwt",
        "passlib",
    ],
    description="JWT authentication package for FastAPI",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/jwt_auth",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
