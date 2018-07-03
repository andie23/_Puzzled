####################################################################
#Author: Andrew Mfune
#Date: 02/07/2018
#Description: Utility methods for generating simple sql statements
####################################################################

def genCharList(char, count):
	"""	
	Generate a list of characters
	:param char: char to replicate in list
	:param count: number of times to replicate character
	
	"""
	
	return [char for x in range(0, count)]
	

def genInsertQueryValPlaceholder(char, length):
	"""Generate insert statement's values placeholders"""

	charList = genCharList(char, length)
	return strTuple(charList)

def genUpdateQueryColValPlaceholderPair(char, cols):
	"""
	Generates a col and placeholder assignment pair like: "column = char, column1 = char".....
	"""
	assignmentList = ['%s= %s' % (col, char) for col in cols] 
	return ', '.join(assignmentList)

def convertDictToStrAssignmentPair(dict, seperator=', '):
	""" 
	Converts a dictionary key and value pair to a list 
	of string key and value assignment pair 
	"""
	
	assignmentList = ["%s= %s" % (key, val) for key, val in dict.items()]
	return seperator.join(assignmentList)

def strTuple(lis):
	strLis = ', '.join(lis)
	strTuple = '(%s)' % strLis
	return strTuple

def genConditionStatements(andWhere, orWhere={}):
	"""
	Generate "where" condition for sql statements
	
	:param andWhere: main dictionary conditions
	:param orWhere: optional alternate dictionary conditions 
	"""

	conditions = convertDictToStrAssignmentPair(andWhere, ' and ')
	if orWhere:
		orWhereConditions = convertDictToStrAssignmentPair(orWhere, ' and ')
		conditions = '%s or %s' % (conditions, orWhereConditions)

	return conditions

def genInsertStatement(table, columns):
	"""
	Generate an SQL insert statement
	
	:param table: name of the table to insert data in
	:param coltuple: a tuple of columns to insert into
	"""

	# base query with placeholders of table, columns and value placeholders
	barequery = """INSERT INTO {0} {1} VALUES {2};"""
	# get value placeholders like (?, ?, ?, ?).. depending on the length of the tuple
	valPlaceholders = genInsertQueryValPlaceholder('?', len(columns))
	return barequery.format(
		table, strTuple(columns),
		valPlaceholders
	)

def genUpdateStatement(table, cols, conditions):
	""" 
	Generate an SQL update statement based on parameters provided
	:param table: name of the table
	:param cols: list of columns to be updated
	:param conditions: dictionary of condition assignements
	"""

	barequery = """UPDATE {0} SET {1} WHERE {2};"""
	strColAssingments = genUpdateQueryColValPlaceholderPair('?', cols)
	
	if 'orWhere' in conditions:
		strConditions = genConditionStatements(
			conditions['where'], conditions['orWhere']
		)
	else:
		strConditions = genConditionStatements(conditions['where'])
	
	return barequery.format(table, strColAssingments, strConditions)

def genSelectStatement(table, cols=['*'],  conditions={}, filters=''):
	"""
	Generate an SQL select statement
	:param table: name of the table to select from 
	:param cols: list of columns to retrieve
	:param filters: filters to apply to results

	"""
	
	barequery = """SELECT {0} FROM {1} {2} {3} {4};"""
	strConditions = ''
	where = ''
	cols = ', '.join(cols)
	
	if conditions:
		where = 'where'
		if 'orWhere' in conditions:
			strConditions = genConditionStatements(
				conditions['where'], conditions['orWhere']
			)
		else:
			strConditions = genConditionStatements(conditions['where'])
	
	
	return barequery.format(cols, table, where ,strConditions, filters)