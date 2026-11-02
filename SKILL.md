---
name: genpark-personal-agent-postural-sway-center-of-pressure-skill
description: Deterministic posturographic modeling of Center of Pressure (COP) statokinesigrams, 95% confidence ellipse area, sway velocity, and Romberg Quotient.
version: 1.0.0
author: GenPark Autonomous Agents Ecosystem
license: MIT
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
---

# Postural Sway & Center of Pressure (COP) Statokinesigram Skill

## Overview
The `genpark-personal-agent-postural-sway-center-of-pressure-skill` delivers clinical posturographic analysis to sovereign personal agents. Maintaining upright quiet stance requires constant multi-sensory integration (proprioceptive muscle spindles, vestibular labyrinthine canals, and ocular retinal slip). By processing 2D Center of Pressure (COP) timeseries from force plates, smart insoles, or inertial trackers, this skill computes statokinesigram path length, sway velocity, the 95% confidence bivariate ellipse area ($CEA_{95}$), and Romberg Quotients ($RQ$).

## Physiological Model & Mathematics
1. **Total Sway Path Length ($L$)**:
   $$L = \sum_{i=1}^{N-1} \sqrt{(x_{i+1} - x_i)^2 + (y_{i+1} - y_i)^2}$$
2. **Mean Sway Velocity ($MV$)**:
   $$MV = \frac{L}{\Delta T} \text{ mm/s}$$
3. **95% Confidence Ellipse Area ($CEA_{95}$)**:
   $$CEA_{95} = 2\pi \cdot F_{0.05, 2, N-2} \cdot \sqrt{\lambda_1 \lambda_2}$$
   where $\lambda_1, \lambda_2$ are eigenvalues of the bivariate spatial covariance matrix:
   $$\begin{bmatrix} s_{xx} & s_{xy} \\ s_{xy} & s_{yy} \end{bmatrix}$$
4. **Romberg Quotient ($RQ$)**:
   $$RQ = \frac{\text{Sway Area (Eyes Closed)}}{\text{Sway Area (Eyes Open)}}$$
   - $RQ \in [1.0, 2.2]$: Normal sensory re-weighting.
   - $RQ > 2.5$: Excessive visual dependence indicative of somatosensory or vestibular degradation.

## Tools & Endpoints
- `analyze_cop_sway`: Calculates path length, mean velocity, 95% ellipse area, and Postural Stability Index ($PSI$).
- `compute_romberg_quotient`: Evaluates sensory weighting and visual dependence ratio.
