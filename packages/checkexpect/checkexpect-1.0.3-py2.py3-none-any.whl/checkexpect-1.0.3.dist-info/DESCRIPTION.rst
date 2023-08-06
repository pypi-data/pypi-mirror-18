checkexpect
============= 

|version|_   |downloads|_

.. |downloads| image:: http://img.shields.io/pypi/dm/checkexpect.svg?style=flat
.. _downloads: https://pypi.python.org/pypi/checkexpect

.. |version| image:: http://img.shields.io/pypi/v/checkexpect.svg?style=flat
.. _version: https://pypi.python.org/pypi/checkexpect

checkexpect is a simple unit testing framework for python development `<https://pypi.python.org/pypi/checkexpect>`_
python library. checkexpect is a mature, viable way to make your test-driven development drive the design of your data,
and your data drive the design of your functions.  It's also a simple tool that allows you to execute unit tests inline
with your code, in a systematic way.

This is a fork of the original `checkexpect <https://github.com/dareljohnson/checkexpect-py>`_, hosted on GitHub and
last updated in 2016.

Features
--------

* [x] Support for inline unit tests. checkExpect will support test created in another directory as well.
* [x] Support for TDD and DDD development.
* [x] Support for Systematic Program Design methods using HtDD and HtDF recipes.
* [x] Support for code coded terminal (console) output.


TODO
--------
* [ ] Python 3.5 support.

Installation
------------

1. Install checkexpect.

   .. code:: python

      pip install checkexpect


2. Now you can now add a reference to the checkexpect package like so.

   .. code:: python

      #!/usr/bin/env python

      # import package
      from checkexpect.core import checkExpect


3. Write some code and test it using checkexpect inline with your code.

   .. code:: python

      #!/usr/bin/env python

      # import packages
      from checkexpect.core import checkExpect
      import math

      # define a function
      def square(a):
	  return a * a                    # could replace return statement with (lambda a: math.pow(a, 2))
                                      # from code_statement_B below.
      # examples
      num_to_square = 12
      code_statement_A = 12 * 12       # used in the function body

      # check the algor1thm design of our square function, and unit test it at the same time
      checkExpect(square, 12, 144, "Square of a number")

      # Or just pass our examples
      checkExpect(square, num_to_square, code_statement_A, "Square of a number")

      # Or use lambda expressions
      code_statement_B = lambda a: math.pow(a, 2)
      checkExpect(square, num_to_square, code_statement_B(12), "Square of a number")


4. Execute your python script from the command line (terminal) to see the unit test results. Most tests usually fail (RED) in the beginning.

5. Refactor your code and execute your script until all functions under test, turn GREEN.

6. That's it! You're done.


Configuration
-------------
None - No configuration needed.

Support
~~~~~~~~~~~~~~~~~~~~~~~~
For checkexpect support contact me at `<dareljohnson@yahoo.com>`_

License
-------

This project originally started life as javascript unit test project. This project was
abandoned in 2013 and was brought back to life as checkexpect by our team in
2016. In the process, most of the project was refactored and brought up to speed
with modern python best practices. The work done prior to the 2013 rewrite is
licensed under MIT. Improvements since then are licensed under MIT.
See `LICENSE <https://github.com/dareljohnson/checkexpect-py/LICENSE>`_ for more details.

SemVer
------

This project implements `Semantic Versioning <http://semver.org/>`_ .

Credits
-------

* `Darel Johnson <https://github.com/dareljohnson>`_


