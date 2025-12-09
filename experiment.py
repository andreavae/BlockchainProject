# experiment.py

import random
import time

from models import Transaction
from blockchain import Blockchain
from anomaly import AnomalyDetector, RuleBasedSecurityChecker


def generate_random_transaction(normal: bool = True) -> Transaction:
    senders = ["Alice", "Bob", "Charlie", "Dave"]
    receivers = ["Eve", "Frank", "Grace", "Heidi"]

    sender = random.choice(senders)
    receiver = random.choice(receivers)

    if normal:
        amount = random.uniform(1, 100)  # normal range
    else:
        amount = random.uniform(1000, 5000)  # anomalously high

    return Transaction(sender=sender, receiver=receiver, amount=amount)


def run_experiment(
    num_blocks: int = 50,
    anomaly_probability: float = 0.2,
    baseline_size: int = 10
):
    """
    Simulate blockchain activity, sometimes injecting anomalous blocks.
    Both a statistical anomaly detector (z-score based)
    and a simple rule-based security checker are applied.
    """
    bc = Blockchain()

    # More sensitive statistical detector (lower z-threshold)
    detector = AnomalyDetector(baseline_size=baseline_size, z_threshold=1.5)

    # Simple rule-based security checker (fixed thresholds)
    rule_checker = RuleBasedSecurityChecker(
        max_single_tx_amount=2000.0,
        max_block_total_amount=5000.0,
        min_time_delta=0.02
    )

    previous_block = bc.last_block

    for i in range(1, num_blocks + 1):
        # Decide whether this block is "normal" or "anomalous" (synthetic label)
        is_anomalous_block = random.random() < anomaly_probability

        # More transactions in anomalous block (just as one possible signal)
        if is_anomalous_block:
            num_txs = random.randint(6, 10)
        else:
            num_txs = random.randint(1, 5)

        txs = []
        for _ in range(num_txs):
            tx = generate_random_transaction(normal=not is_anomalous_block)
            txs.append(tx)

        # Manipulate time interval between blocks:
        # - anomalous blocks: very short interval
        # - normal blocks: slightly longer interval
        if is_anomalous_block:
            time.sleep(0.01)
        else:
            time.sleep(0.1)

        # Add block to chain
        new_block = bc.add_block(txs)

        # Extract features for anomaly detection and rule-based checks
        features = detector.extract_features(new_block, previous_block)

        # Statistical anomaly detection (z-score)
        decision = detector.process_block(new_block.index, features)

        # Rule-based security checks
        rule_decision = rule_checker.check_rules(features)

        # Log output for later analysis in the report
        print("=" * 60)
        print(f"Block {new_block.index}")
        print(f"  Synthetic label (is_anomalous_block)? {is_anomalous_block}")
        print(f"  num_txs={features['num_txs']}, "
              f"total_amount={features['total_amount']:.2f}, "
              f"max_amount={features['max_amount']:.2f}, "
              f"time_delta={features['time_delta']:.3f}")

        # Output anomaly detector (statistical)
        print(f"  [Statistical] baseline_ready={detector.baseline_ready}")
        print(f"  [Statistical] is_anomaly={decision['is_anomaly']}")
        print(f"  [Statistical] Reason: {decision['reason']}")
        if decision["feature_z_scores"]:
            print(
                "  [Statistical] z-scores: "
                + ", ".join(f"{k}={v:.2f}" for k, v in decision["feature_z_scores"].items())
            )

        # Output rule-based checker
        print(f"  [Rules] rule_alert={rule_decision['rule_alert']}")
        if rule_decision["rule_alert"]:
            print("  [Rules] Violations:")
            for v in rule_decision["violations"]:
                print(f"    - {v}")

        previous_block = new_block

    # Final integrity check
    print("=" * 60)
    print("Final chain validity:", bc.is_chain_valid())