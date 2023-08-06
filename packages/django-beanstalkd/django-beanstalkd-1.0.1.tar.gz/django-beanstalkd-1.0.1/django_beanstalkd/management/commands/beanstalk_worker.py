# -*- coding: utf-8 -*-

import logging
import os
import sys
import time
import traceback

from beanstalkc import SocketError
from django.conf import settings
from django_six import CompatibilityBaseCommand

from django_beanstalkd import BeanstalkError, connect_beanstalkd


logger = logging.getLogger('django_beanstalkd')
logger.addHandler(logging.StreamHandler())


class Command(CompatibilityBaseCommand):
    __doc__ = help = 'Start a Beanstalk worker serving all registered Beanstalk jobs'

    def add_arguments(self, parser):
        parser.add_argument(
            '-w',
            '--workers',
            action='store',
            dest='worker_count',
            default=1,
            type=int,
            help='Number of workers to spawn.',
        )
        parser.add_argument(
            '-l',
            '--log-level',
            action='store',
            dest='log_level',
            default='info',
            choices=['debug', 'info', 'warning', 'error'],
            help='Log level of worker process.',
        )

    children = []  # list of worker processes
    jobs = {}

    def handle(self, *args, **options):
        # Set log level
        logger.setLevel(getattr(logging, options['log_level'].upper()))

        # Find beanstalk job modules
        bs_modules = []
        for app in settings.INSTALLED_APPS:
            try:
                modname = '%s.beanstalk_jobs' % app
                __import__(modname)
                bs_modules.append(sys.modules[modname])
            except ImportError:
                pass
        if not bs_modules:
            logger.error('No beanstalk_jobs modules found!')
            return

        # Find all jobs
        jobs = []
        for bs_module in bs_modules:
            try:
                jobs += bs_module.beanstalk_job_list
            except AttributeError:
                pass
        if not jobs:
            logger.error('No beanstalk jobs found!')
            return
        logger.info('Available jobs:')
        for job in jobs:
            # Determine right name to register function with
            app = job.app
            jobname = job.__name__
            try:
                func = settings.BEANSTALK_JOB_NAME % {
                    'app': app,
                    'job': jobname,
                }
            except AttributeError:
                func = '%s.%s' % (app, jobname)
            self.jobs[func] = job
            logger.info('* %s' % func)

        # Spawn all workers and register all jobs
        self.spawn_workers(max(options['worker_count'], 1))

        # Start working
        logger.info('Starting to work... (press ^C to exit)')
        try:
            for child in self.children:
                os.waitpid(child, 0)
        except KeyboardInterrupt:
            sys.exit(0)

    def spawn_workers(self, worker_count):
        """
        Spawn as many workers as desired (at least 1).
        Accepts:
        - worker_count, positive int
        """
        # No need for forking if there's only one worker
        if worker_count == 1:
            return self.work()

        logger.info('Spawning %s worker(s)' % worker_count)
        # Spawn children and make them work (hello, 19th century!)
        for i in range(worker_count):
            child = os.fork()
            if child:
                self.children.append(child)
                continue
            else:
                self.work()
                break

    def work(self):
        """Children only: watch tubes for all jobs, start working"""
        try:

            while True:
                try:
                    # Reattempt Beanstalk connection if connection attempt fails or is dropped
                    beanstalk = connect_beanstalkd()
                    for job in self.jobs.keys():
                        beanstalk.watch(job)
                    beanstalk.ignore('default')

                    # Connected to Beanstalk queue, continually process jobs until an error occurs
                    self.process_jobs(beanstalk)

                except (BeanstalkError, SocketError) as e:
                    logger.info('Beanstalk connection error: ' + str(e))
                    time.sleep(2.0)
                    logger.info('Retrying Beanstalk connection...')

        except KeyboardInterrupt:
            sys.exit(0)

    def process_jobs(self, beanstalk):
        while True:
            logger.debug('Beanstalk connection established, waiting for jobs')
            job = beanstalk.reserve()
            job_name = job.stats()['tube']
            if job_name in self.jobs:
                logger.debug('Calling %s with arg: %s' % (job_name, job.body))
                try:
                    self.jobs[job_name](job.body)
                except Exception, e:
                    tp, value, tb = sys.exc_info()
                    logger.error('Error while calling "%s" with arg "%s": %s' % (job_name, job.body, e))
                    logger.debug('%s:%s' % (tp.__name__, value))
                    logger.debug('\n'.join(traceback.format_tb(tb)))
                    job.bury()
                else:
                    job.delete()
            else:
                job.release()
