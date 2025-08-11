 Covert Timing Channel Simulation

Simulates a **covert timing channel** by encoding bits in inter-packet timings and observing how **network load and queueing** affect recoverable throughput and error rate.

## 🔍 What This Project Explores
- Encode/decode bits via **timing** 
- Queue + buffer dynamics 
- Impact of background traffic on **bitrate**, **BER**, and **detection**

## ✨ Features
- Sender/receiver processes (synthetic trace generation)
- Adjustable load, jitter, and service rate
- Metrics: **bitrate**, **bit error rate (BER)**, confusion matrix
- Plotting for timing histograms and ROC-style detection

## 🛠️ Tech
- Python 3.12+
- NumPy, Pandas, Matplotlib (optional: SciPy)
