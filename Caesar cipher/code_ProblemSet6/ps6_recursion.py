# 6.00x Problem Set 6
#
# Part 2 - RECURSION

#
# Problem 3: Recursive String Reversal
#
def reverseString(aStr):
    """
    Given a string, recursively returns a reversed copy of the string.
    For example, if the string is 'abc', the function returns 'cba'.
    The only string operations you are allowed to use are indexing,
    slicing, and concatenation.

    aStr: a string
    returns: a reversed string
    """
    ### TODO.
    if (len(aStr) == 0) or (len(aStr) == 1):
        return aStr
    else:
        return aStr[-1] + reverseString(aStr[ :-1])

print reverseString('abc')
print reverseString('a')
print reverseString('palindrome')
print "================================="

#
# Problem 4: X-ian
#
def x_ian(x, word):
    """
    Given a string x, returns True if all the letters in x are
    contained in word in the same order as they appear in x.

    >>> x_ian('eric', 'meritocracy')
    True
    >>> x_ian('eric', 'cerium')
    False
    >>> x_ian('john', 'mahjong')
    False

    x: a string
    word: a string
    returns: True if word is x_ian, False otherwise
    """
    ###TODO.
    if len(x) == 1 or len(x) == 0:
        return x in word
    elif x[0] in word:
        index = word.find(x[0])
        return x_ian(x[1: ], word[index+1: ])
    else:
        return False

print x_ian('eric', 'meritocracy')
print x_ian('eric', 'cerium')
print x_ian('john', 'mahjong')
print "================================="

#
# Problem 5: Typewriter
#
def insertNewlines(text, lineLength):
    """
    Given text and a desired line length, wrap the text as a typewriter would.
    Insert a newline character ("\n") after each word that reaches or exceeds
    the desired line length.

    text: a string containing the text to wrap.
    line_length: the number of characters to include on a line before wrapping
        the next word.
    returns: a string, with newline characters inserted appropriately.
    """
    ### TODO.
    if len(text) < lineLength:
        return ""
    elif len(text) == lineLength:
        return text + "\n"
    else:
        text_list = text.split()
        line = ""
        current_line_length = 0
        word_index = 0
        for word in text_list:
            if current_line_length < lineLength:
                line += word + ' '
                current_line_length += len(word) + 1
                word_index += 1
        remaining_text = ' '.join(text_list[word_index:])
        return line + "\n" + insertNewlines(remaining_text, lineLength)

print insertNewlines("What the hell is going on here, man? Let's move this along", 10)
print insertNewlines("What the hell is going on here, man? Let's move this along", 15)
