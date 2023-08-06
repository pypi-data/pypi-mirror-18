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
This module contains the Job class and some related classes.
"""

from collections import OrderedDict
import datetime
import gzip
import os
try:
    import cPickle as pickle
except ImportError:
    import pickle
import re
import urlparse

from enum import Enum

import fastr
from fastr.core.provenance import Provenance
from fastr.core.samples import SampleItem
from fastr.core.serializable import Serializable
from fastr.data import url
from fastr.datatypes import URLType, DataType, Deferred
import fastr.exceptions as exceptions


try:
    from fastr.execution.environmentmodules import EnvironmentModules
    ENVIRONMENT_MODULES = EnvironmentModules(fastr.config.protected_modules)
    ENVIRONMENT_MODULES_LOADED = True
except exceptions.FastrValueError:
    ENVIRONMENT_MODULES_LOADED = False


class JobState(Enum):
    """
    The possible states a Job can be in. An overview of the states and the
    adviced transitions are depicted in the following figure:

    .. graphviz::

       digraph jobstate {
           nonexistent [shape=box];
           created [shape=box];
           queued [shape=box];
           hold [shape=box];
           running [shape=box];
           execution_done [shape=box];
           execution_failed [shape=box];
           processing_callback [shape=box];
           finished [shape=box];
           failed [shape=box];
           cancelled [shape=box];

           nonexistent -> created;
           created -> queued;
           created -> hold;
           hold -> queued;
           queued -> running;
           running -> execution_done;
           running -> execution_failed;
           execution_done -> processing_callback;
           execution_failed -> processing_callback;
           processing_callback -> finished;
           processing_callback -> failed;
           running -> cancelled;
           queued -> cancelled;
           hold -> cancelled;
       }
    """
    nonexistent = ('nonexistent', 'idle', False)
    created = ('created', 'idle', False)
    queued = ('queued', 'idle', False)
    hold = ('hold', 'idle', False)
    running = ('running', 'in_progress', False)
    execution_done = ('execution_done', 'in_progress', False)
    execution_failed = ('execution_failed', 'in_progress', True)
    processing_callback = ('processing_callback', 'in_progress', False)
    finished = ('finished', 'done', False)
    failed = ('failed', 'done', True)
    cancelled = ('cancelled', 'done', True)

    def __init__(self, _, stage, error):
        self.stage = stage
        self.error = error

    @property
    def done(self):
        return self.stage == 'done'

    @property
    def in_progress(self):
        return self.stage == 'in_progress'


class Job(Serializable):

    """Class describing a job.

       Arguments:
       tool_name - the name of the tool (str)
       tool_version - the version of the tool (Version)
       argument - the arguments used when calling the tool (list)
       tmpdir - temporary directory to use to store output data
       hold_jobs - list of jobs that need to finished before this job can run (list)
    """

    # Constants for file names related to jobs
    COMMAND_DUMP = '__fastr_command__.pickle.gz'
    RESULT_DUMP = '__fastr_result__.pickle.gz'
    STDOUT_DUMP = '__fastr_stdout__.txt'
    STDERR_DUMP = '__fastr_stderr__.txt'

    def __init__(self, jobid, tool_name, tool_version, nodeid, sample_id, sample_index, input_arguments, output_arguments, tmpdir, hold_jobs=None,
                 timestamp=None, cores=None, memory=None, walltime=None, status_callback=None, preferred_types=None):
        """
        Create a job

        :param str jobid: the job id
        :param str tool_name: the id of the tool
        :param fastr.core.version.Version tool_version: the version of the tool
        :param str nodeid: the id of the creating node
        :param fastr.core.samples.SampleId sample_id: the id of the sample
        :param list[dict] input_arguments: the argument list
        :param list[dict] output_arguments: the argument list
        :param str tmpdir: the workdir for this job
        :param list[str] hold_jobs: the jobs on which this jobs depend
        :param datetime.datetime timestamp: the time this job was spawned
        :param int cores: number of cores this jobs is allowed consume
        :param str memory: max amount of memory that this job is allowed to consume
        :param str walltime: max amount of time this job is allowed to run
        :return:
        """
        self.jobid = jobid
        self.tool_name = tool_name
        self.nodeid = nodeid
        self.tool_version = str(tool_version)
        self.input_arguments = input_arguments
        self.output_arguments = output_arguments
        self.tmpdir = tmpdir
        self.sample_id = sample_id
        self.sample_index = sample_index
        self._required_cores = None
        self._required_memory = None
        self._required_time = None
        self.required_cores = cores
        self.required_memory = memory
        self.required_time = walltime
        self.translated_values = {}
        self.status_callback = status_callback
        self.preferred_types = preferred_types if preferred_types else {}

        # Some fields for provenance
        self.job_activity = None
        self.tool_agent = None
        self.node_agent = None
        self.network_agent = None

        if isinstance(hold_jobs, (set, list, tuple)):
            self.hold_jobs = list(hold_jobs)
        elif isinstance(hold_jobs, str):
            self.hold_jobs = [hold_jobs]
        elif hold_jobs is None:
            self.hold_jobs = []
        else:
            raise exceptions.FastrTypeError('Cannot create jobs: hold_jobs has invalid type!')

        if timestamp is not None:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.datetime.now()

        self.info_store = {'jobid': self.jobid,
                           'dependencies': self.hold_jobs,
                           'client_tool': {'id': self.tool_name,
                                           'version': str(self.tool_version)},
                           'status': [JobState.nonexistent],
                           'errors': [],
                           'output_hash': {}}
        self.status = JobState.created
        self.provenance = Provenance(self)
        self._init_provenance()

        # Dictionary where the output data will be stored
        self.output_data = {}

    def __getstate__(self):
        """
        Get the state of the job

        :return: job state
        :rtype: dict
        """
        state = {k: v for k, v in self.__dict__.items()}
        del state['status_callback']
        return state

    def __setstate__(self, state):
        """
        Set the state of the job

        :param dict state:
        """
        self.status_callback = None
        self.__dict__.update(state)

    def _init_provenance(self):
        """
        Create initial provenance document
        """
        self.job_activity = self.provenance.activity(self.provenance.job[self.jobid])
        self.tool_agent = self.provenance.agent(
            self.provenance.tool["{}/{}".format(self.tool_name, self.tool_version)],
            {
                'fastrinfo:tool_dump': fastr.toollist[self.tool_name, self.tool_version].dumps()
            }
        )
        self.node_agent = self.provenance.agent(self.provenance.node[self.nodeid])
        #FIXME: Find a better way to collect the current network id
        self.network_agent = self.provenance.agent(
            self.provenance.network["{}/{}".format(fastr.current_network.id, fastr.current_network.version)],
            {
                'fastrinfo:network_dump': fastr.current_network.dumps()
            }
        )
        self.provenance.document.actedOnBehalfOf(self.network_agent, self.provenance.fastr_agent)
        self.provenance.document.actedOnBehalfOf(self.node_agent, self.tool_agent)
        self.provenance.document.actedOnBehalfOf(self.node_agent, self.network_agent)
        self.provenance.document.wasAssociatedWith(self.job_activity, self.node_agent)

    def _collect_provenance(self):
        """
        Collect the provenance for this job
        """
        tool = self.tool
        for input_argument_key, input_argument_value in self.input_arguments.items():
            input_description = tool.inputs[input_argument_key]

            if input_description.hidden:
                # Skip hidden inputs (they are used for the system to feed
                # additional data to sources/sinks etc) not interesting
                # for provenance
                continue

            for cardinality, value in enumerate(input_argument_value.data.iterelements()):
                url = value.data_uri

                parent_provenance = self._get_parent_provenance(value)
                if isinstance(parent_provenance, Provenance):
                    self.provenance.document.update(parent_provenance.document)
                    data_entity = self.provenance.entity(self.provenance.data[url], {
                        'fastrinfo:value': value.value
                    })
                    self.provenance.document.wasGeneratedBy(data_entity, parent_provenance.parent.job_activity)
                else:
                    data_entity = self.provenance.entity(self.provenance.data[url])
                self.provenance.document.used(self.job_activity, data_entity)
        self.provenance.document._records = list(set(self.provenance.document._records))

    @staticmethod
    def _get_parent_provenance(value_url):
        """
        Find the provenace of the parent job

        :param str value_url: url for the value for which to find the job
        :return: the provenance of the job that created the value
        """
        if isinstance(value_url, Deferred):
            return value_url.provenance
        else:
            return None

    def get_result(self):
        """
        Get the result of the job if it is available. Load the output file if
        found and check if the job matches the current object. If so, load and
        return the result.

        :returns: Job after execution or None if not available
        :rtype: Job | None
        """

        if not os.path.exists(self.logfile):
            return None

        try:
            with gzip.open(self.logfile) as fin:
                result = pickle.load(fin)
        except (IOError, EOFError):
            # Errors loading pickle or gzip stream
            return None

        if not isinstance(result, Job):
            fastr.log.debug('Result is not valid Job! (found {})'.format(type(result).__name__))
            return None

        if result.status != JobState.execution_done:
            fastr.log.debug('Result status is wrong ({})'.format(result.status))
            return None

        if result.jobid != self.jobid:
            fastr.log.debug('Result job id is wrong ({})'.format(result.jobid))
            return None

        if result.tool_name != self.tool_name:
            fastr.log.debug('Result tool name is wrong ({})'.format(result.tool_name))
            return None

        if result.tool_version != self.tool_version:
            fastr.log.debug('Result tool version is wrong ({})'.format(result.tool_version))
            return None

        if result.sample_id != self.sample_id:
            fastr.log.debug('Result sample id is wrong ({})'.format(result.sample_id))
            return None

        result_payload = result.create_payload()
        if result_payload != self.create_payload():
            fastr.log.debug('Result payload is wrong ({})'.format(result_payload))
            return None

        return result

    def __repr__(self):
        """
        String representation of the Job
        """
        return '<Job\n  id={job.jobid}\n  tool={job.tool_name} {job.tool_version}\n  tmpdir={job.tmpdir}/>'.format(job=self)

    @property
    def status(self):
        """
        The status of the job
        """
        return self.info_store['status'][-1]

    @status.setter
    def status(self, status):
        """
        Set the status of a job
        :param status: new status
        """
        if not isinstance(status, JobState):
            raise exceptions.FastrTypeError('Job status should be of class JobState, found [{}] {}'.format(type(status).__name__,
                                                                                                           status))
        if self.status != status:
            self.info_store['status'].append(status)

            if self.status_callback is not None:
                self.status_callback(self)

    @property
    def id(self):
        """
        The id of this job
        """
        return self.jobid

    @property
    def fullid(self):
        """
        The full id of the job
        """
        return self.jobid

    @property
    def commandurl(self):
        """
        The url of the command pickle
        """
        return url.join(self.tmpdir, self.COMMAND_DUMP)

    @property
    def logurl(self):
        """
        The url of the result pickle
        """
        return url.join(self.tmpdir, self.RESULT_DUMP)

    @property
    def stdouturl(self):
        """
        The url where the stdout text is saved
        """
        return url.join(self.tmpdir, self.STDOUT_DUMP)

    @property
    def stderrurl(self):
        """
        The url where the stderr text is saved
        """
        return url.join(self.tmpdir, self.STDERR_DUMP)

    @property
    def commandfile(self):
        """
        The path of the command pickle
        """
        return fastr.vfs.url_to_path(self.commandurl)

    @property
    def logfile(self):
        """
        The path of the result pickle
        """
        return fastr.vfs.url_to_path(self.logurl)

    @property
    def stdoutfile(self):
        """
        The path where the stdout text is saved
        """
        return fastr.vfs.url_to_path(self.stdouturl)

    @property
    def stderrfile(self):
        """
        The path where the stderr text is saved
        """
        return fastr.vfs.url_to_path(self.stderrurl)

    @property
    def required_cores(self):
        """
        Number of required cores
        """
        return self._required_cores

    @required_cores.setter
    def required_cores(self, value):
        """
        Number of required cores
        """
        if value is None:
            self._required_cores = value
        else:
            if not isinstance(value, int):
                raise TypeError('Required number of cores should be an integer or None')

            if value < 1:
                raise ValueError('Required number of cores should be above zero ({} < 1)'.format(value))

            self._required_cores = value

    @property
    def required_memory(self):
        """
        Number of required memory
        """
        return self._required_memory

    @required_memory.setter
    def required_memory(self, value):
        """
        Number of required memory
        """
        if value is None:
            self._required_memory = value
        else:
            if isinstance(value, unicode):
                value = str(value)

            if not isinstance(value, str):
                raise TypeError('Required memory should be a str or None (found: {} [{}])'.format(value, type(value).__name__))

            if re.match(r'\d+[mMgG]', value) is None:
                raise ValueError('Required memory should be in the form \\d+[mMgG] (found {})'.format(value))

            self._required_memory = value

    @property
    def required_time(self):
        """
        Number of required runtime
        """
        return self._required_time

    @required_time.setter
    def required_time(self, value):
        """
        Number of required runtime
        """
        if value is None:
            self._required_time = value
        else:
            if isinstance(value, unicode):
                value = str(value)

            if not isinstance(value, str):
                raise TypeError('Required number of cores should be a str or None')

            if re.match(r'^(\d*:\d*:\d*|\d+)$', value) is None:
                raise ValueError('Required memory should be in the form HH:MM:SS or MM:SS (found {})'.format(value))

            self._required_time = value

    @property
    def tool(self):
        return fastr.toollist[self.tool_name, self.tool_version]

    def create_payload(self):
        """
        Create the payload for this object based on all the input/output
        arguments

        :return: the payload
        :rtype: dict
        """
        tool = self.tool
        payload = {'inputs': {}, 'outputs': {}}

        # Fill the payload with the values to use (these should be translated to paths/strings/int etc
        # Translate all inputs to be in correct form
        for id_, value in self.input_arguments.items():
            argument = tool.inputs[id_]
            if isinstance(value, SampleItem):
                if len(value.data.mapping_part()) == 0:
                    value = value.data.sequence_part()
                elif len(value.data.sequence_part()) == 0:
                    value = value.data.mapping_part()
                else:
                    raise ValueError('Fastr does not (yet) accept mixed sequence/mapping input!')

            if not argument.hidden:
                if isinstance(value, tuple):
                    payload['inputs'][id_] = tuple(self.translate_argument(x) for x in value)
                else:  # Should be ordered dict
                    # FIXME: v is actually a tuple that needs fixing
                    payload['inputs'][id_] = OrderedDict((k, tuple(self.translate_argument(x) for x in v)) for k, v in value.items())

            else:
                if issubclass(fastr.typelist[argument.datatype], URLType):
                    payload['inputs'][id_] = tuple(self.translate_argument(x) for x in value)
                else:
                    payload['inputs'][id_] = value

            if len(payload['inputs'][id_]) == 0 and argument.default is not None:
                payload['inputs'][id_] = (argument.default,)

        # Create output arguments automatically
        for id_, spec in self.output_arguments.items():
            if isinstance(spec['cardinality'], int):
                cardinality = spec['cardinality']
            else:
                cardinality = self.calc_cardinality(spec['cardinality'], payload)
            payload['outputs'][id_] = self.fill_output_argument(tool.outputs[id_], cardinality, spec['datatype'])

        return payload

    @staticmethod
    def calc_cardinality(desc, payload):
        if desc[0] == 'int':
            return desc[1]
        elif desc[0] == 'as':
            if desc[1] in payload['inputs']:
                return len(payload['inputs'][desc[1]])
            if desc[1] in payload['outputs']:
                return len(payload['outputs'][desc[1]])
            else:
                raise exceptions.FastrValueError('Cannot determine cardinality from {} (payload {})'.format(desc, payload))
        elif desc[0] == 'val':
            if desc[1] in payload['inputs'] and len(payload['inputs'][desc[1]]) == 1:
                return int(str(payload['inputs'][desc[1]][0]))
            if desc[1] in payload['outputs'] and len(payload['outputs'][desc[1]]) == 1:
                return int(str(payload['outputs'][desc[1]][0]))
            else:
                raise exceptions.FastrValueError('Cannot determine cardinality from {} (payload {})'.format(desc, payload))
        else:
                raise exceptions.FastrValueError('Cannot determine cardinality from {} (payload {})'.format(desc, payload))

    def execute(self):
        """
        Execute this job

        :returns: The result of the execution
        :rtype: InterFaceResult
        """
        tool = fastr.toollist[self.tool_name, self.tool_version]

        # Create the payload
        fastr.log.info('Start executing tool')
        start = datetime.datetime.now()
        payload = self.create_payload()
        end = datetime.datetime.now()
        fastr.log.info('Finished creating payload in {} seconds'.format((end - start).total_seconds()))

        # Execute the tool
        fastr.log.info('Start executing tool')
        start = datetime.datetime.now()
        result = tool.execute(payload)
        end = datetime.datetime.now()
        fastr.log.info('Finished executing tool in {} seconds'.format((end - start).total_seconds()))
        self.info_store['process'] = result.log_data

        fastr.log.info('Start translating results tool')
        start = datetime.datetime.now()
        self.output_data = self.translate_results(result.result_data)
        end = datetime.datetime.now()
        fastr.log.info('Finished translating results in {} seconds'.format((end - start).total_seconds()))

        # Collect the provenance for the node
        self._collect_provenance()

        if not self.validate_results(payload):
            raise exceptions.FastrValueError('Output values are not valid!')

        return result

    def translate_argument(self, value):
        """
        Translate an argument from a URL to an actual path.

        :param value: value to translate
        :param datatype: the datatype of the value
        :return: the translated value
        """
        return self.get_value(value=value)

    def get_output_datatype(self, output_id):
        """
        Get the datatype for a specific output

        :param str output_id: the id of the output to get the datatype for
        :return: the requested datatype
        :rtype: BaseDataType
        """
        output = self.tool.outputs[output_id]
        datatype = fastr.typelist[output.datatype]

        # If there are preferred types, match with that if possible
        if output_id in self.preferred_types and len(self.preferred_types[output_id]) > 0:
            new_datatype = fastr.typelist.match_types(datatype, preferred=self.preferred_types[output_id])
            if new_datatype is not None:
                fastr.log.info('Found new type (after using preferred): {} -> {}'.format(datatype.id, new_datatype.id))
                datatype = new_datatype
        return datatype

    def translate_results(self, result):
        """
        Translate the results of an interface (using paths etc) to the proper
        form using URI's instead.

        :param dict result: the result data of an interface
        :return: the translated result
        :rtype: dict
        """
        for key, value in result.items():
            datatype = self.get_output_datatype(key)

            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    new_subvalue = []
                    for item in subvalue:
                        if not isinstance(item, DataType):
                            item = datatype(str(item))
                        if isinstance(item, URLType):
                            item.value = fastr.vfs.path_to_url(item.value)
                        new_subvalue.append(item)
                    value[subkey] = tuple(new_subvalue)
            else:
                new_value = []
                for item in value:
                    if not isinstance(item, DataType):
                        item = datatype(str(item))
                    if isinstance(item, URLType):
                        item.value = fastr.vfs.path_to_url(item.value)
                    new_value.append(item)
                result[key] = new_value

        return result

    def fill_output_argument(self, output_spec, cardinality, desired_type):
        """
        This is an abstract class method. The method should take the argument_dict
        generated from calling self.get_argument_dict() and turn it into a list
        of commandline arguments that represent this Input/Output.

        :param int cardinality: the cardinality for this output (can be non for automatic outputs)
        :param DataType desired_type: the desired datatype for this output
        :return: the values for this output
        :rtype: list
        """
        values = []

        if not output_spec.automatic:
            datatype = fastr.typelist[desired_type]

            for cardinality_nr in range(cardinality):
                if datatype.extension is not None:
                    output_url = '{}/{}_{}.{}'.format(self.tmpdir, output_spec.id, cardinality_nr, datatype.extension)
                else:
                    output_url = '{}/{}_{}'.format(self.tmpdir, output_spec.id, cardinality_nr)

                # Wrap the output url in the correct DataType
                fastr.log.info('Wrapping {} in a {}'.format(output_url, datatype))
                output_value = datatype(output_url)
                fastr.log.info('Got {}'.format(output_value))

                # Translate to a path and use
                values.append(self.translate_argument(output_value))

        return tuple(values)

    @classmethod
    def get_value(cls, value):
        """
        Get a value

        :param value: the url of the value
        :param datatype: datatype of the value
        :return: the retrieved value
        """
        if isinstance(value, Deferred):
            value = value.target

        # If the value already has valid datatype, use that and don't guess from scratch
        if isinstance(value, URLType):
            datatype = type(value)
            if url.isurl(str(value)):
                value = fastr.vfs.url_to_path(value)
            else:
                if not os.path.exists(value):
                    raise exceptions.FastrValueError('Found a non-url path ({}) that does not exist!'.format(value))
            return datatype(value)
        elif isinstance(value, DataType):
            return value
        else:
            raise exceptions.FastrTypeError('Arguments should be either a DataType, found {}'.format(type(value).__name__))

    def hash_results(self):
        """
        Create hashes of all output values and store them in the info store
        """
        for output in self.output_arguments.values():
            id_ = output['id']
            output_value = self.output_data[id_]
            output_datatype = fastr.typelist[output['datatype']]

            if isinstance(output_value, list):
                self.info_store['output_hash'][id_] = [output_datatype(x).checksum() for x in output_value]
            elif isinstance(output_value, dict):
                self.info_store['output_hash'][id_] = {}
                for sample_id, output_val in output_value.items():
                    self.info_store['output_hash'][id_][sample_id] = [output_datatype(x).checksum() for x in output_val]

    def validate_results(self, payload):
        """
        Validate the results of the Job

        :return: flag indicating the results are complete and valid
        """

        valid = True
        for output in self.output_arguments.values():
            id_ = output['id']
            output_value = self.output_data[id_]

            if isinstance(output_value, (list, tuple)):
                if not self._validate_result(output, output_value, payload):
                    message = 'The output "{}" is invalid!'.format(id_)
                    self.info_store['errors'].append(exceptions.FastrOutputValidationError(message).excerpt())
                    fastr.log.warning(message)
                    valid = False
            elif isinstance(output_value, dict):
                for sample_id, output_val in output_value.items():
                    if not self._validate_result(output, output_val, payload):
                        message = 'The output "{}" for sample "{}" is invalid!'.format(id_, sample_id)
                        self.info_store['errors'].append(exceptions.FastrOutputValidationError(message).excerpt())
                        fastr.log.warning(message)
                        valid = False

            else:
                raise exceptions.FastrTypeError('Output data is not of correct type (expected a list/dict)')

        return valid

    def write(self):
        with gzip.open(self.logfile, 'wb') as result_file:
            result_file.write(pickle.dumps(self))

    def _validate_result(self, output, output_value, payload):
        """
        Validate the result for a specific otuput/sample
        :param output: the output for which to check
        :param output_value: the value for the output
        :return: flag indicating if the result is value
        """
        valid = True

        if output['cardinality'] is not None:
            if ((isinstance(output['cardinality'], int) and output['cardinality'] != len(output_value)) or
                    (isinstance(output['cardinality'], tuple) and self.calc_cardinality(output['cardinality'], payload) != len(output_value))):
                message = 'Cardinality mismatch for {} (found {}, expected {})'.format(output['id'],
                                                                                       len(output_value),
                                                                                       output['cardinality'])
                self.info_store['errors'].append(exceptions.FastrOutputValidationError(message).excerpt())
                fastr.log.warning(message)
                valid = False

        for value in output_value:
            output_datatype = fastr.typelist[output['datatype']]
            typed_value = output_datatype(value)
            if not typed_value.valid:
                message = 'Output value "{}" not valid for datatype "{}"'.format(value, output['datatype'])
                self.info_store['errors'].append(exceptions.FastrOutputValidationError(message).excerpt())
                fastr.log.warning(message)
                valid = False

        return valid


class SinkJob(Job):
    """
    Special SinkJob for the Sink
    """
    def __init__(self,
                 jobid,
                 tool_name,
                 tool_version,
                 nodeid,
                 sample_id,
                 sample_index,
                 input_arguments,
                 output_arguments,
                 tmpdir,
                 hold_jobs=None,
                 timestamp=None,
                 cores=None,
                 memory=None,
                 walltime=None,
                 substitutions=None,
                 status_callback=None,
                 preferred_types=None):
        super(SinkJob, self).__init__(jobid=jobid,
                                      tool_name=tool_name,
                                      tool_version=tool_version,
                                      nodeid=nodeid,
                                      sample_id=sample_id,
                                      sample_index=sample_index,
                                      input_arguments=input_arguments,
                                      output_arguments=output_arguments,
                                      tmpdir=tmpdir,
                                      hold_jobs=hold_jobs,
                                      timestamp=timestamp,
                                      cores=cores,
                                      memory=memory,
                                      walltime=walltime,
                                      status_callback=status_callback,
                                      preferred_types=preferred_types)

        self._substitutions = substitutions if substitutions else {}

    def __repr__(self):
        """
        String representation for the SinkJob
        """
        return '<SinkJob\n  id={job.jobid}\n  tmpdir={job.tmpdir}/>'.format(job=self)

    def get_result(self):
        """
        Get the result of the job if it is available. Load the output file if
        found and check if the job matches the current object. If so, load and
        return the result.

        :returns: Job after execution
        """
        return None

    def validate_results(self, payload):
        """
        Validate the results of the SinkJob

        :return: flag indicating the results are complete and valid
        """
        if self.info_store['process']['stderr'] != '':
            message = 'SinkJob should have an empty stderr, found error messages!\n{}'.format(self.info_store['process']['stderr'])
            fastr.log.warning(message)
            self.info_store['errors'].append(exceptions.FastrOutputValidationError(message).excerpt())
            return False
        else:
            return True

    def create_payload(self):
        """
        Create the payload for this object based on all the input/output
        arguments

        :return: the payload
        :rtype: dict
        """
        payload = super(SinkJob, self).create_payload()
        fastr.log.info('Temp payload: {}'.format(payload))

        payload['inputs']['output'] = (self.substitute(payload['inputs']['output'][0], datatype=type(payload['inputs']['input'][0])),)
        return payload

    def substitute(self, value, datatype=None):
        """
        Substitute the special fields that can be used in a SinkJob.

        :param str value: the value to substitute fields in
        :param BaseDataType datatype: the datatype for the value
        :return: string with substitutions performed
        :rtype: str
        """
        if datatype is None:
            datatype = type(value)

        subs = dict(self._substitutions)
        subs['ext'] = '.{}'.format(datatype.extension) if datatype.extension is not None else ''
        return str(value).format(**subs)


class SourceJob(Job):
    """
    Special SourceJob for the Source
    """
    def __repr__(self):
        """
        String representation for the SourceJob
        """
        return '<SourceJob\n  id={job.jobid}\n  tmpdir={job.tmpdir}/>'.format(job=self)

    def validate_results(self, payload):
        """
        Validate the results of the Job

        :return: flag indicating the results are complete and valid
        """
        if self.info_store['process']['stderr'] != '':
            message = 'SourceJob should have an empty stderr, found error messages!'
            fastr.log.warning(message)
            self.info_store['errors'].append(exceptions.FastrOutputValidationError(message).excerpt())
            return False
        else:
            return True

    def get_output_datatype(self, output_id):
        """
        Get the datatype for a specific output

        :param str output_id: the id of the output to get the datatype for
        :return: the requested datatype
        :rtype: BaseDataType
        """
        return fastr.typelist[self._datatype]


class InlineJob(Job):
    def __init__(self, *args, **kwargs):
        super(InlineJob, self).__init__(*args, **kwargs)
        self._collect_provenance()

    def get_result(self):
        if not os.path.exists(self.logfile):
            return None

        try:
            with gzip.open(self.logfile) as fin:
                result = pickle.load(fin)
        except (IOError, EOFError):
            # Errors loading pickle or gzip stream
            return None

        if not isinstance(result, Job):
            fastr.log.debug('Result is not valid Job! (found {})'.format(type(result).__name__))
            return None

        return result

    def _collect_provenance(self):
        """
        Collect the provenance for this job
        """
        tool = self.tool
        for input_argument_key, input_argument_value in self.input_arguments.items():
            input_description = tool.inputs[input_argument_key]

            if input_description.hidden:
                # Skip hidden inputs (they are used for the system to feed
                # additional data to sources/sinks etc) not interesting
                # for provenance
                continue

            for sample in input_argument_value:
                for cardinality, value in enumerate(sample.data.iterelements()):
                    url = value.data_uri
                    parent_provenance = self._get_parent_provenance(value)
                    if isinstance(parent_provenance, Provenance):
                        self.provenance.document.update(parent_provenance.document)
                        data_entity = self.provenance.entity(self.provenance.data[url], {
                            'fastrinfo:value': value.value
                        })
                        self.provenance.document.wasGeneratedBy(data_entity, parent_provenance.parent.job_activity)
                    else:
                        data_entity = self.provenance.entity(self.provenance.data[url])
                    self.provenance.document.used(self.job_activity, data_entity)
        self.provenance.document._records = list(set(self.provenance.document._records))
