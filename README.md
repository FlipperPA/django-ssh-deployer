# Django Publisher

This package provides Django management commands to publish your site over SSH via Paramiko.

# Installation and Setup

Install via pip into your development environment:

```bash
pip install django-publisher
```

You will need to have set up an account on the destination server; add your public key to `AUTHORIZED_KEYS` on each destination account. Add `django_publisher` to your `INSTALLED_APPS`. Then set up your instances. It is a required convention to have your configuration file ; it is assumed that your configuration file for each instance matches your branch name.

```python
DJANGO_PUBLISHER_INSTANCES = {
    'develop': {
        'repository': '',
        'branch': 'develop',
        'settings': 'config.settings.develop',
        'servers': ['devserver.example.com'],
    },
    'production': {
        'repository': '',
        'branch': 'master',
        'settings': 'config.settings.master',
        'servers': ['prodserver1.example.com', 'prodserver2.example.com'],
    },
}
```

## Contributors

* Timothy Allen (https://github.com/FlipperPA)
