# Compass Mixins for django-libsass
[compass-mixins](https://github.com/Igosuki/compass-mixins) packaged as Django app under the same version number.

## Installation
Follow [django-libsass](https://github.com/Igosuki/compass-mixins) installation instructions, then:
```
$ pip install django-libsass-compass-mixins
```
and add django_libsass_compass_mixins to your INSTALLED_APPS setting

```python
INSTALLED_APPS = [
...
'django_libsass_compass_mixins'
...
]
```

## Building
Building requires npm, wheel ans setuptools installed.

Build Django app package from latest version of [compass-mixins](https://www.npmjs.com/package/compass-mixins):
```
$ make
```
then optionally upload the build to PyPI:
```
$ make upload
```

## License
Copyright (c) 2008-2009 Christopher M. Eppstein<br/>
All Rights Reserved<br/>
Released under a [slightly modified MIT License](https://github.com/Compass/compass/blob/stable/LICENSE.markdown).


