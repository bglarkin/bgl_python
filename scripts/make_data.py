"""Regenerate the bundled simulation. Optional; the lesson reads the CSV directly."""
from pathlib import Path
import numpy as np
import pandas as pd

root = Path(__file__).resolve().parents[1]
rng = np.random.default_rng(42)
n = 60
treatment = np.array(["control", "fertilized"] * (n // 2))
soil_moisture_pct = rng.uniform(15, 45, n).round(1)
height_cm = (
    7 + 0.55 * soil_moisture_pct
    + 4 * (treatment == "fertilized")
    + rng.normal(0, 2.5, n)
).round(2)
data = pd.DataFrame({
    "seedling_id": [f"S{i:03d}" for i in range(1, n + 1)],
    "treatment": treatment,
    "soil_moisture_pct": soil_moisture_pct,
    "height_cm": height_cm,
})
# Deliberate missing measurements: row positions use zero-based indexing.
data.loc[[5, 22], "height_cm"] = np.nan
data.loc[41, "soil_moisture_pct"] = np.nan
data.to_csv(root / "data" / "seedlings.csv", index=False)
print("Wrote 60 simulated seedlings (no real observations).")
