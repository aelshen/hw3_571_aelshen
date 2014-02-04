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
TERMINAL = re.compile(r"\((\w+)\s+([\w?!.,;:]+)\)")
#==============================================================================
#-----------------------------------Main---------------------------------------
#==============================================================================
def main():
    x = "(TOP (SQ (SQ' (VBZ Does) (NP (DT this) (NN flight))) (VP (VB serve) (NP_NN dinner))) (PUNC ?))"
    hw3 = PCFG(sys.argv[1])
    
    print("Hello, World!")
#==============================================================================    
#---------------------------------Functions------------------------------------
#==============================================================================


#==============================================================================    
#----------------------------------Classes-------------------------------------
#==============================================================================
class PCFG:
    def __init__(self, file):
        self.LHS_count = defaultdict(int)
        self.pcfg = defaultdict(lambda: defaultdict(float))
        
        self.CreateGrammar(file)
        x = 1
    
    def CreateGrammar(self, file):
        for line in open(file, 'r').readlines():
            self.ExtractTerminals(line)
            line = line.replace("(","( ").replace(")"," )").split()
            self.ExtractNonterminals(line)
        
        self.CalculateProbabilites()
        
    def ExtractNonterminals(self, line):
        for i in range( len(line) ):
            if line[i] != "(":
                continue
            else:
                open_paren = 0
                LHS = line[i + 1]
                RHS = []
                start_index = []
                end_index = []
                for j in range( i+2, len(line) ):
                    if line[j] == '(':
                        open_paren += 1
                        if open_paren == 1:
                            RHS.append( line[j+1] )
                            start_index.append( j )
                    elif line[j] == ')':
                        open_paren -= 1
                        if open_paren == 0:
                            end_index.append( j )
                    else:
                        continue
                #end j in range( i+2, len(line) ):
            
            if RHS:
                self.LHS_count[LHS] += 1
                self.pcfg[LHS][tuple(RHS)] += 1
                for i in range( len(RHS) ):
                    start = start_index[i]
                    end = end_index[i]
                    self.ExtractNonterminals(line[start:end])
            
            
            break
                    
                    
        #end i in range( len(line) ):
        
        
    def ExtractTerminals(self, line):
        m = TERMINAL.findall(line)
        for terminal in m:
            LHS,RHS = terminal
            RHS = "'" + RHS + "'"
            self.LHS_count[LHS] += 1
            self.pcfg[LHS][RHS] += 1
    
    def CalculateProbabilites(self):
        for LHS in self.pcfg:
            for RHS in self.pcfg[LHS]:
                a = self.pcfg[LHS][RHS]
                b = self.LHS_count[LHS]
                
                self.pcfg[LHS][RHS] = a / b
#==============================================================================    
#------------------------------------------------------------------------------
#==============================================================================
if __name__ == "__main__":
    sys.exit( main() )