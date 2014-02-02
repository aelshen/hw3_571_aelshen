'''
#==============================================================================
cky.py
/Users/aelshen/Documents/Dropbox/School/CLMS 2013-2014/Winter 2014/Ling 571-Deep Processing Techniques for NLP/hw2_571_aelshen/src/cky.py
Created on Jan 29, 2014
@author: aelshen
#==============================================================================
'''
import os
import sys
import re
from collections import defaultdict

#==============================================================================
#--------------------------------Constants-------------------------------------
#==============================================================================
DEBUG = True
NONTERMINAL = re.compile(r"\(.*\)")
TERMINAL = re.compile(r"\((\w+)\s+([\w?!.,;:]+)\)")
#==============================================================================
#-----------------------------------Main---------------------------------------
#==============================================================================
def main():
    LHS_count = defaultdict(int)
    cfg = defaultdict(lambda: defaultdict(int))
    x = "(TOP (SQ (SQ' (VBZ Does) (NP (DT this) (NN flight))) (VP (VB serve) (NP_NN dinner))) (PUNC ?))"
    m = TERMINAL.findall(x)
    for terminal in m:
        LHS,RHS = terminal
        LHS_count[LHS] += 1
        cfg[LHS][RHS] += 1
        
    ExtractNonterminals(x)
    
    print("Hello, World!")
#==============================================================================    
#---------------------------------Functions------------------------------------
#==============================================================================
def ExtractNonterminals(line):
    line = line.replace("(","( ").replace(")",") ").split()
    for i in range( len(line) ):
        if line[i] == "(":
            open_paren = 0
            LHS = line[i + 1]
            RHS = []
            for j in range( i+1, len(line) ):
                if line[j] == '(':
                    open_paren += 1
                elif line[j] == ')':
                    open_paren -= 1
                else:
                    continue
                
                if open_paren == 1:
                    RHS.append( line[j+1] )
    x = 1

#==============================================================================    
#----------------------------------Classes-------------------------------------
#==============================================================================
class Classname:
    def __init__(self):
        self.x = 0

#==============================================================================    
#------------------------------------------------------------------------------
#==============================================================================
if __name__ == "__main__":
    sys.exit( main() )