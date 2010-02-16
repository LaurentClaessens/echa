#! /usr/bin/python
# -*- coding: utf8 -*-

# This is part of Un soupçon de physique, sans être agressif pour autant
# Copyright (C) 2006-2009
#   Laurent Claessens
# See the file fdl-1.3.txt for copying conditions.

"""
La sortie de ce script est à mettre dans DefsExclamations.tex. Cela définit les environnements "idee", "pourquoidonc" et "probleme" avec les couleurs qu'il faut et les mots.
"""

class ParametreNewTheorem():
	def __init__(self,nom,intitule,couleur):
		self.nom = nom
		self.intitule = intitule
		self.couleur = couleur

	def newtheorem(self):
		print "\\newtheorem{pour_%s}[contBla]{%s}"%(self.nom,self.intitule)
	def newenvironment(self):
		print "\\newenvironment{"+self.nom+"}{\\bgroup \\"+self.couleur+" \\begin{pour_"+self.nom+"}}{\end{pour_"+self.nom+"}\egroup}"

def DefsExclamations():
	print "\\newcounter{contBla}"
	print "\\renewcommand{\\thecontBla}{}"
	print "\\newtheoremstyle{exclamations}{9pt}{9pt}{}{}{\\bfseries}{}{\\newline}{}"
	print "\\theoremstyle{exclamations}"

	liste = [ ParametreNewTheorem("idee","Idée !","green"), ParametreNewTheorem("pourquoidonc","Comment ? Pourquoi ?","blue"), ParametreNewTheorem("probleme","Y'a une faute ?","red") ]

	for a in liste :
		a.newtheorem()
	for a in liste :
		a.newenvironment()

DefsExclamations()

