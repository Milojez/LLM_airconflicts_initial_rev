import math
import pyproj
import numpy as np
import json

# Load aircraft data from JSON file
with open("-", "r") as file:
    aircraft_data = json.load(file)

# Assign individual flights
flight1 = aircraft_data[0]
flight2 = aircraft_data[1]

def lat_lon_to_utm(latitude, longitude):
    zone_number = int((longitude + 180) / 6) + 1
    utm_crs = pyproj.CRS(f"EPSG:326{zone_number:02d}")
    if latitude < 0:
        utm_crs = pyproj.CRS(f"EPSG:327{zone_number:02d}")
    crs_wgs84 = pyproj.CRS("EPSG:4326")
    transformer = pyproj.Transformer.from_crs(crs_wgs84, utm_crs, always_xy=True)
    x, y = transformer.transform(longitude, latitude)
    return x, y

def heading_to_velocity(heading_deg, speed_knots):
    heading_rad = math.radians(heading_deg)
    speed_mps = speed_knots * 0.514444  # convert knots to m/s
    vx = speed_mps * math.sin(heading_rad)
    vy = speed_mps * math.cos(heading_rad)
    return np.array([vx, vy])

def compute_cpa(p1, v1, p2, v2):
    # Relative position and velocity
    dp = p2 - p1
    dv = v2 - v1
    dv_norm_sq = np.dot(dv, dv)

    if dv_norm_sq == 0:
        return np.linalg.norm(dp)  # same velocity, just measure initial separation

    # Time to CPA
    t_cpa = -np.dot(dp, dv) / dv_norm_sq

    # Ensure time is not negative
    t_cpa = max(t_cpa, 0)

    # Position at CPA
    pos1_cpa = p1 + v1 * t_cpa
    pos2_cpa = p2 + v2 * t_cpa

    return np.linalg.norm(pos1_cpa - pos2_cpa)

def find_min_heading_change(flight1, flight2, required_sep_nm=5):
    # Convert positions to UTM
    p1 = np.array(lat_lon_to_utm(flight1["latitude"], flight1["longitude"]))
    p2 = np.array(lat_lon_to_utm(flight2["latitude"], flight2["longitude"]))

    # Aircraft 2 velocity (fixed)
    v2 = heading_to_velocity(flight2["heading (degrees)"], flight2["groundspeed (knots)"])

    original_heading = flight1["heading (degrees)"]
    gs1 = flight1["groundspeed (knots)"]
    required_sep_m = required_sep_nm * 1852  # convert NM to meters

    # Try different heading changes, starting from 0 and increasing
    for delta in np.arange(0, 90, 0.1):  # check up to 90° deviation
        for sign in [-1, 1]:  # try left and right
            new_heading = (original_heading + sign * delta) % 360
            v1 = heading_to_velocity(new_heading, gs1)
            distance = compute_cpa(p1, v1, p2, v2)
            if distance >= required_sep_m:
                return {
                    "minimal_heading_change_degrees": round(delta, 2),
                    "new velocity": v1,
                    "new_heading_degrees": round(new_heading, 2),
                    "CPA_distance_nm": round(distance / 1852, 2)
                }
    return {"error": "No heading change within ±90° gives 5 NM separation."}

# #RESULT
test = find_min_heading_change(flight1, flight2, required_sep_nm=5)
print(test)