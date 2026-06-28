import argparse
import sys
import json
import time
import random
import os
import math

# --- PHYSICAL & MATERIAL CONSTANTS ---
MU_0 = 1.256637e-6          # Permeability of free space
SPEED_OF_LIGHT = 2.99e8     # m/s (Limit for PIC solvers)
STEEL_YIELD = 290e6         # 316L Yield Strength in Pascals
M_PROTON = 1.67e-27         # Proton mass (kg)

# Species Mass Mapping (Atomic Mass Units)
SPECIES_MAP = {
    "D-He3": 5.0,  # Deuterium (2) + Helium-3 (3)
    "D-D": 4.0,    # Deuterium (2) + Deuterium (2)
    "H-Beam": 1.0  # Hydrogen
}

def solve_numerical_constraints(nx, ny, nz, cfl):
    """
    Simulates WarpX CFL stability. 
    WarpX timestep (dt) is limited by the smallest cell size / c.
    """
    domain_size = 1.0  # 1 meter cube
    dx = domain_size / nx
    # Courant Limit: dt <= CFL * dx / c
    dt_limit = (cfl * dx) / SPEED_OF_LIGHT
    return dx, dt_limit

def run_simulation(bz, density, nx, ny, nz, steps, species, amr):
    print(f"[INIT] Aether Engine: Numerical Handshake for Species: {species}")
    sys.stdout.flush()

    # 1. Parse Inputs
    try:
        n_e = float(density)
        mass_factor = SPECIES_MAP.get(species, 1.0)
    except ValueError:
        n_e = 1.5e20
        mass_factor = 1.0

    # 2. Grid & Stability Logic
    dx, dt = solve_numerical_constraints(nx, ny, nz, 0.95)
    
    # Simulate Computational Complexity: 
    # Total complexity = cells * steps * (2^amr_levels)
    complexity_factor = (nx * ny * nz * (2**amr)) / 1_000_000 # Normalized
    
    # 3. Mechanical Physics Logic (Lorentz Coupling)
    mag_pressure_pa = (bz ** 2) / (2 * MU_0)
    # Impact pressure scales with particle mass and density
    kinetic_impact_pa = (n_e * mass_factor * 1.6e-19) * 1000 # Approximation
    total_load_pa = mag_pressure_pa + kinetic_impact_pa
    
    # Structural Calculation (Hoop Stress on 20mm 316L Wall)
    radius = 0.5
    thickness = 0.02
    hoop_stress = (total_load_pa * radius) / thickness
    fos = STEEL_YIELD / hoop_stress

    # 4. Simulation Loop
    for step in range(1, int(steps) + 1):
        # WORK SIMULATION: Sleep time scales with grid complexity
        # Real WarpX would be much slower; we scale to keep the UI responsive
        time.sleep(max(0.05, 0.01 * complexity_factor)) 

        # Numerical Divergence Simulation
        # If complexity is too high for the mesh, divergence "jitters"
        convergence_noise = (random.random() * 0.01) * (1.0 / step)
        field_div = (0.0001 * (nx/128)) + convergence_noise

        telemetry = {
            "step": step,
            "energy": 0.999 - (convergence_noise),
            "divergence": field_div,
            "load": total_load_pa / 1e9, # GPa
            "stress_mpa": hoop_stress / 1e6,
            "safety_factor": round(fos, 2),
            "status": "RUNNING"
        }
        
        # UI Bridge Signal
        print(f"DATA_SIGNAL:{json.dumps(telemetry)}")
        sys.stdout.flush()

        # FAILURE CRITERIA: Numerical Instability
        if field_div > 0.05:
            print(f"[CRITICAL] Numerical Divergence detected at Step {step}. Grid too coarse.")
            sys.stdout.flush()
            break

    # 5. GENERATE FINAL ENGINEERING REPORT
    os.makedirs("results", exist_ok=True)
    with open("results/structural_report.json", "w") as f:
        json.dump({
            "solver_metadata": {
                "engine": "WarpX-Coupled-ME",
                "grid_dx": dx,
                "timestep_dt": dt
            },
            "mechanical_results": {
                "peak_wall_pressure_gpa": total_load_pa / 1e9,
                "vessel_hoop_stress_mpa": hoop_stress / 1e6,
                "material_limit_mpa": STEEL_YIELD / 1e6,
                "factor_of_safety": fos
            },
            "verdict": "NOMINAL" if fos > 1.2 else "STRUCTURAL_FAILURE_RISK"
        }, f, indent=4)

    print(f"[SUCCESS] Simulation Complete. FoS: {round(fos, 2)}")
    sys.stdout.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bz", type=float, default=20.0)
    parser.add_argument("--density", type=str, default="1.5e20")
    parser.add_argument("--nx", type=int, default=128)
    parser.add_argument("--ny", type=int, default=128)
    parser.add_argument("--nz", type=int, default=256)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--species", type=str, default="D-He3")
    parser.add_argument("--amr", type=int, default=2)
    
    args = parser.parse_args()
    
    run_simulation(args.bz, args.density, args.nx, args.ny, args.nz, args.steps, args.species, args.amr)