//
// device_fem_data.cu
// GIPC
//
// created by Kemeng Huang on 2022/12/01
// Copyright (c) 2024 Kemeng Huang. All rights reserved.
//

#include "device_fem_data.cuh"
#include "cuda_tools.h"


void device_TetraData::Malloc_DEVICE_MEM(const int& vertex_num, const int& tetradedra_num, const int& triangle_num, const int& softNum, const int& tri_edgeNum){
	int maxNumbers = vertex_num > tetradedra_num ? vertex_num : tetradedra_num;
	CUDA_SAFE_CALL(cudaMalloc((void**)&vertexes, vertex_num*sizeof(double3)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&o_vertexes, vertex_num * sizeof(double3)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&velocities, vertex_num * sizeof(double3)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&rest_vertexes, vertex_num * sizeof(double3)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&temp_double3Mem, vertex_num * sizeof(double3)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&xTilta, vertex_num * sizeof(double3)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&fb, vertex_num * sizeof(double3)));
	
	CUDA_SAFE_CALL(cudaMalloc((void**)&tetrahedras, tetradedra_num * sizeof(uint4)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&tempTetrahedras, tetradedra_num * sizeof(uint4)));


	CUDA_SAFE_CALL(cudaMalloc((void**)&tri_edges, tri_edgeNum * sizeof(uint2)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&tri_edge_adj_vertex, tri_edgeNum * sizeof(uint2)));


	CUDA_SAFE_CALL(cudaMalloc((void**)&volum, tetradedra_num * sizeof(double)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&masses, vertex_num * sizeof(double)));

	CUDA_SAFE_CALL(cudaMalloc((void**)&tempDouble, maxNumbers * sizeof(double)));
	//CUDA_SAFE_CALL(cudaMalloc((void**)&tempM, vertex_num * sizeof(double)));

	CUDA_SAFE_CALL(cudaMalloc((void**)&MChash, maxNumbers * sizeof(uint64_t)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&sortIndex, maxNumbers * sizeof(uint32_t)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&BoundaryType, vertex_num * sizeof(int)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&tempBoundaryType, vertex_num * sizeof(int)));

	CUDA_SAFE_CALL(cudaMemset(BoundaryType, 0, vertex_num * sizeof(int)));

	//CUDA_SAFE_CALL(cudaMalloc((void**)&sortVertIndex, vertex_num * sizeof(uint32_t)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&sortMapVertIndex, vertex_num * sizeof(uint32_t)));

	CUDA_SAFE_CALL(cudaMalloc((void**)&DmInverses, tetradedra_num * sizeof(__GEIGEN__::Matrix3x3d)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&Constraints, vertex_num * sizeof(__GEIGEN__::Matrix3x3d)));

	CUDA_SAFE_CALL(cudaMalloc((void**)&tempMat3x3, maxNumbers * sizeof(__GEIGEN__::Matrix3x3d)));
	//CUDA_SAFE_CALL(cudaMalloc((void**)&tempConstraints, vertex_num * sizeof(__GEIGEN__::Matrix3x3d)));

	

	CUDA_SAFE_CALL(cudaMalloc((void**)&targetIndex, softNum * sizeof(uint32_t)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&targetVert, softNum * sizeof(double3)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&triDmInverses, triangle_num * sizeof(__GEIGEN__::Matrix2x2d)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&area, triangle_num * sizeof(double)));
	CUDA_SAFE_CALL(cudaMalloc((void**)&triangles, triangle_num * sizeof(uint4)));
}

device_TetraData::~device_TetraData() {
	FREE_DEVICE_MEM();
}

void device_TetraData::FREE_DEVICE_MEM() {
	(cudaFree(sortIndex));
	(cudaFree(sortMapVertIndex));
	(cudaFree(vertexes)); 
	(cudaFree(o_vertexes));
	(cudaFree(temp_double3Mem));
	(cudaFree(velocities));
	(cudaFree(rest_vertexes));
	(cudaFree(xTilta));
	(cudaFree(fb));
	(cudaFree(tetrahedras));
	(cudaFree(tempTetrahedras));
	(cudaFree(volum));
	(cudaFree(masses));
	(cudaFree(DmInverses));
	(cudaFree(Constraints));
	(cudaFree(tempMat3x3));
	(cudaFree(MChash));
	(cudaFree(tempDouble));
	(cudaFree(BoundaryType));
	(cudaFree(tempBoundaryType));

	(cudaFree(targetIndex));
	(cudaFree(targetVert));
	(cudaFree(triDmInverses));
	(cudaFree(area));
	(cudaFree(triangles));

	(cudaFree(tri_edges));
	(cudaFree(tri_edge_adj_vertex));
}


