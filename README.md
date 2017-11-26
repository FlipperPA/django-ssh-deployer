# Django Publisher

This package provides Django management commands to publish your site to various instances (develop, stage, production) over SSH via Paramiko.

# Installation and Setup

Install via pip into your development environment:

```bash
pip install django-publisher
```

You will need to have set up an account on the destination server; add your public key to `AUTHORIZED_KEYS` on each destination account. Add `django_publisher` to your `INSTALLED_APPS`. Then set up your instances. It is a required convention to have your configuration file ; it is assumed that your configuration file for each instance matches your branch name.

```python
DJANGO_PUBLISHER_INSTANCES = {
    'develop': {
        'name': 'django-publisher',
        'repository': 'git@github.com:FlipperPA/django-publisher.git',
        'branch': 'develop',
        'settings': 'config.settings.develop',
        'requirements': 'requirements/develop.txt',
        'code_path': '/var/django/sites',
        'virtualenv_path': '/var/django/virtualenvs',
        'virtualenv_python_path': '/usr/bin/python3.6',
        'servers': ['devserver.example.com'],
        'server_user': 'deploy_user',
    },
    'production': {
        'name': 'django-publisher',
        'repository': 'git@github.com:FlipperPA/django-publisher.git',
        'branch': 'master',
        'settings': 'config.settings.master',
        'requirements': 'requirements/master.txt',
        'code_path': '/var/django/sites',
        'virtualenv_path': '/var/django/virtualenvs',
        'virtualenv_python_path': '/usr/bin/python3.6',
        'servers': ['prodserver1.example.com', 'prodserver2.example.com'],
        'server_user': 'deploy_user',
    },
}
```

## Contributors

* Timothy Allen (https://github.com/FlipperPA)
