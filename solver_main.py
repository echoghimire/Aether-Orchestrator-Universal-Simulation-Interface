import argparse
import sys
import json
import time
import random
import os

def generate_engineering_results(bz, density, steps, results_dir):
    """
    Creates physical output files simulating HDF5/JSON engineering data.
    """
    os.makedirs(results_dir, exist_ok=True)
    
    # Simulate a summary of the structural analysis
    summary = {
        "metadata": {
            "solver": "Aether WarpX Wrapper v1.0.0",
            "timestamp": time.ctime(),
            "target_vessel": "Polaris_V1"
        },
        "inputs": {
            "magnetic_field_tesla": bz,
            "plasma_density": density,
            "iterations": steps
        },
        "outputs": {
            "peak_vessel_load_gpa": round((bz * 0.18) + (random.random() * 0.2), 4),
            "max_thermal_flux_mw": round((bz * 12.5) + random.random(), 2),
            "safety_factor": round(1.5 + random.random(), 2),
            "convergence_status": "SUCCESS"
        }
    }

    file_path = os.path.join(results_dir, "simulation_summary.json")
    with open(file_path, "w") as f:
        json.dump(summary, f, indent=4)
    
    return file_path

def run_simulation(bz, density, nx, ny, nz, steps):
    """
    The main PIC (Particle-In-Cell) simulation loop.
    Prints DATA_SIGNAL for the Wails/JS UI to intercept.
    """
    print(f"[INIT] Aether Engine: Initializing Mesh {nx}x{ny}x{nz}...")
    sys.stdout.flush()
    time.sleep(1)

    print(f"[INFO] Applied B-Field: {bz} Tesla. Species: {density}")
    sys.stdout.flush()

    for step in range(1, steps + 1):
        # Simulate computational delay (Mimicking WarpX GPU cycles)
        time.sleep(0.15) 

        # Physics-based mock data
        # Higher B-field results in higher energy and load
        energy_conv = 0.998 - (random.random() * 0.005)
        vessel_load = (bz * 0.2) + (random.random() * 0.3)
        field_div = random.random() * 0.0002

        # DATA_SIGNAL is the protocol used to update the UI charts live
        telemetry = {
            "step": step,
            "energy": energy_conv,
            "divergence": field_div,
            "load": vessel_load,
            "status": "RUNNING"
        }
        
        print(f"DATA_SIGNAL:{json.dumps(telemetry)}")
        sys.stdout.flush() # CRITICAL: Allows Go to see data immediately

    # Finalize by creating the physical output files
    results_path = generate_engineering_results(bz, density, steps, "results")
    print(f"[SUCCESS] Simulation Converged. Data written to: {results_path}")
    sys.stdout.flush()

if __name__ == "__main__":
    # 1. Setup CLI Arguments (Matches the Go exec.Command call)
    parser = argparse.ArgumentParser(description="Aether Orchestrator: WarpX Simulation Wrapper")
    
    parser.add_argument("--bz", type=float, default=20.0, help="Magnetic Field in Tesla")
    parser.add_argument("--density", type=str, default="1.5e20", help="Plasma Density")
    parser.add_argument("--nx", type=int, default=128)
    parser.add_argument("--ny", type=int, default=128)
    parser.add_argument("--nz", type=int, default=256)
    parser.add_argument("--steps", type=int, default=100)
    
    args = parser.parse_args()
    
    try:
        run_simulation(args.bz, args.density, args.nx, args.ny, args.nz, args.steps)
    except KeyboardInterrupt:
        print("\n[HALT] Simulation terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"[FATAL] Solver Error: {str(e)}")
        sys.exit(1)