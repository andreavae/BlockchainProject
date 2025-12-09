Blockchain-Based Data Integrity with Simple AI-Assisted Anomaly Detection
This repository contains a minimal Python prototype developed for the course Cryptography and Security.
The project illustrates how cryptographic hashing and block chaining can be used to ensure data integrity in a blockchain-style ledger, and how basic anomaly detection techniques (statistical and rule-based) can be applied on top of the chain to flag suspicious activity.

1. Overview
The prototype consists of three main layers:

Blockchain layer

In-memory blockchain with:
Block (index, timestamp, transactions, previous_hash, nonce, hash)
Transaction (sender, receiver, amount)
Each block’s hash is computed using SHA-256 over its contents.
A validation routine (is_chain_valid) recomputes hashes and checks the hash chain for tampering.
Monitoring layer

Extracts simple features from each block:
num_txs (number of transactions)
total_amount (sum of transaction amounts)
max_amount (maximum transaction amount)
time_delta (time difference from previous block)
Detection layer

Statistical anomaly detector (z-score based):
Builds a baseline (mean and std) on the first N blocks.
Flags blocks as anomalous when any feature’s z-score exceeds a threshold.
Rule-based security checker:
Simple security policies:
max single transaction amount
max total amount per block
minimum allowed time between blocks
Synthetic experiments generate normal and anomalous blocks and log detection results.

2. Repository Structure
text


                
					
.
├─ models.py        # Data structures: Transaction, Block
├─ blockchain.py    # Blockchain management and integrity verification
├─ anomaly.py       # AnomalyDetector (z-scores) and RuleBasedSecurityChecker
├─ experiment.py    # Synthetic data generation and experiment driver
└─ main.py          # Entry point to run the experiment

				
            
3. Requirements
Python 3.9+ (any recent Python 3 should work)
No external dependencies beyond the standard library are required.
To create an isolated environment (optional but recommended):

bash


                
					
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install --upgrade pip

				
            
4. How to Run
From the project root:

bash


                
					
python main.py

				
            
This will:

Initialize an in-memory blockchain.
Generate a sequence of normal and anomalous blocks.
For each block, print:
Synthetic anomaly label (normal vs. anomalous).
Block features (num_txs, total_amount, max_amount, time_delta).
Statistical detector output:
whether baseline is ready,
anomaly decision,
z-scores and reason.
Rule-based checker output:
whether any rule fired,
list of violated rules (if any).
At the end, print the result of blockchain integrity verification:
Final chain validity: True if the chain is consistent.
You can modify main.py to change:

num_blocks (number of blocks),
anomaly_probability (fraction of anomalous blocks),
baseline_size (blocks used for statistical baseline).
You can also tune:

z-score threshold in AnomalyDetector (in anomaly.py),
rule thresholds in RuleBasedSecurityChecker (in anomaly.py).
5. Educational Focus
This code is intended for educational purposes only.
It is not a production-ready blockchain or security system.

The main learning objectives are:

understanding how hash functions and block chaining provide tamper-evident logging;
seeing how simple anomaly detection (z-scores) and rule-based security policies can be layered on top of a blockchain to detect suspicious behaviour;
exploring basic trade-offs between cryptographic guarantees and behavioural monitoring in a security context.
