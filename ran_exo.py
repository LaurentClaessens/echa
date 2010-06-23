#! /usr/bin/python
# -*- coding: utf8 -*-

#
# Création d'exercices aléatoire (sous certaines contraintes) pour mon cours de physique.
#
#

import random, string, math, os, commands

PWD = commands.getoutput("pwd")

#########################################
###### La classe Fichier
##########
# Une instance de cette classe est créée en donnant le chemin d'un fichier (qui existe ou non).
# self.chemin	est le chemin du fichier
# self.Nom	est son nom sans le répertoire
# self.Rep	est juste le répertoire
# self.existe	est si le fichier donné existe. Note que si il existe un lien du nom donné, il sera existant.
class Fichier(object):
	def __init__ (self, filename):
		self.chemin = filename
		self.Nom = self.chemin[self.chemin.rindex('/')+1:]
		#self.Rep = self.chemin.replace(self.Nom,"")			# Ceci ne fournit pas le / au bout du nom du répertoire
		posPoint=self.chemin.rfind('.')
		if posPoint<> -1:
			self.Extension = self.chemin[posPoint:]
		if posPoint == -1:
			self.Extension = ""
		self.Rep = self.chemin[:self.chemin.rindex('/')+1]
		#self.cheminGene = self.Nom.replace(self.Extension,"")		# CompletGene est le nom complet sans l'extension
		self.existe = os.path.isfile(self.chemin) or os.path.islink(self.chemin)		# Vaut 1 si le fichier existe (ou un lien).
	def OpenFile(self,opt):
		self.file = open(self.chemin,opt)			# Pour fermer le fichier, c'est self.file.close()


###################################
#### Les classes VarType 123
######
# Donnent les paramètres des différents types d'exercices.
# self.StrFichierE	est ce qui est écrit au haut du fichier d'exercice
# self.StrFichierC	est ce qui est écrit au haut du fichier de correction
# self.StrConcll	est ce qui est écrit au bas du fichier de correction.
# self.Nlin et self.Ncol	sont le nombre de lignes et de colonnes sur lesquels les exercices seront écrits. Le produit des deux est le nombre total d'exercices ui seront générés.
class VarType1 (object):
	def __init__(self,num):
		self.StrFichierE = ["% Ce fichier est généré automatiquement par le script ran_exo.py\n  \\begin{exercice}\\label{exo"+str(num)+"}\n \\corrref{"+str(num)+"}\n Les trinômes suivants ont deux racines entières entre -10 et 10. Trouves les. \n\\begin{align*}\n"]
		self.StrFichierC = ["\n% Ce fichier est généré automatiquement par le script ran_exo.py\n  \\begin{corrige}{"+str(num)+"}\n\n\\begin{align*}\n"]
		self.StrConcl ="\n\\end{align*}\n Affin d'avoir deux solutions entières, un trinome doit s'écrire sous la forme $a(x-x_1)(x-x_2)$ où $x_1$ et $x_2$ sont les deux racines entières. Le trinôme aura donc toujours la forme $ax^2-a(x_1+x_2)+ax_1x_2$. C'est pour cela que \emph{tous} les trinômes de cet exercice peuvent commencer par simplifier le coefficient de $x^2$.\n\\end{corrige}"
		self.fExo = Fichier (PWD+"/exo"+str(num)+".tex")
		self.fCorr = Fichier (PWD+"/corr"+str(num)+".tex")
		self.Nlin = 5
		self.Ncol = 2
		self.Al = Alea(-10,10,10)

class VarType2 (object):
	def __init__(self,num):
		self.StrFichierE = ["% Ce fichier est généré automatiquement par le script ran_exo.py\n  \\begin{exercice}\\label{exo"+str(num)+"}\n \\corrref{"+str(num)+"}\n Les trinômes suivants ont deux racines rationnelles -10 et 10. Trouves les.\\begin{align*}\n"]
		self.StrFichierC = ["\n% Ce fichier est généré automatiquement par le script ran_exo.py\n  \\begin{corrige}{"+str(num)+"}\n\n\\begin{align*}\n"]
		self.StrConcl ="\n\\end{align*}\n \\end{corrige}"
		self.fExo = Fichier (PWD+"/exo"+str(num)+".tex")
		self.fCorr = Fichier (PWD+"/corr"+str(num)+".tex")
		self.Nlin = 5
		self.Ncol = 2
		self.Al = Alea(-5,5,10)


class VarType3 (object):
	def __init__(self,num):
		self.StrFichierE = ["% Ce fichier est généré automatiquement par le script ran_exo.py\n  \\begin{exercice}\\label{exo"+str(num)+"}\n \\corrref{"+str(num)+"} Les trinômes suivants sont aléatoires; trouves les solutions quand il y en a. \\begin{align*}\n"]
		self.StrFichierC = ["\n% Ce fichier est généré automatiquement par le script ran_exo.py\n  \\begin{corrige}{"+str(num)+"}\n\n\\begin{align*}\n"]
		self.StrConcl ="\n\\end{align*}\n \\end{corrige}"
		self.fExo = Fichier (PWD+"/exo"+str(num)+".tex")
		self.fCorr = Fichier (PWD+"/corr"+str(num)+".tex")
		self.Nlin = 5
		self.Ncol = 2
		self.Al = Alea(-10,10,10)

#########################
#### Deux définitions pour les PGCD
########################

## Retourne le pgcd de deux nombres.
def pgcd (a,b):
	x = abs(a)
	y = abs(b)
	if a == 0 : 
		return 1
	if a <> 0 :
 		l = range(1,min(x,y) + 1)
		l.reverse()
		for i in l:
			if x % i == 0 and y % i == 0:
				return i

# Retourne le pgcd d'une liste de nombres.
def pgcdL (a):
	x = [abs(n) for n in a]
	if min([ n == 0 for n in x ]) == True : 
		return 1
	else :
 		l = range(1,min(x) + 1)
		l.reverse()
		for i in l:
			if min( n % i == 0 for n in x ) == True:
				return i


###############################################
#
# Quelque fonctions de calcul et de simplification d'expressions
#
################################################

# Retourne si un nombre donné est un carré parfait ou non
def carre_parfait(x):
	if x > 0:
		return round(math.sqrt(x))==math.sqrt(x) 
	else : 
		return False

#####################################
# La fonction suivante prends un entier f comme argument et sort deux entiers a et b tels que sqrt(x)=a*sqrt(b)
#	avec a, le plus grand possible. Inutile de dire que ce n'est pas optimisé !
# Il sort la réponse sous la forme d'un couple (sorti,interieur).
######################################
def Sort_carre(f):
	sorti = 1
	interieur = f
	i = 2
	while i < int( math.sqrt(interieur)+1):
		while interieur % (i**2) == 0:
			sorti = sorti * i
			interieur = interieur/(i**2)
		i = i + 1	
	return [sorti,interieur]

########################
# Part d'un quatruple (a,b,c,d) qui signifie (a+b*sqrt(c))/d et retourne la même chose en simplifié sous forme d'un quadruple.
# 	self.liste est un quadruple [a,b,c,d] qui signifie la même chose qu'au départ.
####################
class SoluceReduite(object):
	def __init__(self,a,b,c,d):		
			# Éliminer le dénominateur
		x1 = [ a/d,b/d,c ]
			# Sortir ce qui peut de la racine, et l'inclure au b.
		x = [x1[0] , x1[1]*(x1[2].sqrt()[0]) , x1[2].sqrt()[1]]
		if x[0].den == x[1].den :
			y = [  Fraction(x[0].num,1) , Fraction(x[1].num,1) , x[2] ,  Fraction(x[0].den,1) ]
		else :
			y = [ x[0] , x[1] ,x[2] , Fraction(1,1)  ]
		self.liste = y

	def LaTeX(self):
		affi =[]
		l = self.liste
		if l[2].num == 0:
			return (l[0]/l[3]).LaTeX()
		if (l[2].num == l[2].den):
			fr = (l[0]+l[1])/l[3]
			return fr.LaTeX()
		if l[1].num == 0:
			return (l[0]/l[3]).LaTeX()	
			
		if (l[3].num<>0 and l[2].num <> l[2].den and l[1].num <>0 ) :
			nume = []
			if l[0].num <> 0:
				nume.append(l[0].LaTeX())
			if (l[1].num > 0 and l[0].num <> 0 ):
				nume.append("+")
			if l[1].num == -l[1].den == -1 :
				nume.append("-")
			if abs(l[1].num)<>l[1].den :
				nume.append(l[1].LaTeX())
			nume.append("\sqrt{"+l[2].LaTeX()+"}")
			if l[3].num == 1:
				return "".join(nume)
			if l[3].num <> 1:
				affi.append("\\frac{")
				affi.append("".join(nume))
				affi.append("}{"+l[3].LaTeX()+"}")
				return "".join(affi)
			
#####################################
##### La classe Fraction
#
# Une instance se crée en donnant le numérateur et le dénominateur (entiers).
# self.num	est le numérateur de la fraction
# self.den	est le dénominateur.  (la fraction est simplifiée, et l'éventuel signe est automatiquement porté par le numérateur)
class Fraction (object):
	def __init__ (self,x,y):
		div = pgcd(x,y)
		a = x/div
		b = y/div
		if a*b < 0 :
			a = -abs(a)
			b = abs(b)
		if a*b > 0 :
			a = abs(a)
			b = abs(b)
		self.num = a
		self.den = b
		self.carre_parfait = (carre_parfait(self.num) and carre_parfait(self.den))
		if self.den == 0:
			print "J'ai un problème de dénominateur nul dans la fraction "+str(self.num)+"/"+str(self.den)+"."
		self.valeur = round(self.num/self.den)

	# La méthode sqrt sur une fraction sort ce qu'elle peut de la racine carré d'une fraction. Ça prend
	#	sqrt{self} et en fait x*sqrt{y} où x et y sont des fractions.
	def sqrt(self) :
		numD = Sort_carre(self.num)
		denD = Sort_carre(self.den)
		return [ Fraction( numD[0],denD[0] ),Fraction( numD[1],denD[1] ) ]
		
# Surcharger les opérateurs mathématiques courants
	def inverse(self):
		return Fraction (self.den,self.num)
	def __add__ (self,f):
		return Fraction (self.num*f.den+f.num*self.den,self.den*f.den)
	def __sub__ (self,f):
		return Fraction (self.num*f.den-f.num*self.den,self.den*f.den)
	def __mul__ (self,f):
		if type(f) == Fraction :
			return Fraction ( self.num*f.num,self.den*f.den )
		if type(f) == int :
			return Fraction( self.num*f,self.den )
	def __div__ (self,f):
		return self * f.inverse()
	def __pow__ (self,exp):
		return Fraction ( self.num**(exp),self.den**(exp) )

# Affichage
	def affiche (self):
		if self.num == 0:
			return str(0)
		if abs(self.den) <> 1:
			return str(self.num)+"/"+str(self.den)
		else :
			return str(self.num)
	def LaTeX (self):
		affi = []
		if self.num == 0:
			return "0"
		if self.num <> 0:
			if self.num < 0:
				affi.append("-")
			if self.den <> 1:
				affi.append("\\frac{"+str(abs(self.num))+"}{"+str(self.den)+"}")
			if self.den == 1:
				affi.append(str(abs(self.num)))
		return "".join(affi)
			
			
	
#################################################
# Les Points sont donnés par leurs coordonnées qui peuvent être passées soit en entiers soit en Fraction. 
#   Dans les deux cas, en bout de compte les méthodes x et y sont du type Fraction.
#################################################
class Point (object):
	def __init__(self,x,y):
		if type(x) == int :		
			a = Fraction(x,1)
		else :
			a = x
		if type(y) == int :
			b = Fraction(y,1)
		else :
			b = y
		self.x = a
		self.y = b
	def affiche (self) :
		return "("+self.x.affiche()+" , "+self.y.affiche()+")"

#####################################################################################
#
#  Alea sert à donner des nombres aléatoires dans un certains intervalle.  
#
#	m : le nombre minimum
#	M : le maximum
#	Num : la taille maximale du dénominateur quand on demande une fraction. La valeur de la fraction est toujours dans l'intervalle donné
#
#	self.entier donne un entier
#	self.entierNN donne un entier non nul
#	self.fraction retourne une fraction
#	self.Point retourne un point dont le x n'est pas dans nnx et dont le y n'est pas dans nny, mais dont les deux sont dans [self.min,self.max]
#		En utilisant cette méthode, les points tirés sont toujours dans un carré
#
######################################################################################
class Alea (object):
	def __init__(self,m,M,Num):
		self.min = m
		self.max = M
		self.INum = Num
		self.intervalle = self.min,self.max
	def entier (self):
		return random.randint(self.min,self.max)
	def entierNN (self):
		a = self.entier()
		while a == 0 :
			a = self.entier()
		return a
	def fraction (self):
		base = Fraction ( random.randint(self.min,self.max-1),1 )
		den = 0
		while den == 0 :
			den = random.randint(-self.INum,self.INum)
		decimal = Fraction (1,den)
		return base + decimal
	def fractionNN (self):
		x = self.fraction()
		while x.num == 0:
			x = self.fraction()
		return x
	def Point (self,nnx,nny) : 
		x = self.fraction()
		while x.valeur in nnx :
			x = self.fraction()
		y = self.fraction()
		while y.valeur in nny :
			y = self.fraction()
		return Point(x,y)
	def PointEntier (self,nnx,nny) : 
		x = self.entier()
		while x in nnx :
			x = self.entier()
		y = self.entier()
		while y in nny :
			y = self.entier()
		return Point(x,y)
		


#######################################################
#  Un objet de la classe binome est un binôme ax+b donné par son a et b
###########################################################
class Binome (object):
	def __init__(self,a,b):
		self.a = a
		self.b = b
		if a == 0 and b <> 0 :
			self.nsoluce = 0
			self.soluce = []
		if a <> 0 :
			self.nsoluce = 1
			self.soluce = [(-1)*self.b/self.a]



#######################################################
#  Un objet de la classe trinome est un trinôme ax^2+bx+c donné par son a,b,c
##################################################"
class Trinome (object):
	def __init__(self,aa,bb,cc):
		if type(aa) == int :
			self.a = Fraction(aa,1)
		else :
			self.a = aa
		if type(bb) == int :
			self.b = Fraction(bb,1)
		else :
			self.b = bb
		if type(cc) == int :
			self.c = Fraction(cc,1)
		else :
			self.c = cc
		if self.a.num <> 0 :
			self.discriminant = (self.b**2)-self.a*self.c*4
# Ici, j'utilise implicitement le fait que le signe d'une Fraction est porté par le numérateur; le déno est toujours positif.
			if self.discriminant.num < 0 :
				self.nsoluce = 0	
				self.soluce = []			
			if self.discriminant.num == 0 :
				self.nsoluce = 1	
				self.soluce = [ self.b*(-1)/(self.a*2) ]
			if self. discriminant.num > 0 :
				self.nsoluce = 2
		
			self.sommet = Point ( (self.b*(-1))/(self.a*2),self.discriminant*(-1)/(self.a*4))
		if self.a.num == 0:
			L = Binome(self.b,self.c)
			self.nsoluce = L.nsoluce
			self.soluce = L.soluce
	def affsoluce(self):
		if self.nsoluce == 0:
			return "Vide"
		if self.nsoluce == 1:
			return "{ "+self.soluce[0].affiche+" }"
		if self.nsoluce == 2:
			if self.soluceQ:
				return "{ "+self.soluce[0].affiche+" , "+self.soluce[1].affiche+"}"
			else :
				affi = []
				inva = (self.a*2).inverse()
				affi.append("("+inva.affiche()+")")
				affi.append( "("+(self.b*(-1)).affiche())
				affi.append("+- sqrt("+ self.discriminant.affiche() +")" )
				return "".join(affi)
				
	def affiche (self):
		return  "("+self.a.affiche()+","+self.b.affiche()+","+self.c.affiche()+")"
	
	# Produit le code LaTeX du trinôme
	def LaTeX (self):
		affi = []
		if (self.a.num <> 0) :
			if abs(self.a.num) <> self.a.den:
				affi.append(self.a.LaTeX())
			else:
				if self.a.num < 0:
					affi.append("-")
			affi.append("x^2")

		if (self.b.num <> 0) :
			if self.b.num > 0:
				affi.append("+")
			if abs(self.b.num) <> self.b.den:
				affi.append(self.b.LaTeX())
			else:
				if self.b.num < 0:
					affi.append("-")
			affi.append("x")

		if (self.c.num <> 0) :
			if self.c.num > 0:
				affi.append("+")
			affi.append(self.c.LaTeX())

		return "".join(affi)

	# Produit le code LaTeX de la solution
	def sLaTeX (self):
		affi = []
		if self.a == self.b == self.c == 0:
			return ("\\eR")
		if self.nsoluce == 0:
			return ("\\emptyset")

		return "\\left\\{"+SoluceReduite( Fraction(-1,1)*self.b , Fraction(1,1) , self.discriminant , self.a*2).LaTeX()+","+SoluceReduite( Fraction(-1,1)*self.b , Fraction(-1,1) , self.discriminant , self.a*2).LaTeX()+"\\right\\}"
	
	def affiche (self):
		return  "("+self.a.affiche()+","+self.b.affiche()+","+self.c.affiche()+")"
			


#####################################"
#
# Donne un trinôme avec la donnée de trois points
# 	En réalité, il sort le triple de Fractions qui sont les paramètres. Ainsi le créateur d'exercice décide si le trinôme est acceptable ou non.
#
######################################
def TrinTroisPts(P,Q,R):
	deno = (Q.x-P.x)*(R.x-P.x)*(R.x-Q.x)
	aa = ((Q.x-P.x)*R.y+(P.y-Q.y)*R.x+P.x*Q.y-P.y*Q.x)/deno
	T1 = ((P.x**2)*(R.y-Q.y))
	T2 = ( (Q.x**2)*R.y )
	T3 = ( Q.y*(R.x**2) )
	T4 = (P.y*(Q.x**2-R.x**2))
	bb = (T1-T2+T3+T4)/deno
	cc = ((P.x*(Q.x**2)-(P.x**2)*Q.x)*R.y+(P.y*Q.x-P.x*Q.y)*(R.x**2)+((P.x**2)*Q.y-P.y*(Q.x**2))*R.x)/deno

	return [aa,bb,cc]

#####################################
##### CreeTrin retourne un trinôme d'un certain type avec les paramètres var
#####
#####	type 1 : coefficients entiers, deux solutions entières
#####		var contient un élément de la classe Alea qui dit les valeurs possibles
#####	type 2 : Deux solutions rationnelles; toutes les fractions ont numérateur et dénominateur plus petits que 100
#####	type 3 : Le trinôme a trois coefficients rationnels aléatoires. Les coefficients sont entre -5 et 5, 
#####			et les nombres dans les fractions sont limités à 20
#####	type 4 : idem que le 3, mais à coefficients entiers
#####
####################################
def CreeTrin( type,var ):
	if type == 1:
		P = Point (var.entier(),0)
		Q = Point (var.entier(),0)
		
		aa = var.entierNN()
		bb = (P.x+Q.x)*aa
		cc = (P.x*Q.x)*aa
		
		return Trinome(aa,bb,cc)
	if type == 2:
		aa = bb = cc = Fraction (1000,1)
		while max( abs(aa.num) , aa.den , abs(bb.num) , bb.den , abs(cc.num) , cc.den ) > 100:
			P = Point (var.fraction(),0)
			Q = Point (var.fraction(),0)
		
			aa = var.fractionNN()
			bb = (P.x+Q.x)*aa
			cc = (P.x*Q.x)*aa
		
		return Trinome(aa,bb,cc)
	if type == 3:
		aa = bb = cc = Fraction (1000,1)
		while max( abs(aa.num) , aa.den , abs(bb.num) , bb.den , abs(cc.num) , cc.den ) > 20:
			aa = var.fraction()
			bb = var.fraction()
			cc = var.fraction()
		return Trinome(aa,bb,cc)
	if type == 4:
		aa = var.entier()
		bb = var.entier()
		cc = var.entier()
		return Trinome(aa,bb,cc)

# La fonction qui crée effectivement les fichiers d'exercices et de corrections en termes du type d'exercice et des variables données.
def Cree_Fichiers (type,vars):
	for i in range(1,vars.Nlin+1):
		if i <> 1:
			vars.StrFichierE.append("\\\\\n")	
			vars.StrFichierC.append("\\\\\n")	
		for j in range(1,vars.Ncol+1):
			xi = CreeTrin(type,vars.Al)
			if j <> 1 :
				vars.StrFichierE.append("&")
				vars.StrFichierC.append("&")
			vars.StrFichierE.append("f_{"+str((i-1)*vars.Ncol+j)+"}(x)&="+xi.LaTeX())
			vars.StrFichierC.append("S_{"+str((i-1)*vars.Ncol+j)+"}&="+xi.sLaTeX())

	vars.StrFichierE.append("\n\\end{align*}\n\\end{exercice}")
	vars.StrFichierC.append(vars.StrConcl)
		
	vars.fExo.OpenFile("w")
	vars.fExo.file.write("".join(vars.StrFichierE))
	vars.fExo.file.close()
	print vars.fExo.chemin

	vars.fCorr.OpenFile("w")
	print "".join(vars.StrFichierC)
	vars.fCorr.file.write("".join(vars.StrFichierC))
	vars.fCorr.file.close()


################# Création de l'exercice 200 ###########################
####                des exercices de type 1             #######
########################################################################

var200 = VarType1(200)
Cree_Fichiers(1,var200)

################# Création de l'exercice 201 ###########################
####                des exercices de type 2             #######
########################################################################

var201 = VarType2(201)
Cree_Fichiers(2,var201)

################# Création de l'exercice 202 ###########################
####                des exercices de type 3           #######
########################################################################

var202 = VarType3(202)
Cree_Fichiers(4,var202)
