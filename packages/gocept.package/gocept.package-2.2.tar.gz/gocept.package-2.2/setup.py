"""A paste.script template following gocept Python package conventions."""

from setuptools import setup, find_packages
import glob
import os.path


def project_path(*names):
    """Path to the project."""
    return os.path.join(os.path.dirname(__file__), *names)


setup(
    name='gocept.package',
    version='2.2',

    install_requires=[
        'PasteScript',
        'pkginfo>=0.9',
        'setuptools',
    ],

    extras_require={
        'doc': [
            'Sphinx>=1.3',
        ],
        'test': [
            'gocept.testing',
        ],
    },

    entry_points={
        'console_scripts': [
            'doc=gocept.package.doc:main',
        ],
        'paste.paster_create_template': [
            'gocept-package = gocept.package.skeleton:PackageSkeleton',
            'gocept-webapp = gocept.package.skeleton:WebAppDeploymentSkeleton',
        ],
    },

    author='gocept <mail@gocept.com>',
    author_email='mail@gocept.com',
    license='ZPL 2.1',
    url='https://bitbucket.org/gocept/gocept.package/',

    keywords='paste.script paster create template python package sphinx theme'
             'deployment batou webapp',
    classifiers="""\
Environment :: Plugins
Framework :: Paste
Intended Audience :: Developers
License :: OSI Approved :: Zope Public License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
"""[:-1].split('\n'),
    description=__doc__.strip(),
    long_description='\n\n'.join(open(project_path(name)).read() for name in (
        'README.rst',
        'HACKING.rst',
        'CHANGES.rst',
    )),

    namespace_packages=['gocept'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    data_files=[('',
                 glob.glob(project_path('*.txt')),
                 glob.glob(project_path('*.rst')))],
    zip_safe=False,
)
