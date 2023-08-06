import io
import re
import ast
from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with io.open('django_libsass_compass_mixins/__init__.py', encoding='utf-8') as f:
    version = str(ast.literal_eval(_version_re.search(f.read()).group(1)))

with io.open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-libsass-compass-mixins',
    version=version,
    url='https://github.com/dgladkov/django-libsass-compass-mixins',
    license='MIT',
    author='Dmitry Gladkov',
    author_email='dmitry.gladkov@gmail.com',
    description='Compass mixins packaged as Django app',
    long_description=long_description,
    packages=['django_libsass_compass_mixins'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
