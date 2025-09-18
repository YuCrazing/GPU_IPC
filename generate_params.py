#!/usr/bin/env python3
import json
import numpy as np
from datetime import datetime
time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")[:-3]

N = 500
rng = np.random.default_rng()
eps = 1e-5

params = []
for i in range(N):
    while True:
        ball_center = rng.uniform([-0.5, -0.1, -0.5], [0.5, 0.0, 0.5]).tolist()
        ball_radius = float(rng.uniform(2e-2, 0.3))
        cloth_center = rng.uniform([-0.5, 0.0, -0.5], [0.5, 1.0, 0.5]).tolist()
        cloth_velocity = rng.uniform([-1.0, -3.0, -1.0], [1.0, 3.0, 1.0]).tolist()
        # Make sure the cloth is above the ball
        if cloth_center[1] - ball_center[1] > ball_radius + eps:
            break
    # specific_output_dir 按要求格式 sim_00000/
    specific_output_dir = f"sim_{i:05d}/"
    params.append({
        "ball_center": ball_center,
        "ball_radius": ball_radius,
        "cloth_center": cloth_center,
        "cloth_velocity": cloth_velocity,
        "specific_output_dir": specific_output_dir
    })

with open(f"params_{time_stamp}.json", "w") as f:
    json.dump(params, f, indent=2)

print(f"生成完成: params_{time_stamp}.json")
