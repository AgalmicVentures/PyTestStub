
import ast
import collections
import os

from PyTestStub import Templates

def generateUnitTest(root, fileName):
	"""
	Generates a unit test, given a root directory and a subpath to a file.

	:param root: str
	:param fileName: str
	:return: str or None
	"""
	if not fileName.endswith('.py'):
		return None

	path = os.path.join(root, fileName)

	#Skip symlinks
	if os.path.islink(path):
		print('Symlink: %s' % path)
		return None

	pathParts = os.path.split(path)
	fileName = pathParts[-1]
	module, _ = os.path.splitext(fileName)

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

	unitTestsStr = '\n\n'.join(unitTest for unitTest in unitsTests if unitTest != '')
	unitTest = Templates.unitTestBase % unitTestsStr

	return unitTest
