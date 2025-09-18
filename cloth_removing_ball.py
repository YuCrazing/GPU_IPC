# -*- coding: utf-8 -*-
import os
import sys
import argparse

# 尝试导入Houdini的Python模块'hou'。
# 如果失败，说明脚本不是在Houdini环境中运行的。
try:
    import hou
except ImportError:
    print("错误：此脚本必须在Houdini的Python环境 (hython) 中运行。")
    print("请使用 'hython your_script_name.py' 来执行。")
    sys.exit(1)

def batch_process_geometry(hip_path, input_dir, output_dir):
    """
    使用指定的Houdini文件批量处理OBJ文件。

    :param hip_path: .hip文件的完整路径。
    :param input_dir: 包含输入OBJ文件的目录。
    :param output_dir: 用于保存输出OBJ文件的目录。
    """
    # --- 1. 加载Houdini场景文件 ---
    try:
        # 使用 hou.hipFile.load 加载场景
        hou.hipFile.load(hip_path)
        print(f"成功加载Houdini文件: {hip_path}")
    except hou.LoadWarning as e:
        print(f"加载Houdini文件时出现警告: {e}")
    except Exception as e:
        print(f"加载Houdini文件时发生致命错误: {e}")
        return

    # --- 2. 检查并创建输出目录 ---
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已创建输出目录: {output_dir}")

    # --- 3. 定位关键节点 ---
    # 根据您的截图，输入节点路径是 /obj/file1
    input_node = hou.node("/obj/file1/file1")
    if not input_node:
        print("错误：在 /obj/file1/file1 未找到输入节点 'file1'。请检查节点路径。")
        return

    # 您的节点图在blast1处结束，我们需要一个输出节点来保存结果。
    # 我们将连接到blast1；如果找不到，则备用连接到file1。
    last_node_in_chain = hou.node("/obj/file1/blast1")
    if not last_node_in_chain:
        print("警告：在 /obj/file1/blast1 未找到节点 'blast1'。将从 'file1' 节点输出。")
        last_node_in_chain = input_node
    
    print(f"将从节点 '{last_node_in_chain.name()}' 的输出创建结果。")

    # # --- 4. 创建并配置ROP几何体输出节点 ---
    # # 这是自动化保存几何体的标准做法。
    # obj_context = hou.node("/obj")
    # # 创建一个唯一的节点名以避免冲突
    # output_rop_name = "temp_script_output_rop"
    # output_rop = obj_context.createNode("rop_geometry", output_rop_name)
    
    # # 将ROP节点的输入连接到处理链的末端
    # output_rop.setInput(0, last_node_in_chain)

    output_rop = hou.node("/obj/file1/rop_geometry1")
    if not output_rop:
        print("错误：在 /obj/file1/rop_geometry1 未找到ROP节点 'rop_geometry1'。请检查节点路径。")
        return

    
    # --- 5. 递归查找并处理所有输入OBJ文件 ---
    processed_count = 0
    try:
        # 使用 os.walk 递归遍历输入目录
        for root, _, files in os.walk(input_dir):
            for filename in files:
                # 检查文件是否为 .obj 文件（不区分大小写）
                if not filename.lower().endswith(".obj"):
                    continue

                processed_count += 1

                # a. 构建完整的输入文件路径
                input_path = os.path.join(root, filename).replace('\\', '/')

                # b. 构建输出路径，同时保留相对目录结构
                #    获取当前文件相对于输入根目录的路径
                relative_dir = os.path.relpath(root, input_dir)
                
                #    构建目标输出目录
                #    如果文件直接在input_dir下, relative_dir会是'.', os.path.join会正确处理
                target_output_dir = os.path.join(output_dir, relative_dir)

                #    确保目标子目录存在
                if not os.path.exists(target_output_dir):
                    os.makedirs(target_output_dir)

                # c. 根据您的命名规则创建输出文件名
                #    例如: "surf_0001.obj" -> "processed_0001.obj"
                output_filename = filename.replace('surf_', 'processed_')

                # d. 构建最终的完整输出文件路径
                output_path = os.path.join(target_output_dir, output_filename).replace('\\', '/')

                print(f"\n正在处理: {filename}")
                print(f"  输入: {input_path}")
                print(f"  输出: {output_path}")

                # e. 更新Houdini节点参数
                input_node.parm("file").set(input_path)
                output_rop.parm("sopoutput").set(output_path)

                # f. 执行渲染（保存文件）
                try:
                    output_rop.render()
                    print(f"  -> 成功保存: {output_filename}")
                except hou.Error as e:
                    print(f"  -> 保存文件时出错: {e}")

        if processed_count == 0:
            print(f"警告：在输入目录 '{input_dir}' 及其子目录中未找到任何 .obj 文件。")

    finally:
        # --- 6. 清理 ---
        # 无论处理成功与否，都删除ROP节点
        if output_rop and hou.node(output_rop.path()): # 检查节点是否还存在
            output_rop.destroy()
            print("\n已清理输出节点。")

    print(f"\n所有文件处理完毕，共处理了 {processed_count} 个文件。")



if __name__ == "__main__":
    # --- 使用argparse设置命令行参数，使脚本更灵活 ---
    parser = argparse.ArgumentParser(
        description="使用Houdini场景文件批量处理OBJ文件。",
        formatter_class=argparse.RawTextHelpFormatter # 保持帮助信息格式
    )
    parser.add_argument(
        "--hip",
        required=True,
        help="Houdini场景文件 (.hip) 的路径。\n例如: C:/path/to/cloth_removing_ball.hip"
    )
    parser.add_argument(
        "--input_dir",
        required=True,
        help="包含源 .obj 文件的输入目录。\n例如: C:/path/to/input_objs"
    )
    parser.add_argument(
        "--output_dir",
        required=True,
        help="用于保存处理后 .obj 文件的输出目录。\n例如: C:/path/to/output_results"
    )

    args = parser.parse_args()

    # 调用主函数，传入解析后的命令行参数
    batch_process_geometry(args.hip, args.input_dir, args.output_dir)