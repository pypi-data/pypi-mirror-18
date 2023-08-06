from setuptools import setup, find_packages

setup(
    name='pychatwork',
    description="A Python wrapper for ChatWork's API",
    version='1.0.1',
    license='MIT',
    packages=find_packages(),
    author='takeshi0406',
    author_email='sci.and.eng@gmail.com',
    url='https://github.com/takeshi0406/pychatwork',
    keywords='chatwork api wrapper',
    install_requires=['requests'],
    test_suite='tests',
)
