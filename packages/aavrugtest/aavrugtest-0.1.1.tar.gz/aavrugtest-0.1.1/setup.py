from setuptools import setup

setup(
    name='aavrugtest',
    version='0.1.1',
    description="Test",
    keywords='test',
    author='Gaurav Kumar',
    author_email='aavrug@gmail.com',
    url='https://github.com/aavrug/aavrugtest.git',
    packages=['aavrugtest'],
    install_requires=['click'],
    scripts=['bin/aavrugtest'],
    license='MIT')
