# Bolt Strength Calculator MVP v0.1

Streamlit calculator for preliminary metric bolt tensile, shear and combined-load screening.

## Run on Windows
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy
Upload `app.py`, `requirements.txt`, and `README.md` to a GitHub repository. Deploy with Streamlit Community Cloud using branch `main` and main file `app.py`.

## Scope
Metric coarse sizes M3–M36; common property classes 4.6, 4.8, 5.8, 8.8, 10.9, 12.9; approximate tensile stress area; preliminary tensile/shear capacity; one/two shear planes; thread/shank shear plane choice; user-selected safety factor; CSV report.

## Limitations
Not a code-compliant bolted-joint design. No preload, torque, proof-load table, fatigue, prying, thread stripping, bearing, tear-out, block shear, eccentric bolt-group analysis, slip-critical design, or code-specific resistance factors. Strength assumptions are nominal screening values; confirm the applicable fastener standard and certificate. Never use as the sole basis for safety-critical design.
