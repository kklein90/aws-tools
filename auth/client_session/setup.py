from setuptools import find_packages, setup

setup(
    name='clientsessionauth',
    packages=find_packages(),
    version='0.1.0',
    description="Get boto3 client depending on where you're at.",
    author='kklein',
    install_requires=['boto3','requests']
)