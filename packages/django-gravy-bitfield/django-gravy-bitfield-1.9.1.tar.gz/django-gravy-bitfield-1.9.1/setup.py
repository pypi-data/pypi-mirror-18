import os
from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='django-gravy-bitfield',
    version='1.9.1',
    packages=find_packages(),
    install_requires=[
        'Django>=1.8',
        'six',
    ],
    extras_require={
        'tests': [
            'flake8',
            'mysqlclient',
            'psycopg2>=2.3',
            'pytest-django',
        ],
    },
    include_package_data=True,
    license='Apache License',
    description='BitField in Django',
    long_description=README,
    author='DISQUS',
    author_email='opensource@disqus.com',
    url='https://github.com/disqus/django-bitfield',
    zip_safe=False,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)
