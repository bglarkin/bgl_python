# Simulated seedling measurements

`seedlings.csv` contains **60 invented observations**, one independent seedling per
row. It is not project data or evidence about actual plants. A field-style example
lets us practice measurement units, missing values, and a treatment comparison
without downloading another package or dataset. No external data attribution is needed.

| Column | Meaning | Type |
|---|---|---|
| `seedling_id` | Unique label S001–S060 | string |
| `treatment` | `control` or `fertilized`; 30 each before cleaning | categorical text |
| `soil_moisture_pct` | Simulated soil moisture, 15–45 percent | number |
| `height_cm` | Simulated seedling height, centimeters | number |

Generator: `scripts/make_data.py`, NumPy `default_rng(42)`. Heights follow
`7 + 0.55 * moisture + 4 * fertilized + Normal(0, 2.5)` before rounding.
Two heights and one moisture value are deliberately replaced with missing values
(empty CSV fields). Complete-case analysis leaves **57 seedlings**: 29 control,
28 fertilized. The true simulation coefficients are known; fitted estimates vary
from those values because of the generated noise.

The lesson explicitly drops missing values only for required analysis columns.
That is an instructional choice; real missing-data decisions require understanding
why measurements are absent. Treat each simulated row as independent; actual
seedlings sharing sites or plots could require a different model.

To regenerate from the repository root, using the optional terminal environment:
`.venv/bin/python scripts/make_data.py` (Windows: use `.venv\Scripts\python.exe`).
The CSV is already included; regeneration is not part of the hour.
