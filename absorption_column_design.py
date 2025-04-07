import numpy as np
import matplotlib.pyplot as plt

# === INPUT PARAMETERS ===
G = 1500      # Gas molar flow rate [kmol/h]
L = 800       # Liquid molar flow rate [kmol/h]
y_in = 0.05
y_out = 0.04
x_in = 0.0
m = 1.5       # Henry's law constant: y* = m * x
HOG = 1.2     # Height of Overall Gas Transfer Unit [m]

# === PHYSICAL PROPERTIES ===
T = 298       # Temperature [K]
P = 101325    # Pressure [Pa]
R = 8314      # Gas constant [J/kmol·K]
rho_L = 1000  # Liquid density [kg/m³]
rho_G = 1.2   # Gas density [kg/m³]

# === STRUCTURED PACKING PROPERTIES ===
a_packing = 250       # Specific surface area [m²/m³]
epsilon = 0.97        # Void fraction
bulk_density = 150    # Packing bulk density [kg/m³]
dp_structured_per_m = 30  # Pressure drop per meter [Pa/m]
d_p = 0.025           # Equivalent structured packing element size [m]

# === STEP 1: MATERIAL BALANCE ===
x_out = (G * (y_in - y_out)) / L

# === STEP 2: NTU AND HEIGHT CALCULATION ===
numerator = y_in - m * x_in
denominator = y_out - m * x_out
slope_factor = 1 - (m * L / G)

if denominator > 0 and slope_factor != 0:
    NTU = (1 / slope_factor) * np.log(numerator / denominator)
    Z = NTU * HOG
else:
    raise ValueError("Invalid design: operating line crosses equilibrium line.")

# === STEP 3: GAS FLOW RATE AND COLUMN DIAMETER ===
n_G = G / 3600  # kmol/s
Q_G = (n_G * R * T) / P  # Ideal gas law: m³/s
U_g = 2.5  # Fixed gas velocity [m/s]
A_col = Q_G / U_g  # Column cross-sectional area [m²]
D_col = np.sqrt((4 * A_col) / np.pi)  # Column diameter [m]

# === STEP 4: STRUCTURED PACKING SIZING ===
Z_structured = Z
V_packed = A_col * Z_structured
packing_mass = V_packed * bulk_density
total_dp = Z_structured * dp_structured_per_m

# === STEP 5: PACKING DIAMETER RECOMMENDATION ===
packing_diameter_min = max(5 * d_p, 0.1 * D_col)

# === PRINT RESULTS ===
print("\n=== ABSORPTION PACKED COLUMN DESIGN ===")
print(f"Gas flow rate (G): {G} kmol/h")
print(f"Liquid flow rate (L): {L} kmol/h")
print(f"Volumetric gas flow rate (Q_G): {Q_G:.2f} m³/s")
print(f"Fixed gas velocity (U_g): {U_g:.2f} m/s")
print(f"Column area (A_col): {A_col:.2f} m²")
print(f"Column diameter (D_col): {D_col:.2f} m")
print(f"Recommended packing diameter (min): {packing_diameter_min:.2f} m")
print(f"Outlet liquid mole fraction (x_out): {x_out:.4f}")
print(f"Number of Transfer Units (NTU): {NTU:.2f}")
print(f"Packed height (Z): {Z_structured:.2f} m")
print(f"Packed volume: {V_packed:.2f} m³")
print(f"Estimated packing mass: {packing_mass:.2f} kg")
print(f"Estimated pressure drop: {total_dp:.1f} Pa")
print("=========================================")

# === PLOT EQUILIBRIUM AND OPERATING LINES ===
x_vals = np.linspace(0, x_out, 100)
y_eq = m * x_vals
y_op = y_in - (G / L) * x_vals

plt.plot(x_vals, y_eq, label="Equilibrium Line (y* = m·x)")
plt.plot(x_vals, y_op, label="Operating Line")
plt.xlabel("x (liquid mole fraction)")
plt.ylabel("y (gas mole fraction)")
plt.title("Equilibrium vs Operating Line")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
