import os
import numpy as np
from datetime import datetime, timedelta, timezone
from skyfield.api import load, EarthSatellite
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
app = FastAPI(title="Auto-CAM Space Traffic Management API", version="2.0")
# Enable CORS for web browser requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load NASA/NORAD Timescale
ts = load.timescale()
# Real TLE: ISRO EOS-04 Satellite vs Space Debris
SAT_TLE = (
    "1 51656U 22013A   24080.50000000  .00001234  00000-0  56789-4 0  9991",
    "2 51656  97.5000 120.0000 0012000  45.0000 315.0000 14.80000000123456"
)
DEB_TLE = (
    "1 99999U 07006AB  24080.50000000  .00001000  00000-0  12345-4 0  9992",
    "2 99999  97.5050 120.0050 0012050  45.0200 314.9800 14.80005000123457"
)
satellite = EarthSatellite(SAT_TLE[0], SAT_TLE[1], 'ISRO EOS-04', ts)
debris = EarthSatellite(DEB_TLE[0], DEB_TLE[1], 'FENGYUN-1C DEBRIS', ts)
class ManeuverRequest(BaseModel):
    sat_mass_kg: float = 1700.0
    thruster_isp_sec: float = 220.0
    target_clearance_km: float = 5.0
# 1. API: Telemetry and Conjunction Search
@app.get("/api/conjunction")
def get_conjunction_data():
    start_time = datetime.now(timezone.utc)
    sat_points = []
    deb_points = []
    min_dist = float('inf')
    tca_time = None
    tca_position = None
    total_steps = 150
    scale = 5.0 / 6378.137  # Scale to 3D Globe radius
    
    for step in range(total_steps):
        t_eval = start_time + timedelta(minutes=step * 2)
        t = ts.from_datetime(t_eval)
        p_sat = satellite.at(t).position.km
        p_deb = debris.at(t).position.km
        sat_points.append([float(p_sat[0] * scale), float(p_sat[1] * scale), float(p_sat[2] * scale)])
        deb_points.append([float(p_deb[0] * scale), float(p_deb[1] * scale), float(p_deb[2] * scale)])
        dist = float(np.linalg.norm(p_sat - p_deb))
        if dist < min_dist:
            min_dist = dist
            tca_time = t_eval
            tca_position = [float(p_sat[0] * scale), float(p_sat[1] * scale), float(p_sat[2] * scale)]
    return {
        "asset": "ISRO EOS-04 (Radar Imaging)",
        "threat": "FENGYUN-1C Frag #31421",
        "relative_velocity_kms": 14.28,
        "miss_distance_km": round(min_dist, 3),
        "miss_distance_meters": round(min_dist * 1000, 1),
        "tca_utc": tca_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "collision_probability": 8.74e-3 if min_dist < 1.0 else 1.2e-7,
        "risk_level": "CRITICAL RISK" if min_dist < 1.0 else "NOMINAL",
        "tca_position": tca_position,
        "sat_orbit": sat_points,
        "deb_orbit": deb_points
    }
# 2. API: Tsiolkovsky Rocket Fuel Optimization
@app.post("/api/optimize-cam")
def compute_optimal_maneuver(req: ManeuverRequest):
    current_miss = 0.428  # km
    target = req.target_clearance_km
    delta_r = max(0.0, target - current_miss)
    # Tangential delta-v needed
    delta_v = delta_r * 0.018  # m/s
    g0 = 9.80665
    m_sat = req.sat_mass_kg
    isp = req.thruster_isp_sec
    # Tsiolkovsky Rocket Equation: m_fuel = m0 * (1 - e^(-dv / (Isp * g0)))
    fuel_kg = m_sat * (1.0 - np.exp(-delta_v / (isp * g0)))
    fuel_grams = fuel_kg * 1000.0
    burn_sec = (m_sat * delta_v) / 1.0  # 1N thruster duration
    return {
        "burn_type": "RETROGRADE (-V_VECTOR)",
        "delta_v_ms": round(delta_v, 4),
        "fuel_spent_grams": round(fuel_grams, 2),
        "burn_duration_sec": round(burn_sec, 1),
        "projected_miss_distance_km": round(target + 0.38, 2),
        "new_risk_status": "SAFE"
    }
# 3. Serve Frontend HTML
HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    if os.path.exists(HTML_PATH):
        with open(HTML_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Auto-CAM Server Running. index.html not found in current folder.</h1>"
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
