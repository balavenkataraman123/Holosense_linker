#include <boost/interprocess/shared_memory_object.hpp>
#include <boost/interprocess/mapped_region.hpp>
#include <cstring>
#include <bits/stdc++.h> 

int main(int argc, char *argv[])
{
   using namespace boost::interprocess;
   using namespace std;

   // Open the shared memory object.


   // Map the whole shared memory in this process.

   // Get the address of the mapped region.

    while(1 == 1){
    time_t start, end; 
    time(&start); 

    // Cast the address to a float pointer and read the three floating point numbers.
    shared_memory_object shm(open_only, "holosenseData", read_only);
    mapped_region region(shm, read_only);
    void* addr = region.get_address();
    double* data = static_cast<double*>(addr);
    double num1 = data[0];
    double num2 = data[1];
    double num3 = data[2];
    time(&end); 
    double time_taken = double(end - start); 
    cout << "Time taken by program is : " << fixed 
        << time_taken << setprecision(12); 
    cout << " sec " << endl; 
    // Print the read numbers.
    cout << "Read numbers: " << num1 << ", " << num2 << ", " << num3 << std::endl;
    }

   return 0;
}
