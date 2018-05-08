from setuptools import setup, find_packages
from sys import version

if version < '3':
    raise RuntimeError("Python v3 at least needed")


try:
    import codecs
    readme = codecs.open("README.rst", encoding="utf-8")
    long_description = readme.read()
    readme.close()
except:
    long_description = ''


setup(
    name='KernelUpgrader',
    version='1.16',
    packages=find_packages(),
    url='https://goo.gl/ZJ4zP9',
    license='GPL-3.0',
    author='Javinator9889',
    author_email='javialonso007@hotmail.es',
    description='Download, compile and install the latest stable kernel for your Linux system',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    zip_safe=False,
    download_url="https://github.com/Javinator9889/KernelUpgrader/archive/master.zip",
    entry_points={
        'console_scripts': [
            'kernel_upgrader=kernel_upgrader.__init__:main'
        ]
    }, install_requires=['packaging', 'psutil', 'beautifulsoup4', 'lxml', 'requests', 'clint'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
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
