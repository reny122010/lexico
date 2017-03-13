#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import sys
import re

line = 1;
ck = False;
cp = False;
hasCK = False;

def checkKeys(codeList):
	dados = []

	cont = 0;
	for char in codeList:
		if char == '{':
			cont += 1
		if char == '}':
			cont -= 1
		if cont == 2:
			print "Comentário aplicado incorretamente!"
			sys.exit()
	if cont != 0:
		print "Comentário aplicado incorretamente!"
		sys.exit()

def checkSymbol(codeList):
	if re.match("^[a-zA-Z0-9=<>+-:*;,:.(){}_\t\n ]*$",codeList) is None:
		print "Algum simbolo não pertece a linguagem"
		sys.exit()
	
def tabuleDelimiter(char): 
	print char+"\tDelimitador\t"+str(line)

def tabuleOperator(char): 
	print char+"\tOperator\t"+str(line)

def isDelimiter(char):
	delimiterList = [';',':','.', '(', ')', ',']
	global ck
	global hasCK 
	global cp
	

	if cp and re.match("([0-9])",char):
		cp = False
		return False

	if cp:
		cp = False
		return True

	if char == '.':
		cp = True
		return False

	if char == ':':
		ck = True
		return False

	if ck and char == '=':
		tabuleOperator(":=")
		hasCK = True
		ck = False
		return False


	if ck and char != '=':
		tabuleDelimiter(':')
		ck = False

	for delimiter in delimiterList:
		if delimiter == char:
			return True

	 
	return False

def isKeyWords(word):
	keyWordsList = ['program','var','integer','real','boolean','procedure','begin','end','if','then','else','while','do','not']
	for keyWord in keyWordsList:
		if keyWord == word:
			return True
	return False

def isOperator(word):
	operatorList = ['=', '<', '>', '<=', '>=', '<>', ':=', '+', '-', 'or', '*', '/', 'and']

	for operator in operatorList:
		if operator == word:
			return True
	return False

def isIdentifier(word):
	if re.match("([a-zA-Z][_0-9a-zA-Z]*)",word):
		print word +"\tIdentificador\t"+str(line)
		return
	elif re.match("(^[0-9]+$)",word):
		print word +"\tNumero natural\t"+str(line)
		return
	elif re.match("([0-9]+\.[0-9]+)",word):
		print word +"\tNumero real\t"+str(line)
		return


def checkType(word):
	if isKeyWords(word):
		print word+"\tPalavra Chave\t"+str(line) 
	else:
		isIdentifier(word)


word = '';
arq = open(sys.argv[1], 'r') 
codeList = arq.read()

comment = True
codeList += " " 
checkSymbol(codeList)
checkKeys(codeList)
for char in codeList:
	if comment:
		if char == '{':
			comment = False;
		else:
			if isDelimiter(char):
				checkType(word)
				tabuleDelimiter(char)
				word = ''
			elif isOperator(char):
				checkType(word)
				word = ''
				if hasCK:
					ck = False
					hasCK = False
				else:
					tabuleOperator(char)
			elif char == str('\t') or char == str('\n') or char == str(' '):
				checkType(word)
				word = ''
				if char == '\n':
					line += 1;
			elif char == str(':'):
				checkType(word)
				word = ''
			else:
				if ck == False:
					word = word + char
	elif char == '}':
		comment = True
if cp: 
	checkType(word.replace(".", ""))
	tabuleDelimiter('.')
if ck: 
	checkType(word.replace(":", ""))
	tabuleDelimiter(':')

arq.close()