from setuptools import setup, find_packages

setup(
    name='littler',
    version='0.1',
    packages=find_packages(),
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
