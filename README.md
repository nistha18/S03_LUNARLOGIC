🛰️ Auto-CAM: Autonomous Collision Avoidance Maneuver Engine
Next-Gen Space Traffic Management & Fuel-Optimal Orbital Safety for Indian Space Assets

Domain
FastAPI
Three.js
ISRO

📌 Project Overview

Auto-CAM is an autonomous space traffic management decision-support platform designed to solve the $500M satellite collision dilemma in Low Earth Orbit (LEO). Powered by high-precision SGP4 orbital propagation and Tsiolkovsky rocket equation optimization, Auto-CAM detects conjunctions in real-time and computes fuel-optimal thruster burn vectors (Δv), reducing operational decision latency from hours to under 3 seconds.

Developed for ASTRA 2026 (Anterix | VIT Bhopal University) under Domain 06: Sustainable Space & Space Environment.

🚨 The Problem in Low Earth Orbit
Lethal Debris Belt: Over 30,000 tracked debris fragments travel at hypervelocities (~28,000 km/h). Even a 1 cm paint fleck or fragment can destroy a multi-crore national space asset.
Alert Fatigue: Satellite operators receive thousands of Conjunction Data Messages (CDMs) weekly, with 95% being low-risk false alarms due to sensor uncertainty.
The Propellant Penalty: Unnecessary avoidance burns waste precious on-board propellant (Hydrazine/Xenon), directly cutting years off an active satellite's mission lifespan.
💡 System Architecture

[ CelesTrak / Space-Track Live Telemetry ] │ ▼ [ SGP4 Orbital Propagator ] (Calculates 72h future orbits & Time of Closest Approach - TCA) │ ▼ [ Autonomous Risk Triage Engine ] (Identifies critical conjunctions: Miss Distance < 1.0 km) │ ▼ [ Optimal Burn Vector Optimizer ] (Calculates minimal Δv & fuel mass consumed via Rocket Equation) │ ▼ [ 3D Cyber Mission Control WebGL Interface ] (Renders real-time Earth, Hazard Trajectory, and Safe Evasion Orbit)

---
## 🔬 Core Physics & Mathematical Formulation
### 1. Conjunction Geometry
At time $t$, Euclidean separation between satellite $\vec{r}_{\text{sat}}(t)$ and debris $\vec{r}_{\text{deb}}(t)$:
$$d(t) = \|\vec{r}_{\text{sat}}(t) - \vec{r}_{\text{deb}}(t)\|$$
$\text{TCA}$ (Time of Closest Approach) is found where $\frac{d}{dt} d(t) = 0$.
### 2. Along-Track Evasion Impulse
A tangential thrust ($\Delta v$) applied 1 orbit prior (~90 mins) alters the semi-major axis $a$, expanding miss distance at TCA from 400 meters to >5.0 km with minimal energy expenditure.
### 3. Tsiolkovsky Fuel Consumption
Propellant mass consumed is calculated using:
$$m_{\text{fuel}} = m_{\text{dry}} \cdot \left(1 - e^{-\frac{\Delta v}{I_{\text{sp}} \cdot g_0}}\right)$$
*For ISRO EOS-04 ($1700\text{ kg}$ dry mass, $I_{\text{sp}} = 220\text{ s}$), a $0.082\text{ m/s}$ avoidance burn consumes **only 64.8 grams of fuel**!*
---
## 🛠️ Tech Stack
* **Backend:** Python 3.10+, FastAPI, Uvicorn, Skyfield (NASA/NORAD SGP4), NumPy, SciPy
* **Frontend:** Three.js (WebGL), OrbitControls, Tailwind CSS, Space Grotesk typography
* **Data Standard:** NORAD Two-Line Element (TLE) / CCSDS Conjunction Data Message (CDM)
---
## 🚀 Quickstart Guide (Run Locally)
### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/autocam-space-traffic-management.git
cd autocam-space-traffic-management