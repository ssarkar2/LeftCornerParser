#implements the rules from this site:
#http://www.umiacs.umd.edu/~resnik/ling723_fa2006/assignments/4b/lc_parser.pdf
#Note rule 2 (LC predict is wrong. it should be:
#A->beta* is TOS and X->A gamma is in the grammar (not X->A beta)

class chartParser():
    def __init__(self, axiom, goal, grammar, sentence):
        self.axiom = axiom; self.goal = goal; self.grammar = grammar; self.sentence = sentence.split();
        self.chart = [axiom]; self.c = 0;
        self.space = -1;

    def parse(self):
        while(len(self.chart) > 0):
            if self.checkGoal() == 1:
                print 'space', self.space
                print 'accepted'
                return

            self.applyRule()
        print 'failed'


    def applyRule(self):
        config = self.chart.pop();
        newconfiglistR1 = self.applyRule1(config);  #print newconfiglistR1
        newconfiglistR2 = self.applyRule2(config);  #print newconfiglistR2
        newconfiglistR3 = self.applyRule3(config);  #print newconfiglistR3
        self.chart = self.chart + newconfiglistR1 + newconfiglistR2 + newconfiglistR3;
        print self.chart
        print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', self.c; self.c += 1;

    def applyRule3(self, config): #complete
        stack = config[0]; wordidx = config[1];
        newconfiglist = []
        if len(stack) > 1:
            if self.checkIfCompleteOnTOS(stack) == 1:
                first = stack[-1]; second = stack[-2]; #the top 2 rules in the stack
                if self.checkSecond(first, second) == True:
                    Z = first[0][0]; beta = first[1:-1]
                    X = second[0][0];
                    dotLocation = second[1].index('*')
                    alpha = second[1][0:dotLocation]
                    gamma = second[1][dotLocation+2:]
                    x = stack[0:len(stack)-2]  #the last element of the list is the ead of the stack. chopping off 2 elements to create x
                    x += [([X], alpha + [Z, '*']+ gamma)]
                    newconfiglist += [(x, wordidx)]
        return newconfiglist

    def checkSecond(self, first, second):
        if second[1].index('*') < len(second[1])-1:
            return first[0][0] == second[1][second[1].index('*') + 1]  #check if LHS of first and first element after dot in RHS of second are same
        else:
            return False;  #for rules of this type: ['VI'], ['laughed', '*'])] : which do not have any symbol after *

    def applyRule2(self, config): #LC predict
        stack = config[0]; wordidx = config[1];
        newconfiglist = []
        if len(stack) > 0:
            if self.checkIfCompleteOnTOS(stack) == 1:
                rulelist = self.checkForLeftCornerRule(stack[-1][0][0])
                for r in rulelist:
                    x = stack[0:len(stack)-1]  #the last element of the list is the ead of the stack. chopping off TOS to create x
                    x += [(r[0], [r[1][0], '*'] + r[1][1:])]
                    newconfiglist += [(x, wordidx)]
        return newconfiglist

    def checkForLeftCornerRule(self, symbol):  #see if is part of any rules in the grammar where it is left corner
        rulelist = []
        for i in self.grammar:
            if symbol == i[1][0]: #left corner
                rulelist += [i]
        return rulelist


    def checkIfCompleteOnTOS(self, stack):
        return stack[-1][1][-1] == '*' #last element of top of stack's RHS is '*', that is TOS is a completed rule

    def applyRule1(self, config): #shift rule #config is a tuple, (stack and wordidx)
        #apply rule1 to config
        wordidx = config[1]; stack = config[0];
        newconfiglist = []
        if wordidx < len(self.sentence)-1:
            nextword = self.sentence[wordidx + 1]
            rulelist = self.findRule(nextword)  #rulelist is a list of RHS of grammar rules that satisfy A->word
            for r in rulelist:
                newconfiglist = newconfiglist + [(stack + [([r], [nextword, '*'])], wordidx+1)]
        return newconfiglist


    def findRule(self, word):  #find a rule in the grammar that says A -> word
        rulelist = []
        for i in self.grammar:
            if len(i[1]) == 1:
                if i[1][0] == word:
                    rulelist += i[0]
        return rulelist

    def checkGoal(self):
        for ch in self.chart:
            self.space = max(self.space, len(ch[0]))
            if ch in self.goal:
                return 1
        return 0



sentence = 'the man laughed'

grammar = [(['S'], ['NP', 'VP']), (['NP'], ['DT', 'N']), (['DT'], ['the']), (['N'], ['man']), (['N'], ['woman']), (['VP'], ['VI']), (['VI'], ['laughed']), (['VI'], ['sang'])]
axiom = ([], -1)  #since python is 0 indexed, we start with -1
goal = [ ([(['S'], ['NP', 'VP', '*'])],2) ]

ch = chartParser(axiom, goal, grammar, sentence)
ch.parse()

print; print; print;

###left and right recursion
sentence = 'x c'; e = len(sentence.split())-1
grammar = [(['S'], ['A', 'S', 'B']), (['S'], ['C']), (['S'], ['X', 'S']), (['S'], ['S', 'Y']), (['A'], ['a']), (['B'], ['b']), (['C'], ['c']), (['X'], ['x']), (['Y'], ['y'])]
axiom = ([], -1)
goal = [([(['S'], ['A', 'S', 'B', '*'])],e), ([(['S'], ['C', '*'])],e), ([(['S'], ['X', 'S', '*'])],e),  ([(['S'], ['S', 'Y', '*'])],e)]
ch = chartParser(axiom, goal, grammar, sentence)
ch.parse()

sentence = 'x x x x c'; e = len(sentence.split())-1;
goal = [([(['S'], ['A', 'S', 'B', '*'])],e), ([(['S'], ['C', '*'])],e), ([(['S'], ['X', 'S', '*'])],e),  ([(['S'], ['S', 'Y', '*'])],e)]
ch = chartParser(axiom, goal, grammar, sentence); ch.parse()

sentence = 'x x'; e = len(sentence.split())-1;
goal = [([(['S'], ['A', 'S', 'B', '*'])],e), ([(['S'], ['C', '*'])],e), ([(['S'], ['X', 'S', '*'])],e),  ([(['S'], ['S', 'Y', '*'])],e)]
ch = chartParser(axiom, goal, grammar, sentence); ch.parse()

sentence = 'c y y'; e = len(sentence.split())-1;
goal = [([(['S'], ['A', 'S', 'B', '*'])],e), ([(['S'], ['C', '*'])],e), ([(['S'], ['X', 'S', '*'])],e),  ([(['S'], ['S', 'Y', '*'])],e)]
ch = chartParser(axiom, goal, grammar, sentence); ch.parse()

sentence = 'c y y y y y y'; e = len(sentence.split())-1;
goal = [([(['S'], ['A', 'S', 'B', '*'])],e), ([(['S'], ['C', '*'])],e), ([(['S'], ['X', 'S', '*'])],e),  ([(['S'], ['S', 'Y', '*'])],e)]
ch = chartParser(axiom, goal, grammar, sentence); ch.parse()

####centre recursion
sentence = 'a a c b b'; e = len(sentence.split())-1;
goal = [([(['S'], ['A', 'S', 'B', '*'])],e), ([(['S'], ['C', '*'])],e), ([(['S'], ['X', 'S', '*'])],e),  ([(['S'], ['S', 'Y', '*'])],e)]
ch = chartParser(axiom, goal, grammar, sentence); ch.parse()

sentence = 'a a a a a a c b b b b b b'; e = len(sentence.split())-1;
goal = [([(['S'], ['A', 'S', 'B', '*'])],e), ([(['S'], ['C', '*'])],e), ([(['S'], ['X', 'S', '*'])],e),  ([(['S'], ['S', 'Y', '*'])],e)]
ch = chartParser(axiom, goal, grammar, sentence); ch.parse()
