Blockchain + Anomaly Detection

Python project that shows:
- a simple blockchain-style hash chain using SHA-256 for data integrity
- basic anomaly detection on blocks (z-scores + fixed security rules)

Summary
The scritp builds a small blockchain in memory
generates normal and anomalous blocks
prints block features, anomaly detector output, and rule-based violations
finally checks that the chain is still valid

Files
models.py – Transaction, Block
blockchain.py – Blockchain + integrity check
anomaly.py – AnomalyDetector + RuleBasedSecurityChecker
experiment.py – Synthetic blocks and detection logic
main.py – Runs the experiment

Requirements
Python 3.9+
Only Python standard library modules

