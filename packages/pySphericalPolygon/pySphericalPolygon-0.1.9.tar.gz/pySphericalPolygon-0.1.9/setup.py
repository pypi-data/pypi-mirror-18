from setuptools import setup

setup(name='pySphericalPolygon',
		version='0.1.9',
		description='preform point in spherical polygon operations',
		long_description=open('README.rst').read(),
		author='Omry V',
		author_email='omryv@post.bgu.ac.il',
		license='MIT',
		packages=['pySphericalPolygon'],
		url='https://github.com/omrivolk/pySphericalPolygon',
		install_requires=[
		   'numpy',
		   'pyproj',
		   'matplotlib'
		],
		zip_safe=False)