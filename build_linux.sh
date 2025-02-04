build_type="Debug"
# build_type="RelWithDebInfo"
# build_type="Release"

mkdir build; cd build
# cmake Could NOT find OpenGL
# https://github.com/ContinuumIO/anaconda-issues/issues/8779
cmake -S .. -DCMAKE_BUILD_TYPE=$build_type 
cmake --build . --parallel 10 --config $build_type
build_status=$?
cd ..
if [ $build_status -eq 0 ]; then
    ./build/gipc
else
    echo "Build failed."
fi