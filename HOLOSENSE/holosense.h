#ifndef HOLOSENSE_H // include guard
#define HOLOSENSE_H
#include <bits/stdc++.h> 
#include<glm/glm.hpp>

// to do
// make a standardized JSON config file parser. Config file is stored in the library path

// validator program?
// environment variable to set holosense config path?



namespace Holosense
{
    class Holosense
    {
    public:
        double screen_width;
        double screen_height;
        glm::mat4 getProjectionMatrix();
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
                    return;
                }

        }

    };


}

#endif