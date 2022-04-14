from setuptools import setup, find_packages

setup(
    name='sorting_algorithms',
    version='1.0.1',
    author='Daniil Shynkarenko',
    author_email='dahhwe@gmail.com',
    description='Sorting algorithms',
    long_description='Using all famous sorting algorithms to sort a list',
    packages=find_packages(),
    install_requires=['pytest'],
    include_package_data=True
)
