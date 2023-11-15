import re

# A regular expression for finding variables.
AIRegex = re.compile(r'\(\?(\S+)\)')

def match(template, AIStr):
    """
    Given two strings, 'template': a string containing variables
    of the form '(?x)', and 'AIStr': a string that 'template'
    matches, with certain variable substitutions.

    Returns a dictionary of the set of variables that would need
    to be substituted into template in order to make it equal to
    AIStr, or None if no such set exists.
    """
    try:
        vars = re.match( AIStringToRegex(template), 
                         AIStr ).groupdict()
        print("vars: {}".format(vars))
        return vars
    except AttributeError: # The re.match() expression probably
                           # just returned None
        return None

def AIStringToRegex(AIStr):

    regex = AIRegex.sub( r'(?P<\1>\\S+)', AIStr )+'$'
    print("converting {} to {} regex".format(AIStr,regex))
    return regex

data = 'rock beats paper'
template = '(?x) beats (?y)'

# print( match(template,data) )

# print( re.match(r'\(\?(?P<group1>\S+)\) beats \(\?(?P<group2>\S+)\)', template).groupdict() )

# regex = re.sub(r'\(\?(\S+)\)', r'(?P<\1>\\S+)', template )

# print( re.match(regex, data ).groupdict() )

match( template, data )