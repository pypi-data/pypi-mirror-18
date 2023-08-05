#   Copyright 2015 Antonio Cuni anto.cuni@gmail.com

from setuptools import setup

desc = "A collection of useful tools to use PyPy-specific features, with CPython fallbacks"


setup(
    name="pypytools",
    use_scm_version=True,
    author="Antonio Cuni",
    author_email="anto.cuni@gmail.com",
    url="http://bitbucket.org/antocuni/pypytools/",
    license="MIT X11 style",
    description=desc,
    packages=["pypytools"],
    long_description=desc,
    install_requires=["py"],
    setup_requires=['setuptools_scm'],
)
