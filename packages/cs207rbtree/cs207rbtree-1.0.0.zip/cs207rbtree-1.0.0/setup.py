from setuptools import setup, find_packages

setup(
	name='cs207rbtree',

	version='1.0.0',

	description='A red-black tree implemented key-value database',

	url='https://github.com/rubix-cube/cs207project',

	author='rubix-cube',

	classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3.5'
    ],

    packages=find_packages(),

    install_requires=['portalocker'],

)