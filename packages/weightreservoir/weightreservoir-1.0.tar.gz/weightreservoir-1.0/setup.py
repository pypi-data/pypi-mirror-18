from distutils.core import setup

setup(
	name='weightreservoir',
	version='1.0',
	author='Ke Sang',
	author_email='kesang0156357@gmail.com',
	packages=['weightreservoir'],
	url='https://github.com/minddrummer/weightreservoir',
	license='LICENSE.txt',
	description='reservoir sampling with or without weight from a stream of data',
	install_requires=[
		'numpy',
	],
)
