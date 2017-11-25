from os import putenv, system

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


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

    def handle(self, *args, **options):
        """
        Handler for the command. Backs up the database in the source environment,
        then restores it to the target. Sanity check in place to never restore to
        production.
        """

        # Check to ensure the require setting is in Django's settings.
        if settings.DJANGO_PUBLISHER_INSTANCES is not None:
            instances = settings.DJANGO_PUBLISHER_INSTANCES
        else:
            raise CommandError('You have not configured in DJANGO_PUBLISHER_INSTANCES in your Django settings.')

        # Grab the instance settings if they're properly set
        if options['instance'] in instances:
            instance = instances[options['instance']]
        else:
            raise CommandError(
                'The instance name you provided ("{instance}") is not configured in your settings DJANGO_PUBLISHER_INSTANCES.'.format(
                    instance=options['instance'],
                )
            )

        print(
            "We are about to deploy the instance '{instance}' to the following servers: {servers}.".format(
                instance=options['instance'],
                servers=', '.join(instance['servers']),
            )
        )
        verify = input('Are you sure you want to do this (enter "yes" to proceed)? ')

        if verify == 'yes':
            print("Publishing...")
