// Holosense runner file that uses GLM to calculate the location
#include <boost/interprocess/shared_memory_object.hpp>
#include <boost/interprocess/mapped_region.hpp>
#include "holosense.h" // header in local directory
#include <glm/glm.hpp>

using namespace Holosense;
using namespace boost::interprocess;

glm::mat4 getProjectionMatrix(double dpi)
{
    shared_memory_object shm(open_only, "holosenseData", read_only);
    mapped_region region(shm, read_only);
    void* addr = region.get_address();
    double* data = static_cast<double*>(addr);
    double num1 = data[0];
    double num2 = data[1];
    double num3 = data[2];
    
    
}
