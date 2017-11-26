from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from paramiko import SSHClient, AutoAddPolicy


class Command(BaseCommand):
    """
    This command will create Django models by introspecting the PostgreSQL data.
    Why not use inspectdb? It doesn't have enough options; this will be broken
    down by schema / product.
    """
    help = 'This command will copy the database from one environment to another. BE CAREFUL!'

    def add_arguments(self, parser):
        parser.add_argument(
            '--instance',
            action='store',
            dest='instance',
            default=None,
            help='''The instance from DJANGO_PUBLISHER_INSTANCES to publish.'''
        )
        parser.add_argument(
            '--quiet',
            action='store',
            dest='quiet',
            default=False,
            help='''Shuts off not quiet output.'''
        )

    def command_output(self, stdout, stderr, quiet):
        if not quiet:
            print(stdout.read().decode("utf-8"))
            print(stderr.read().decode("utf-8"))
        else:
            stdout.read()

    def handle(self, *args, **options):
        """
        Handler for the command. Backs up the database in the source environment,
        then restores it to the target. Sanity check in place to never restore to
        production.
        """

        # Grab the quiet settings
        quiet = options['quiet']

        # Check to ensure the require setting is in Django's settings.
        if hasattr(settings, 'DJANGO_PUBLISHER_INSTANCES'):
            instances = settings.DJANGO_PUBLISHER_INSTANCES
        else:
            raise CommandError('You have not configured DJANGO_PUBLISHER_INSTANCES in your Django settings.')

        # Grab the instance settings if they're properly set
        if options['instance'] in instances:
            instance = instances[options['instance']]
        else:
            raise CommandError(
                'The instance name you provided ("{instance}") is not configured in your settings DJANGO_PUBLISHER_INSTANCES. Valid instance names are: {instances}'.format(
                    instance=options['instance'],
                    instances=', '.join(list(instances.keys())),
                )
            )

        print(
            "We are about to deploy the instance '{instance}' to the following servers: {servers}.".format(
                instance=options['instance'],
                servers=', '.join(instance['servers']),
            )
        )
        verify = input('Are you sure you want to do this (enter "yes" to proceed)? ')

        if verify.lower() != 'yes':
            print("You did not type 'yes' - aborting.")
            return

        for server in instance['servers']:
            print("Connecting to {}...".format(server))

            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            print(server)
            print(instance['server_user'])
            ssh.connect(server, username=instance['server_user'])

            stdin, stdout, stderr = ssh.exec_command(
                """
                cd {code_path}
                rm -rf {name}-{branch}-new
                git clone --verbose -b {branch} {repository} {name}-{branch}-new
                """.format(
                    code_path=instance['code_path'],
                    name=instance['name'],
                    branch=instance['branch'],
                    repository=instance['repository'],
                )
            )
            print(
                """
                cd {code_path}
                rm -rf {name}-{branch}-new
                git clone --verbose -b {branch} {repository} {name}-{branch}-new
                """.format(
                    code_path=instance['code_path'],
                    name=instance['name'],
                    branch=instance['branch'],
                    repository=instance['repository'],
                )
            )
            self.command_output(stdout, stderr, quiet)

            import sys
            sys.exit()

            print("Installing requirements in a new virtualenv...")
            stdin, stdout, stderr = ssh.exec_command("""
                rmvirtualenv {1}-{0}-new
                mkvirtualenv {1}-{0}-new
                pip install --ignore-installed -r /var/django/html/{1}-{0}-new/requirements/{0}.txt
            """.format(instance, instance['name']))
            if not quiet:
                print(stdout.read().decode("utf-8"))
            else:
                stdout.read()
            print(stderr.read().decode("utf-8"))

            print("Collecting static files...")
            stdin, stdout, stderr = ssh.exec_command("""
                cd /var/django/html/{1}-{0}-new
                workon {1}-{0}-new
                python manage.py collectstatic --noinput --settings=config.settings.{0}
            """.format(instance, instance['name']))
            if not quiet:
                print(stdout.read().decode("utf-8"))
            else:
                stdout.read()
            print(stderr.read().decode("utf-8"))

            print("Saving previous two publishes, and installing new...")
            stdin, stdout, stderr = ssh.exec_command("""
                rmvirtualenv {1}-{0}-old-old
                cpvirtualenv {1}-{0}-old {1}-{0}-old-old
                rmvirtualenv {1}-{0}-old
                cpvirtualenv {1}-{0} {1}-{0}-old
                rmvirtualenv {1}-{0}
                cpvirtualenv {1}-{0}-new {1}-{0}
                rmvirtualenv {1}-{0}-new
                cd /var/django/html
                rm -rf {1}-{0}-old-old
                mv {1}-{0}-old {1}-{0}-old-old
                mv {1}-{0} {1}-{0}-old
                mv {1}-{0}-new {1}-{0}
                workon {1}-{0}
                cd {1}-{0}
                python manage.py migrate --noinput --settings=config.settings.{0}
            """.format(instance, instance['name']))
            if not quiet:
                print(stdout.read().decode("utf-8"))
            else:
                stdout.read()
            print(stderr.read().decode("utf-8"))

        print("All done!")
