from setuptools import setup, find_packages
import nose2unitth
import os

# parse dependencies and their links from requirements.txt files
install_requires = [line.rstrip() for line in open('requirements.txt')]
tests_require = [line.rstrip() for line in open('tests/requirements.txt')]

# install package
setup(
    name="nose2unitth",
    version=nose2unitth.__version__,
    description="Convert nose-style test reports to UnitTH-style test reports",
    url="https://github.com/KarrLab/nose2unitth",
    download_url='https://github.com/KarrLab/nose2unitth/tarball/{}'.format(nose2unitth.__version__),
    author="Jonathan Karr",
    author_email="jonrkarr@gmail.com",
    license="MIT",
    keywords='nose unitth xunit junit',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    entry_points={
        'console_scripts': [
            'nose2unitth = nose2unitth.__main__:main',
        ],
    },
)
