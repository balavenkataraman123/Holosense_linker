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
        double window_right_offset;
        double window_left_offset;
        double window_top_offset;
        double window_bottom_offset;
        double wpx = 3840; // temporary stuff
        double hpx = 2160;
        Holosense() { // constructor method

                double scdiag = 15.6; // meant to read this from the config file.
                screen_width = scdiag * (wpx/sqrt(wpx * wpx + hpx * hpx)); // sets the screen width and height in inches
                screen_width = scdiag * (hpx/sqrt(wpx * wpx + hpx * hpx));
                window_top_offset = screen_height / 2;
                window_bottom_offset = -screen_height / 2;
                window_right_offset = screen_width / 2;
                window_left_offset = -screen_width / 2;
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
        void updateViewport(int top, int left, int bottom, int right){
            window_left_offset = -(screen_width/2) + ((double)left/ (double)wpx)*screen_width;
            window_left_offset = ((double)(right)/ (double)wpx)*screen_width;
            window_bottom_offset = -((double)(bottom) / (double)hpx)*screen_height;
            window_top_offset = (screen_height/2) - ((double)top/ (double)hpx)*screen_height;
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
            double left = xcoord + this->window_left_offset*dpi;
            double right = xcoord + this->window_right_offset*dpi;
            double top = ycoord + this->window_top_offset*dpi;
            double bottom = ycoord + this->window_bottom_offset*dpi;
            double nearplane = zcoord;

            glm::mat4 projectionMatrix = glm::frustum(left, right, top, bottom, nearplane, farplane);
            projectionMatrix = glm::translate(projectionMatrix, glm::vec3(xcoord, ycoord, zcoord));
            return projectionMatrix;

        }

    };

}

#endif
