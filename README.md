
# PyTestStub
PyTestStub is a Python unit test stub generator. It takes a module name and
generates test stubs for each class and function in the module.

## Scripts

### `GenerateUnitTests.py`
Generates the actual unit tests.

	> ~/path/to/PyTestStub/GenerateUnitTests.py -h
	usage: GenerateUnitTests.py [-h] [-m TEST_MODULE] [-p TEST_PREFIX] module

	Python Unit Test Stub Generator

	positional arguments:
	  module                The path of the module to test.

	optional arguments:
	  -h, --help            show this help message and exit
	  -m TEST_MODULE, --test-module TEST_MODULE
	                        The path of the test module to generate.
	  -p TEST_PREFIX, --test-prefix TEST_PREFIX
	                        The prefix for test files.

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

		@staticmethod
		def setUpClass(cls):
			pass #TODO

		@staticmethod
		def tearDownClass(cls):
			pass #TODO

		def setUp(self):
			pass #TODO

		def tearDown(self):
			pass #TODO

		def test_generateUnitTest(self):
			raise NotImplementedError() #TODO: test generateUnitTest
