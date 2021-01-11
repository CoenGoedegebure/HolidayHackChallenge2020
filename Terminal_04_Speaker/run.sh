#!/bin/bash

# Execute this script in the ./lab/ folder on the speaker terminal. It will produce a wordlist containing all
# plain text passwords and their encrypted variants

for letter in {{a..z},{A..Z},{0..9}}
do
    rm vending-machines.json                    # Remove the old config file
    plain=$(printf "%-8s")                      # Construct the plain text password by repeating
    string=${plain// /$letter}                  # the letter 8 times
    echo 'processing '$string                   # Output the plain-text password
    (echo 'nobody'
     echo $string
     echo '') | ./vending-machines              # Feed the 'nobody', plaintext, '' in sequence as input to the executable
    cipher=$(sed '3q;d' vending-machines.json)  # Retrieve the 3rd line from the config file containing the encrypted
                                                # password
    echo "$string :$cipher" >> wordlist.txt     # Add the plain text password and 3rd line to the wordlist.txt file
done

echo 'done'