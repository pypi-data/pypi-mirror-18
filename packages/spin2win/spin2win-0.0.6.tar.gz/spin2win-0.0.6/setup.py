# -*- coding: ISO-8859-1 -*-

import os
import codecs
from setuptools import setup, find_packages

# Save version and author to __meta__.py
version = open('VERSION.txt').read().strip()
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'src', 'spin2win', '__meta__.py')
meta = '''# Automatically created. Please do not edit.
__version__ = '%s'
__author__ = 'Filippe Henriques Leal & Karine Santos Valença'
''' % version
# with open(path, 'w') as F:
#     F.write(meta)

setup(
        # Basic info
        name='spin2win',
        version=version,
        author='Karine Santos Valença',
        author_email='valenca.karine@gmail.com',
        url='https://github.com/FilippeLeal/spin2win',
        description='SPIN2WIN!!!',

        classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
			'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            ],

        # Packages and dependencies
        include_package_data=True,
        package_data={
            'spin2win':  [
				'images/*.png', 'images/*.jpg', 'sounds/*.mp3', 'sounds/*.wav'
			]
            },

        install_requires=[
			'FGAme', 
			'pygame',
        ],
        extras_require={
            'dev': [
                'python-boilerplate[dev]',
                ],
            },

        # Other configurations
        # zip_safe=False,
        platforms='any',
		
        entry_points={
            'console_scripts': [
                'spin2win = spin2win.__main__:main',
            ],
			'gui_scripts': [
                'spin2wingui = spin2win.__main__:main',
            ],
        },
)