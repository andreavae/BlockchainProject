# models.py

import hashlib
import json
from dataclasses import dataclass, field
from typing import List


@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float


@dataclass
class Block:
    index: int
    timestamp: float
    transactions: List[Transaction]
    previous_hash: str
    nonce: int = 0
    hash: str = field(init=False)

    def __post_init__(self):
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """
        Compute SHA-256 hash of the block contents
        (excluding the current hash field itself).
        """
        block_dict = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [t.__dict__ for t in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()