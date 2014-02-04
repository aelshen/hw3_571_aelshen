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
from math import log

#==============================================================================
#--------------------------------Constants-------------------------------------
#==============================================================================
DEBUG = True
TERMINAL = re.compile(r"\((\w+)\s+([\w?!.,;':]+)\)")
#==============================================================================
#-----------------------------------Main---------------------------------------
#==============================================================================
def main():
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
        self.start_symbol = None
        self.LHS_count = defaultdict(int)
        self.pcfg = defaultdict(lambda: defaultdict(float))
        self.terminal_rules_by_daughter = defaultdict(set)
        self.nonterminal_rules_by_daughter = defaultdict(lambda: defaultdict(set))
        self.CreateGrammar(file)
        
        
        self.OrderRulesByChildren()
        
        
        
        self.PrintGrammar()
        x = 1
    
    
    def OrderRulesByChildren(self):
        #create an inverse dictionary for terminal rules such that 
        #each terminal production maps to a POS tag, 
        #create an inverse dictionary for nonterminal rules such that
        #the left daughter of the rule maps to a dictionary of tuples of 
        #(left daughter, right daughter), which maps to the parent of the rule
        for LHS in self.pcfg:
            for RHS in self.pcfg[LHS]:
                if len(RHS) == 1:
                    self.terminal_rules_by_daughter[RHS[0]].add(LHS)
                elif len(RHS) == 2:
                    self.nonterminal_rules_by_daughter[RHS[0]][RHS].add(LHS)
    
    def PrintGrammar(self):
        output_file = open('trained.pcfg','w')
        for RHS in self.pcfg[self.start_symbol]:
            prob = self.pcfg[self.start_symbol][RHS]
            output_file.write(self.start_symbol + " -> " + " ".join(RHS) + "\t[" + str(prob) + "]" + os.linesep)
        output_file.write(os.linesep)
        for LHS in self.pcfg:
            if LHS == self.start_symbol:
                continue
            for RHS in self.pcfg[LHS]:
                prob = self.pcfg[LHS][RHS]
                output_file.write(LHS + " -> " + " ".join(RHS) + "\t[" + str(prob) + "]" + os.linesep)
                
            output_file.write(os.linesep)
    
    
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
                if self.start_symbol == None:
                    self.start_symbol = line[i + 1]
                    
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
            RHS = tuple(["'" + RHS + "'"])
            self.LHS_count[LHS] += 1
            self.pcfg[LHS][RHS] += 1
    
    def CalculateProbabilites(self):
        for LHS in self.pcfg:
            for RHS in self.pcfg[LHS]:
                a = self.pcfg[LHS][RHS]
                b = self.LHS_count[LHS]
                
                self.pcfg[LHS][RHS] = log( a / b )
#==============================================================================    
#------------------------------------------------------------------------------
#==============================================================================
if __name__ == "__main__":
    sys.exit( main() )