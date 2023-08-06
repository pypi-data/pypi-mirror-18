# Copyright 2011-2014 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module holds the ExecutionPluginManager as well as the base-class
for all ExecutionPlugins.
"""

from abc import abstractmethod
import functools
import gzip
import pickle
import sys
import threading
import traceback
import types

from enum import Enum

import fastr
from fastr import exceptions
from fastr.core.baseplugin import Plugin
from fastr.core.pluginmanager import PluginSubManager
from fastr.execution.job import Job, JobState
from fastr.utils import iohelpers


class JobAction(Enum):
    """
    Job actions that can be performed. This is used for checking
    if held jobs should be queued, held longer or be cancelled.
    """

    hold = 'hold'
    queue = 'queue'
    cancel = 'cancel'


class ExecutionPlugin(Plugin):
    """
    This class is the base for all Plugins to execute jobs somewhere. There are
    many methods already in place for taking care of stuff. Most plugins should
    only need to redefine a few abstract methods:

    * :py:meth:`__init__ <fastr.execution.executionpluginmanager.ExecutionPlugin.__init__>`
      the constructor
    * :py:meth:`cleanup <fastr.execution.executionpluginmanager.ExecutionPlugin.__init__>`
      a clean up function that frees resources, closes connections, etc
    * :py:meth:`_queue_job <fastr.execution.executionpluginmanager.ExecutionPlugin._queue_job>`
      the method that queues the job for execution
    * :py:meth:`_cancel_job <fastr.execution.executionpluginmanager.ExecutionPlugin._cancel_job>`
      cancels a previously queued job
    * :py:meth:`_release_job <fastr.execution.executionpluginmanager.ExecutionPlugin._release_job>`
      releases a job that is currently held
    * :py:meth:`_job_finished <fastr.execution.executionpluginmanager.ExecutionPlugin._job_finished>`
      extra callback for when a job finishes

    Not all of the functions need to actually do anything for a plugin. There
    are examples of plugins that do not really need a ``cleanup``, but for
    safety you need to implement it. Just using a ``pass`` for the method could
    be fine in such a case.

    .. warning::

        When overwriting other function, extreme care must be taken not to break
        the plugins working.
    """

    @abstractmethod
    def __init__(self, finished_callback=None, cancelled_callback=None, status_callback=None):
        """
        Setup the ExecutionPlugin

        :param finished_callback: the callback to call after a job finished
        :param cancelled_callback: the callback to call after a job cancelled
        :return: newly created ExecutionPlugin
        """
        super(ExecutionPlugin, self).__init__()

        # Pylint seems to be unable to figure out the .dict() member
        # pylint: disable=no-member

        self.job_status = {}
        self.job_dict = {}
        self.job_archive = {}
        self._finished_callback = finished_callback
        self._cancelled_callback = cancelled_callback
        self._status_callback = status_callback

        # Dict indicating the depending jobs for a certain jobs (who is waiting on the key jobid)
        self.held_queue = {}
        self.held_queue_lock = threading.Lock()

        # Flag indicating the plugin is accepting new jobs queued
        self.accepting = True

    def __enter__(self):
        return self

    def __exit__(self, type_, value, tb):
        self.cleanup()

    def __del__(self):
        """
        Cleanup if the variable was deleted on purpose
        """
        fastr.log.debug('Calling cleanup')
        self.cleanup()

    @abstractmethod
    def cleanup(self):
        """
        Method to call to clean up the ExecutionPlugin. This can be to clear
        temporary data, close connections, etc.

        :param force: force cleanup (e.g. kill instead of join a process)
        """
        # Stop accepting new jobs (close the queue)
        self.accepting = False

        # Cancel all queued jobs
        while len(self.job_dict) > 0:
            jobid, job = self.job_dict.popitem()
            fastr.log.debug('Cleanup cancelling {}'.format(jobid))
            self.cancel_job(job)

    def queue_job(self, job):
        """
        Add a job to the execution queue

        :param Job job: job to add
        """
        if not self.accepting:
            return

        if isinstance(job, list):
            for j in job:
                self.queue_job(j)
            return

        self.job_dict[job.jobid] = job
        self.job_status[job.jobid] = job.status = JobState.queued

        for hold_id in job.hold_jobs:
            # Add job reference to held queue to receive signal when the
            # required jobs are finished/failed. Do not subscribe for jobs that
            # are already finished.
            if hold_id in self.job_status and self.job_status[hold_id].done:
                continue

            with self.held_queue_lock:
                if hold_id not in self.held_queue:
                    self.held_queue[hold_id] = []

                # append to held_queue, because of the managed dict, we need to replace the value (not update)
                self.held_queue[hold_id].append(job.jobid)

        # Save the job to file before serializing
        with gzip.open(job.commandfile, 'wb') as fout:
            fastr.log.debug('Writing job pickle.gz to: {}'.format(job.commandfile))
            pickle.dump(job, fout)

        self._queue_job(job)

    def cancel_job(self, job):
        """
        Cancel a job previously queued

        :param job: job to cancel
        """
        if not isinstance(job, Job):
            try:
                job = self.job_dict[job]
            except KeyError:
                fastr.log.warning('Job {} is no longer under processing, cannot cancel!'.format(job))
                return

        fastr.log.debug('Cancelling {}'.format(job.jobid))

        job.status = self.job_status[job.id] = JobState.cancelled

        fastr.log.debug('Cancelling children for {}'.format(job.id))
        if job.id in self.held_queue:
            fastr.log.debug('Found children....')
            held_queue = self.held_queue[job.id]
            for dependent_job in held_queue:
                fastr.log.debug('Checking sub {}'.format(dependent_job))
                if dependent_job in self.job_dict and dependent_job in self.job_status and not self.job_status[dependent_job].done:
                    fastr.log.debug('Cancelling sub {}'.format(dependent_job))
                    self.cancel_job(dependent_job)
        else:
            fastr.log.debug('No children....')

        self._cancel_job(job)

        fastr.log.debug('Removing {} from jobdict'.format(job.jobid))
        self.job_archive[job.id] = job
        try:
            del self.job_dict[job.id]
        except KeyError:
            pass

        fastr.log.debug('Calling cancelled for {}'.format(job.id))
        if self._cancelled_callback is not None:
            self._cancelled_callback(job)

    def release_job(self, job):
        """
        Release a job that has been put on hold

        :param jobid: job to release
        """
        if not isinstance(job, Job):
            if job not in self.job_dict:
                fastr.log.warning('Job {} is no longer under processing, cannot release!'.format(job))
                return

            try:
                job = self.job_dict[job]
            except KeyError:
                fastr.log.warning('Job {} is no longer under processing, cannot release!'.format(job))
                return

        job.status = JobState.queued
        self._release_job(job.id)

    def job_finished(self, job, blocking=False):
        """
        The default callback that is called when a Job finishes. This will
        create a new thread that handles the actual callback.

        :param Job job: the job that finished
        :return:
        """
        if not blocking:
            # The callback has to finish immediately, so create thead to handle callback and return
            callback_thread = threading.Thread(target=self._job_finished_body,
                                               name='fastr_jobfinished_callback',
                                               args=(job,))
            callback_thread.start()
        else:
            self._job_finished_body(job)

    def _job_finished_body(self, job):
        """
        The actual callback that is executed in a separate thread. This
        method handles the collection of the result, the release of depending
        jobs and calling the user defined callback.

        :param Job job: the job that finished
        """
        fastr.log.debug('ExecutorInterface._job_finished_callback called')
        self.job_status[job.jobid] = JobState.processing_callback

        # The Job finished should always log the errors rather than
        # crashing the whole execution system
        # pylint: disable=bare-except
        try:
            try:
                job = iohelpers.load_gpickle(job.logfile)
            except EOFError:
                job.info_store['errors'].append(
                exceptions.FastrResultFileNotFound(
                    ('Could not read job result file {}, assuming '
                     'the job crashed during output write.').format(job.logfile)).excerpt())
                job.status = JobState.failed
            except IOError:
                job.info_store['errors'].append(
                    exceptions.FastrResultFileNotFound(
                        ('Could not find/read job result file {}, assuming '
                         'the job crashed before it created output.').format(job.logfile)).excerpt())
                job.status = JobState.failed

            if self._status_callback is not None:
                self._status_callback(job)
                job.status_callback = self._status_callback

        except:
            exc_type, _, trace = sys.exc_info()
            exc_info = traceback.format_exc()
            trace = traceback.extract_tb(trace, 1)[0]
            fastr.log.error('Encountered exception ({}) during execution:\n{}'.format(exc_type.__name__, exc_info))
            if 'errors' not in job.info_store:
                job.info_store['errors'] = []
            job.info_store['errors'].append((exc_type.__name__, exc_info, trace[0], trace[1]))
            job.status = JobState.execution_failed

        result = job
        fastr.log.debug('Finished {} with status {}'.format(job.jobid, job.status))
        jobid = result.jobid

        # Make sure the status is either finished or failed
        if result.status == JobState.execution_done:
            result.status = JobState.finished
        else:
            result.status = JobState.failed

        # Set the job status so the hold jobs will be release properly
        self.job_status[jobid] = result.status
        if jobid in self.job_dict:
            self.job_dict[jobid].status = JobState.finished

        # The ProcessPoolExecutor has to track job dependencies itself, so
        # therefor we have to check for jobs depending on the finished job
        if jobid in self.held_queue:
            fastr.log.debug('Signaling depending jobs {}'.format(self.held_queue[jobid]))
            ready_jobs = []
            for held_jobid in self.held_queue[jobid]:
                action = self.check_job_requirements(held_jobid)
                if action == JobAction.queue:
                    # Re-assign managed dict member
                    if held_jobid in self.job_dict:
                        held_job = self.job_dict[held_jobid]
                        self.job_dict[held_jobid] = held_job
                    fastr.log.debug('Job {} is now ready to be submitted'.format(held_jobid))

                    # If ready, flag job for removal from held queue and send
                    # to pool queue to be executed
                    ready_jobs.append(held_jobid)
                    self.release_job(held_jobid)
                elif action == JobAction.cancel:
                    fastr.log.debug('Job {} will be cancelled'.format(held_jobid))
                    ready_jobs.append(held_jobid)
                    self.cancel_job(held_jobid)
                else:
                    fastr.log.debug('Job {} still has unmet dependencies'.format(held_jobid))

            # Remove jobs that no longer need to be held from held_queue
            for readyjobid in ready_jobs:
                job = self.get_job(readyjobid)

                for hold_id in job.hold_jobs:
                    with self.held_queue_lock:
                        if hold_id in self.held_queue:
                            # remove from held_queue. because of the managed dict,
                            # we need to replace the value (not update)
                            required_job = self.held_queue[hold_id]
                            if readyjobid in required_job:
                                required_job.remove(readyjobid)
                            else:
                                fastr.log.warning('Could not remove {} from {}'.format(readyjobid, required_job))

            with self.held_queue_lock:
                del self.held_queue[jobid]

        # Extra subclass callback
        fastr.log.debug('Subclass callback')
        try:
            self._job_finished(result)
        except:
            exc_type, _, _ = sys.exc_info()
            exc_info = traceback.format_exc()
            fastr.log.error('Encountered exception ({}) during callback {}._job_finished:\n{}'.format(exc_type.__name__, type(self).__name__, exc_info))

        # Extra callback from object
        fastr.log.debug('Calling callback for {}'.format(jobid))
        if self._finished_callback is not None:
            try:
                self._finished_callback(result)
            except:
                if isinstance(self._finished_callback, functools.partial):
                    args = self._finished_callback.args + tuple('{}={}'.format(k, v) for k, v in self._finished_callback.keywords.items())
                    callback_name = '{f.__module__}.{f.func_name}({a})'.format(f=self._finished_callback.func, a=','.join(args))
                elif isinstance(self._finished_callback, types.FunctionType):
                    callback_name = '{f.__module__}.{f.func_name}'.format(f=self._finished_callback)
                elif isinstance(self._finished_callback, types.MethodType):
                    callback_name = '{m.__module__}.{m.im_class.__name__}.{m.im_func.func_name}'.format(m=self._finished_callback)
                else:
                    callback_name = repr(self._finished_callback)
                exc_type, _, _ = sys.exc_info()
                exc_info = traceback.format_exc()
                fastr.log.error('Encountered exception ({}) during callback {}:\n{}'.format(exc_type.__name__, callback_name, exc_info))
        else:
            fastr.log.debug('No callback specified')

        # Move the job to archive (to keep the number of working jobs limited
        # in the future the archive can be moved to a db/disk if needed
        fastr.log.debug('Archiving job {} with status {}'.format(jobid, result.status))
        try:
            del self.job_status[jobid]
        except KeyError:
            pass

        self.job_archive[jobid] = result

        try:
            del self.job_dict[jobid]
        except KeyError:
            pass
        fastr.log.debug('Done archiving')

    def get_job(self, jobid):
        try:
            return self.job_dict[jobid]
        except KeyError:
            try:
                return self.job_archive[jobid]
            except:
                raise exceptions.FastrKeyError('Could not find job {}'.format(jobid))

    def get_status(self, job):
        if not isinstance(job, Job):
            job = self.get_job(job)

        return job.status

    @abstractmethod
    def _queue_job(self, job):
        """
        Method that a subclass implements to actually queue a Job for execution

        :param job: job to queue
        """
        pass

    @abstractmethod
    def _cancel_job(self, jobid):
        """
        Method that a subclass implements to actually cancel a Job

        :param jobid: job to queue
        """
        pass

    @abstractmethod
    def _release_job(self, jobid):
        """
        Method that a subclass implements to actually release a job

        :param jobid: job to queue
        """
        pass

    @abstractmethod
    def _job_finished(self, job):
        """
        Method that a subclass can implement to add to the default callback.
        It will be called by ``_job_finished_body`` right before the user
        defined callback will be called.

        :param job: Job that resulted from the execution
        """
        pass

    def show_jobs(self, req_status=None):
        """
        List the queued jobs, possible filtered by status

        :param req_status: requested status to filter on
        :return: list of jobs
        """
        if isinstance(req_status, basestring):
            req_status = JobState[req_status]

        if not isinstance(req_status, JobState):
            return []

        results = []
        for key, status in self.job_status.items():
            if req_status is None or status == req_status:
                results.append(self.get_job(key))

        return results

    def check_job_status(self, jobid):
        """
        Get the status of a specified job

        :param jobid: the target job
        :return: the status of the job (or None if job not found)
        """
        try:
            return self.get_status(jobid)
        except exceptions.FastrKeyError:
            return None

    def check_job_requirements(self, jobid):
        """
        Check if the requirements for a job are fulfilled.

        :param jobid: job to check
        :return: directive what should happen with the job
        :rtype: JobAction
        """
        job = self.get_job(jobid)
        if job.hold_jobs is None or len(job.hold_jobs) == 0:
            return JobAction.queue

        all_done = True
        for hold_id in job.hold_jobs:
            status = self.check_job_status(hold_id)
            if status is not None and status != JobState.finished:
                if status.done:
                    return JobAction.cancel
                else:
                    fastr.log.debug('Dependency {} for {} is unmet ({})'.format(hold_id, jobid, status))
                    all_done = False

        if all_done:
            return JobAction.queue
        else:
            return JobAction.hold


class ExecutionPluginManager(PluginSubManager):
    """
    Container holding all the ExecutionPlugins known to the Fastr system
    """

    def __init__(self):
        """
        Initialize a ExecutionPluginManager and load plugins.

        :param path: path to search for plugins
        :param recursive: flag for searching recursively
        :return: newly created ExecutionPluginManager
        """
        super(ExecutionPluginManager, self).__init__(parent=fastr.plugin_manager,
                                                     plugin_class=self.plugin_class)

    @property
    def plugin_class(self):
        """
        The class of the Plugins expected in this BasePluginManager
        """
        return ExecutionPlugin
