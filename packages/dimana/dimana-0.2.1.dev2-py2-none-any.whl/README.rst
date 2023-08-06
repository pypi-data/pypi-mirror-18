========================
_DIM_ensional _ANA_lysis
========================

A python library for tracking and verifying dimensional units of measure.

For background see the `dimensional analysis wikipedia entry`_.

.. _`dimensional analysis wikipedia entry`: https://en.wikipedia.org/wiki/Dimensional_analysis

.. contents::

A Tour of `dimana`
==================

Parsing Values
--------------

`dimana` values can be parsed with the ``Value.parse`` classmethod:

.. code:: python

   >>> from dimana import Value
   >>> reward = Value.parse('12.5 [BTC]')
   >>> reward
   <Value '12.5 [BTC]'>

The grammar for units can handle powers expressed with the ``^`` symbol,
and a single division with the ``/`` symbol:

   >>> Value.parse('9.807 [meter/sec^2]')
   <Value '9.807 [meter / sec^2]'>

Arithmetic Operations
---------------------

Values track their units through arithmetic operations:

.. code:: python

   >>> time = Value.parse('10 [min]')
   >>> rate = reward / time
   >>> rate
   <Value '1.25 [BTC / min]'>

Incoherent operations raise exceptions:

.. code:: python

   >>> reward + time
   Traceback (most recent call last):
     ...
   Mismatch: Units mismatch: 'BTC' vs 'min'

Value Components
----------------

A value associates a `scalar amount` with `dimensional units`. These
are available on the instance as ``amount`` and ``units``:

.. code:: python

   >>> rate.amount
   Decimal('1.25')
   >>> rate.units
   <Units 'BTC / min'>

Amounts
~~~~~~~

The scalar amount of a value is represented with ``decimal.Decimal``
instance on the ``amount`` attribute:

.. code:: python

   >>> reward.amount
   Decimal('12.5')

Arithmetic operations rely on the `decimal` library for numeric logic,
including precision tracking:

.. code:: python

   >>> reward * Value.parse('713.078000 [USD / BTC]')
   <Value '8913.4750000 [USD]'>

Units
~~~~~

Units are available in the ``units`` attribute of ``Value``
instances. They are instances of ``dimana.units.Units``. You can parse
``Units`` instances directly:

.. code:: python

   >>> from dimana import Units
   >>> meter = Units.parse('meter')
   >>> meter
   <Units 'meter'>
   >>> sec = Units.parse('sec')
   >>> sec
   <Units 'sec'>

Construction
------------

There are four ways to create values:

* parsing a 'value text': ``Value.parse``,
* as the result of arithmetic operations on other values,
* explicitly with the ``Value`` constructor, or
* with 'units-specific parsing`.

The first two are described above, the last two next:

Value Constructor
~~~~~~~~~~~~~~~~~

Values can be constructed directly given ``Decimal`` and ``Units`` instances:

.. code:: python

   >>> from decimal import Decimal
   >>> Value(Decimal('23.50'), meter)
   <Value '23.50 [meter]'>

Units-Specific Parsing
~~~~~~~~~~~~~~~~~~~~~~

Many applications require a finite statically known set of ``Units``
instances, and then need to create ``Value`` instances from specific
explicit ``Units`` instances, for example:

.. code:: python

   >>> from decimal import Decimal
   >>> from dimana import Units, Value
   >>> cm = Units.parse('cm')
   >>> userinput = '163' # In an application this might be from arbitrary input.
   >>> height = Value(Decimal(userinput), cm)
   >>> height
   <Value '163 [cm]'>

Because this pattern is so common, ``Units`` instances support parsing
an amount directly with the ``Units.from_string`` method:

.. code:: python

   >>> from dimana import Units
   >>> cm = Units.parse('cm')
   >>> height2 = cm.from_string(userinput)
   >>> height == height2
   True

str() and repr()
----------------

The ``str()``\ -ification of ``Value`` and ``Units`` instances matches the
'canonical parsing format':

.. code:: python

   >>> trolls = Value.parse('3 [troll]')
   >>> print trolls
   3 [troll]
   >>> trolls == Value.parse(str(trolls))
   True

The ``repr()`` of these class instances contains the class name and the
``str()``\ -ification:

   >>> print repr(trolls)
   <Value '3 [troll]'>
   >>> print repr(trolls.units)
   <Units 'troll'>

More About Units
----------------

This section explores the ``Units`` class more closely.

``zero`` and ``one``
~~~~~~~~~~~~~~~~~~~~

Because the 0 and 1 amounts are very common, they are available as
attributes of a ``Units`` instance:

.. code:: python

   >>> meter.zero
   <Value '0 [meter]'>
   >>> sec.one
   <Value '1 [sec]'>

Scalar Units
~~~~~~~~~~~~

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

.. code:: python

   >>> experience * Value.parse('1.25')
   <Value '52.50 [XP]'>

Units Uniqueness and Matching
-----------------------------

There is a single instance of ``Units`` for each combination of unit:

.. code:: python

   >>> (meter + meter) is meter
   True
   >>> (meter / sec) is Units.parse('meter / sec')
   True

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
