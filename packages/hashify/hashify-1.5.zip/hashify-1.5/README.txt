NAME: 
hashify

AUTHOR:
Daniel Rayn

EMAIL:
danierayn@gmail.com

SUMMARY:
hashify generates 'superhashes' which though similar are actually more powerful than normal sha224 hashes. It generates 
hashes that will be more resistant to brute-forcing thereby adding another layer of security if stored password hashes are
stolen or compromised. With this script, hashes would be twice as secure and bruteforcing hashes will be twice as hard.
It's a work in progress and is by no means perfect, including the concept but it is very stable. Contact me for thoughts,
suggestions, advice, help, etcetera.

USAGE:
	>>> import hashify
	>>> hashify.hash('python')
	'a6c54deb8078594cb1ac83a09855e821dbb78f90429228e236434c15'

HOW IT WORKS:
The program takes the input string and uses the length along with two arbitrary integers which can & should be changed to 
improve the effectiveness, strength and security of the hash to generate translations or mappings(dictionaries) for each 
character in the english character set and then translates the orginal string with the dictionaries, hashes the translations 
(as opposed to directly hashing the string) and then returns the hash as output. I decided to use sha224 because it's 
powerful, secure and fast. Look into the file 'superhash'.py for a proof of concept or email me for any questions.

VERSION: 
1.5

DATE: 12/4/2016

TIME: 1:50AM EET

Written with Python 3.4.3 for Python 3 (Should work for Python 2 though) I haven't tested this on Python 2 but I'm confident
it will work.

