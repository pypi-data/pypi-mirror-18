from distutils.core import setup
from distutils import dir_util
from distutils import sysconfig
import os

setup(
    name='kervi-ui',
    packages=['kervi-ui'],
    version='0.4.0',
    description='UI module for the kervi framework. It is included as dependency when kervi in installed.',
    author='Tim Wentzlau',
    author_email='tim.wentzlau@gmail.com',
    url='https://github.com/kervi/kervi-ui',
    download_url='https://github.com/wentzlau/kervi-ui/archive/v1.0-alpha.tar.gz',
    keywords=['ui', 'robotic', 'automation'],
    classifiers=[],
    
)

