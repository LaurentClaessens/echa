Les sources du document sont à télécharger sur gitorious
Ne pas oublier le fichier de style exocorr.sty

COMPILATION FACILE

Du fait de l'utilisation de pstricks, ce document ne peut pas être compilé avec pdflatex. Il faut passer par la chaine

latex echa.tex (jusqu'à ce que les références soient correctes)
dvips echa.dvi
ps2pdf echa.ps

COMPILATION DES FIGURES

Pour régénérer les fichiers *.pstricks, lisez la doc de phystricks.

