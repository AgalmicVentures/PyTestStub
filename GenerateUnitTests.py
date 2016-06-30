#!/usr/bin/env python2.7

import ast
import os
import sys

functionTest = '''
	def test_%s(self):
		pass #TODO
'''

classTest = '''class %sTest(unittest.TestCase):
	"""
	%s
	"""
	%s'''

unitTestBase = '''
import unittest
%s
%s
'''

def generateUnitTest(root, fileName):
	path = os.path.join(root, fileName)

	#Skip symlinks
	if os.path.islink(path):
		print('Symlink: %s' % path)
		return

	pathParts = os.path.split(path)
	fileName = pathParts[-1]
	module, ext = os.path.splitext(fileName)

	#Load the file
	with open(path) as f:
		text = f.read()

	#Parse it
	try:
		tree = ast.parse(text)
	except:
		print('Failed to parse %s' % path)
		return

	#Walk the AST
	classes = []
	functions = []
	for node in tree.body:
		nodeType = type(node)
		if nodeType is ast.ClassDef:
			classes.append(node.name)
		elif nodeType is ast.FunctionDef:
			functions.append(node.name)

	if len(functions) == 0 and len(classes) == 0:
		print('No classes or functions in %s' % path)
		return

	#Generate a functions test?
	if len(functions) > 0:
		moduleTestComment = 'Tests for functions in the %s module.' % module
		functionTests = '\n'.join(functionTest % function for function in functions)

		functionsTestStr = classTest % (
			module, module,
			functionTests
		)
	else:
		functionsTestStr = ''

	#Generate class tests?
	if len(classes) > 0:
		classTests = []
		for c in classes:
			classTestComment = 'Tests for methods in the %s class.' % c
			functionTests = '' #'\n'.join(functTest % function for function in functions)
			classTests.append(classTest % (
				c, classTestComment,
				'#TODO\n'
			))
		classTestsStr = '\n'.join(classTests)
	else:
		classTestsStr = ''

	unitTest = unitTestBase % (
		functionsTestStr,
		classTestsStr,
	)

	return unitTest

def main():
	modulePath = sys.argv[1]
	testModulePath = sys.argv[2]

	for root, directoryNames, fileNames in os.walk(modulePath):
		for fileName in fileNames:
			#Skip ignored files
			unitTest = generateUnitTest(root, fileName)
			if unitTest is None:
				continue

			#Write it
			outFile = 'test_%s' % fileName
			outFolder = os.path.join(testModulePath, root)
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
