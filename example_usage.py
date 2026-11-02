"""
Example usage for Postural Sway & Center of Pressure (COP) Skill.
Demonstrates analyzing quiet stance COP statokinesigram and Romberg ratio.
"""

import math
from client import PosturalSwayClient


def generate_synthetic_cop(n_points: int = 150, radius: float = 4.0, noise: float = 1.0):
    x_vals = []
    y_vals = []
    for i in range(n_points):
        theta = i * 0.15
        x = radius * math.sin(theta) + (i % 5 - 2) * 0.2 * noise
        y = radius * 1.5 * math.cos(theta * 0.8) + (i % 7 - 3) * 0.3 * noise
        x_vals.append(round(x, 2))
        y_vals.append(round(y, 2))
    return x_vals, y_vals


def main():
    client = PosturalSwayClient()

    print("=== 1. Analyzing Center of Pressure Statokinesigram (Quiet Stance) ===")
    x_eo, y_eo = generate_synthetic_cop(n_points=200, radius=3.5)
    sway_res = client.analyze_cop_sway(x_eo, y_eo, sample_rate_hz=50.0)
    print(f"Total Path Length: {sway_res['total_path_length_mm']} mm")
    print(f"Mean Sway Velocity: {sway_res['mean_sway_velocity_mm_s']} mm/s")
    print(f"95% Confidence Ellipse Area: {sway_res['confidence_ellipse_area_95_mm2']} mm^2")
    print(f"Postural Stability Index: {sway_res['postural_stability_index']} / 100")
    print(f"Status: {sway_res['status']}")
    print(f"Interpretation: {sway_res['interpretation']}")

    print("\n=== 2. Evaluating Romberg Quotient (Eyes Open vs Eyes Closed) ===")
    area_eo = sway_res['confidence_ellipse_area_95_mm2']
    area_ec = area_eo * 1.65  # Typical mild expansion without vision
    romberg_res = client.compute_romberg_quotient(area_eo, area_ec)
    print(f"Eyes Open Area: {romberg_res['eyes_open_area_mm2']} mm^2 | Eyes Closed Area: {romberg_res['eyes_closed_area_mm2']} mm^2")
    print(f"Romberg Quotient: {romberg_res['romberg_quotient']}")
    print(f"Classification: {romberg_res['classification']}")
    print(f"Guidance: {romberg_res['guidance']}")


if __name__ == "__main__":
    main()
