
# Copyright (c) 2015-2019 Agalmic Ventures LLC (www.agalmicventures.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import ast
import collections
import os

from PyTestStub import Templates

def generateUnitTest(root, fileName, includeInternal=False):
	"""
	Generates a unit test, given a root directory and a subpath to a file.

	:param root: str
	:param fileName: str
	:return: str or None
	"""
	#Skip non-Python files
	if not fileName.endswith('.py'):
		return None

	#Skip symlinks
	path = os.path.join(root, fileName)
	if os.path.islink(path):
		print('Symlink: %s' % path)
		return None

	#Get the parts of the filename
	pathParts = os.path.split(path)
	fileName = pathParts[-1]
	module, _ = os.path.splitext(fileName)

	#Load the file
	try:
		with open(path) as f:
			text = f.read()
	except UnicodeDecodeError as ude:
		print('Unicode decode error for %s: %s' % (path, ude))
		return None

	#Parse it
	try:
		tree = ast.parse(text)
	except Exception as e: #@suppress warnings since this really does need to catch all
		print('Failed to parse %s' % path)
		print(e)
		return None

	#Walk the AST
	classes = []
	classToMethods = collections.defaultdict(list)
	functions = []
	for node in tree.body:
		nodeType = type(node)
		if nodeType is ast.ClassDef:
			if not node.name.startswith('_') or includeInternal:
				classes.append(node.name)

			#Track methods
			for child in node.body:
				if type(child) is ast.FunctionDef and not child.name.startswith('_') or includeInternal:
					classToMethods[node.name].append(child.name)

		elif nodeType is ast.FunctionDef:
			if not node.name.startswith('_') or includeInternal:
				functions.append(node.name)

	if len(functions) == 0 and len(classes) == 0:
		print('No classes or functions in %s' % path)
		return None

	#Generate a functions test?
	unitsTests = []
	if len(functions) > 0:
		moduleTestComment = 'Tests for functions in the %s module.' % module
		functionTests = '\n'.join(Templates.functionTest % (function, function) for function in functions)

		unitsTests.append(Templates.classTest % (
			module, moduleTestComment,
			functionTests
		))

	#Generate class tests?
	if len(classes) > 0:
		for c in classes:
			classTestComment = 'Tests for methods in the %s class.' % c
			methodTests = '\n'.join(Templates.functionTest % (method, method) for method in classToMethods[c] if method[0] != '_')
			unitsTests.append(Templates.classTest % (
				c, classTestComment,
				methodTests,
			))
			#TODO: generate instance construction stub

	#Assemble the unit tests in the template
	unitTestsStr = '\n\n'.join(unitTest for unitTest in unitsTests if unitTest != '')
	unitTest = Templates.unitTestBase % unitTestsStr

	return unitTest
