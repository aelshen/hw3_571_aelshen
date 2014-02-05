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
from copy import deepcopy
from math import log

#==============================================================================
#--------------------------------Constants-------------------------------------
#==============================================================================
DEBUG = True
MIN_FREQ = 1
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
##-------------------------------------------------------------------------
## Class PCFG
##-------------------------------------------------------------------------
##    Description:    A class that builds a probabilistic context free 
##                    grammar from a parsed training file. 
##
##    Arguments:      file; a parsed text to be used for training
##
##
##    Properties:     start_symbol; the start symbol for the grammar
##                    LHS_count; a count of the times LHS parent is found
##                               in the grammar
##                    pcfg; a double hash of all rules found in the grammar
##                          (A -> B C or A -> a), and the number of times
##                          that rule was found
##                    terminal_rules_by_daughter; an inverted dictionary
##                          so that terminals are associated with the POS
##                          that creates them (a -> A)
##                    nonterminal_rules_by_daughter; an inverted double hash
##                          to find the parent of a rule by the left child
##                          of the production (B -> B C -> A 
##                    vocabulary; a dict of all words and their frequencies
##
##    Calls:          PCFG.ExtractTerminals()
##                    PCFG.ExtractNonterminals()
##                    PCFG.CalculateProbabilities()
##
##-------------------------------------------------------------------------
class PCFG:
    ##-------------------------------------------------------------------------
    ## __init__
    ##-------------------------------------------------------------------------
    ##    Description:    on init, initialize properties and induce a grammar
    ##
    ##    Arguments:      file; a parsed text to be used for training
    ##
    ##    Calls:          PCFG.CreateGrammar()
    ##                    PCFG.PrintGrammar()
    ##-------------------------------------------------------------------------
    def __init__(self, file):
        self.start_symbol = None
        self.LHS_count = defaultdict(int)
        self.pcfg = defaultdict(lambda: defaultdict(float))
        self.terminal_rules_by_daughter = defaultdict(set)
        self.nonterminal_rules_by_daughter = defaultdict(lambda: defaultdict(set))
        self.vocabulary = defaultdict(int)
        
        self.CreateGrammar(file)
        self.OrderRulesByChildren()
        self.PrintGrammar()
    
    
    ##-------------------------------------------------------------------------
    ## PCFG.Smooth()
    ##-------------------------------------------------------------------------
    ##    Description:    Add smoothing to the grammar to account for any 
    ##                    unknown words that might appear.
    ##-------------------------------------------------------------------------
    def Smooth(self):
        new_pcfg = deepcopy(self.pcfg)
        unk_words = []
        new_vocab = deepcopy(self.vocabulary)
        for word in self.vocabulary:
            #if count of the word is less than the MIN_FREQ (in -Constants-)
            #add word to list of unknowns
            if self.vocabulary[word] <= MIN_FREQ:
                unk_words.append(tuple([word]))
        
#         for LHS in self.pcfg:
#             for RHS in self.pcfg[LHS]:
#                 if len(RHS) == 1 and self.pcfg[LHS][RHS] <= MIN_FREQ:
#                     del new_pcfg[LHS][RHS]
#                     new_pcfg[LHS][tuple(["'UNK'"])] += 1
#                     new_vocab[RHS[0]] -= 1
        
        #run through all rules, removing all rules that produce an unk_word
        #and replacing with a new production called UNK while removing
        #the unknown word from the vocabulary
        for LHS in self.pcfg:
            for RHS in self.pcfg[LHS]:
                if RHS in unk_words:
                    del new_pcfg[LHS][RHS]
                    new_pcfg[LHS][tuple(["'UNK'"])] += self.pcfg[LHS][RHS]
                    new_vocab[RHS] -= 1
         
        #recreate pcfg and vocabulary to now no longer include any
        #unk_words.
        new_vocab = {k: v for k, v in new_vocab.items() if v}
        self.pcfg = new_pcfg
        self.vocabulary = new_vocab
    
    ##-------------------------------------------------------------------------
    ## PCFG.OrderRulesByChildren()
    ##-------------------------------------------------------------------------
    ##    Description:    create an inverse dictionary for terminal rules such that 
    ##                    each terminal production maps to a POS tag, 
    ##                    create an inverse dictionary for nonterminal rules such that
    ##                    the left daughter of the rule maps to a dictionary of tuples of 
    ##                    (left daughter, right daughter), which maps to the parent of the rule
    ##-------------------------------------------------------------------------
    def OrderRulesByChildren(self):
        for LHS in self.pcfg:
            for RHS in self.pcfg[LHS]:
                if len(RHS) == 1:
                    self.terminal_rules_by_daughter[RHS[0]].add(LHS)
                elif len(RHS) == 2:
                    self.nonterminal_rules_by_daughter[RHS[0]][RHS].add(LHS)
    
    ##-------------------------------------------------------------------------
    ## PCFG.PrintGrammar()
    ##-------------------------------------------------------------------------
    ##    Description:    Print all the rules of a grammar, beginning with 
    ##                    all the start-symbol rules, to an output file.
    ##-------------------------------------------------------------------------
    def PrintGrammar(self):
        output_file = open('trained_imp.pcfg','w')
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
    
    ##-------------------------------------------------------------------------
    ## PCFG.CreateGrammar()
    ##-------------------------------------------------------------------------
    ##    Description:    From a given training file, build a pcfg by extracting
    ##                    all rules and calculating all probabilities
    ##
    ##    Arguments:      file; a parsed text to be used for training
    ##
    ##    Calls:          PCFG.ExtractTerminals()
    ##                    PCFG.ExtractNonterminals()
    ##                    PCFG.CalculateProbabilities()
    ##                    PCFG.Smooth()
    ##
    ##-------------------------------------------------------------------------
    def CreateGrammar(self, file):
        for line in open(file, 'r').readlines():
            self.ExtractTerminals(line)
            line = line.replace("(","( ").replace(")"," )").split()
            self.ExtractNonterminals(line)
        
        self.Smooth()
        
        self.CalculateProbabilites()
        
    ##-------------------------------------------------------------------------
    ## PCFG.ExtractNonterminals()
    ##-------------------------------------------------------------------------
    ##    Description:    Read through a parsed training file, and recursively 
    ##                    break each line down into a rule production A -> B C
    ##
    ##    Calls:          PCFG.ExtractNonterminals()
    ##
    ##-------------------------------------------------------------------------
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
        
    ##-------------------------------------------------------------------------
    ## PCFG.ExtractTerminals()
    ##-------------------------------------------------------------------------
    ##    Description:    Use regex to extract all terminal productions
    ##                    (i.e. any patterns matching two strings, seperated by
    ##                    whitespace, in between two parentheses. (x y) )
    ##-------------------------------------------------------------------------
    def ExtractTerminals(self, line):
        m = TERMINAL.findall(line)
        for terminal in m:
            LHS,RHS = terminal
            RHS = tuple(["'" + RHS + "'"])
            self.LHS_count[LHS] += 1
            self.pcfg[LHS][RHS] += 1
            self.vocabulary[RHS[0]] += 1
            
    ##-------------------------------------------------------------------------
    ## PCFG.CalculateProbabilities()
    ##-------------------------------------------------------------------------
    ##    Description:    Calculate the logprob of a rule production
    ##-------------------------------------------------------------------------
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