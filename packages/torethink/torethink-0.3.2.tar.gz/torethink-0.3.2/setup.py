from distutils.core import setup

setup(
    name='torethink',
    version='0.3.2',
    packages=['torethink'],
    url='https://github.com/mehmetkose/torethink',
    license='MIT',
    author='Mehmet Kose',
    author_email='mehmet@linux.com',
    description='Rethinkdb Mixin For Tornado Framework.',
    platforms=('Any'),
    keywords=['tornado', 'rethinkdb', 'torethink', 'async'],
    install_requires=[
        'tornado',
        'rethinkdb',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Utilities",
    ],
)
