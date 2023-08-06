from setuptools import setup, find_packages
import os
import codecs


PACKAGENAME = 'sqre-codekit'
DESCRIPTION = 'LSST Data Management SQuaRE code management tools'
AUTHOR = 'Frossie Economou'
AUTHOR_EMAIL = 'frossie@lsst.org'
URL = 'https://github.com/lsst-sqre/sqre-codekit'
VERSION = '1.0.1'
LICENSE = 'MIT'


def read(filename):
    full_filename = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        filename)
    return codecs.open(full_filename, 'r', 'utf-8').read()

long_description = read('README.md')


setup(
    name=PACKAGENAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='lsst',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'github3.py==1.0.0a4',
        'uritemplate.py==2.0.0',
        'requests==2.8.1',
        'urllib3==1.12',
        'progressbar2==3.11.0',
        'GitPython==1.0.1',
        'MapGitConfig==1.1'
    ],
    tests_require=['pytest'],
    # package_data={},
    entry_points={
        'console_scripts': [
            'github-auth = codekit.cli.github_auth:main',
            'github-delete-shadow = codekit.cli.github_delete_shadow:main',
            'github-fork-repos = codekit.cli.github_fork_repos:main',
            'github-list-repos = codekit.cli.github_list_repos:main',
            'github-mv-repos-to-team = codekit.cli.github_mv_repos_to_team:main',  # NOQA
            'github-tag-version = codekit.cli.github_tag_version:main',
            'lsst-bp = codekit.cli.lsst_bp:main',
        ]
    }
)
