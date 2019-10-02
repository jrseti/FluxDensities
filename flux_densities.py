#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Jon Richards
# 
# Using the method defined in 
#    Perley and Butler, 2016: https://arxiv.org/pdf/1609.05940.pdf
# Calculate the flux densities of vaious sources from 1 to 10GHz
# and produce a graph that is automatically displayed in a browser.

import os
from math import pow
from math import log
import sys
from collections import namedtuple
import webbrowser
  
# log(S) = a0 + a1 log(νG) + a2[log(νG)]2 + a3[log(νG)]3 + · · ·

# Table 5. Fitted Coefficients for the Twenty Sources
# Cleaned up into a nice table, with zeroes inserted
#Source               a0                a1                a2                a3                a4                a5        χ**2   fmin fmax
#J0133-3629,   1.0440 ± 0.0010, -0.6620 ± 0.0020, -0.225  ± 0.006,   0.0000 ± 0.0000,  0.0000 ± 0.0000,  0.0000 ± 0.0000, 267.0, 0.20, 4
#3C48,         1.3253 ± 0.0005, -0.7553 ± 0.0009, -0.1914 ± 0.0011,  0.0498 ± 0.0009,  0.0000 ± 0.0000,  0.0000 ± 0.0000,   3.1, 0.05, 50
#Fornax A,     2.2180 ± 0.0030, -0.6610 ± 0.0060,  0.0000 ± 0.0000,  0.0000 ± 0.0000,  0.0000 ± 0.0000,  0.0000 ± 0.0000,  17.0, 0.20, 0.5
#3C123,        1.8017 ± 0.0007, -0.7884 ± 0.0012, -0.1035 ± 0.0023, -0.0248 ± 0.0013,  0.0090 ± 0.0013,  0.0000 ± 0.0000,   1.9, 0.05, 50
#J0444-2809,   0.9710 ± 0.0011, -0.8940 ± 0.0040, -0.118  ± 0.0100,  0.0000 ± 0.0000,  0.0000 ± 0.0000,  0.0000 ± 0.0000,   3.3, 0.20, 2.0
#3C138,        1.0088 ± 0.0009, -0.4981 ± 0.0022, -0.155  ± 0.0030, -0.0100 ± 0.0700,  0.0220 ± 0.0030,  0.0000 ± 0.0000,   1.5, 0.20, 50
#Pictor A,     1.9380 ± 0.0010, -0.7470 ± 0.0013, -0.074  ± 0.0050,  0.0000 ± 0.0000,  0.0000 ± 0.0000,  0.0000 ± 0.0000,   8.1, 0.20, 4.0
#Taurus A,     2.9516 ± 0.0010, -0.2170 ± 0.0030, -0.047  ± 0.0050, -0.0670 ± 0.0130,  0.0000 ± 0.0000,  0.0000 ± 0.0000,   1.9, 0.05, 4.0
#3C147,        1.4516 ± 0.0010, -0.6961 ± 0.0017, -0.201  ± 0.0050,  0.0640 ± 0.0040, -0.0460 ± 0.0040,  0.0290 ± 0.0030,   2.2, 0.05, 50
#3C196,        1.2872 ± 0.0007, -0.8530 ± 0.0012, -0.153  ± 0.0020, -0.0200 ± 0.0013,  0.0201 ± 0.0013,  0.0000 ± 0.0000,   1.6, 0.05, 50
#Hydra A,      1.7795 ± 0.0009, -0.9176 ± 0.0012, -0.084  ± 0.0040, -0.0139 ± 0.0014,  0.0300 ± 0.0030,  0.0000 ± 0.0000,   3.5, 0.05, 12
#Virgo A,      2.4466 ± 0.0007, -0.8116 ± 0.0020, -0.048  ± 0.0030,  0.0000 ± 0.0000,  0.0000 ± 0.0000,  0.0000 ± 0.0000,   2.0, 0.05, 3
#3C286,        1.2481 ± 0.0005, -0.4507 ± 0.0009, -0.1798 ± 0.0011,  0.0357 ± 0.0009,  0.0000 ± 0.0000,  0.0000 ± 0.0000,   1.9, 0.05, 50
#3C295,        1.4701 ± 0.0007, -0.7658 ± 0.0012, -0.2780 ± 0.0023, -0.0347 ± 0.0013,  0.0399 ± 0.0013,  0.0000 ± 0.0000,   1.6, 0.05, 50
#Hercules A,   1.8298 ± 0.0007, -1.0247 ± 0.0009, -0.0951 ± 0.0020,  0.0000 ± 0.0000,  0.0000 ± 0.0000,  0.0000 ± 0.0000,   2.3, 0.20, 12
#3C353,        1.8627 ± 0.0010, -0.6938 ± 0.0014, -0.100  ± 0.0050, -0.0320 ± 0.0005,  0.0000 ± 0.0000,  0.0000 ± 0.0000,   2.2, 0.20, 4
#3C380,        1.2320 ± 0.0016, -0.7910 ± 0.0040,  0.095  ± 0.0220,  0.0980 ± 0.0220, -0.1800 ± 0.0600, -0.1600 ± 0.0500,   2.9, 0.05, 50
#Cygnus A,     3.3498 ± 0.0010, -1.0022 ± 0.0014, -0.225  ± 0.0060,  0.0230 ± 0.0020,  0.0430 ± 0.0050,  0.0000 ± 0.0000,   1.9, 0.05, 12
#3C444,        1.1064 ± 0.0009, -1.0050 ± 0.0020, -0.075  ± 0.0040, -0.0770 ± 0.0050,  0.0000 ± 0.0000,  0.0000 ± 0.0000,   5.7, 0.20, 12
#Cassiopeia A, 3.3584 ± 0.0010, -0.7518 ± 0.0014, -0.035  ± 0.0050, -0.0710 ± 0.0050,  0.0000 ± 0.0000,  0.0000 ± 0.0000,   2.1, 0.20, 4

coeff_table = [
('J0133-3629',   1.0440, -0.6620, -0.225 ,  0.0000,  0.0000,  0.0000, 267.0, 0.20, 4),
('3C48',         1.3253, -0.7553, -0.1914,  0.0498,  0.0000,  0.0000,   3.1, 0.05, 50),
('Fornax A',     2.2180, -0.6610,  0.0000,  0.0000,  0.0000,  0.0000,  17.0, 0.20, 0.5),
('3C123',        1.8017, -0.7884, -0.1035, -0.0248,  0.0090,  0.0000,   1.9, 0.05, 50),
('J0444-2809',   0.9710, -0.8940, -0.118 ,  0.0000,  0.0000,  0.0000,   3.3, 0.20, 2.0),
('3C138',        1.0088, -0.4981, -0.155 , -0.0100,  0.0220,  0.0000,   1.5, 0.20, 50),
('Pictor A',     1.9380, -0.7470, -0.074 ,  0.0000,  0.0000,  0.0000,   8.1, 0.20, 4.0),
('Taurus A',     2.9516, -0.2170, -0.047 , -0.0670,  0.0000,  0.0000,   1.9, 0.05, 4.0),
('3C147',        1.4516, -0.6961, -0.201 ,  0.0640, -0.0460,  0.0290,   2.2, 0.05, 50),
('3C196',        1.2872, -0.8530, -0.153 , -0.0200,  0.0201,  0.0000,   1.6, 0.05, 50),
('Hydra A',      1.7795, -0.9176, -0.084 , -0.0139,  0.0300,  0.0000,   3.5, 0.05, 12),
('Virgo A',      2.4466, -0.8116, -0.048 ,  0.0000,  0.0000,  0.0000,   2.0, 0.05, 3),
('3C286',        1.2481, -0.4507, -0.1798,  0.0357,  0.0000,  0.0000,   1.9, 0.05, 50),
('3C295',        1.4701, -0.7658, -0.2780, -0.0347,  0.0399,  0.0000,   1.6, 0.05, 50),
('Hercules A',   1.8298, -1.0247, -0.0951,  0.0000,  0.0000,  0.0000,   2.3, 0.20, 12),
('3C353',        1.8627, -0.6938, -0.100 , -0.0320,  0.0000,  0.0000,   2.2, 0.20, 4),
('3C380',        1.2320, -0.7910,  0.095 ,  0.0980, -0.1800, -0.1600,   2.9, 0.05, 50),
('Cygnus A',     3.3498, -1.0022, -0.225 ,  0.0230,  0.0430,  0.0000,   1.9, 0.05, 12),
('3C444',        1.1064, -1.0050, -0.075 , -0.0770,  0.0000,  0.0000,   5.7, 0.20, 12),
('Cassiopeia A', 3.3584, -0.7518, -0.035 , -0.0710,  0.0000,  0.0000,   2.1, 0.20, 4)
]


def get_source_coeffs(source_name):

    """
    Using the name of a source return the associated tuple from the global
    list coeffs_table.
    Return None if source name is not in table.
    """

    global coeff_table

    SourceCoeffs = namedtuple('SourceCoeffs', 'name a0 a1 a2 a3 a4 a5 fit fmin fmax')

    for coeffs in coeff_table:
        if coeffs[0].lower() == source_name.lower():
            return SourceCoeffs(coeffs[0], coeffs[1], coeffs[2], coeffs[3], 
                    coeffs[4], coeffs[5], coeffs[6], coeffs[7], coeffs[8], coeffs[9])

    return None

def get_jy(source, freq_ghz):

    """
    Given a source name and frequency in GHz calculate the 
    flux density in Jy.
    """

    coeffs = get_source_coeffs(source)
    # log(S) = a0 + a1 log(νG) + a2[log(νG)]2 + a3[log(νG)]3 + · · ·
    jy_pre = coeffs.a0 + \
        coeffs.a1 * log(freq_ghz, 10) + \
        coeffs.a2 * pow(log(freq_ghz, 10), 2.0) + \
        coeffs.a3 * pow(log(freq_ghz, 10), 3.0) + \
        coeffs.a4 * pow(log(freq_ghz, 10), 4.0) + \
        coeffs.a5 * pow(log(freq_ghz, 10), 5.0) 

    return pow(10.0, jy_pre)

def frange(start, stop, step):
    """
    Generator that is a version of xrange that allows specifying a step.
    """
    x = start
    while x <= stop:
        yield x
        x += step

def print_sources():
    """
    Print the list of available sources.
    """
    for coeffs in coeff_table:
        print(coeffs[0])

def print_help():

        """
        Print help for the user, then exit.
        """
        print("\n%s syntax:" % sys.argv[0].replace("./", ""))
        print("\t -l|-list will list all the available sources")
        print("\t ")
        exit(0)

def create_html(coeffs):

    """
    Create an html page for displaying the data in a graph.
    """
    data = []
    for f in frange(1,10,0.1):
        d = [float("%.1f"%f), float("%.4f"%(get_jy(source, float(f))))]
        print(d)
        data.append(d)

    f_out = open("index.html", "w")
    with open("template.html") as f:
        for line in f:
            if "$source" in line:
                line = line.replace("$source", coeffs[0])
            if "$data" in line:
                line = line.replace("$data", str(data))
            f_out.write(line.replace("\n", ""))
    f_out.close()


# main execution starts here

if len(sys.argv) == 1:
    print_help()

cmd = sys.argv[1]

if cmd == "-l" or cmd == "-list":
    print_sources()
    sys.exit(0)
else:
    source = sys.argv[1]
    for s in sys.argv[2:]:
        source += " " + s
    print(source)
    coeffs = get_source_coeffs(source)
    if coeffs == None:
        print("Source name not recognized\n")
        sys.exit(1)
    for f in frange(1,10,0.5):
        print ("%0.1f, Jy=%.3f" % (f, get_jy(source, float(f))))

    create_html(coeffs)

    print("file:/%s/index.html"%os.getcwd())
    # Pop up in a web browser!
    webbrowser.open("file://%s/index.html"%os.getcwd(), 1)

    sys.exit(0)


