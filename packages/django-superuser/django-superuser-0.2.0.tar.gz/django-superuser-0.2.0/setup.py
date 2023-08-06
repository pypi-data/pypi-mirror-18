from setuptools import setup


setup(
    name='django-superuser',
    version='0.2.0',
    description='Middleware that gives you super powers.',
    long_description=open('README.rst').read(),
    author='Mikko Hellsing',
    author_email='mikkohellsing@gmail.com',
    url='http://github.com/sorl/django-superuser',
    packages=['superuser'],
    license='ICS',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
    ],
    zip_safe=False
)
