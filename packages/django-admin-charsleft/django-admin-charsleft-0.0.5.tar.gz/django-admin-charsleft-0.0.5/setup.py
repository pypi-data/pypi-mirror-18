from setuptools import setup, find_packages
import os
import charsleft

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
]

setup(
    author="Marc Widmer, Jonas Ohrstrom",
    author_email="marc@pbi.io, jonas@pbi.io",
    name='django-admin-charsleft',
    version=charsleft.__version__,
    description='Widgets and admin mixin to display remaining characters in django admin.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    url='https://github.com/palmbeach-interactive/django-admin-charsleft/',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'Django>=1.9',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
