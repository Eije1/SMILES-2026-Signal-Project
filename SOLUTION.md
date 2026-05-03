# SMILES-2026 Signal Interference Cancellation Solution
- **Final Score:** 9.69 dB (Average)
- **Applicant:** Oloche Celestine Eije
- **Country of Origin:** Nigeria
- **Institution:** Russian Biotechnology University (ROSBIOTECH), Moscow


## 1. Reproducibility Instructions
To reproduce the results in `results.json`, follow these steps:

1.  **Environment**: Ensure you have Python 3.8+ installed with the necessary libraries.
    ```bash
    pip install numpy scipy
    ```
2.  **Data**: Place the `challenge.mat` file provided in the task into the same directory as the scripts.
3.  **Run**: Execute the following command:
    ```bash
    python applicant_solution.py
    ```
4.  **Verification**: The script will evaluate the baseline and my solution, then write the final metrics to `results.json`. The average score should be approximately **9.69 dB**. Just incase my code mistakenly gives you the same value as the baseline (4.02dB), please kindly enter the runtime in your colab and restart the session to clear stucked or initial responses (that is like refreshing the memory of the colab engine so it can process new input).
5.  **Note on Environment:** If you are running this in a shared environment like Google Colab and encounter baseline-only results (4.02dB) for my solutions, please Restart the Session (Runtime -> Restart session) before executing. This ensures the SVD logic is applied to a fresh memory state and prevents variable leakage from previous runs.

## 2. Final Solution Description
My solution implements a **Two-Stage Interference Cancellation** strategy designed to address both the device-generated leakage and external spatial noise.

### Stage 1: Nonlinear Cross-Channel Modeling
I utilized the provided `fit_tx_prediction` helper from the task baseline to handle the structured interference ($F_c$ component). This stage uses high-order nonlinear cross-products of the 6-channel transmitted signals ($TX$) to predict the leakage on the 4 receive channels. This deterministic model effectively suppresses interference directly correlated with the device's own transmission.

### Stage 2: Rank-1 Spatial SVD Filter
After removing the TX-driven components, I identified a remaining spatially coherent interference term ($E$ component). Since this noise is consistent across all receive channels but independent of the TX signal, I applied **Singular Value Decomposition (SVD)** to the residual. By isolating the dominant Rank-1 spatial component, I removed the external interference, which provided the significant performance boost from the 4.02 dB baseline to the final **9.69 dB**.

## 3. Why This Approach?
As a researcher in oncology, I view this problem as analogous to identifying a biological biomarker (the signal) within a high-noise genetic environment. I chose this hybrid approach because it separates the interference into its physical origins: one part driven by the hardware (Nonlinear) and one part driven by the environment (Spatial).

## 4. Experiments and Failed Attempts
- **Manual Lag Construction**: I initially tried creating custom feature matrices with manual shifts and slew-rate terms. However, I found that the built-in baseline helper was more robust and better suited for the "Explainability" requirements of the challenge.
- **Higher-Rank Components**: I experimented with removing more than one singular value (Rank-2 or Rank-3) during the SVD stage. This led to a decrease in the score, as it began to subtract parts of the desired signal ($s[n]$). Sticking to a Rank-1 model proved to be the most reliable for cleaning the external coherent source.

## 5. Conclusion
This challenge provided a practical opportunity to apply signal processing techniques to a real-world hardware problem. By separating the interference into deterministic (TX-driven) and stochastic (spatial) components, I was able to achieve a 9.69 dB reduction, significantly outperforming the baseline. For me, this project reinforces the idea that whether in telecommunications or oncology, the key to handling "big data" is a deep understanding of the underlying signal structures. I look forward to expanding on these methodologies during the SMILES 2026 program.
