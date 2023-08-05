# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='ovp-uploads',
    version='0.1.2',
    author=u'Atados',
    author_email='arroyo@atados.com.br',
    packages=['ovp_uploads'],
    url='https://github.com/OpenVolunteeringPlatform/django-ovp-uploads',
    download_url = 'https://github.com/OpenVolunteeringPlatform/django-ovp-core/tarball/0.1.2',
    license='AGPL',
    description='This module has core upload functionality.',
    long_description=open('README.rst', encoding='utf-8').read(),
    zip_safe=False,
    install_requires = [
      'Django>=1.10.1,<1.11.0',
      'djangorestframework>=3.4.7,<3.5.0',
      'codecov>=2.0.5,<2.1.0',
      'coverage>=4.2,<4.3.0',
      'django-resized>=0.3.5,<0.4.0',
      'Pillow>=3.4.2,<3.5'
      'ovp-users>=1.0.1,<2.0'
    ]
)
