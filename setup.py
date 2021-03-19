from setuptools import setup
__version__ = 14

setup(
    name='drf-swagger-missing',
    version=__version__,
    url='https://github.com/tovmeod/drf-swagger-missing',
    license='BSD',
    author='Avraham Seror',
    author_email='tovmeod@gmail.com',
    description='Add missing things to actually generate a swagger definition for your DRF project',
    long_description=__doc__,
    packages=['drf_swagger_missing'],
    install_requires=[
        'coreapi==2.3.3',
        'coreschema==0.0.4',
        'openapi_codec==1.3.2',
        'djangorestframework==3.11.2',
        'django-rest-swagger==2.2.0',
        'django==1.11.21',
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
