# filename: create_tet_mesh.py

import gmsh
import sys
import os

def create_tet_mesh(obj_file_path, msh_file_path):
    """
    使用 Gmsh 将 OBJ 表面网格文件转换为四面体网格 MSH 文件。

    为了成功生成四面体网格，输入的 OBJ 文件必须是一个封闭的（watertight）
    且无自相交的流形表面（manifold surface）。

    Args:
        obj_file_path (str): 输入的 .obj 文件路径。
        msh_file_path (str): 输出的 .msh 文件路径。
    """
    if not os.path.exists(obj_file_path):
        print(f"错误：输入文件不存在 -> {obj_file_path}")
        return

    # 初始化 Gmsh
    gmsh.initialize()

    try:
        # 设置 Gmsh 日志的详细程度
        # 0: silent, 1: errors, 2: warnings, 3: direct, 4: information, 5: status, 99: debug
        gmsh.option.setNumber("General.Verbosity", 3)

        # 设置输出的 MSH 文件格式
        # 1: MSH ASCII v1.0 (obsolete)
        # 2: MSH ASCII v2.2
        # 3: MSH Binary v2.2
        # 4: MSH ASCII v4.1
        # 5: MSH Binary v4.1
        # 我们根据要求选择版本 2.2 ASCII
        gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
        gmsh.option.setNumber("Mesh.Format", 0) # 0 for ASCII, 1 for Binary

        # 新建一个模型
        gmsh.model.add(os.path.splitext(os.path.basename(msh_file_path))[0])

        print(f"正在读取 OBJ 文件: {obj_file_path} ...")
        # 合并（导入）OBJ 文件。Gmsh 会自动读取表面网格。
        gmsh.merge(obj_file_path)

        # 为了从一个表面网格生成体网格，我们需要定义一个体积。
        # 首先，我们需要找到由 OBJ 文件导入的所有表面。
        surfaces = gmsh.model.getEntities(2) # 获取所有二维实体（表面）
        if not surfaces:
            print("错误：在 OBJ 文件中没有找到任何表面。")
            return

        surface_tags = [s[1] for s in surfaces]

        # 创建一个“表面环”(Surface Loop)来包围一个体积。
        # 对于一个封闭的表面（如从一个 watertight OBJ 文件导入的），
        # 所有的表面构成一个单独的表面环。
        surface_loop = gmsh.model.geo.addSurfaceLoop(surface_tags)

        # 从表面环创建一个体积。
        gmsh.model.geo.addVolume([surface_loop])

        # 同步 CAD 内核，这是在进行几何操作后必须执行的步骤。
        gmsh.model.geo.synchronize()

        # --- 可选的网格尺寸设置 ---
        # 你可以取消下面的注释来控制网格密度
        # min_size = 0.1  # 最小网格尺寸
        # max_size = 0.5  # 最大网格尺寸
        # gmsh.model.mesh.setSize(gmsh.model.getEntities(0), min_size) # 设置点的尺寸
        # gmsh.model.mesh.setSize(gmsh.model.getEntities(1), max_size) # 设置线的尺寸

        print("正在生成三维四面体网格...")
        # 生成三维网格（1=一维, 2=二维, 3=三维）
        gmsh.model.mesh.generate(3)

        print(f"正在将网格写入 MSH 文件: {msh_file_path} ...")
        # 将生成的网格写入文件
        gmsh.write(msh_file_path)

        print("处理完成！")

    except Exception as e:
        print(f"发生错误: {e}")

    finally:
        # 始终确保在最后关闭 Gmsh
        gmsh.finalize()


if __name__ == '__main__':
    # --- 命令行接口 ---
    # 使用方法:
    # python create_tet_mesh.py path/to/your/input.obj path/to/your/output.msh

    if len(sys.argv) != 3:
        print("用法: python create_tet_mesh.py <input_obj_file> <output_msh_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    create_tet_mesh(input_file, output_file)