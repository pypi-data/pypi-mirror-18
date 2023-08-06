from distutils.core import setup
from distutils import dir_util
from distutils import sysconfig
import os

setup(
    name='kervi-ui',
    packages=['server'],
    version='0.2.0',
    description='UI module for the kervi framework. It is included as dependency when kervi in installed.',
    author='Tim Wentzlau',
    author_email='tim.wentzlau@gmail.com',
    url='https://github.com/kervi/kervi-ui',
    download_url='https://github.com/wentzlau/kervi-ui/archive/v1.0-alpha.tar.gz',
    keywords=['ui', 'robotic', 'automation'],
    classifiers=[],
    include_package_data=True,
    package_data={
        'kervi-ui': [
            'web/dist/*.html',
            'web/dist/*.js',
            'web/dist/*.css',
            'web/dist/*.map',
            'web/dist/*.ico',
            'web/dist/*.eot',
            'web/dist/*.svg',
            'web/dist/*.woff',
            'web/dist/*.woff2',
            'web/dist/*.ttf'
            ],
    },
)

