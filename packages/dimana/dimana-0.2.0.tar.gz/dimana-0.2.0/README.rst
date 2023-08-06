========================
_DIM_ensional _ANA_lysis
========================

A python library for tracking and verifying dimensional units of measure.

For background see the `dimensional analysis wikipedia entry`_.

.. _`dimensional analysis wikipedia entry`: https://en.wikipedia.org/wiki/Dimensional_analysis

.. contents::

A Tour of `dimana`
==================

Parsing
-------

`dimana` values can be parsed with the ``Value.parse`` classmethod:

.. code:: python

   >>> from dimana.value import Value
   >>> reward = Value.parse('12.5 [BTC]')
   >>> reward
   <Value '12.5 [BTC]'>

Arithmetic Operations
---------------------

Values track their units through arithmetic operations:

.. code:: python

   >>> time = Value.parse('10 [min]')
   >>> reward / time
   <Value '1.25 [BTC / min]'>

Incoherent operations raise exceptions:

.. code:: python

   >>> reward + time
   Traceback (most recent call last):
     ...
   Mismatch: Units mismatch: 'BTC' vs 'min'

Scalars
-------

A value associates a scalar amount with dimensional units. The scalar
amount of a value is represented with ``decimal.Decimal`` instance on the
``v.decimal`` attribute:

.. code:: python

   >>> reward.decimal
   Decimal('12.5')

Arithmetic operations rely on the decimal library for numeric logic,
including precision tracking:

.. code:: python

   >>> reward * Value.parse('713.078000 [USD / BTC]')
   <Value '8913.4750000 [USD]'>

Units
-----

Units are tracked with instances of ``dimana.units.Units``. You can parse
``Units`` instances directly:

.. code:: python

   >>> from dimana.units import Units
   >>> Units.parse('meter')
   <Units 'meter'>

Units instances support arithmetic operations, just as values. The
results are the same units you would get if the associated valued went
through the same operations:

.. code:: python

   >>> meter = Units.parse('meter')
   >>> sec = Units.parse('sec')
   >>> meter / sec
   <Units 'meter / sec'>
   >>> meter * sec**2
   <Units 'meter * sec^2'>
   >>> meter + meter
   <Units 'meter'>

Value Constructor
-----------------

Aside from the ``Value.parse`` and ``Units.parse`` APIs, values can be
constructed directly given a ``Decimal`` and ``Units``:

.. code:: python

   >>> from decimal import Decimal
   >>> Value(Decimal('23.50'), meter)
   <Value '23.50 [meter]'>

Scalar Units
------------

The base case of units with 'no dimension' is available as
``Units.scalar``. This instance of ``Units`` represents, for example,
ratios:

.. code:: python

   >>> total = Value.parse('125 [meter]')
   >>> current = Value.parse('15 [meter]')
   >>> completion = current / total
   >>> completion
   <Value '0.12'>
   >>> completion.units is Units.scalar
   True

By design, `dimana` does not do implicit coercion (such as promoting
`float` or `Decimal` instances into `Value` instances) to help avoid
numeric bugs:

.. code:: python

   >>> experience = Value.parse('42 [XP]')
   >>> experience * 1.25
   Traceback (most recent call last):
     ...
   TypeError: Expected 'Value', found 'float'

Using ``Units.scalar`` is necessary in these cases. Parsing
a value with no units specification gives a 'scalar value':

   >>> experience * Value.parse('1.25')
   <Value '52.50 [XP]'>

Units Uniqueness and Matching
-----------------------------

There is a single instance of ``Units`` for each combination of unit:

.. code:: python

   >>> assert (meter + meter) is meter
   >>> assert (meter / sec) is Units.parse('meter / sec')

Thus, to test if two ``Units`` instances represent the same units,
just use the ``is`` operator:

.. code:: python

   >>> if meter is (Units.parse('meter / sec') * sec):
   ...     print 'Yes, it is meters.'
   ...
   Yes, it is meters.

The ``Units.match`` method does such a check and raises ``Units.Mismatch``
if the units do not match:

.. code:: python

   >>> meter.match(Units.parse('meter / sec') * sec)
   >>> meter.match(Units.parse('meter / sec^2') * sec)
   Traceback (most recent call last):
     ...
   Mismatch: Units mismatch: 'meter' vs 'meter / sec'

Uniqueness Implications
~~~~~~~~~~~~~~~~~~~~~~~

This uniqueness depends globally on the unit string names, so if a large
application depended on two completely separate libraries, each of which
rely on `dimana`, and both libraries define ``<Units 's'>`` they will
be using the same instance. This could be a problem if, for example,
one library uses the ``s`` to represent `seconds` while the other uses
it to represent a `satisfaction point` rating system.

Each instance of ``Units`` persists to the end of the process, so
instantiating ``Units`` dynamically could present a resource management
problem, especially if a malicious entity can instantiate arbitrary
unit types.

(The plan is to wait for real life applications that encounter these
problems before adding complexity to this package.)


Future Work
===========

There is no definite roadmap other than to adapt to existing users'
needs. However, some potential new features would be:

- Nicer
- Add an 'expression evaluator' for quick-and-easy interactive interpreter
  calculations, eg: ``dimana.eval``
- Add a commandline wrapper around ``eval``.
