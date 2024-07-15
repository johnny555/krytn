cmake_minimum_required(VERSION 3.8)
project(krytn)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

find_package(ament_cmake_auto REQUIRED)

ament_auto_find_build_dependencies()

install(PROGRAMS
   krytn/app.py 
   krytn/krytn_web.py 
   krytn/move_krytn.py
   DESTINATION lib/${PROJECT_NAME}
)

ament_auto_package(
  INSTALL_TO_SHARE
    config
    launch
    meshes
    models
    worlds
)


install(DIRECTORY
  DESTINATION
  share/${PROJECT_NAME}/models/${PROJECT_NAME}
)
# Create symlink to meshes folder, otherwise RVIz won't find the model
install(CODE "execute_process( \
    COMMAND ${CMAKE_COMMAND} -E create_symlink \
    ${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME}/meshes \
    ${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME}/models/${PROJECT_NAME}/meshes  \
    )"
)
