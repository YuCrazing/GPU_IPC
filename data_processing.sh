#!/bin/bash

# /opt/hfs20.5.278/bin/hython cloth_removing_ball.py --hip /home/yuzhang/Documents/cloth_removing_ball.hip --input_dir Output/saveSurface_32x32/ --output_dir hou_output/32x32/sim_00000
# python3 convert_obj_to_npz.py --file_prefix processed_surf --input_dir ./hou_output/32x32/ --output_path /home/yuzhang/repos/renderformer_phys/circle_data/cloth_32x32.npz


/opt/hfs20.5.278/bin/hython cloth_removing_ball.py --hip /home/yuzhang/Documents/cloth_removing_ball.hip --input_dir Output/saveSurface_100x100/ --output_dir hou_output/100x100/sim_00000
python3 convert_obj_to_npz.py --file_prefix processed_surf --input_dir ./hou_output/100x100/ --output_path /home/yuzhang/repos/renderformer_phys/circle_data/cloth_100x100.npz