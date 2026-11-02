"""
Postural Sway & Center of Pressure (COP) Statokinesigram Engine.
Provides deterministic, zero-dependency calculation of 95% confidence ellipse area,
path length, mean sway velocity, and Romberg Quotient for proprioceptive stability.
"""

import math
from typing import Dict, Any, List, Optional


class PosturalSwayClient:
    """
    Deterministic client for analyzing Center of Pressure (COP) statokinesigram trajectories.
    Pure Python standard library implementation based on ISO and clinical posturography standards.
    """

    def __init__(self):
        pass

    def analyze_cop_sway(
        self,
        x_coords_mm: List[float],
        y_coords_mm: List[float],
        sample_rate_hz: float = 50.0
    ) -> Dict[str, Any]:
        """
        Analyzes 2D COP statokinesigram trajectory.
        x: mediolateral (ML) displacement in mm.
        y: anterior-posterior (AP) displacement in mm.
        """
        n = min(len(x_coords_mm), len(y_coords_mm))
        if n < 5:
            return {"error": "Insufficient COP samples (minimum 5 required)"}

        x = x_coords_mm[:n]
        y = y_coords_mm[:n]
        total_time_sec = n / sample_rate_hz

        # Mean positions and detrending
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        dx_vals = [xi - mean_x for xi in x]
        dy_vals = [yi - mean_y for yi in y]

        # Path length computation (sway path length in mm)
        path_length_mm = 0.0
        for i in range(n - 1):
            step = math.sqrt((x[i + 1] - x[i]) ** 2 + (y[i + 1] - y[i]) ** 2)
            path_length_mm += step

        mean_velocity_mm_s = path_length_mm / max(0.01, total_time_sec)

        # Variance and Covariance matrix
        s_xx = sum(dx * dx for dx in dx_vals) / (n - 1)
        s_yy = sum(dy * dy for dy in dy_vals) / (n - 1)
        s_xy = sum(dx * dy for dx, dy in zip(dx_vals, dy_vals)) / (n - 1)

        # Eigenvalues of 2x2 covariance matrix
        trace = s_xx + s_yy
        det = s_xx * s_yy - s_xy * s_xy
        disc = max(0.0, trace * trace - 4.0 * det)
        sqrt_disc = math.sqrt(disc)
        lambda1 = max(0.0001, (trace + sqrt_disc) / 2.0)
        lambda2 = max(0.0001, (trace - sqrt_disc) / 2.0)

        # 95% Confidence Ellipse Area (CEA95 in mm^2): ~ 2 * pi * 3.0 * sqrt(lambda1 * lambda2)
        # where 3.0 corresponds to chi-square critical value at p=0.05 (approx 5.991 / 2)
        ellipse_area_mm2 = 2.0 * math.pi * 3.0 * math.sqrt(lambda1 * lambda2)

        # Postural Stability Index (0 - 100):
        # Baseline healthy quiet standing: mean velocity ~ 8-15 mm/s, ellipse area ~ 50-200 mm^2
        vel_penalty = min(50.0, (mean_velocity_mm_s / 25.0) * 50.0)
        area_penalty = min(50.0, (ellipse_area_mm2 / 400.0) * 50.0)
        psi_score = round(max(5.0, min(100.0, 100.0 - vel_penalty - area_penalty + 15.0)), 1)

        if psi_score >= 80.0:
            status = "SUPERIOR_POSTURAL_STABILITY"
            interpretation = "Minimal center of pressure drift; excellent vestibular and proprioceptive integration."
        elif psi_score >= 60.0:
            status = "NORMAL_QUIET_STANDING_BALANCE"
            interpretation = "Standard postural sway envelope consistent with normative adult stability."
        elif psi_score >= 40.0:
            status = "MODERATE_POSTURAL_UNSTEADINESS"
            interpretation = "Elevated sway velocity and expanded ellipse area; potential lower limb fatigue or sensory conflict."
        else:
            status = "MARKED_POSTURAL_INSTABILITY"
            interpretation = "Excessive center of pressure excursion. Fall risk elevated; recommend balance training and vestibular review."

        return {
            "sample_count": n,
            "duration_sec": round(total_time_sec, 2),
            "mean_x_ml_mm": round(mean_x, 2),
            "mean_y_ap_mm": round(mean_y, 2),
            "total_path_length_mm": round(path_length_mm, 2),
            "mean_sway_velocity_mm_s": round(mean_velocity_mm_s, 2),
            "confidence_ellipse_area_95_mm2": round(ellipse_area_mm2, 2),
            "postural_stability_index": psi_score,
            "status": status,
            "interpretation": interpretation
        }

    def compute_romberg_quotient(
        self,
        eyes_open_sway_area_mm2: float,
        eyes_closed_sway_area_mm2: float
    ) -> Dict[str, Any]:
        """
        Calculates Romberg Quotient (RQ): Sway Area Eyes Closed / Sway Area Eyes Open.
        Normative range is 1.0 to 2.2.
        RQ > 2.5 reveals heavy visual compensation for underlying somatosensory/vestibular deficit.
        """
        if eyes_open_sway_area_mm2 <= 0:
            return {"error": "Eyes open sway area must be positive"}

        rq = round(eyes_closed_sway_area_mm2 / max(0.1, eyes_open_sway_area_mm2), 2)

        if rq < 1.0:
            tier = "PARADOXICAL_STABILIZATION"
            desc = "Sway area did not increase upon eye closure; possible visual distraction during eyes-open phase."
        elif rq <= 2.2:
            tier = "NORMAL_SOMATOSENSORY_WEIGHTING"
            desc = "Standard physiological response: moderate sensory re-weighting to proprioceptive/vestibular channels."
        elif rq <= 3.0:
            tier = "MODERATE_VISUAL_DEPENDENCE"
            desc = "Higher reliance on vision to stabilize quiet stance; subtle proprioceptive fatigue present."
        else:
            tier = "MARKED_VISUAL_DEPENDENCE_POSITIVE_ROMBERG"
            desc = "Sway area expanded over 3-fold without vision. Prominent somatosensory or vestibular deficiency indicated."

        return {
            "eyes_open_area_mm2": eyes_open_sway_area_mm2,
            "eyes_closed_area_mm2": eyes_closed_sway_area_mm2,
            "romberg_quotient": rq,
            "classification": tier,
            "guidance": desc
        }
