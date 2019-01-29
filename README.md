# Django SSH Deployer

This package provides a Django management command to deploy your site to various instances (develop, stage, production) over SSH via Paramiko.

## Pre-Requisites

With great power comes great responsibility! Target servers (`DEPLOYER_INSTANCES['instance']['servers']`) must each have `git` and Python 3.3+ installed, and support Linux-style OS commands. Target servers must have a user (`DEPLOYER_INSTANCES['instance']['server_user']`) with keys set up from the control machine where you run the Django command from. This typically means installing the control machine account's public key into the target server's user account's `AUTHORIZED_KEYS`.

## Installation and Required Django Settings

Install via `pip` into your development environment:

```bash
pip install django-ssh-deployer
```

Then add `django_ssh_deployer` to your `INSTALLED_APPS`. Next, we need to configure your instances in Django's settings; these can live in your development or local settings, as they won't be required by production.

```python
DEPLOYER_INSTANCES = {
    'develop': {
        'name': 'your-project',
        'repository': 'git@github.com:youruser/your-project.git',
        'branch': 'develop',
        'settings': 'config.settings.develop',
        'requirements': 'requirements/develop.txt',
        'code_path': '/var/django/sites',
        'venv_python_path': '/usr/bin/python3.6',
        'upgrade_pip': False,
        'servers': ['devserver.example.com'],
        'server_user': 'deploy_user',
        'save_deploys': 3,
        'selinux': False,
    },
    'production': {
        'name': 'your-project',
        'repository': 'git@github.com:youruser/your-project.git',
        'branch': 'master',
        'settings': 'config.settings.master',
        'requirements': 'requirements/master.txt',
        'code_path': '/var/django/sites',
        'venv_python_path': '/usr/bin/python3.6',
        'upgrade_pip': False,
        'servers': ['prodserver-1.example.com', 'prodserver-2.example.com'],
        'server_user': 'deploy_user',
        'save_deploys': 3,
        'selinux': True,
	'additional_commands': [
            "chmod -R a+rX /var/django/sites/your-project-master",
            "curl -kLs -o /dev/null --max-time 5 --resolve 'your-domain.com:443:127.0.0.1' https://your-domain.com/",
        ],
    },
}
```

* `name`: A name for your project.
* `repository`: The repository for your Django project, which will be cloned on each target server.
* `branch`: The branch to check out for the instance.
* `settings`: A full path to the Django settings for the instnace.
* `requirements`: A relative path to a `requirements` file to be `pip install`'d for the instance.
* `code_path`: The root path for your code repository to be checked out to on the target servers.
* `venv_python_path`: The full path to the version of Python for the `venv` to use on the target servers.
* `upgrade_pip`: If set to `True`, will upgrade `pip` to the latest version.
* `servers`: A list of servers to deploy the Django project to.
* `server_user`: The user on the target servers which has been set up with keys from the control machine.
* (optional) `save_deploys`: If a positive integer, will only keep the most recent number of deployments. By default, will keep all.
* (optional) `selinux`: If set to True, the deployer will run `chcon` command to set the necessary security context on files for SELinux. It will set all files in the `codepath` to `httpd_sys_content_t`, and any `*.so` files in the `venv` to `httpd_sys_script_exec_t`.
* (optional) `additional_commands`: A list of commands to run after the deployment is complete.

## Running the Command

```bash
python manage.py deploy --instance=develop
```

* `instance`: Required. The name of the instance to deploy in `DEPLOYER_INSTANCES`. In the example above, either `develop` or `production`.
* `quiet`: Less verbose output. Does not display the output of the commands being run to the terminal.
* `stamp`: By default, Django SSH Deployer will append a datetime stamp to the `git clone`. This overrides the datetime default.

## What It Does

The `deploy` command will SSH to each server in `servers` as the `server_user`, and perform the following functions in two passes.

First, it will connect to each server and prepare the new deployment:

* clone the repository from git with a stamp
* create a `venv` with a stamp
* run the `collectstatic` command

After the deployment has been prepared on all servers without error, it will proceed to the final deployment steps:

* run the `migrate` command on the first server only
* create or update the symlink to point to the completed deploy on each server

## Known Limitations and Issues

* Windows servers are not supported, however, you can use Windows as your control machine.
* Your repository's host must be in your target server's known hosts list, as git checkouts over SSH require an initial fingerprint.
* This is not meant to be a replacement for a fully featured continous integration product, like Jenkins.

## Release Notes

#### 0.4.3

* Add `upgrade_pip` option to upgrade pip in the destination venv to the latest version.

#### 0.4.2

* Add support for additional `.so` file patterns that may be installed with `pip` for SELinux.

#### 0.4.1

* Add ability to run commands per-environment after the publish is complete. These will be the last thing run before migrations. This is handy for things like required `chmod` changes, or `curl` calls.

### 0.4.0

* SELinux is now supported. When a publish occurs, the proper security context is set for the published files and venv.

#### 0.3.1

* Some documentation touch ups.

### 0.3.0

* `virtualenv` has been deprecated in favor of `venv`, which ships with Python 3.3+. If you need support for `virtualenv`, please use the latest release from the 0.2 family.
* To simplify, `virtualenv_path` is not longer supported as an option. The `venv` will be created at the root of the project.
* The setting `virtualenv_python_path`, which points to the Python executable to build the `venv`, has been renamed to `venv_python_path` for consistency.

#### 0.2.1

* Fix a bug where a redundant symlink was being overwritten, creating unnecessary time where the database might be out of sync with code on nodes.
* Update long description with Markdown for the awesome new PyPI interface.

### 0.2.0

* Refactored to prepare code and virtualenvs on all nodes, then change the symlinks on a second pass through. This drastically cuts down the amount of potential time the code is out of sync across nodes.
* Migrations are only run on the first node, run before the symlinks are changed, again minimize the time code and database are out of sync.
* Ensure the base directories for `code_path` and `virtualenvpath` exist or can be created by the `deploy_user`.

### 0.1.0

* Initial release

## Contributors

* Timothy Allen (https://github.com/FlipperPA)
