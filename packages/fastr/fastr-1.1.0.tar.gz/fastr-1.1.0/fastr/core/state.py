from enum import Enum
import textwrap


class JobState(Enum):
    """
    The state a Job is in.
    """
    nonexistent = ('idle', ('created',), False)
    created = ('idle', ('queued', 'hold'), False)
    queued = ('idle', ('running', 'hold', 'cancelled'), False)
    hold = ('idle', ('queued', 'cancelled'), False)
    running = ('in_progress', ('execution_done', 'execution_failed', 'cancelled'), False)
    execution_done = ('in_progress', ('processing_callback',), False)
    execution_failed = ('in_progress', ('processing_callback',), True)
    processing_callback = ('in_progress', ('finished', 'failed'), False)
    finished = ('done', (), False)
    failed = ('done', (), True)
    cancelled = ('done', (), True)

    def __init__(self, stage, transitions_to, error):
        self.stage = stage
        self.error = error
        self.transitions_to = transitions_to

    @property
    def done(self):
        return self.stage == 'done'

    @property
    def in_progress(self):
        return self.stage == 'in_progress'


class NodeState(Enum):
    """
    The state the Node is in.
    """

    invalid = (('valid',),)
    valid = (('invalid', 'in_progress'),)
    in_progress = (('done', 'error'),)
    done = ((),)
    error = ((),)

    def __init__(self, transitions_to):
        self.transitions_to = transitions_to


def state_property(field, state_cls):
    if not issubclass(state_cls, Enum):
        raise TypeError('State class should be enum')

    def getter(self):
        return getattr(self, field)

    def setter(self, value):
        if not isinstance(value, state_cls):
            raise TypeError('State should be of class {}, found {}'.format(state_cls,
                                                                           type(value).__name__))
        current_value = getattr(self, field)
        if value.name in current_value.transitions_to:
            setattr(self, field, value)
        else:
            raise ValueError('Cannot set state to {}, current state only transitions into {}'.format(value,
                                                                                                     current_value.transitions_to))

    # Create graphviz documentation
    nodes = '\n'.join('            {name} [shape=box];'.format(name=x) for x, _ in state_cls.__members__.items())
    transitions = '\n'.join('            {source} -> {target};'.format(source=s, target=t) for s, v in state_cls.__members__.items() for t in v.transitions_to)

    graphviz = """
    An overview of the states and the allowed transitions are depicted in the
    following figure:

    .. graphviz::

        digraph jobstate {{
{nodes}

{transitions}
        }}
    """.format(nodes=nodes, transitions=transitions)

    doc = "{}\n\n{}".format(textwrap.dedent(state_cls.__doc__),
                            textwrap.dedent(graphviz))

    return property(getter, setter, None, doc)


class ExampleJob(object):
    job_state = state_property('_job_state', JobState)
    node_state = state_property('_node_state', NodeState)

    def __init__(self):
        self._job_state = JobState.created
        self._node_state = NodeState.invalid
