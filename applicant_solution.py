import json
import gdown
import numpy as np
from scipy.io import loadmat
from task_and_baseline import baseline, build_task_helpers

# Download the dataset
url = "https://drive.google.com/file/d/1BBHVSI4KB-B8OX46eN1Nm4ARCeq6Rui4/view?usp=sharing"
downloaded_file = "challenge.mat"
gdown.download(url, downloaded_file, quiet=False, fuzzy=True)

data = loadmat("challenge.mat", simplify_cells=True)
tx = data["tx"].astype(np.complex128)
rx = data["rx"].astype(np.complex128)
Fs = float(data["Fs"])
N, _ = tx.shape

tx_n = tx / (np.sqrt(np.mean(np.abs(tx) ** 2, axis=0, keepdims=True)) + 1e-30)
helpers = build_task_helpers(tx_n, Fs, N)

def your_canceller(tx_n, rx):
    # I started by importing the helpers locally to keep the environment clean
    from task_and_baseline import build_task_helpers
    
    # I set the sample rate to 7.68 MHz as specified in the task
    n_samples = rx.shape[0]
    helpers = build_task_helpers(tx_n, 7.68e6, n_samples)
    fit_tx = helpers["fit_tx_prediction"]

    # I removed the structured transmitter interference.
    #After that, I used the provided nonlinear model to subtract the TX-driven leakage
    tx_pred = fit_tx(rx)
    res_tx = rx - tx_pred

    # I addressed the spatially coherent external noise (the 'E' term)
    # I applied SVD to the residual to find the primary shared noise source
    U, S, Vh = np.linalg.svd(res_tx, full_matrices=False)
    
    # I reconstructed the strongest rank-1 component to isolate that external source
    shared_noise = np.outer(U[:, 0] * S[0], Vh[0, :])

    # My final result removes both the hardware leakage and the environmental noise
    rx_clean = res_tx - shared_noise
    
    return rx_clean

print("\n=== Baseline ===")
baseline_reds, baseline_avg = helpers["score"](
    rx, baseline(tx_n, rx, helpers["fit_tx_prediction"]), label="baseline"
)

print("=== Your Solution ===")
yours_reds, yours_avg = helpers["score"](rx, your_canceller(tx_n, rx), label="yours")

results = {
    "baseline": {
        "per_channel_db": baseline_reds,
        "average_db": baseline_avg,
    },
    "yours": {
        "per_channel_db": yours_reds,
        "average_db": yours_avg,
    },
}

with open("results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)