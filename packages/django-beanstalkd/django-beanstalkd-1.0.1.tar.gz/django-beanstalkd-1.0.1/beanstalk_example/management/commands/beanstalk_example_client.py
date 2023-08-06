# -*- coding: utf-8 -*-

from django_six import CompatibilityBaseCommand

from django_beanstalkd import BeanstalkClient


class Command(CompatibilityBaseCommand):
    __doc__ = help = 'Execute an example command with the django_beanstalk_jobs interface'

    def handle(self, *args, **options):
        client = BeanstalkClient()

        print 'Asynchronous Beanstalk Call'
        print '-------------------------'
        print 'Notice how this app exits, while the workers still work on the tasks.'
        for i in range(4):
            client.call('beanstalk_example.background_counting', '5')
