
# PyTestStub
PyTestStub is a Python unit test stub generator. It takes a module name and
walks each file in the module. If it encounters a file without a
corresponding test file, it will generate one with stub tests for each function
and class method in the file.

Besides reducing time spent on boilerplate, this approach ensures complete
coverage when creating new tests, so developers can focus on the actual tests.
Rework after generation is limited to removing unneeded stubs and duplicating
those which require multiple tests (copy+paste), after which the tests can be
implemented by anyone (e.g. delegated to junior team members).

## Scripts

### `GenerateUnitTests.py`
Generates the actual unit tests, with options like a header file to prepend as
a license:

	> ~/path/to/PyTestStub/GenerateUnitTests.py -h
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

	> ~/path/to/PyTestStub/GenerateUnitTests.py PyTestStub
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
