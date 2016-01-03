#! /usr/bin/python
# -*- coding: utf8 -*-

import os, sys
import manip

# Commande en 3 arguments
# 1. Nom de la série d'exercices
# 2. Numéro de début
# 3. Numéro de fin

# Avant d'utiliser ce scipt, voir si il ne faut pas ajouter une mention de FDL au début des fichiers.
#  Par défaut, il met le fichier fdl-notice.txt.  En cas d'oubli, les lignes suivantes peuvent sauver la vie.
# for f in corrINGE1114-00* ; do (cat fdl-notice.txt $f)>$f.tmp  ;done
# for f in corrINGE1114-00*; do mv $f.tmp $f ;done


notice_fdl = "".join(manip.Fichier("fdl-notice.txt").contenu())
print notice_fdl

def AjouteZero(n):
	N = str(n)
	a = []
	for i in range(len(N),4): a.append("0")
	a.append(N)
	return "".join(a)

args = sys.argv[1:]
NomGene = args[0]
deb = int(args[1])
fin = int(args[2])

for i in range(deb,fin+1) :
	label = NomGene+AjouteZero(i)
	fCorr = manip.Fichier("exo"+label+".tex")
	fExo = manip.Fichier("corr"+label+".tex")

	texte = notice_fdl+"\\begin{exercice}\label{exo"+label+"}\n\n<++>\n\n\corrref{"+label+"}\n\end{exercice}"
	fCorr.write(texte,"w")

	texte = notice_fdl+"\\begin{corrige}{"+label+"}\n\n<++>\n\n\end{corrige}"
	fExo.write(texte,"w")

	print "\Exo{"+label+"}"
