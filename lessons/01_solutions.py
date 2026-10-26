"""Run after sections 1-5 of 01_intro.py, in the same Python session."""

# A: Every comparison gets parentheses. Use & for elementwise AND.
practice = df.loc[
    (df["treatment"] == "control") & (df["soil_moisture_pct"] > 30)
]
print(len(practice))

# B: pandas Series support elementwise arithmetic.
df["height_m"] = df["height_cm"] / 100
print(df["height_m"].mean())

# C: Give the result a useful column name, then write it without a row index.
practice_summary = (
    df.groupby("treatment", observed=True)
    .agg(mean_height_m=("height_m", "mean"))
    .reset_index()
)
practice_summary.to_csv(out / "practice_summary.csv", index=False)
print(practice_summary)
