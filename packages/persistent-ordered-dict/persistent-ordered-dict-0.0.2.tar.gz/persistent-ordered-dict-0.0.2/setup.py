'''
Setup for the persistent_ordered_dict, a datastructure that keeps a 
persistent copy of itself synchronized in storage.  
'''

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='persistent-ordered-dict',
    version='0.0.2',
    description='a transparently persisted datastructure',
    long_description='a transparently persisted datastructure',
    url='https://github.com/enewe101/persistent-ordered-dict',
    author='Edward Newell',
    author_email='edward.newell@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords= (
		'data structure, storage, synchronized, dictionary, collection'
	),

    packages=['pod'],

)
