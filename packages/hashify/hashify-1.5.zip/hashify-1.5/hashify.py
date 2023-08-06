""" This module generates 'superhashes' resistant to bruteforcing
by adding an extra layer of security. It protects stolen hashes from
being brute-forced to reveal the original strings. It's purpose is to
make it incredibly hard to brute-force hashes."""

import hashlib
import codecs
import string

def hash(input_string):
    """Generates translation & returns one-way superhash from input and sha224 algorithm."""

    # Checks if input_string is actually a string
    if type(input_string) != str:
        return 'Error: Function only accepts strings'
            
    ALPHABETS = list(string.ascii_letters)      # Create list containing all letters
    ALPHABETS.append(' ')                       # Add [space] character to the list to handle spaces
    NUMBERS = list(string.digits)               # Create list containing all NUMBERS
    PUNCTUATIONS = list(string.punctuation)     # Create list containing all punctuation characters

    start_num = len(input_string) * 10          # Start number [It is strongly advised to change this]
    step = len(input_string) * 20               # Increment value [It is strongly advised to change this]

    num = start_num                             # For mapping purposes (In order not to over-ride 'start_num')
    translator = {}                             # Dictionary to hold translations

    # Go into loop to generate translation dictionary
    for letter in ALPHABETS:
        translator[letter] = '{}'.format(num)
        num = num + step
    for number in NUMBERS:
        translator[number] = '{}'.format(num)
        num = num + step
    for punctuation in PUNCTUATIONS:
        translator[punctuation] = '{}'.format(num)
        num = num + step

    # Go into loop to translate every character in the password
    result = []
    for char in list(input_string):
        code = translator.get(char)
        if code:
            result.append(code + ' ')
        else:
            pass

    # Join list containing results into a string
    result = ''.join(result)

    # Hash and return result
    hash_result = hashlib.sha224(codecs.encode(result)).hexdigest()
    
    return hash_result

if __name__ == '__main__':
    hash_result = hash(input("Input string: "))
    print(hash_result)
    input("Enter [Return] to close this window.")
