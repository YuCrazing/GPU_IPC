# !/bin/bash

export CUDA_HOME=/usr/local/cuda-12.4
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:${LD_LIBRARY_PATH}


# build_type="Debug"
# build_type="RelWithDebInfo"
build_type="Release"

mkdir build; cd build
# cmake Could NOT find OpenGL
# https://github.com/ContinuumIO/anaconda-issues/issues/8779
cmake .. -DCMAKE_TOOLCHAIN_FILE=../vcpkg/scripts/buildsystems/vcpkg.cmake -DCMAKE_BUILD_TYPE=$build_type -DFETCHCONTENT_QUIET=OFF
cmake --build . --parallel 10 --config $build_type
build_status=$?
cd ..
if [ $build_status -eq 0 ]; then
    ./build/gipc
else
    echo "Build failed."
fi