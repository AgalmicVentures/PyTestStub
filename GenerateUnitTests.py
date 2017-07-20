#!/usr/bin/env python3

import argparse
import os
import sys

from PyTestStub import Generator

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
	parser.add_argument('-t', '--tab-width', type=int,
		help='The width of a tab in spaces (default None = actual tabs).')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	#Walk the directory finding Python files
	for root, directoryNames, fileNames in os.walk(arguments.module):
		for fileName in fileNames:
			#Skip ignored files
			unitTest = Generator.generateUnitTest(root, fileName)
			if unitTest is None:
				continue

			#Replace tabs
			if arguments.tab_width is not None:
				unitTest = unitTest.replace('\t', ' ' * arguments.tab_width)

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
