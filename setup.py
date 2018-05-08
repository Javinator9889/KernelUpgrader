from setuptools import setup
from sys import version

if version < '3':
    raise RuntimeError("Python v3 at least needed")

setup(
    name='KernelUpgrader',
    version='1.0',
    packages=['net', 'utils', 'values', 'exceptions', 'data_manager'],
    url='https://goo.gl/ZJ4zP9',
    license='GPL-3.0',
    author='Javinator9889',
    author_email='javialonso007@hotmail.es',
    description='Download, compile and install the latest stable kernel for your Linux system',
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'kernel_upgrader=KernelUpgrader:main'
        ]
    }, install_requires=['packaging', 'psutil', 'beautifulsoup4', 'lxml', 'requests', 'clint'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English'
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
