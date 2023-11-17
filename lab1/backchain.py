from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    rv = simplify( find_matching_rules(rules,hypothesis,OR()) )
    # rv = find_matching_rules(rules,hypothesis,OR())

    print(rv)

    return rv


def find_matching_rules(rules,hypothesis,backchain):

    print("evaluating hypothesis: {}".format(hypothesis) )

    or_rule = OR()
    or_rule.append(hypothesis)
    backchain.append(or_rule)


    # obtain all rules where the consequent matches the hypothesis
    # assumption: every rule has exactly one consequent
    # returns a list of tuples, each tuple contains the antecedent, consequent, and matched bindings
    matching_rules = [(
            rule.antecedent(),
            rule.consequent()[0],
            match(rule.consequent()[0],hypothesis) 
        ) 
        for rule in rules 
        if match(rule.consequent()[0], hypothesis) is not None ]

    # if there are one or more matching rules, then combine them into an OR()
    if( len(matching_rules) > 0 ):

        for matching_rule in matching_rules:

            antecedent = matching_rule[0]
            consequent = matching_rule[1]
            bindings = matching_rule[2]


            if(isinstance(antecedent,str)):

                prior_hypothesis = populate( antecedent, bindings )
                find_matching_rules( rules, prior_hypothesis, or_rule)

            elif(isinstance(antecedent,AND)):

                and_rule = AND()
                or_rule.append(and_rule)
            
                for a in antecedent:

                    prior_hypothesis = populate( a, bindings )
                    find_matching_rules( rules, prior_hypothesis, and_rule)

            elif(isinstance(antecedent,OR)):

                nested_or_rule = OR()
                or_rule.append(nested_or_rule)
            
                for a in antecedent:

                    prior_hypothesis = populate( a, bindings )
                    find_matching_rules( rules, prior_hypothesis, nested_or_rule)

    return backchain
            


# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
