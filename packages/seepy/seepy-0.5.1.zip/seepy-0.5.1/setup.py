from distutils.core import setup
setup(
    name='seepy',
    version='0.5.1',
    description='Python script visualization tool',
    long_description = open("README.txt").read(),
    author='Lukasz Laba',
    author_email='lukaszlab@o2.pl',
    url='https://seepy.org',
    packages=['seepy', 'seepy.icons', 'seepy.examples', 'seepy.memos', 'seepy.pycore', 'seepy.templates'],
    package_data = {'': ['*.png', '*.md', '*.svg']},
    license = 'GNU General Public License (GPL)',
    keywords = 'notebook ,script, report',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        ],
    )
