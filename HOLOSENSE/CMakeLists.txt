cmake_minimum_required(VERSION 3.22)
project(HoloSenseLib)

set(CMAKE_CXX_STANDARD 20)

set(glm_DIR 3rdparty/glm/cmake/glm)

find_package(glm REQUIRED)

include_directories(${glm_INCLUDE_DIRS})

add_executable(${PROJECT_NAME}
        src/holosense.h
        )

target_link_libraries(${PROJECT_NAME} PRIVATE ${OPENGL_LIBRARIES})
target_link_libraries(${PROJECT_NAME} PRIVATE ${OPENGL_gl_LIBRARY} glfw)
target_link_libraries(${PROJECT_NAME} PRIVATE glm::glm)

#file(COPY ${GLFW_DLL} DESTINATION ${CMAKE_BINARY_DIR})
