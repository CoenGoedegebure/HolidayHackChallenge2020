#############################################
# Script for the Snowball Terminal Player name prediction
#############################################


# Borrowed from https://github.com/tliston/mt19937
# this is simply a python implementation of a standard Mersenne Twister PRNG.
# the parameters used, implement the MT19937 variant of the PRNG, based on the
# Mersenne prime 2^19937−1
# see https://en.wikipedia.org/wiki/Mersenne_Twister for a very good explanation
# of the math behind this...
class mt19937():
    u, d = 11, 0xFFFFFFFF
    s, b = 7, 0x9D2C5680
    t, c = 15, 0xEFC60000
    l = 18
    n = 624

    def my_int32(self, x):
        return (x & 0xFFFFFFFF)

    def __init__(self, seed):
        w = 32
        r = 31
        f = 1812433253
        self.m = 397
        self.a = 0x9908B0DF
        self.MT = [0] * self.n
        self.index = self.n + 1
        self.lower_mask = (1 << r) - 1
        self.upper_mask = self.my_int32(~self.lower_mask)
        self.MT[0] = self.my_int32(seed)
        for i in range(1, self.n):
            self.MT[i] = self.my_int32((f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (w - 2))) + i))

    def extract_number(self):
        if self.index >= self.n:
            self.twist()
            self.index = 0
        y = self.MT[self.index]
        # this implements the so-called "tempering matrix"
        # this, functionally, should alter the output to
        # provide a better, higher-dimensional distribution
        # of the most significant bits in the numbers extracted
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        self.index += 1
        return self.my_int32(y)

    def twist(self):
        for i in range(0, self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1
            if (x % 2) != 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA

# so... guess what! while it isn't necessarily obvious, the
# functioning of the tempering matrix are mathematically
# reversible. this function impliments that...
#
# by using this, we can take the output of the MT PRNG, and turn
# it back into the actual values held within the MT[] array itself
# and therefore, we can "clone" the state of the PRNG from "n"
# generated random numbers...
#
# initially, figuring out the math to do this made my brain hurt.
# simplifying it caused even more pain.
# please don't ask me to explain it...
def untemper(y):
    y ^= y >> mt19937.l
    y ^= y << mt19937.t & mt19937.c
    for i in range(7):
        y ^= y << mt19937.s & mt19937.b
    for i in range(3):
        y ^= y >> mt19937.u & mt19937.d
    return y


# Read and parse the first 624 seeds (player names) from the playernames.txt file
# This file is made by copy-pasting the seeds found in the source code of the impossible difficulty of
# the snowball fight game.
# Returns
def parse_playernames():
    with open('playernames.txt', 'r') as in_file:
        lines = [int(x.split('-')[0].strip()) for x in in_file.readlines()]
        return lines


def run():
    # Parse the player names obtained from the source-code of the impossible difficulty game
    names = parse_playernames()

    # Initialize the MT-19937 PRNG
    my_prng = mt19937(0)

    # Untemper all 624 player names before the one currently generated
    for i in range(mt19937.n):
        my_prng.MT[i] = untemper(names[i])
        print(f'Untempered player name "{names[i]}"')

    # The current player name is the one that can be predicted next
    print(f'Current player name is "{my_prng.extract_number()}"')


run()
