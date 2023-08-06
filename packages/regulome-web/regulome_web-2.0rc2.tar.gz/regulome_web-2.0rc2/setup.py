import sys
import os
from setuptools import setup, find_packages
from regulome_app.webapp.tools.metadata import __author__, __version__, __description__, __package_name__


if sys.version_info < (3, 5):
    raise RuntimeError('This package requires Python 3.5 or later')


try:
    from pypandoc import convert_file

    def read_md(f):
        """Convert Markdown to RST"""
        return convert_file(f, 'rst')
except ImportError:
    convert = None
    print("WARNING: pypandoc module not found, could not convert Markdown to RST")

    def read_md(f):
        return open(f, 'r').read()

README = os.path.join(os.path.dirname(__file__), 'README.md')


setup(
    name=__package_name__,
    version=__version__,
    packages=find_packages(),
    license='MIT License',
    author=__author__,
    author_email='loris@mularoni.com',
    package_data={
        'regulome_web': [
            'regulome_app/webapp/templates/*.html',
            'regulome_app/webapp/static/*/*',
            'regulome_app/tools/*.py',
            'regulome_app/webapp/*.py',
            'regulome_app/regulome.cfg.template'
        ]
    },
    include_package_data=True,
    url="https://bitbucket.org/batterio/regulome_web",
    download_url="https://bitbucket.org/batterio/regulome_web/get/" + __version__ + ".tar.gz",
    description=__description__,
    long_description=read_md(README),
    install_requires=[
        'Flask',
        'Jinja2',
        'Click',
        # 'SQLAlchemy',
        # 'Flask-SQLAlchemy',
        # 'MarkupSafe',
    ],
    entry_points={
        'console_scripts': [
            'regulome_web = regulome_app.run:main'
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
)


