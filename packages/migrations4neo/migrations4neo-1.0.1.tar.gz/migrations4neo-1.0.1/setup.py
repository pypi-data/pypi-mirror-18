from setuptools import setup

version = '1.0.1'


setup(
    name='migrations4neo',
    packages=['migrations4neo'],
    version=version,
    description='Easy neo4j migrations',
    author='turkus',
    author_email='wojciechrola@wp.pl',
    url='https://github.com/turkus/migrations4neo',
    download_url=(
        'https://github.com/turkus/migrations4neo/tarball/{}'.format(version)
    ),
    keywords=['neo4j', 'migrations'],
    entry_points={
        'console_scripts': [
            'mig4neo = migrations4neo.main:main',
        ]
    },
    install_requires=['py2neo', 'awesome-slugify', 'six'],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
