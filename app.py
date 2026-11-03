import math
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bolt Strength Calculator", page_icon="🔩", layout="wide")
st.title("🔩 Bolt Strength Calculator")
st.caption("MVP v0.1 | Preliminary metric bolt tensile, shear and combined-load screening")
st.warning("Engineering screening only — not a code-compliant bolted-joint design. Confirm the governing code, exact fastener standard/certificate, preload, fatigue, prying, bearing, tear-out, thread stripping, eccentricity, corrosion, temperature and installation method. Do not use as the sole basis for safety-critical design.")

threads = {
"M3":(3,.5),"M4":(4,.7),"M5":(5,.8),"M6":(6,1),"M8":(8,1.25),
"M10":(10,1.5),"M12":(12,1.75),"M14":(14,2),"M16":(16,2),
"M18":(18,2.5),"M20":(20,2.5),"M22":(22,2.5),"M24":(24,3),
"M27":(27,3),"M30":(30,3.5),"M33":(33,3.5),"M36":(36,4)
}
grades = {"4.6":(400,240),"4.8":(400,320),"5.8":(500,400),
          "8.8":(800,640),"10.9":(1000,900),"12.9":(1200,1080)}

with st.sidebar:
    st.header("Bolt configuration")
    size = st.selectbox("Metric coarse bolt size", list(threads), index=6)
    grade = st.selectbox("Property class", list(grades), index=3)
    qty = st.number_input("Number of bolts", min_value=1, value=4, step=1)
    sf = st.number_input("User-selected safety factor", min_value=1.0, max_value=10.0, value=2.0, step=.1)
d,p = threads[size]
fu,fy = grades[grade]
At = math.pi/4*(d-.9382*p)**2

st.subheader("1. Applied loads")
a,b = st.columns(2)
with a:
    total_t = st.number_input("Total tensile load (kN)", min_value=0.0, value=20.0, step=1.0)
    t_mode = st.radio("Tension distribution", ["Equal across bolts","Enter per-bolt load"], horizontal=True)
    t_each = total_t/qty if t_mode == "Equal across bolts" else st.number_input("Tension per bolt (kN)", min_value=0.0, value=5.0)
with b:
    total_v = st.number_input("Total shear load (kN)", min_value=0.0, value=10.0, step=1.0)
    v_mode = st.radio("Shear distribution", ["Equal across bolts","Enter per-bolt load"], horizontal=True)
    v_each = total_v/qty if v_mode == "Equal across bolts" else st.number_input("Shear per bolt (kN)", min_value=0.0, value=2.5)

st.subheader("2. Joint assumptions")
c1,c2,c3 = st.columns(3)
with c1: planes = st.selectbox("Number of shear planes", [1,2])
with c2: shear_location = st.selectbox("Shear plane location", ["Threads included","Unthreaded shank"])
with c3:
    st.checkbox("Friction-grip / slip-critical joint", value=False, disabled=True)
    st.caption("Slip resistance is not calculated in this MVP.")

As = At if shear_location == "Threads included" else math.pi*d*d/4
t_nom = At*fu/1000
t_allow = t_nom/sf
v_nom = .6*fu*As*planes/1000
v_allow = v_nom/sf
tr = t_each/t_allow if t_allow else 0
vr = v_each/v_allow if v_allow else 0
interaction = tr**2 + vr**2
status = "PASS — PRELIMINARY SCREEN" if interaction <= 1 else "FAIL — REVIEW REQUIRED"

st.subheader("3. Results")
m1,m2,m3,m4 = st.columns(4)
m1.metric("Tensile stress area", f"{At:.2f} mm²")
m2.metric("Tensile allowable / bolt", f"{t_allow:.2f} kN")
m3.metric("Shear allowable / bolt", f"{v_allow:.2f} kN")
m4.metric("Combined interaction", f"{interaction:.3f}")
if interaction <= 1: st.success(status)
else: st.error(status)

rows = [
("Bolt size",size),("Thread pitch",f"{p} mm"),("Property class",grade),
("Assumed nominal tensile strength Fu",f"{fu} MPa"),("Assumed nominal yield strength Fy",f"{fy} MPa"),
("Tensile stress area At",f"{At:.3f} mm²"),("Shear area used",f"{As:.3f} mm²"),
("Bolt quantity",qty),("Safety factor",sf),("Tension per bolt",f"{t_each:.3f} kN"),
("Shear per bolt",f"{v_each:.3f} kN"),("Nominal tensile capacity per bolt",f"{t_nom:.3f} kN"),
("Screening tensile allowable per bolt",f"{t_allow:.3f} kN"),("Nominal shear capacity per bolt",f"{v_nom:.3f} kN"),
("Screening shear allowable per bolt",f"{v_allow:.3f} kN"),("Tension utilization",f"{tr:.3f}"),
("Shear utilization",f"{vr:.3f}"),("Combined interaction T² + V²",f"{interaction:.3f}"),
("Overall result",status)]
report = pd.DataFrame(rows, columns=["Parameter","Value"])
st.dataframe(report, use_container_width=True, hide_index=True)
st.download_button("Download bolt calculation report (CSV)", report.to_csv(index=False).encode(), "bolt_strength_report.csv", "text/csv")

st.markdown("### Calculation basis")
st.latex(r"A_t \\approx \\frac{\\pi}{4}(d-0.9382p)^2")
st.latex(r"F_{t,nom}=A_t F_u,\\qquad F_{v,nom}=0.6F_u A_s n_s")
st.caption("Nominal capacities are divided by the user-entered safety factor. Combined interaction T² + V² is a simplified screen, not a universal code interaction equation.")

with st.expander("Not included — required for a complete bolted-joint design"):
    st.write("Proof-load resistance tables; preload and tightening torque; joint stiffness; external-load fraction; thread stripping; nut engagement; bearing and tear-out; block shear; net-section failure; prying; eccentric bolt-group loading; fatigue; vibration; slip-critical resistance; temperature and corrosion; code-specific resistance factors.")
st.caption("Version 0.1 | Verify all assumptions against the applicable fastener standard, design code and manufacturer certificate.")
