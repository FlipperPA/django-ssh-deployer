from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="django-ssh-deployer",
    description="This package provides Django management commands to deploy your site "
    "over SSH via Paramiko.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tim Allen",
    author_email="tim@pyphilly.org",
    url="https://github.com/FlipperPA/django-ssh-deployer",
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=["Django", "paramiko",],
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Django",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
