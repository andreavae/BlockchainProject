# blockchain.py

import time
from typing import List

from models import Block, Transaction


class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Create the first block with no real transactions.
        """
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0"
        )
        self.chain.append(genesis_block)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, transactions: List[Transaction]) -> Block:
        """
        Add a new block with the given transactions.
        No real consensus or PoW; just link and hash.
        """
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=transactions,
            previous_hash=self.last_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        """
        Verify that all blocks are correctly linked and not tampered.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Recompute hash and compare
            if current.hash != current.compute_hash():
                print(f"Invalid hash at block {current.index}")
                return False

            # Check chaining
            if current.previous_hash != previous.hash:
                print(f"Broken chain link between blocks {previous.index} and {current.index}")
                return False

        return True