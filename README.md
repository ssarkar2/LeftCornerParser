# LeftCornerParser
A simple implementation of left corner parsing. Not very optimised, just repetitively applying the rules of LC parsing. 



The parser is implemented as a class. It needs to be initialized with the sentence, grammar, axiom and goal.
Sentence: a space separated string of words. Eg: “the man laughed”,  “x x c”
Grammar: a list of rules. Rules are 2-tuples. 1st element of tuple is LHS and 2nd element is RHS. For example a S->ASB is expressed by (['S'], ['A', 'S', 'B']). Grammar is a list of such tuples
Axiom: a tuple denoting the stack and the word counter. ([], -1) in this case.
Goal: A list of possible goal states. For example  ([(['S'], ['NP', 'VP', '*'])],2) is a goal. It is a tuple of the stack state and the word counter value. The stack state is a list of entries that is present in the stack now. The entries in the stack are similar to tuples that make up the Grammar (except these tuples also contain ‘*’)
After the initialization the main function of the class is parse(). This is its basic structure:
while(len(self.chart) > 0):
            if self.checkGoal() == 1:
                return
            self.applyRule()
        print 'failed'

def applyRule(self):
        config = self.chart.pop();
        newconfiglistR1 = self.applyRule1(config);  #print newconfiglistR1
        newconfiglistR2 = self.applyRule2(config);  #print newconfiglistR2
        newconfiglistR3 = self.applyRule3(config);  #print newconfiglistR3
        self.chart = self.chart + newconfiglistR1 + newconfiglistR2 + newconfiglistR3;
We have a ‘chart’ in our chart parser. It is initialized with the axiom. The chart contains all the possible configurations we could reach on correctly applying the rules to previous configurations.
In each loop of the main while loop, we check if the chart contains any configurations that is a valid goal state (using checkGoal()). If not then we call applyRule() function. This function, pops a configuration off the chart and applies the 3 rules (if its possible to apply the rule) and gets new configurations which it pushes back into the chart.
In applyRule() we print the chart variable after each iteration, which shows how rules get applied. It also show dead end configurations, which if present in the chart, will be popped at some time and then when the parser tries to apply either of the rules, it will find that none is applicable. So no new config is added back to the chart. Thus that config is popped off but does not leave behind any children.
Note that in case of failure, after exploring the full state space and on hitting deadends, the chart starts to decrease until it is finally empty. At this stage we declare that the sentence is rejected.
To keep track of the space requirement of the parser, we keep track of the maximum size of the configurations.
Prints from the parser for “the man laughed” is shown below: Each iteration is demarcated by the line of ‘x’s. The printed stuff is the chart, so it’s a list of configurations. The correct proof pathway is shown in bold.
[([(['DT'], ['the', '*'])], 0)]
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 0
[([(['DT'], ['the', '*']), (['N'], ['man', '*'])], 1), ([(['NP'], ['DT', '*', 'N'])], 0)]
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 1
[([(['DT'], ['the', '*']), (['N'], ['man', '*'])], 1), ([(['NP'], ['DT', '*', 'N']), (['N'], ['man', '*'])], 1)]
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 2
[([(['DT'], ['the', '*']), (['N'], ['man', '*'])], 1), ([(['NP'], ['DT', '*', 'N']), (['N'], ['man', '*']), (['VI'], ['laughed', '*'])], 2), ([(['NP'], ['DT', 'N', '*'])], 1)]
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 3
[([(['DT'], ['the', '*']), (['N'], ['man', '*'])], 1), ([(['NP'], ['DT', '*', 'N']), (['N'], ['man', '*']), (['VI'], ['laughed', '*'])], 2), ([(['NP'], ['DT', 'N', '*']), (['VI'], ['laughed', '*'])], 2), ([(['S'], ['NP', '*', 'VP'])], 1)]
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 4
[([(['DT'], ['the', '*']), (['N'], ['man', '*'])], 1), ([(['NP'], ['DT', '*', 'N']), (['N'], ['man', '*']), (['VI'], ['laughed', '*'])], 2), ([(['NP'], ['DT', 'N', '*']), (['VI'], ['laughed', '*'])], 2), ([(['S'], ['NP', '*', 'VP']), (['VI'], ['laughed', '*'])], 2)]
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 5
[([(['DT'], ['the', '*']), (['N'], ['man', '*'])], 1), ([(['NP'], ['DT', '*', 'N']), (['N'], ['man', '*']), (['VI'], ['laughed', '*'])], 2), ([(['NP'], ['DT', 'N', '*']), (['VI'], ['laughed', '*'])], 2), ([(['S'], ['NP', '*', 'VP']), (['VP'], ['VI', '*'])], 2)]
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 6
[([(['DT'], ['the', '*']), (['N'], ['man', '*'])], 1), ([(['NP'], ['DT', '*', 'N']), (['N'], ['man', '*']), (['VI'], ['laughed', '*'])], 2), ([(['NP'], ['DT', 'N', '*']), (['VI'], ['laughed', '*'])], 2), ([(['S'], ['NP', 'VP', '*'])], 2)]
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 7
space 3
accepted 

