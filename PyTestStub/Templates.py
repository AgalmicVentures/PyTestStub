
functionTest = '''
	def test_%s(self):
		raise NotImplementedError() #TODO: test %s'''

classTest = '''class %sTest(unittest.TestCase):
	"""
	%s
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
%s'''

unitTestBase = '''
import unittest

%s
'''
