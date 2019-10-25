from setuptools import setup
setup(
    name='papers',
    version='0.1.0',
    packages=['papers'],
    entry_points={
        'console_scripts': [
            'papers = papers.__main__:main'
        ]
    })
