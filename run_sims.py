#!/usr/bin/env python3
import json
import subprocess
import os
import argparse

if __name__ == "__main__":

    # --- 使用argparse设置命令行参数，使脚本更灵活 ---
    parser = argparse.ArgumentParser(
        description="运行布料仿真程序的批处理脚本。",
        formatter_class=argparse.RawTextHelpFormatter # 保持帮助信息格式
    )

    parser.add_argument(
        "--input_params",
        required=True,
        help="包含仿真参数的JSON文件路径。\n例如: params.json"
    )

    args = parser.parse_args()

    # 修改为你的可执行文件路径
    EXEC_PATH = "/home/yuzhang/repos/GPU_IPC/build/gipc"

    with open(args.input_params, "r") as f:
        all_params = json.load(f)

    failed_runs = []
    # for p in all_params:
    for i, p in enumerate(all_params):
        # if i != 24:
        #     continue
        specific_output_dir = "/home/yuzhang/repos/GPU_IPC/Output/sims/" + p["specific_output_dir"]
        args = [
            EXEC_PATH,
            str(p["ball_center"][0]), str(p["ball_center"][1]), str(p["ball_center"][2]),
            str(p["ball_radius"]),
            str(p["cloth_center"][0]), str(p["cloth_center"][1]), str(p["cloth_center"][2]),
            str(p["cloth_velocity"][0]), str(p["cloth_velocity"][1]), str(p["cloth_velocity"][2]),
            specific_output_dir
        ]
        print("Running:", " ".join(args))
        # 创建输出目录
        os.makedirs(specific_output_dir, exist_ok=True)
        # 调用可执行文件
        res = subprocess.run(args, check=False)
        # res = subprocess.run(args, env={"CUDA_VISIBLE_DEVICES": "0"}, check=False)
        if res.returncode != 0:
            print(f"Simulation failed for params set {i}, return code: {res.returncode}")
            failed_runs.append((i, res.returncode))
    print("All simulations completed.")
    if failed_runs:
        print("Failed runs:")
        for run in failed_runs:
            print(f"Params set {run[0]} failed with return code {run[1]}")
