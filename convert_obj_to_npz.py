import os
import argparse
import numpy as np
import trimesh
from tqdm import tqdm

def convert_obj_to_npz(file_prefix, base_dir, output_path, num_traj_frames=128):
    """
    将一系列OBJ格式的布料仿真数据转换为一个NPZ文件。

    Args:
        base_dir (str): 包含 'sim_xxxxx' 子目录的根目录路径。
                        例如: 'data/mesh_trajectories'
        output_path (str): 输出的 .npz 文件路径。
                           例如: 'data/cloth_trajectories.npz'
        num_traj_frames (int): 每个轨迹中用于 'traj' 张量的帧数。
                               默认值为 128 (对应 frame_000000 到 frame_000127)。
    """
    # 1. 查找所有有效的模拟轨迹目录
    try:
        sim_dirs = sorted([d for d in os.listdir(base_dir) if d.startswith('sim_')])
    except FileNotFoundError:
        print(f"错误：找不到目录 '{base_dir}'。请检查路径是否正确。")
        return

    if not sim_dirs:
        print(f"警告：在 '{base_dir}' 中没有找到任何 'sim_' 前缀的目录。")
        return

    print(f"找到了 {len(sim_dirs)} 个模拟轨迹。")

    # 2. 初始化用于存储所有轨迹数据的列表
    initial_data_list = []
    traj_data_list = []

    # 3. 遍历每个模拟轨迹目录
    # 使用 tqdm 创建一个进度条
    for sim_dir_name in tqdm(sim_dirs, desc="处理轨迹"):
        sim_path = os.path.join(base_dir, sim_dir_name)

        # --- 处理初始帧 (initial data) ---
        try:
            # 构建 file_prefix_00000.obj 的路径
            initial_frame_path = os.path.join(sim_path, f'{file_prefix}_00000.obj')

            # 使用 trimesh 加载网格
            # process=False 可以在加载大型文件时提高速度，因为它跳过了trimesh的内部处理步骤
            initial_mesh = trimesh.load(initial_frame_path, process=False)
            
            # 提取顶点位置 (N_V, 3) 和 UV 坐标 (N_V, 2)
            vertices = initial_mesh.vertices
            try:
                uvs = initial_mesh.visual.uv
            except AttributeError:
                print(f"\n警告：在 {initial_frame_path} 中未找到UV坐标。生成默认UV。")
                uvs = np.zeros((vertices.shape[0], 2))  # 生成默认UV

            # 检查顶点和UV数量是否匹配
            if vertices.shape[0] != uvs.shape[0]:
                print(f"\n警告：在 {initial_frame_path} 中顶点数和UV坐标数不匹配。跳过此轨迹。")
                continue

            # 合并成 (N_V, 5) 的数组
            initial_frame_data = np.concatenate([vertices, uvs], axis=1)
            initial_data_list.append(initial_frame_data)

        except Exception as e:
            print(f"\n处理初始帧 {initial_frame_path} 时出错: {e}。跳过此轨迹。")
            continue

        # --- 处理轨迹帧 (traj data) ---
        current_traj_frames = []
        has_error = False
        for i in range(0, num_traj_frames):
            frame_filename = f'{file_prefix}_{i:05d}.obj'
            frame_path = os.path.join(sim_path, frame_filename)
            
            try:
                # 加载网格并只提取顶点
                mesh = trimesh.load(frame_path, process=False)
                current_traj_frames.append(mesh.vertices)
            except Exception as e:
                print(f"\n处理轨迹帧 {frame_path} 时出错: {e}。中止处理此轨迹。")
                has_error = True
                break
        
        # 如果当前轨迹处理时发生错误，则不将其添加到最终列表中
        if has_error:
            # 由于轨迹不完整，我们也不应该保留其对应的初始帧数据
            initial_data_list.pop()
            continue

        # 将当前轨迹的所有帧堆叠成一个 (T, N_V, 3) 的数组
        traj_data = np.stack(current_traj_frames, axis=0)
        traj_data_list.append(traj_data)

    # 4. 将数据列表转换为最终的 Numpy 数组
    if not initial_data_list or not traj_data_list:
        print("没有成功处理任何数据，不生成 NPZ 文件。")
        return
        
    try:
        initial_tensor = np.stack(initial_data_list, axis=0)
        traj_tensor = np.stack(traj_data_list, axis=0)
        print(initial_tensor[0, :5])
        print(traj_tensor[0, 0, :5])
    except ValueError as e:
        print(f"\n错误：无法将数据堆叠成最终的张量。这通常是因为不同轨迹的顶点数(N_V)不一致。")
        print(f"错误详情: {e}")
        return

    # 5. 打印最终张量的形状以供验证
    print("\n数据转换完成。")
    print(f"  - 'initial' 张量的形状: {initial_tensor.shape}")
    print(f"  - 'traj' 张量的形状: {traj_tensor.shape}")

    # 6. 保存为压缩的 .npz 文件
    # 使用 savez_compressed 可以显著减小文件大小
    np.savez_compressed(output_path, initial=initial_tensor, traj=traj_tensor)
    print(f"数据已成功保存到: {output_path}")


if __name__ == '__main__':


    # --- 使用argparse设置命令行参数，使脚本更灵活 ---
    parser = argparse.ArgumentParser(
        description="OBJ文件转换为NPZ格式的布料仿真数据。",
        formatter_class=argparse.RawTextHelpFormatter # 保持帮助信息格式
    )

    parser.add_argument(
        "--file_prefix",
        required=True,
        help="输入OBJ文件的前缀，例如 'frame_' (对应 'frame_00000.obj')。"
    )
    parser.add_argument(
        "--input_dir",
        required=True,
        help="包含源 .obj 文件的输入目录。\n例如: C:/path/to/input_objs"
    )
    parser.add_argument(
        "--output_path",
        required=True,
        help="用于保存处理后 .npz 文件的输出路径。\n例如: C:/path/to/output.npz"
    )
    parser.add_argument(
        "--num_traj_frames",
        type=int,
        default=128,
        help="每个轨迹中用于 'traj' 张量的帧数 (默认: 128)。\n对应 frame_000000 到 frame_000127"
    )

    args = parser.parse_args()

    # --- 配置参数 ---
    # 设置包含 'sim_xxxxx' 文件夹的基础目录
    BASE_DATA_DIR = args.input_dir
    
    # 设置输出 .npz 文件的路径和名称
    OUTPUT_NPZ_FILE = args.output_path
    
    # 设置每个轨迹要读取的帧数 (从 frame_000001 开始)
    NUM_TRAJECTORY_FRAMES = args.num_traj_frames

    # --- 执行转换 ---
    convert_obj_to_npz(args.file_prefix, BASE_DATA_DIR, OUTPUT_NPZ_FILE, NUM_TRAJECTORY_FRAMES)
