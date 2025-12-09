# anomaly.py

from typing import List, Dict, Any, Optional
import statistics

from models import Block


class AnomalyDetector:
    def __init__(self, baseline_size: int = 10, z_threshold: float = 3.0):
        self.baseline_size = baseline_size
        self.z_threshold = z_threshold

        # Store history of each feature separately
        self.num_txs_history: List[float] = []
        self.total_amount_history: List[float] = []
        self.max_amount_history: List[float] = []
        self.time_delta_history: List[float] = []

        # Baseline statistics (computed after enough blocks)
        self.baseline_ready = False
        self.stats = {
            "num_txs": {"mean": None, "std": None},
            "total_amount": {"mean": None, "std": None},
            "max_amount": {"mean": None, "std": None},
            "time_delta": {"mean": None, "std": None},
        }

    def _update_history(
        self,
        num_txs: float,
        total_amount: float,
        max_amount: float,
        time_delta: float
    ):
        self.num_txs_history.append(num_txs)
        self.total_amount_history.append(total_amount)
        self.max_amount_history.append(max_amount)
        self.time_delta_history.append(time_delta)

    def _compute_baseline(self):
        """
        Compute mean and std for each feature based on history.
        Assumes history length >= baseline_size.
        """
        def mean_std(lst):
            m = statistics.mean(lst)
            s = statistics.stdev(lst) if len(lst) > 1 else 0.0
            return m, s

        m, s = mean_std(self.num_txs_history)
        self.stats["num_txs"]["mean"], self.stats["num_txs"]["std"] = m, s

        m, s = mean_std(self.total_amount_history)
        self.stats["total_amount"]["mean"], self.stats["total_amount"]["std"] = m, s

        m, s = mean_std(self.max_amount_history)
        self.stats["max_amount"]["mean"], self.stats["max_amount"]["std"] = m, s

        m, s = mean_std(self.time_delta_history)
        self.stats["time_delta"]["mean"], self.stats["time_delta"]["std"] = m, s

        self.baseline_ready = True

    def _z_score(self, value: float, mean: float, std: float) -> float:
        if std == 0:
            return 0.0  # if no variation yet, no anomaly
        return (value - mean) / std

    def extract_features(
        self,
        current_block: Block,
        previous_block: Optional[Block]
    ) -> Dict[str, float]:
        num_txs = len(current_block.transactions)
        total_amount = sum(t.amount for t in current_block.transactions) if current_block.transactions else 0.0
        max_amount = max((t.amount for t in current_block.transactions), default=0.0)
        time_delta = (
            current_block.timestamp - previous_block.timestamp
            if previous_block is not None else 0.0
        )

        return {
            "num_txs": num_txs,
            "total_amount": total_amount,
            "max_amount": max_amount,
            "time_delta": time_delta,
        }

    def process_block(
        self,
        block_index: int,
        features: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Update histories, possibly update baseline, and (if baseline ready)
        compute z-scores and anomaly decision.
        Returns a dict with decision info.
        """
        # Update histories
        self._update_history(
            features["num_txs"],
            features["total_amount"],
            features["max_amount"],
            features["time_delta"]
        )

        decision = {
            "block_index": block_index,
            "is_anomaly": False,
            "feature_z_scores": {},
            "reason": ""
        }

        # If not enough blocks for baseline, skip detection
        if len(self.num_txs_history) < self.baseline_size:
            decision["reason"] = "Not enough data for baseline"
            return decision

        # If this is the first time we reach baseline_size, compute baseline
        if not self.baseline_ready:
            self._compute_baseline()
            decision["reason"] = "Baseline just computed; no detection yet"
            return decision

        # Compute z-scores for each feature
        z_scores = {}
        for feat_name in ["num_txs", "total_amount", "max_amount", "time_delta"]:
            value = features[feat_name]
            mean = self.stats[feat_name]["mean"]
            std = self.stats[feat_name]["std"]
            z = self._z_score(value, mean, std)
            z_scores[feat_name] = z

        decision["feature_z_scores"] = z_scores

        # Decide anomaly if any |z| exceeds threshold
        anomalies = [f for f, z in z_scores.items() if abs(z) > self.z_threshold]
        if anomalies:
            decision["is_anomaly"] = True
            decision["reason"] = f"Anomalous features: {', '.join(anomalies)} (z-score threshold = {self.z_threshold})"
        else:
            decision["reason"] = "Within normal range"

        return decision

class RuleBasedSecurityChecker:
        """
        Simple rule-based security checks on block-level features.
        These rules emulate basic security policies.
        """

        def __init__(
                self,
                max_single_tx_amount: float = 2000.0,
                max_block_total_amount: float = 5000.0,
                min_time_delta: float = 0.02
        ):
            """
            :param max_single_tx_amount: If any transaction exceeds this amount, raise an alert.
            :param max_block_total_amount: If total_amount in a block exceeds this, raise an alert.
            :param min_time_delta: If time_delta between blocks is below this, raise an alert.
            """
            self.max_single_tx_amount = max_single_tx_amount
            self.max_block_total_amount = max_block_total_amount
            self.min_time_delta = min_time_delta

        def check_rules(self, features: Dict[str, float]) -> Dict[str, any]:
            """
            Evaluate the security rules on the given features.
            Returns a dict with rule violations and overall decision.
            """
            violations = []

            # Rule 1: Single transaction amount too high
            if features["max_amount"] > self.max_single_tx_amount:
                violations.append(
                    f"Rule1: max_amount {features['max_amount']:.2f} > {self.max_single_tx_amount:.2f}"
                )

            # Rule 2: Block total amount too high
            if features["total_amount"] > self.max_block_total_amount:
                violations.append(
                    f"Rule2: total_amount {features['total_amount']:.2f} > {self.max_block_total_amount:.2f}"
                )

            # Rule 3: Blocks created too quickly
            # (ignore the very first block after genesis where time_delta may be 0)
            if features["time_delta"] != 0.0 and features["time_delta"] < self.min_time_delta:
                violations.append(
                    f"Rule3: time_delta {features['time_delta']:.3f} < {self.min_time_delta:.3f}"
                )

            decision = {
                "rule_alert": len(violations) > 0,
                "violations": violations
            }
            return decision