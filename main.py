import random

from experiment import run_experiment


if __name__ == "__main__":
    random.seed(42)  # for reproducibility

    # You can adjust these parameters if you want
    num_blocks = 40
    anomaly_probability = 0.25
    baseline_size = 10

    run_experiment(
        num_blocks=num_blocks,
        anomaly_probability=anomaly_probability,
        baseline_size=baseline_size
    )