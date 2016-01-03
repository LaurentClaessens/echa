#! /usr/bin/python
# -*- coding: utf8 -*-

import LaTeXparser
import LaTeXparser.PytexTools

myRequest = LaTeXparser.PytexTools.Request("seconde")
myRequest.original_filename="echa.tex"

myRequest.ok_filenames_list=["e_smath"]
myRequest.ok_filenames_list.append("e_echa")
myRequest.ok_filenames_list.append("fonctions")
myRequest.ok_filenames_list.append("derivation")
