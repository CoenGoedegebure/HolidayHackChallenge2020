####################################################
# Script to solve the Speaker UNPrep Terminal challenge
#
####################################################
from collections import namedtuple
lookup = namedtuple('lookup', 'plain cipher')

password = 'LVEdQPpBwr'         # The password we want to decrypt
block_size = 8

# Read the wordlist-file generated by run.sh and store the plain-text and cipher-text in the lookup table
# The writing function in run.sh was lazy, no pre-parsing. This means the read-function needs to do a bit
# more effort to extract the data.
# Format of the wordlist.txt is:
#   <plain-text> :  "password": "<cipher-text>"
dict = {}
with open('wordlist.txt', 'r') as in_file:
    for line in in_file.readlines():
        seg = line.split(':')
        plain = seg[0].strip()
        cipher = seg[2].strip().replace('"', '')
        dict[plain] = cipher

# Construct the lookup tables. For this we'll be using a plain_lookup string containing all plain-text characters.
# From the wordlist, we know the encrypted variants of each of these plain-text characters on each position in the
# block. Since the block-size is 8, the cipher_lookup table is a list of 8 strings containing the encrypted characters
# on each position in the block. The position of a character in the cipher-string corresponds to its plain-text variant
# on that same position in the plain_lookup string; essentially creating a grid.
#
# For example, consider the plain_lookup string below and the cipher_lookup strings for the plain-text character 'd'.
# Note that other characters have been left out for easy visibility:
#
# plain_lookup          abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
# cipher_lookup 1       ...L..........
# cipher_lookup 2       ...q..........
# cipher_lookup |
# cipher_lookup 8       ...v..........
#
# The character 'd' on position 1 in the block, occurs as the character 'L', on position 2 it is the letter 'q'. During
# decryption, when the password has a letter 'q' on position 2, we know the plain-text is the character 'd' by doing
# a reverse lookup.

# Initialize the lookup table
plain_lookup = ''
cipher_lookup = []
for i in range(block_size):
    cipher_lookup.append('')

print(f'Filling the lookup tables from the wordlist')

# Fill the cipher lookup table by reading the wordlist contents
for item in dict.items():
    print(f'Plaintext: {item[0]} - Cipher: {item[1]}')
    plain_lookup += item[0][i]

    for i in range(0, block_size):
        cipher_lookup[i] += item[1][i]

print(f'\nDecrypting "{password}" using the lookup table')

# Decrypt the password by doing a reverse lookup, character by character
decrypted_password = ''
for i in range(len(password)):
    lookup_table = cipher_lookup[i % block_size]
    found_location = lookup_table.find(password[i])
    if found_location == -1:
        # This should not happen with a correctly filled cipher_lookup table
        print(f'{password[i]} on position {i} MISSING')
        decrypted_password += '_'
    else:
        print(f'{password[i]} on position {i} decrypts to {plain_lookup[found_location]}')
        decrypted_password += plain_lookup[found_location]

print(f'Password "{password}" decrypts to "{decrypted_password}"')