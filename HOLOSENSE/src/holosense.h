#ifndef HOLOSENSE_H // include guard
#define HOLOSENSE_H
#include <bits/stdc++.h> 
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <boost/interprocess/shared_memory_object.hpp>
#include <boost/interprocess/mapped_region.hpp>
// to do
// make a standardized JSON config file parser. Config file is stored in the library path

// validator program?
// environment variable to set holosense config path?


using namespace boost::interprocess;
namespace Holosense
{
    class Holosense
    {
    public:
        double screen_width;
        double screen_height;
        double centre_x_offset;
        double centre_y_offset;
        Holosense() { // constructor method
                try{
                    shared_memory_object shm_source(open_only, "holosenseData", read_only);
                    std::string name = shm_source.get_name();

                    std::cout << (!name.empty()) << "\n";
                    std::cout << name << "\n";
                }
                catch (const std::exception &ex){
                    std::cout << "Holosense configuration error: The shared memory object does not exist\n";
                    std::cout << "Start the Holosense backend, or a compatible replacement. \n";
                    throw &ex;
                }

        }
        glm::mat4 getProjectionMatrix(double dpi, double farplane) // dpi the ratio between game coordinate space and inches in real life. 
        { 
            shared_memory_object shm(open_only, "holosenseData", read_only);
            mapped_region region(shm, read_only);
            void* addr = region.get_address();
            double* data = static_cast<double*>(addr);
            double xcoord = data[0] * dpi;
            double ycoord = -data[1] * dpi;
            double zcoord = data[2] * dpi;
            double left = xcoord - this->screen_width * 0.5;
            double right = xcoord + this->screen_width * 0.5;
            double top = ycoord - this->screen_width * 0.5;
            double bottom = ycoord + this->screen_width * 0.5;
            double nearplane = zcoord;
            glm::mat4 projectionMatrix = glm::frustum(left, right, top, bottom, nearplane, farplane);
            projectionMatrix = glm::translate(projectionMatrix, glm::vec3(xcoord, ycoord, zcoord));
            return projectionMatrix;

        }




    };

}

#endif