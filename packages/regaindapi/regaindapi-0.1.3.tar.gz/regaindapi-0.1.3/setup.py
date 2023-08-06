import glob
from setuptools import setup

setup(
    name='regaindapi',
    version='0.1.3',
    description='Regaind API python bindings',
    long_description=open("README.md").read(),
    url='https://github.com/Regaind/regaind-api',
    author='Regaind',
    author_email='hello@regaind.io',
    license='MIT',
    packages=['regaindapi'],
    scripts=glob.glob("examples/*.py"),
    install_requires=[
        'requests>=2.9.1'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',
    ],
)
