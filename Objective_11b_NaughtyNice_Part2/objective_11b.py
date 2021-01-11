from naughty_nice import Chain, Block
from Crypto.Hash import MD5, SHA256


def objective_11b():
    c2 = Chain(load=True, filename='blockchain.dat')

    # The sha256 of the altered block to search for
    altered_block_sha = '58a3b9335a6ceb0234c12d35a0564c4ef0e90152d0eb2ce2082383b38028a90f'
    altered_block = None
    for i in range(len(c2.blocks)):
        block = c2.blocks[i]
        # Calculate the SHA256 hash of the block
        block_hash = SHA256.new(block.block_data_signed()).hexdigest()

        # See if the calculated hash matches the one we're looking for
        if block_hash == altered_block_sha:
            print(f'Found altered block - {block}')
            altered_block = block
            # Save the block to a file so we can analyze it
            c2.save_a_block(i, 'altered_block.dat')
            break

    # Defensive programming. Just make sure no mistakes were made in the search functionality
    if not altered_block:
        print("Altered block not found in the blockchain")
        exit(1)

    # Save all block documents to disk (this will create 129459.bin and 129459.pdf)
    for i in range(len(altered_block.data)):
        altered_block.dump_doc(i)

    # Calculate the MD5 hash of the altered block. Any modifications made to the block, should result in a block
    # with this same hash value.
    md5_block = MD5.new(altered_block.block_data_signed()).hexdigest()

    # Revert Jack Frost's block modifications in 4 bytes:
    # 1. Change the Sign from nice (1) to naughty (0)
    altered_block.sign -= 1
    # 2. Compensate the decrement of the Sign value by incrementing the value of the byte 64 bytes further in the block
    #    This byte is the 54th byte of the first data item in the block (a binary blob)
    #    Retrieve the blob data, modify it and put it back in the altered_block
    bin = list(altered_block.data[0]['data'])
    bin[53] = bin[53] + 1
    altered_block.data[0]['data'] = bytes(bin)

    # In the PDF document, we need to do 2 modifications:
    # 3. Change the 'Pages' value from 2 to 3 (byte 64)
    pdf = list(altered_block.data[1]['data'])
    pdf[63] += 1

    # 4. Compensate for this change by decrementing the value of the byte that is 64 bytes further in
    #    the block (i.e. byte 128).
    #    Retrieve the PDF document data, make both modifications and put it back in the altered block
    pdf[127] -= 1
    altered_block.data[1]['data'] = bytes(pdf)

    # For analysis, also save the modified altered_block to a file
    with open('altered_block_modified.dat', 'wb') as fh:
        fh.write(bytes(altered_block.block_data_signed()))

    # Calculate the MD5 of the modified altered_block
    md5_new = MD5.new(altered_block.block_data_signed()).hexdigest()

    if md5_new == md5_block:
        print('Modifications successful, MD5 hashes match')
        sha256 = SHA256.new(altered_block.block_data_signed()).hexdigest()
        print(f'The SHA256 of the original block is:\n\t{sha256}')
    else:
        print('Back to the drawing board, the MD5 hashes of the blocks do not match')


if __name__ == '__main__':
    objective_11b()
