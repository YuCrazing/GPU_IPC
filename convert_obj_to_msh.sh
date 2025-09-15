#!/bin/bash

export PATH=$PATH:/home/yuzhang/Downloads/gmsh-4.14.1-Linux64/bin

# Read input obj file from command line argument
input_obj_file=$1
if [ -z "$input_obj_file" ]; then
    echo "Usage: $0 <input_obj_file>"
    exit 1
fi
echo "Input OBJ file: $input_obj_file"
# Read output msh file from command line argument
output_msh_file=$2
if [ -z "$output_msh_file" ]; then
    echo "Usage: $0 <input_obj_file> <output_msh_file>"
    exit 1
fi
echo "Output MSH file: $output_msh_file"

tempfile=$(mktemp)
trap 'rm -f "$tempfile"' EXIT  # 脚本结束时自动删除

# 向临时文件写入多行文本
cat << EOF > "$tempfile"
// 导入 OBJ 文件，它会创建一个 Surface，ID 通常为 1
Merge "$input_obj_file";

// 将导入的 Surface (ID=1) 创建成一个 Surface Loop
Surface Loop(1) = {1};

// 使用上面的 Surface Loop 创建一个 Volume
Volume(1) = {1};

// ======================== 核心修改部分 ========================

// 1. 为 Volume(1) 创建一个 Physical 组。
// 这是为了在保存时能够识别出我们只想要体积网格（四面体）。
// "MyTetrahedra" 是自定义的名称，也可以用数字ID，如 Physical Volume(101) = {1};
Physical Volume("MyTetrahedra") = {1};

// 2. 设置网格保存选项，不保存每个元素关联的标签。
//    - 默认值为 2，表示保存 Physical 组的标签。
//    - 设置为 0 表示不保存任何标签。
//    注意：此选项在 msh2 文件格式下效果最明确。
Mesh.SaveElementTagType = 0;

// ==========================================================

// 生成 3D 网格（包含表面和体积）
Mesh 3;

// (可选) 如果想在脚本中直接保存，可以添加下面这行
// Save "output_mesh.msh";
EOF
cat "$tempfile"
which gmsh

gmsh $tempfile -3 -o $output_msh_file -format msh2
