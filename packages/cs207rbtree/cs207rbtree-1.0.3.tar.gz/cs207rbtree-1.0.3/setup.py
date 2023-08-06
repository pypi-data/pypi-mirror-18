from setuptools import setup

setup(
	name='cs207rbtree',

	version='1.0.3',

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

    packages=['cs207rbtree'],

    install_requires=['portalocker'],

)