from setuptools import setup

setup(
    name='littler',
    version='0.1',
    packages=['littler'],
    package_dir={'littler': 'littler'},
    url='',
    license='',
    author='Fred Bunt',
    author_email='',
    description='Program for converting data files to LITTLE_R format',
    entry_points={
        'console_scripts' : [
            'littler = littler.__main__:main'
        ]
    }
)
