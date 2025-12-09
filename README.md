# Blockchain + Simple Anomaly Detection Prototype

Minimal Python prototype that shows:

- how a **blockchain-style hash chain** (using SHA-256) provides **tamper-evident data integrity**;
- how simple **anomaly detection** (z-scores) and **rule-based security checks** can flag suspicious blocks.

Developed for a **Cryptography and Security** course.

---

## Structure

```text
.
├─ models.py      # Transaction, Block
├─ blockchain.py  # Blockchain + is_chain_valid()
├─ anomaly.py     # AnomalyDetector (z-score) + RuleBasedSecurityChecker
├─ experiment.py  # Synthetic data + experiment driver
└─ main.py        # Entry point

				
            
Requirements
Python 3.9+
Only standard library modules.
Optional venv:

bash


                
					
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

				
            
Run
bash


                
					
python main.py

				
            
For each block you will see:

synthetic label: normal / anomalous
features: num_txs, total_amount, max_amount, time_delta
statistical detector output (z-scores, is_anomaly)
rule-based checker output (rule_alert, violations)
At the end:

text


                
					
Final chain validity: True

				
            
if the hash chain is still valid.

What this is for
Project for combining:

cryptographic integrity (hashes + block chaining)
with basic monitoring (statistical + rule-based checks) on top of a blockchain-style ledger.


                
