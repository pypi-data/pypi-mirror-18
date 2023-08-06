from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-mongologging',
    version='0.1',
    description='Logging changes in Django Models to MongoDB for HTTP requests and Celery tasks',
    long_description=long_description,
    url='https://github.com/abramovd/django-mongolog',
    author='Dmitry Abramov',
    author_email='diabramo@yandex.ru',
    license='APACHE',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
    ],
    keywords='django mongodb logging celery history',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django==1.10.3',
        'django-celery==3.1.17',
        'celery==3.1.25',
        'pymongo==3.3.1',
    ]
)
