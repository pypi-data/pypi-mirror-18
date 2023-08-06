"""
Register a device using : libreerp [username@server] [optional : action, default : 'login'].
"""
from setuptools import find_packages, setup

dependencies = ['click' , 'requests' , 'fabric']

setup(
    name='libreERP-cli',
    version='0.1.2',
    url='https://github.com/pkyad/libreERP-cli',
    license='GPL2',
    author='Pradeep Yadav',
    author_email='pkyisky@gmail.com',
    description='Command line tools and dev modules for libreERP project.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'libreerp = libreerp.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        # 'Operating System :: POSIX',
        # 'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
