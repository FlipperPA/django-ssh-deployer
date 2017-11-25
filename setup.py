from setuptools import setup, find_packages
setup(
    name='django-publisher',
    version="0.1dev0",
    description='This package provides Django management commands to publish your site over SSH via Paramiko.',
    long_description='This package provides Django management commands to publish your site over SSH via Paramiko.',
    author='Tim Allen',
    author_email='tim@pyphilly.org',
    url='https://github.com/FlipperPA/django-publisher',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'paramiko',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)