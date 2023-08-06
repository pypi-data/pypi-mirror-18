A SerialObject is an object that supports serialization from/to json-like
objects (dicts and lists of builtin types).

The serialization specification is taken from the ``__fields__`` class attribute,
which is on the form:

::

    __fields__: {
        FIELD_NAME: FIELD_SPEC
    }

A FIELD_NAME is a string, its only constraint is that it should be a valid
object attribute name.

FIELD_SPEC can be:

* Any native type from:

    * ``str``

    * ``unicode`` (Python2)

    * ``int``

    * ``float``

    * ``bool``

    * ``dict``

* A ``SerialObject`` subclass

* ``Choice(val1, val2, ...)`` to form enumerations, values should be of a
    native type (see above).

* ``[FIELD_SPEC]``: a list of objects depicted by the above specs.

Additionally, SerialObjects support a ``__strict__`` boolean class attribute
(False by default). When ``__strict__`` == True, an exhaustivity check is performed
during (de-)serialization and missing or unknown keys yield errors.

On Python2, ``str`` instances are automatically coerced to unicode strings.

Install
=======


``serialobj`` is registered on the PyPi. Simply type the following commands.

::

    pip install serialobj


Alternatively, you can run the following commands after having cloned the
source repository:

::

    python setup.py install


Quick tutorial
==============

Simple types and inheritance
----------------------------

Let us define a very basic Person type that defines two string fields:

::

    class Person(SerialObject):
        __fields__ = {
            'name': str,
            'job': str
        }


Now we can simply deserialize json-compatible data to it, and/or serialize its
instances to a json-like structure:

::

    >>> person_data = {
    ...     'name': 'Bob',
    ...     'job': 'lumberjack'
    ... }
    >>> bob = Person.deserialize(person_data)
    >>> bob.name
    'Bob'
    >>> bob.job
    'lumberjack'
    >>> bob.serialize()
    {'job': 'lumberjack', 'name': 'Bob'}


Of course there is more to it than that. Let us subclass our ``Person``, to
define, for instance a ``TeamMate``, which overrides the ``job`` field to allow it
to be a ``dict`` and to add a new ``str`` field: ``role``.

::

    class TeamMate(Person):
        __fields__ = {
            'role': str,
            'job': dict
        }

Of course this is a silly example, but this allows us to demonstrate that
inheriting a `SerialObject` class allows to inherit, override and specialize
the structure definition :

::

    >>> bob2 = TeamMate.deserialize(teammate_data)
    >>> bob2.name
    'Bob'
    >>> bob2.job
    {'all night': 'sleep', 'all day': 'work'}
    >>> bob2.serialize()
    {'role': 'lumberjack', 'name': 'Bob', 'job': {'all night': 'sleep', 'all day': 'work'}}

It also allows us to demonstrate that the structure is actually *checked*
against the model: let's try and deserialize our ``teammate_data`` with the
incompatible ``Person`` model.

::

    >>> Person.deserialize(teammate_data)
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
        Person.deserialize(teammate_data)
      File "/home/arnaud/work/serialobj/serialobj.py", line 242, in deserialize
        for key, val in data.items() if key in cls.__fields__
      File "/home/arnaud/work/serialobj/serialobj.py", line 242, in <dictcomp>
        for key, val in data.items() if key in cls.__fields__
      File "/home/arnaud/work/serialobj/serialobj.py", line 86, in deserialize
        .format(self.cls_.__name__, data))
    serialobj.InvalidTypeError: Expected str, got {'all night': 'sleep', 'all day': 'work'}

Isn't it starting to get interesting?

List of objects
---------------

Let us spice it up a little bit. What if I want to define a field as a *list of
strings*?

Well, there is some sugar for this:

::

    class Task(SerialObject):
        __fields__ = {
            'title': str,
            'description': str,
            'checklist': [str]
        }

See for yourself:

::

    >>> data = {
    ...     'title': 'timber some wood',
    ...     'description': '',
    ...     'checklist': [
    ...         'some wood is timbered',
    ...         'the lumberjack is okay',
    ...         'he sleeps all night and works all day'
    ...     ]
    ... }
    >>> tsk = Task.deserialize(data)
    >>> tsk.checklist
    ['some wood is timbered', 'the lumberjack is okay', 'he sleeps all night and works all day']
    >>> tsk.checklist.append("... and that's it")
    >>> pprint(tsk.serialize())
    {'checklist': ['some wood is timbered',
                   'the lumberjack is okay',
                   'he sleeps all night and works all day',
                   "... and that's it"],
     'description': '',
     'title': 'timber some wood'}

Going fancy
-----------

Of course, all these are the base building blocks to define arbitrarily
complex JSON-API structures:

::

    class Team(SerialObject):
        __fields__ = {
            'name': str,
            'manager': TeamMate,
            'members': [TeamMate],
            'backlog': [Task]
        }


    COMPLEX_DATA = {
        'name': "The good ol' lumberjacks",
        'manager': {
            'name': 'Bob',
            'role': 'Be okay'
        },
        'members': [
            {
                'name': 'Jack',
                'role': 'sleep all night'
            },
            {
                'name': 'Barry',
                'role': 'work all day',
            }],
        'backlog': [
            {
                'title': 'timber some wood',
                'description': '',
                'checklist': [
                    'some wood is timbered',
                    'the lumberjack is okay',
                    'he sleeps all night and works all day'
                ]
            }]
        }

Here we go:

::

    >>> team = Team.deserialize(COMPLEX_DATA)
    >>> team.manager.name
    'Bob'
    >>> team.manager
    <__console__.TeamMate object at 0x7f34edd2c9a8>
    >>> team.backlog[0]
    <__console__.Task object at 0x7f34edd9b7c8>
    >>> team.backlog[0].title
    'timber some wood'
    >>> pprint(team.serialize())
    {'backlog': [{'checklist': ['some wood is timbered',
                                'the lumberjack is okay',
                                'he sleeps all night and works all day'],
                  'description': '',
                  'title': 'timber some wood'}],
     'manager': {'name': 'Bob', 'role': 'Be okay'},
     'members': [{'name': 'Jack', 'role': 'sleep all night'},
                 {'name': 'Barry', 'role': 'work all day'}],
     'name': "The good ol' lumberjacks"}

Testing
=======

You can trigger all tests using ``tox``. Tests are currently run for python
2.7 and 3.5.


