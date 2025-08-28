export CUDA_HOME=/usr/local/cuda-12.4
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:${LD_LIBRARY_PATH}



build_type="Debug"
# build_type="RelWithDebInfo"
# build_type="Release"

mkdir build; cd build
# cmake Could NOT find OpenGL
# https://github.com/ContinuumIO/anaconda-issues/issues/8779
# cmake -S .. -DCMAKE_BUILD_TYPE=$build_type
cmake -S .. \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda-12.1/bin/nvcc \
  -DCMAKE_CUDA_STANDARD=17 \
  -DCMAKE_CUDA_ARCHITECTURES=60 \
  -DCMAKE_BUILD_TYPE=$build_type \
  -DCMAKE_NO_SYSTEM_FROM_IMPORTED=1
cmake --build . --parallel 10 --config $build_type
build_status=$?
cd ..
if [ $build_status -eq 0 ]; then
    ./build/gipc
else
    echo "Build failed."
fi
