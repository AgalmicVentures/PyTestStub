#!/usr/bin/env python3

import argparse
import ast
import collections
import os
import sys

functionTest = '''
	def test_%s(self):
		raise NotImplementedError() #TODO: test %s'''

classTest = '''class %sTest(unittest.TestCase):
	"""
	%s
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
%s'''

unitTestBase = '''
import unittest

%s
'''

def generateUnitTest(root, fileName):
	if not fileName.endswith('.py'):
		return None

	path = os.path.join(root, fileName)

	#Skip symlinks
	if os.path.islink(path):
		print('Symlink: %s' % path)
		return None

	pathParts = os.path.split(path)
	fileName = pathParts[-1]
	module, ext = os.path.splitext(fileName)

	#Load the file
	try:
		with open(path) as f:
			text = f.read()
	except UnicodeDecodeError as e:
		print('Unicode decode error for %s: %s' % (path, e))
		return None

	#Parse it
	try:
		tree = ast.parse(text)
	except:
		print('Failed to parse %s' % path)
		return None

	#Walk the AST
	classes = []
	classToMethods = collections.defaultdict(list)
	functions = []
	for node in tree.body:
		nodeType = type(node)
		if nodeType is ast.ClassDef:
			classes.append(node.name)

			#Track methods
			for child in node.body:
				if type(child) is ast.FunctionDef:
					classToMethods[node.name].append(child.name)

		elif nodeType is ast.FunctionDef:
			functions.append(node.name)

	if len(functions) == 0 and len(classes) == 0:
		print('No classes or functions in %s' % path)
		return None

	#Generate a functions test?
	unitsTests = []
	if len(functions) > 0:
		moduleTestComment = 'Tests for functions in the %s module.' % module
		functionTests = '\n'.join(functionTest % (function, function) for function in functions)

		unitsTests.append(classTest % (
			module, module,
			functionTests
		))

	#Generate class tests?
	if len(classes) > 0:
		for c in classes:
			classTestComment = 'Tests for methods in the %s class.' % c
			methodTests = '\n'.join(functionTest % (method, method) for method in classToMethods[c] if method[0] != '_')
			unitsTests.append(classTest % (
				c, classTestComment,
				methodTests,
			))
			#TODO: generate instance construction stub

	unitTestsStr = '\n\n'.join(unitsTests)
	unitTest = unitTestBase % unitTestsStr

	return unitTest

def main(argv=None):
	"""
	The main function of the unit test generator tool.

	:param argv: optional arguments (defaults to sys.argv if not specified)
	:return: int
	"""
	#Parse arguments
	parser = argparse.ArgumentParser(description='Python Unit Test Stub Generator')

	parser.add_argument('module', help='The path of the module to test.')
	parser.add_argument('-m', '--test-module', default='test',
		help='The path of the test module to generate.')
	parser.add_argument('-p', '--test-prefix', default='test_',
		help='The prefix for test files.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	#Walk the directory finding Python files
	for root, directoryNames, fileNames in os.walk(arguments.module):
		for fileName in fileNames:
			#Skip ignored files
			unitTest = generateUnitTest(root, fileName)
			if unitTest is None:
				continue

			#Write it
			outFile = '%s%s' % (arguments.test_prefix, fileName)
			outFolder = arguments.test_module
			if not os.path.exists(outFolder):
				os.makedirs(outFolder)

			testInit = os.path.join(outFolder, '__init__.py')
			if not os.path.exists(testInit):
				with open(testInit, 'w') as testInitFile:
					testInitFile.write('')

			outPath = os.path.join(outFolder, outFile)
			print('Writing test to %s' % outPath)
			if not os.path.exists(outPath):
				with open(outPath, 'w') as outFile:
					outFile.write(unitTest)

	return 0

if __name__ == '__main__':
	sys.exit(main())
