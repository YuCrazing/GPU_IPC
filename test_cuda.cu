#include <stdio.h>
#include <cuda_runtime.h>

int main()
{
    int deviceCount = 0;
    cudaError_t status = cudaGetDeviceCount(&deviceCount);

    if (status != cudaSuccess) {
        fprintf(stderr, "cudaGetDeviceCount failed! Error: %s\n",
                cudaGetErrorString(status));
        return 1;
    }

    printf("Detected %d CUDA capable device(s).\n", deviceCount);

    for (int dev = 0; dev < deviceCount; dev++) {
        cudaDeviceProp prop;
        cudaGetDeviceProperties(&prop, dev);
        printf("Device %d: %s\n", dev, prop.name);
        printf("  Compute capability: %d.%d\n", prop.major, prop.minor);
        printf("  Total Global Memory: %zu MB\n", prop.totalGlobalMem / (1024 * 1024));
        printf("  MultiProcessor Count: %d\n", prop.multiProcessorCount);
    }

    // 尝试设置 GPU 0
    if (deviceCount > 0) {
        status = cudaSetDevice(0);
        if (status != cudaSuccess) {
            fprintf(stderr, "cudaSetDevice(0) failed! Error: %s\n",
                    cudaGetErrorString(status));
            return 1;
        }
        printf("Successfully set device 0.\n");
    }

    return 0;
}
