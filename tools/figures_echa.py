#! /usr/bin/sage -python
# -*- coding: utf8 -*-


# This is part of Un soupçon de physique, sans être agressif pour autant
# Copyright (C) 2006-2009
#   Laurent Claessens
# See the file fdl-1.3.txt for copying conditions.


from __future__ import division
import commands, os, copy, math						# Le module copy est pour faire des copies d'objets
from phystricks import *
from phystricks import mecanique

# Le module phystricks demande d'avoir installé Sage et qu'il doit bien placé dans /usr/bin/sage
#  Notez que les paquets Ubuntu sont d'une vieille version ultra boguée. Il vaut nettement mieux télécharger les binaires depuis le site.
# http://www.sagemath.org/download-linux.html

REP = commands.getoutput("pwd")

def figures_derr():
	# Les données générales
	#########################################################################
	n_ssfig = 6
	taille_tg = 4
	taille_approx = taille_tg
	debTrace = 0.5
	finTrace = 8
	f = Fonction("(-3/x)+5")
	P = f.PointDessus(1)
	Q = f.PointDessus(3)

	# Création de la toute petite figure qui ne contient que l'énoncé du problème.
	##########################################################################
	pspict_pt = pspicture()
	pspict_pt.TraceFonction(f,"",debTrace,finTrace)
	pspict_pt.MarquePoint(P,0.3,135,"*","$P$")
	fig_pt = figure("Comment trouver la tangente au point $P$ à cette courbe ?","fig_derrtrois",REP+"/fig_derr3.pstricks")
	fig_pt.AjoutePspicture(pspict_pt)
	fig_pt.Dilate(0.5)
	fig_pt.Conclure()
	fig_pt.EcrireFichier()

	# Création d'une pspicture qui contient les éléments communs à toutes celles que je vais dessiner
	##########################################################################
	pspict_gene = pspicture()
	angle = Point(Q.x , P.y)
	mX = Segment(P,angle).Milieu()
	mY = Segment(Q,angle).Milieu()
	pspict_gene.TraceFonction(f,"",debTrace,finTrace)
	pspict_gene.DrawSegment( f.tangente(P.x).FixeTaille(taille_tg),"linecolor=green" )
	
	# Création de la grande figure.
	##########################################################################
	pspict_gd = copy.deepcopy(pspict_gene)
	pspict_gd.DrawSegment(Segment(P,angle),"linestyle=dashed")
	pspict_gd.DrawSegment(Segment(Q,angle),"linestyle=dashed")
	pspict_gd.DrawSegment(Segment(P,Q).AugmenteTaille(1,1),"linecolor=blue")
	pspict_gd.MarquePoint(P,0.3,135,"*","$P$")
	pspict_gd.MarquePoint(Q,0.3,90,"*","$Q$")
	pspict_gd.MarquePoint(angle,0.3,-45,"*","$R$")
	pspict_gd.MarquePoint(mX,0.3,-90,"none","$\Delta x$")
	pspict_gd.MarquePoint(mY,0.4,0,"none","$\Delta y$")
	#pspict_gd.TraceRectangle( Rectangle(pspict_gd.BB.bg,pspict_gd.BB.hd),"linecolor=cyan" )			# La boubding box
	
	fig_gd = figure("Nous plaçons le point $P$ à l'abcisse $x$, et le point $Q$ un peu plus loin : en $x+\Delta x$. En vert, la tangente que nous cherchons.","fig_derrun",REP+"/fig_derr1.pstricks")
	fig_gd.AjoutePspicture(pspict_gd)
	fig_gd.Dilate(0.7)
	fig_gd.Conclure()
	fig_gd.EcrireFichier()
	
	# Création des sous figures
	##########################################################################
	
	ssfigs = []
	for i in range(0,n_ssfig):
		legende = "\ldots{} de mieux en mieux \ldots"
		if i == 0 :
			legende = "Pas très bon \ldots"
		if i == n_ssfig-1 :
			legende = "\ldots{} presque parfait."

		ssfig = subfigure(legende,"labelpetit")

		pspict = copy.deepcopy(pspict_gene)
		Qi = f.PointDessus( Q.x-i*(Q.x-P.x)/(n_ssfig) )
		pspict.DrawSegment(Segment(P,Qi).FixeTaille(taille_approx),"linecolor=blue")
		#pspict.TraceRectangle( Rectangle(pspict.BB.bg,pspict.BB.hd),"linecolor=cyan" )       # La boubding box
		pspict.MarquePoint(P,0.3,135,"*","$P$")
		pspict.MarquePoint(Qi,0.4,-45,"*","$Q_"+str(i)+"$")
		ssfig.AjoutePspicture(pspict)
		ssfigs.append(ssfig)
		
	# Création de la figure principale contenant toutes les petites
	##########################################################################
	
	fig_pr = figure("Au fur et à mesure que le point $Q_i$ se rapproche de $P$, l'approximation se rapproche de la tangente.","FigTanApproxSuite",REP+"/fig_derr2.pstricks")
	for ssf in ssfigs :
		fig_pr.AjouteSSfigure(ssf)
	fig_pr.Dilate(0.5)
	fig_pr.Conclure()
	
	fig_pr.EcrireFichier()
	
def figure_tg_parab():
	f = Fonction("(x)^2/2")
	mx = -3			# Les abscisses entre lesquelles on va tracer la fonction.
	Mx = 3
	P = f.PointDessus(1)
	Q = f.PointDessus(-2)

	pspict = pspicture()
	pspict.TraceFonction(f,"",mx,Mx)

	tanP = f.tangente(P.x).AugmenteTaille(1,1)
	pspict.DrawSegment(tanP,"linecolor = blue")

	tanQ = f.tangente(Q.x)#.AugmenteTaille(1,1)
	pspict.DrawSegment(tanQ,"linecolor = red")

	# Comme toujours, on marque les points après.
	pspict.MarquePoint(P,0.3,135,"*","$P$")
	pspict.MarquePoint(Q,0.3,45,"*","$Q$")

	axes = Axes( Point(0,0), BoundingBox(Point(-1,-1), Point(1,1)) )
	axes.AjusteFonction(f,mx,Mx)
	axes.AjouteGrille()
	pspict.TraceAxes(axes)
	#pspict.TraceBB()

	fig = figure("La dérivée à la fonction $x\mapsto x^2/2$. La dérivée vaut $x\mapsto x$, et, en effet, tu remarqueras que le coefficient angulaire de la tangente vaut $-2$ en $Q$ et $1$ en $P$.","fig_tg_parab",REP+"/"+"fig_tg_parab.pstricks")
	fig.AjoutePspicture(pspict)
	fig.Conclure()
	fig.EcrireFichier()
	

def figure_surface():
	#f = Fonction("(-4/(x+3))+5")
	f = Fonction("-((x+0.5)/3)^2+4+x")
	mx = -0.5
	Mx = 7
	x = 5
	dx = 1
	P = f.PointDessus( x )
	absP = Point( P.x,0 )
	Q = f.PointDessus( x+dx )
	absQ = Point( Q.x,0 )
	Qa = Point( x+dx,P.y )
	CouleurExt = "red"		# La couleur du petit rectangle.

	pspict = pspicture()

	axes = Axes( Point(0,0), BoundingBox(Point(-1,-1), Point(1,1)) )
	axes.AjusteFonction(f,mx,Mx)
	axes.AjouteOption("labels=none,ticks=none")
	f.AjouteSurface(0,P.x)
	f.ListeSurface[-1].options.DicoOptions["fillstyle"] = "vlines"

	# g est la fonction horizontale qui "approxime" f.
	g = Segment(P,Qa).fonction
	g.AjouteSurface(P.x,Qa.x)
	g.ListeSurface[-1].options.DicoOptions["fillstyle"] = "vlines"
	g.ListeSurface[-1].ChangeCouleur(CouleurExt)

	pspict.TraceAxes(axes)
	pspict.TraceFonction(f,"",mx,Mx)
	pspict.TraceFonction(g,"linecolor="+CouleurExt,P.x,Qa.x)
	pspict.MarquePoint(P,0.3,90,"*","$f(x)$")
	#pspict.MarquePoint(Q,0.3,90,"*","$Q$")
	pspict.MarquePoint(absP,0.3,-90,"*","$x$")
	pspict.MarquePoint(absQ,0.3,-60,"*","$x+\Delta x$")
	#pspict.TraceBB()

	fig = figure("L'aire en-dessous d'une courbe. Le rectangle rouge, d'aire $f(x)\Delta x$, approxime de combien l'aire en-dessous de la fonction $f$ augmente lorsqu'on passe de $x$ à $x+\Delta x$.","fig_surface",REP+"/"+"fig_surface.pstricks")
	fig.AjoutePspicture(pspict)
	#fig.Dilate(0.6)
	fig.Conclure()
	fig.EcrireFichier()

def figure_derr_enveloppe():
	# Si tu changes la fonction, il faut changer le caption qui est dans la commande \CaptionDerrEnveloppe,  à l'endroit du \input de la figure.
	f = Fonction("(x)^2/3")
	mx = -4
	Mx = 4
	Npts = 10
	taille = 3
	P = []
	tangentes = []
	for i in range(1,Npts):
		x =  mx+i*(Mx-mx)/Npts 
		P.append( f.PointDessus(x) )
		tangentes.append( f.tangente(x).FixeTaille( taille ) )

	pspict = pspicture()

	axes = Axes( Point(0,0), BoundingBox(Point(-1,-1), Point(1,1)) )
	axes.AjusteFonction(f,mx,Mx)
	#axes.AjouteOption("labels=none,ticks=none")

	pspict.TraceAxes(axes)
	for seg in tangentes :
		pspict.DrawSegment(seg,"linecolor=blue")
	pspict.TraceFonction(f,"linecolor=red,linestyle=dashed",mx,Mx)

	fig = figure("\CaptionDerrEnveloppe","fig_derr_enveloppe",REP+"/"+"fig_derr_enveloppe.pstricks")
	fig.AjoutePspicture(pspict)
	fig.Conclure()
	fig.EcrireFichier()

def figure_CarrEtCubes():
	f = Fonction("(x)^2")
	g = Fonction("(x)^3")
	gmx = -1.7
	gMx = -gmx
	fmx = -2.3
	fMx = -fmx

	pspict = pspicture()
	pspict.TraceFonction(f,"linecolor=red",fmx,fMx)
	pspict.TraceFonction(g,"linecolor=cyan",gmx,gMx)

	axes = Axes( Point(0,0), BoundingBox(Point(-1,-1), Point(1,1)) )
	axes.AjusteFonction(f,fmx,fMx)
	axes.AjusteFonction(g,gmx,gMx)
	axes.AjouteGrille()
	pspict.TraceAxes(axes)
	#pspict.TraceBB()

	fig = figure("\CaptionFigCarrEtCubes","FigCarrEtCubes",REP+"/"+"fig_CarrEtCubes.pstricks")

	fig.AjoutePspicture(pspict)
	fig.Conclure()
	fig.EcrireFichier()

	
def figures_Rolle():
	f = Fonction("-(x+1)^2/10+1.5")
	mx = -6
	Mx = 4

	I = f.PointDessus(mx+0.5)
	P = f.PointsNiveau(I.y)[0]
	Q = f.PointsNiveau(I.y)[1]

	pspict = pspicture()
	pspict.TraceFonction(f,"linecolor=red",mx,Mx)

	M = f.extrema()[0]
	tg = f.tangente(M.x).FixeTaille(3)


	axes = Axes( Point(0,0), BoundingBox(Point(-1,-1), Point(1,1)) )
	axes.AjusteFonction(f,mx,Mx)
	axes.AjouteGrille()
	pspict.TraceAxes(axes)
	pspict.DrawSegment(tg,"linecolor=blue")
	pspict.MarquePoint(M,0.3,45,"*","$c$")
	pspict.MarquePoint(P,0.3,45,"*","$a$")
	pspict.MarquePoint(Q,0.3,135,"*","$b$")
	#pspict.TraceBB()

	fig = figure("\CaptionRolle","FigRolle",REP+"/"+"figure_Rolle_Rolle")

	fig.AjoutePspicture(pspict)
	fig.Conclure()
	fig.EcrireFichier()


def figure_Rolle_AccFinis():
	#f = Fonction("(x)^2/3-0.5")
	f = Fonction("5/(x+4)-1")
	mx = -3
	Mx = 4

	P = f.PointDessus(mx+0.2)
	Q = f.PointDessus(Mx-0.5)
	seg = Segment(P,Q).AugmenteTaille(1,1)
	ca = (Q.y-P.y)/(Q.x-P.x)

	# Ce petit for, c'est parce que j'ai besoin de prendre un endroit où la tangente est parallèle, entre P et Q.
	for x in maxima().solve([f.derive().fx+"="+str(ca)],["x"])[0]:
		if x > P.x and x < Q.x :
			C = f.PointDessus( x ) 

	pspict = pspicture()
	pspict.TraceFonction(f,"linecolor=red",mx,Mx)

	tg = f.tangente(C.x).FixeTaille(3)


	axes = Axes( Point(0,0), BoundingBox(Point(-1,-1), Point(1,1)) )
	axes.AjusteFonction(f,mx,Mx)
	axes.AjouteGrille()
	axes.AjouteOption("labels=none,ticks=none")
	pspict.TraceAxes(axes)
	pspict.DrawSegment(tg,"linecolor=blue")
	pspict.DrawSegment(seg,"linecolor=green,linestyle=dashed")
	pspict.MarquePoint(C,0.3,45,"*","$c$")
	pspict.MarquePoint(P,0.3,45,"*","$a$")
	pspict.MarquePoint(Q,0.3,-90,"*","$b$")
	#pspict.TraceBB()

	fig = figure("\CaptionAccfinis","FigAccFinis",REP+"/"+"figure_Rolle_AccFinis")

	fig.AjoutePspicture(pspict)
	fig.Conclure()
	fig.EcrireFichier()



def figure_surfMRUA():
	a = 0.7
	v0 = 1
	f = Fonction(str(a)+"*x+"+str(v0))
	g = Fonction(str(v0))
	mx = 0
	Mx = 7
	x = 6
	dx = 0.5
	P = f.PointDessus( x )
	D = f.PointDessus( 0 )
	VF = f.PointDessus( x )
	F = Point( 0,VF.y )
	absP = Point( P.x,0 )
	CouleurExt = "black"		# La couleur du petit rectangle.

	pspict = pspicture()

	axes = Axes( Point(0,0), BoundingBox(Point(-1,-1), Point(1,1)) )
	axes.AjusteFonction(f,mx,Mx)
	axes.AjouteOption("labels=none,ticks=none")

	f.AjouteSurface(0,P.x)
	f.ListeSurface[-1].options.DicoOptions["fillstyle"] = "vlines"

	# Le but d'en faire deux est que la première soit remplie pour effacer le coloriage de f en-dessous de v0.
	g.AjouteSurface(0,P.x)
	g.ListeSurface[-1].options.DicoOptions["fillcolor"] = "white"
	g.AjouteSurface(0,P.x)
	g.ListeSurface[-1].ChangeCouleur("red")
	#g.ListeSurface[-1].options.DicoOptions["fillcolor"] = "white"
	g.ListeSurface[-1].options.DicoOptions["fillstyle"] = "hlines"
	

	pspict.TraceFonction(f,"",mx,Mx)
	pspict.TraceFonction(g,"",mx,Mx)
	pspict.MarquePoint(absP,0.3,-90,"*","$t$")
	pspict.MarquePoint(D,0.3,180,"*","$v_0$")
	pspict.MarquePoint(F,0.9,180,"*","$v_0+at$")
	pspict.DrawSegment( Segment(VF,F),"linestyle=dotted" )
	pspict.TraceAxes(axes)
	#pspict.TraceBB()

	fig = figure("\CaptionSurfMRUA","FigSurfMRUA",REP+"/"+"fig_surfMRUA.pstricks")
	fig.AjoutePspicture(pspict)
	#fig.Dilate(0.6)
	fig.Conclure()
	fig.EcrireFichier()


def figure_Euclide():
	P = Polynome([1,2,0,-1])
	Q = Polynome([1,7])
	x = DivEuclide(P,Q)

	for i  in range(0,P.deg-Q.deg+2):
		x.EcrireFichier("divEuclideFAQ"+str(i)+".pstricks",i)

def figure_Matrix():
	pspict=pspicture()
	fig = GenereFigure(REP,"Matrix")

	g = 9.81
	h = 10					# Hauteur des immeubles
	d = 4					# Distance entre les immeubles
	DeltaH = 3				# La hauteur tombée 
	l = 2					# Largeur des immeubles
	vZero = math.sqrt(g*d**2/(2*DeltaH))	# Vitesse initiale, calculée pour tomber de DeltaH sur une distance d
	norme_vZero = 2				# Taille du vecteur (à l'affichage)
	var('x')
	f = Fonction(h-(g*x**2)/(2*vZero**2))	# L'équation de la trajectoire
	A = Point(d,h)				# Le point en face de l'endroit d'où on saute
	B = f.PointDessus(d)			# Point d'arrivée dans l'immeuble d'en face
	dh = MesureLongueur(A,B)

	Immeuble1 = Rectangle( Point(-l,h),Point(0,0) )
	Immeuble2 = Rectangle( Point(d,h),Point(d+l,0) )
	base1 = Point(0,0)
	base2 = Point(d,0)
	dRue = MesureLongueur(base1,base2)
	vitesse = Vecteur( Point(0,h),Point(norme_vZero,h) )
	
	mx = 0
	Mx = d
	pspict.TraceRectangle(Immeuble1,"")
	pspict.TraceRectangle(Immeuble2,"")
	pspict.TraceFonction(f,mx,Mx,"linecolor=red")
	pspict.TraceVecteur(vitesse,"linecolor=blue").MarqueVecteur(0.3,90,"$v_0$")
	pspict.TracePoint(B,"*","linecolor=brown")
	pspict.TraceMesureLongueur(dh,-0.2,"linecolor=blue").MarqueMesureLongueur(0.3,"$\Delta h$")
	pspict.TraceMesureLongueur(dRue,0,"linecolor=blue").MarqueMesureLongueur(0.2,"$d$")

	pspict.Dilate(0.5)			# Mettre le dessin à l'échelle 1/2

	fig.AjoutePspicture(pspict)
	fig.Conclure()
	fig.EcrireFichier()


def figure_lancerDiagonal():
	pspict=pspicture()
	fig = GenereFigure(REP,"lancerDiagonal")

	g = 9.81
	mx = 0
	h  = 1
	depart = Point(0,h)

	for a in [ [20,"green"] , [40,"green"] , [70,"red"] , [80,"red"] ] :
		courbe = mecanique.TirOblilque(depart,6,radian(a[0]))
		pspict.TraceCourbeParamatrique(courbe.F,mx,courbe.Dt,"linecolor=%s"%a[1])		

	pspict.TraceAxesDefaut()

	pspict.Dilate(2)

	fig.AjoutePspicture(pspict)
	fig.Conclure()
	fig.EcrireFichier()

def prefig_DecompVitesse(angleD):
	pspict=pspicture()
	
	O = Point(0,0)
	norme = 10
	norme_affiche = 5
	angle = radian(angleD)
	P = Point(norme_affiche*math.cos(angle),norme_affiche*math.sin(angle))
	courbe = mecanique.TirOblilque(O,norme,angle)
	v = Vecteur(O,P)
	X = Point(1,0)
	Y = Point(0,1)

	OX = Segment(O,X)
	OY = Segment(O,Y)

	Px = P.projection(OX)
	Py = P.projection(OY)

	lx = MesureLongueur(O,Px)
	ly = MesureLongueur(O,Py)

	pspict.TraceCourbeParamatrique(courbe.F,courbe.depart.x,courbe.Dt,"linecolor=red")		
	pspict.TraceVecteur(v,"linecolor=blue").MarqueVecteur(0.3,0,"$\\fv_0$")
	pspict.DrawSegment(Segment(P,Px),"linecolor=green,linestyle=dotted")
	pspict.DrawSegment(Segment(P,Py),"linecolor=green,linestyle=dotted")
	pspict.MarqueAngle(Px,O,P,"$\\alpha$","")
	pspict.TraceMesureLongueur(lx,-0.1,"linecolor=blue").MarqueMesureLongueur(0.3,"$v_0\cos(\\alpha)$")
	pspict.TraceMesureLongueur(ly,0.1,"linecolor=blue").MarqueMesureLongueur(0.8,"$v_0\sin(\\alpha)$")

	pspict.axes.SansDeco()
	pspict.TraceAxesDefaut()
	pspict.DilateX(1)

	return pspict


def figure_DecompVitesse():
	fig_pr = GenereFigure(REP,"DecompVitesse")

	for a in [40,70] :
		pspict=prefig_DecompVitesse(a)

		ssfig = subfigure("","labelpetit")
		ssfig.AjoutePspicture(pspict)
		
		fig_pr.AjouteSSfigure(ssfig)

	fig_pr.Dilate(1)

	fig_pr.Conclure()
	fig_pr.EcrireFichier()
	
def figure_DistanceAngle():
	pspict=pspicture()
	fig = GenereFigure(REP,"DistanceAngle")

	var('x')
	f1 = Fonction(sin(x)*cos(x))
	f2 = Fonction(sin(x))
	mx = -math.pi
	Mx = math.pi

	pspict.TraceFonction(f1,mx,Mx,"linecolor=blue")
	pspict.TraceFonction(f2,mx,Mx,"linecolor=red,linestyle=dotted")

	pspict.TraceAxesDefaut()

	pspict.DilateY(2)

	fig.AjoutePspicture(pspict)
	fig.Conclure()
	fig.EcrireFichier()

def figure_graviton():
	pspict=pspicture()
	fig = GenereFigure(REP,"graviton")

	O = Point(0,0)
	n = 20
	d = 1
	angles = [i*360/n for i in range(0,n)]
	points = []

	for d in [1,3,5,9]:
		for alpha in angles : 
			P = PolaireToPoint(d,alpha)
			points.append(P)
	for P in points :
		pspict.TraceVecteur(Vecteur(O,P),"linecolor=blue")
	for P in points :
		pspict.TracePoint(P,"*","")

	#pspict.TraceAxesDefaut()

	pspict.Dilate(0.4)

	fig.AjoutePspicture(pspict)
	fig.Conclure()
	fig.EcrireFichier()

def figure_OrbiteCentrifuge():
	pspict=pspicture()
	fig = GenereFigure(REP,"OrbiteCentrifuge")

	O = Point(0,1)
	r = 2
	angle = -20
	C = Cercle(O,r)

	pspict.TraceCercle(C,"linecolor=blue")

	for angle in range(0,360,45):
		p = C.PointDessus(angle)
		T = C.VecteurTangent(angle)
		N = C.VecteurNormal(angle)
		G = N.inverse()

		pspict.TraceVecteur(T,"linecolor=red").MarqueVecteur(0.3,angle,"$v$")
		pspict.TraceVecteur(N,"linecolor=green").MarqueVecteur(0.3,angle,"$\\fF_{cf}$")
		pspict.TraceVecteur(G,"linecolor=cyan").MarqueVecteur(0.3,angle+90,"$\\fG$")
		pspict.TracePoint(p,"*","")

	pspict.Dilate(1)

	fig.AjoutePspicture(pspict)
	fig.Conclure()
	fig.EcrireFichier()

def figure_graphesinsrsin():
	pspict=pspicture()
	fig = GenereFigure(REP,"graphefonctionsisisi")

	var('x')
	f = Fonction( (x+sin(x))/(x-sin(x))   )
	mx = 1
	Mx = 50
	F = GrapheUneFonction(f,mx,Mx)
	F.plotpoints = 1000					# Augmente le nombre de points à tracer.
	#F.color = "cyan"
	pspict.TraceGrapheUneFonction(F)
	pspict.axes.Dx = 10					# Ne mettre une marque que tous les 10 sur l'axe X.
	pspict.axes.Dy = 5					

	pspict.TraceAxesDefaut()

	pspict.Dilate(0.5)
	pspict.DilateX(0.5)

	fig.AjoutePspicture(pspict)
	fig.Conclure()
	fig.EcrireFichier()

def figure_parallelograme():
	pspict=pspicture()
	fig = GenericFigure("Parallelograme")

	b = Point(0,0)
	d = Point(2,0)
	c = Point(3,1)
	a = Point(1,1)
	k = Point(0,1)
	bd = Segment(b,d)
	dc = Segment(d,c)
	ca = Segment(c,a)
	ab = Segment(a,b)
	bk = Segment(b,k)
	ka = Segment(k,a)

	pspict.DrawSegment(bd,"linecolor=blue")
	pspict.DrawSegment(dc,"linecolor=blue")
	pspict.DrawSegment(ca,"linecolor=blue")
	pspict.DrawSegment(ab,"linecolor=blue")

	pspict.DrawSegment(ka,"linecolor=green,linestyle=dashed")
	pspict.DrawSegment(bk,"linecolor=green,linestyle=dashed")

	pspict.MarkThePoint(b,"*",0.3,225,"$b$")
	pspict.MarkThePoint(d,"*",0.3,-45,"$d$")
	pspict.MarkThePoint(c,"*",0.3,45,"$c$")
	pspict.MarkThePoint(a,"*",0.3,90,"$a$")
	pspict.MarkThePoint(k,"*",0.3,135,"$k$")

	pspict.Dilate(1)

	fig.AjoutePspicture(pspict)
	fig.Conclure()
	fig.EcrireFichier()


figure_parallelograme()
#figure_graphesinsrsin()
#figure_OrbiteCentrifuge()
#figure_graviton()
#figure_DistanceAngle()
#figure_DecompVitesse()
#figure_lancerDiagonal()
#figure_Matrix()
#figure_Euclide()
#figure_surfMRUA()
#figure_Rolle_AccFinis()
#figures_Rolle()
#figure_tg_parab()
#figure_CarrEtCubes()
#figure_derr_enveloppe()
#figures_derr() 
#figure_surface()	



# Parmi les bogues connus, je te rappelle que le \psset{xunit=1cm,yunit=1cm} arrive APRÈS la pspicture quand tu n'a que la pspicture dans la figure. Je crois qu'une solution est de faire Conclure dans EcrireFichier, et de créer une liste de pspictures dans les figures.
