from setuptools import setup

setup(
    name='postcodeuk',
    version='0.4',
    author="Lucas Santos",
    author_email="lffsantos@gmail.com",
    packages=['postcodeuk'],
    description="library that supports validating and formatting post codes for UK",
    install_requires=[
        "rstr==2.2.5",
    ]
)