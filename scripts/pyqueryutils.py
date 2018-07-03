####################################################################
#Author: Andrew Mfune
#Date: 02/07/2018
#Description: Utility methods for generating simple sql statements
####################################################################

from sqlscripts import INSERT, UPDATE, SELECT

def genStrPlaceholderList(cols, seperator=', '):
	assignmentList = [':%s' % col for col in cols] 
	return '(%s)' % seperator.join(assignmentList)

def genStrColValAssignmentList(cols, seperator=', '):
	assignmentList = ['{0}=:{0}'.format(col) for col in cols] 
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

	conditions = genStrColValAssignmentList(andWhere, ' and ')
	if orWhere:
		orWhereConditions = genStrColValAssignmentList(orWhere, ' and ')
		conditions = '%s or %s' % (conditions, orWhereConditions)

	return conditions

def genInsertStatement(table, columns):
	"""
	Generate an SQL insert statement
	
	:param table: name of the table to insert data in
	:param coltuple: a tuple of columns to insert into
	"""

	# base query with placeholders of table, columns and value placeholders
	placeholderlist = genStrPlaceholderList(columns)
	return INSERT.format(
		table, strTuple(columns), placeholderlist
	)

def getStrConditionList(conditions):
	if 'orWhere' in conditions:
		strConditions = genConditionStatements(
			conditions['where'], conditions['orWhere']
		)
	else:
		strConditions = genConditionStatements(conditions['where'])
	
	return 'WHERE %s' % strConditions

def genUpdateStatement(table, cols, conditions):
	""" 
	Generate an SQL update statement based on parameters provided
	:param table: name of the table
	:param cols: list of columns to be updated
	:param conditions: dictionary of condition assignements
	"""

	strAssignmentsList = genStrColValAssignmentList(cols)
	conditionList = getStrConditionList(conditions)

	return UPDATE.format(table, strAssignmentsList, conditionList)

def genSelectStatement(table, cols=['*'],  conditions={}, filters=''):
	"""
	Generate an SQL select statement
	:param table: name of the table to select from 
	:param cols: list of columns to retrieve
	:param filters: filters to apply to results

	"""

	cols = ', '.join(cols)
	conditionList = getStrConditionList(conditions)

	return SELECT.format(cols, table, conditionList, filters)
