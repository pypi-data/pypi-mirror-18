from setuptools import setup, find_packages
setup(
    name='simplepush_api',
    version='0.4',
    description='A simplepush API',
    url='https://github.com/luke-spademan/simplepush/',
    author='Luke Spademan',
    author_email='luke.spademan@gmail.com',
    license="MIT",
    packages=find_packages(exclude=("tests")),
)
