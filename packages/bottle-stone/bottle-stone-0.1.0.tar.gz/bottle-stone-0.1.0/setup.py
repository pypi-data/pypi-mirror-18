from setuptools import setup

import bottle_stone

install_reqs = [
    'bottle>=0.10',  # Need the plugin v2 API
    'six>=1.3.0',
]

setup(
    name='bottle-stone',
    version=bottle_stone.__version__,
    description='Plugin to use the Stone IDL with Bottle.',
    author='Ken Elkabany',
    author_email='ken@elkabany.com',
    url='https://github.com/braincore/bottle-stone',
    install_requires=install_reqs,
    py_modules=['bottle_stone'],
    license='MIT',
    platforms=['CPython 2.7', 'CPython 3.4', 'CPython 3.5'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ],
    )
