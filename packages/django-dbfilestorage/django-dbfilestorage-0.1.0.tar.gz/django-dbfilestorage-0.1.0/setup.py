import re
import os

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name="django-dbfilestorage",
    version="0.1.0",
    description="Database backed file storage for testing.",
    long_description="Database backed file storage for testing. Stores files as base64 encoded textfields.",
    author="Tyrel Souza",
    author_email="tyrelsouza@gmail.com",
    url="https://github.com/tyrelsouza/django-dbfilestorage",
    download_url="https://github.com/tyrelsouza/django-dbfilestorage.git",
    license="MIT License",
    packages=[
        "dbfilestorage",
    ],
    include_package_data=True,
    install_requires=[
        "Django>=1.8.0",
    ],
    tests_require=[
        "nose",
        "coverage",
    ],
    zip_safe=False,
    test_suite="tests.runtests.start",
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
