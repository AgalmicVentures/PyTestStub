
# PyTestStub
PyTestStub reads your Python code to generate unit test stubs. Given a module name,
it walks each file in the module. If it encounters a file without a
corresponding test file, it generates one with test stubs for each function
and class method in the file.

Besides reducing time spent on boilerplate, this approach ensures complete
coverage when creating new tests, so developers can focus on the actual tests.
After generation, rework is limited to removing unneeded stubs and duplicating
those which require multiple tests (copy+paste). The resulting skeleton is
sufficiently complete to delegate the test implementation to another developer.

## Installation
To install, simply use `pip`:

	> python3 -m pip install PyTestStub

## Scripts

### `GenerateUnitTests.py`
Generates the actual unit tests, with options like a header file to prepend as
a license:

	> python3 -m PyTestStub.GenerateUnitTests -h
	usage: GenerateUnitTests.py [-h] [-F FOOTER] [-H HEADER] [-f] [-m TEST_MODULE]
	                            [-p TEST_PREFIX] [-t TAB_WIDTH]
	                            module

	Python Unit Test Stub Generator

	positional arguments:
	  module                The path of the module to test.

	optional arguments:
	  -h, --help            show this help message and exit
	  -F FOOTER, --footer FOOTER
	                        File to use as a footer.
	  -H HEADER, --header HEADER
	                        File to use as a header.
	  -f, --force           Force files to be generated, even if they already
	                        exist.
	  -m TEST_MODULE, --test-module TEST_MODULE
	                        The path of the test module to generate.
	  -p TEST_PREFIX, --test-prefix TEST_PREFIX
	                        The prefix for test files.
	  -t TAB_WIDTH, --tab-width TAB_WIDTH
	                        The width of a tab in spaces (default actual tabs).

Output is simple and human readable:

	> python3 -m PyTestStub.GenerateUnitTests PyTestStub
	No classes or functions in PyTestStub/__init__.py
	Writing test to test/test_Generator.py
	No classes or functions in PyTestStub/Templates.py

Output files have stubs for everything but are easily pruned if e.g. setup
methods are not needed:

	import unittest

	class GeneratorTest(unittest.TestCase):
		"""
		Tests for functions in the Generator module.
		"""

		@classmethod
		def setUpClass(cls):
			pass #TODO

		@classmethod
		def tearDownClass(cls):
			pass #TODO

		def setUp(self):
			pass #TODO

		def tearDown(self):
			pass #TODO

		def test_generateUnitTest(self):
			raise NotImplementedError() #TODO: test generateUnitTest
