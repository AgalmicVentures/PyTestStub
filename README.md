
# PyTestStub
PyTestStub is a Python unit test stub generator. It takes a module name and
generates test stubs for each class and function in the module.

## Scripts

### `GenerateUnitTests.py`
Generates the actual unit tests:

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

	> ~/path/to/PyTestStub/GenerateUnitTests.py -m Test NanoPcap
	No classes or functions in NanoPcap/__init__.py
	Writing test to Test/NanoPcap/test_Format.py
	Writing test to Test/NanoPcap/test_Listener.py
	Writing test to Test/NanoPcap/test_Parser.py
	No classes or functions in NanoPcap/Tools/__init__.py
	Writing test to TestNanoPcap/Tools/test_PcapDump.py
	Writing test to Test2/NanoPcap/Tools/test_PcapSummary.py
	No classes or functions in NanoPcap/Utility/__init__.py
	Writing test to Test/NanoPcap/Utility/test_Statistics.py
	Writing test to Test/NanoPcap/Utility/test_Units.py
