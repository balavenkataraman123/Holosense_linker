#include <boost/interprocess/shared_memory_object.hpp>
#include <boost/interprocess/mapped_region.hpp>
#include<iostream>

using namespace boost::interprocess;

  int main()
  {
    try
    {
      shared_memory_object shm_source(open_only, "holosenseData", read_only);

      std::string name = shm_source.get_name();

      std::cout << (!name.empty()) << "\n";
      std::cout << name << "\n";
    }
    catch (const std::exception &ex)
    {
      std::cout << "The shared memory object does not exist\n";
    }
  }