# Aether Orchestrator: Universal Simulation Interface
**Bridging HPC Physics Solvers with Mechanical Engineering Safety Validation**

Aether Orchestrator is a cloud-native desktop integration platform designed to manage, execute, and visualize high-fidelity physics simulations (WarpX/AMReX). It solves the "Data Gravity" problem by allowing engineers to remotely configure and monitor local GPU-accelerated simulations via a sleek, cloud-synced dashboard.

## 🚀 The Engineering Solution
Most fusion simulation tools are "black boxes" accessible only via CLI. Aether Orchestrator provides:
- **Cloud-Native Logic Sync:** The physics solver (`solver_main.py`) is fetched from Cloudflare R2 on startup, ensuring the engineering team always uses the latest validated physics models.
- **Real-Time Telemetry:** Uses Inter-Process Communication (IPC) to stream data from the local Python kernel to a Glassmorphism UI via a Go-based bridge.
- **ME Validation Suite:** Automatically calculates **Magnetic Pressure** and **Hoop Stress** on vacuum vessel walls using first-principles (Lorentz Force) to determine real-time **Factors of Safety (FoS)**.

## 🛠 Technical Stack
- **Native Shell:** Go (Wails) for system-level process management and file I/O.
- **Frontend:** React + Tailwind CSS for a light-weight, high-density engineering dashboard.
- **Solver Engine:** Python 3.11 with `argparse` and `json` IPC signals.
- **Infrastructure:** Cloudflare for solver version control.

## 🏗 Mechanical Engineering Logic
The integrated solver calculates structural integrity based on the following:
1. **Magnetic Pressure:** $P = B^2 / (2\mu_0)$
2. **Vessel Hoop Stress:** $\sigma = (P \cdot r) / t$
3. **Safety Factor:** Derived against 316L Stainless Steel yield strength ($~290$ MPa).

## 📦 Running the Application
1. Download the standalone binary from the `/build` folder.
2. Ensure **Python 3.x** is installed on your local machine.
3. Launch `Ai Dashboard.exe`.
4. The app will automatically sync with `simulation.chakaap.com` and fetch the latest solver from R2.
5. Adjust **Bz (Tesla)** and **Mesh Density**, then click **Execute Local Solver**.
6. Check `Documents/AetherSim/results` for the generated `structural_report.json`.

---
*Created by Gunjan Ghimire - Mechanical Engineer with a focus on Simulation Tools & System Architecture.*
