'''
#==============================================================================
cky.py
/Users/aelshen/Documents/Dropbox/School/CLMS 2013-2014/Winter 2014/Ling 571-Deep Processing Techniques for NLP/hw2_571_aelshen/src/cky.py
Created on Jan 29, 2014
@author: Ahmad Elshenawy
#==============================================================================
'''
from __future__ import print_function
import os
import sys
from time import time
from learn_PCFG import PCFG
from math import log
from collections import defaultdict

#==============================================================================
#--------------------------------Constants-------------------------------------
#==============================================================================
DEBUG = True

#==============================================================================
#-----------------------------------Main---------------------------------------
#==============================================================================
def main():
    if len(sys.argv) < 3:
        print("cky.py requires two arguments:"\
               + os.linesep + "\t(1)training parse file"\
               + os.linesep + "\t(2)input data file")
        sys.exit()
        
    grammar_file = sys.argv[1]
    sentences = open(sys.argv[2],'r')
    
    #pcfg is extracted
    grammar = PCFG(grammar_file)
    
    PCKY(sentences, grammar)
    
#==============================================================================    
#---------------------------------Functions------------------------------------
#==============================================================================
##-------------------------------------------------------------------------
## PCKY()
##-------------------------------------------------------------------------
##    Description:    Use the PCKY algorithm to parse text 
##
##    Arguments:      data; test data to be parsed
##                    grammar; pcfg grammar that has already been created
##
##    Calls:          ParsePrint()
##-------------------------------------------------------------------------
def PCKY(data, grammar):
    runtime = time()
    lines_parsed = 0
    total_parses = 0
    #read each line of the input data
    for line in data:
        lines_parsed += 1
    
        sentence = line.strip().split()
                
        #the (n+1)x(n+1) table needed for the cky algorithm
        table = [[(None, 0.0) for x in xrange(len(sentence) + 1)] for x in xrange(len(sentence) + 1)]
        back_trace = defaultdict(set)
        
        for j in xrange( 1, len(sentence) + 1 ):
            word = "'" + sentence[j - 1] + "'"
            #list of tuples
            labels = []
            #get every preterminal that produces the current word
            for LHS in grammar.terminal_rules_by_daughter[word]:
                terminal_logprob = grammar.pcfg[LHS][tuple([word])]
                parent = Node(LHS, [word], terminal_logprob)
                labels.append(parent)
                back_trace[(j-1,j)].add( parent )
            #end LHS in grammar.terminal_rules_by_daughter[word]:
            table[j-1][j] = labels

            
            for i in range(j-2,-1,-1):
                k = i + 1
                LHS = []
                while k <= j - 1:
                    B = table[i][k]
                    C = table[k][j]
                    
                    
                    for left_child in B:
                        for right_child in C:
                            if left_child.label in grammar.nonterminal_rules_by_daughter:
                                RHS = (left_child.label, right_child.label)
                                #if a rule exists that produces this (left,right) pair
                                if RHS in grammar.nonterminal_rules_by_daughter[left_child.label]: 
                                    for label in grammar.nonterminal_rules_by_daughter[left_child.label][RHS]:
                                        #calculate the probability of this current production 
                                        #i.e. P(A->B C) * P(B) * P(C)  (logprob is used to prevent underflow)
                                        logprob = grammar.pcfg[label][tuple(RHS)] + left_child.logprob + right_child.logprob
                                        #create an object to keep track of the parent, 
                                        #and the left and right children that led to it
                                        parent = Node(label, [left_child, right_child], logprob)
                                        #save to a list of all possible parents for this j
                                        LHS.append(parent)
                                        #add this parent object to the backtrace, 
                                        #using the start and stop (i.e. (i,j) ) tuple as a key
                                        #to keep track of the length of the span
                                        back_trace[(i,j)].add( parent )
                    k += 1
                #while k <= j - 1:
                table[i][j] = LHS
                
            #for i in range(j-2,-1,-1):
            
            
        #end for j in range( 1,len(sentence) ):
        
        maximum = (float("-inf"), None)
        
        full_spans = list( back_trace[(0, len(sentence) )] )
        
        for i in range( len(full_spans) ):
            #for any such span that begins with the start symbol of the grammar
            if full_spans[i].label == grammar.start_symbol:
                #find the parse with the greatest probability
                if full_spans[i].logprob > maximum[0]:
                    maximum = (full_spans[i].logprob, i)

        #if no parse was found, output a blank line, 
        #else print the parse with the grates probability
        if maximum[1] == None:
            print(" ", end='')
        else:
            ParsePrint(full_spans[maximum[1]])
        print("")
        
    #end for line in data:

    runtime = time() - runtime
    print("Runtime (s): " + str(runtime))
     

##-------------------------------------------------------------------------
## ParsePrint()
##-------------------------------------------------------------------------
##    Description:    Print a simlple bracket-structure for a backtrace.
##
##    Calls:          ParsePrint()
##-------------------------------------------------------------------------
def ParsePrint(trace):
    if len(trace.children) == 1:
        print("(" + trace.label + " " + trace.children[0][1:-1] + ")", end='')
        return
    else:
        print("(" + trace.label + " ", end='')
        ParsePrint(trace.children[0])
        ParsePrint(trace.children[1])
        print(")", end='')
    
    
#==============================================================================    
#----------------------------------Classes-------------------------------------
#==============================================================================
##-------------------------------------------------------------------------
## Struct Node
##-------------------------------------------------------------------------
##    Description:    A struct used in CKY() to contain all rule information
##
##    Arguments:      file; a parsed text to be used for training
##
##
##    Properties:     label; the LHS label of a rule (the 'A' of A -> B C)
##                    children; a list of the left and right children of 
##                          the rule (the 'B' and 'C' of A -> B C)
##                    logprob; the logprob of the rule
##
##-------------------------------------------------------------------------
class Node:
    def __init__(self, label, children = [], logprob = float("-inf") ):
        self.label = label
        self.children = children
        self.logprob = logprob
#==============================================================================    
#------------------------------------------------------------------------------
#==============================================================================
if __name__ == "__main__":
    sys.exit( main() )