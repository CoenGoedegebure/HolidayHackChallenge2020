from naughty_nice import Chain


# Just a method to get some information out of the blockchain
def objective_11a_investigation():
    # Load the blockchain data
    c2 = Chain(load=True, filename='blockchain.dat')

    first_block = c2.blocks[0]
    last_block = c2.blocks[len(c2.blocks) - 1]
    print(f'{"#"*80}\nFirst Block:\n{first_block}')
    print(f'{"#"*80}\nLast Block:\n{last_block}')
    print(f'{"#"*80}\nNumber of Blocks in Chain: {len(c2.blocks)}')
    print(f'Index of last Block in Chain: {c2.index}')


objective_11a_investigation()
