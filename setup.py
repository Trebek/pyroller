try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as f:
    README = f.read()

setup(
    name='pyroller',
    version='1.1.0',
    author='Alex Crawford',
    author_email='kebert406@yahoo.com',
    packages=['pyroller'],
    scripts=[],
    url='https://github.com/Trebek/pyroller',
    license='LICENSE.txt',
    description=('A package for simulating dice, that uses '
        'standard dice notations to build dice objects.'),
    long_description=README,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3"
    ],
    keywords='dice die game fudge coin roll flip toss rpg role playing',
    install_requires=[],
    include_package_data=True,
    zip_safe=False
)