from setuptools import setup

setup(
    name='ExifSort',
    author='Andrew Dunn',
    author_email='andrew.g.dunn@gmail.com',
    version='0.1',
    url='http://github.com/storrgie/exifsort',
    packages=['exifsort'],
    description='Sort images into directories based '
                'on their exchangeable image file format.',
    install_requires=[
        'ExifRead'
    ],
    entry_points='''
        [console_scripts]
        exifsort=exifsort.exifsort:cli
    ''',

    # classifiers=[
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python',
    # ],
)
