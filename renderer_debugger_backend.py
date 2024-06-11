# Holosense debug emulator, so developers can test the rendering library by hard-coding the coordinates provided by the HoloSense backend.
# This acts like the main holosense backend. Type in the spatial coordinates yourself to test without having a camera installed.

#lib imports
import struct
from multiprocessing import shared_memory
import time
# Creates the shared memory block to be read by the Rendering library
shm = shared_memory.SharedMemory(name = "holosenseData", create=True, size=32)


# Create a buffer to hold the shared memory contents
buffer = shm.buf

#main loop
while True:
    # Read sample coordinates and write them to the memory link
    xcoord = float(input("Enter the user's X coordinate in inches relative to the screen: "))
    struct.pack_into('d', buffer, 0, xcoord)
    ycoord = float(input("Enter the user's Y coordinate in inches relative to the screen: "))
    struct.pack_into('d', buffer, 8, ycoord)
    zcoord = float(input("Enter the user's Z coordinate in inches relative to the screen: "))
    struct.pack_into('d', buffer, 16, zcoord)
    struct.pack_into('d', buffer, 24, time.time())
    print("Coordinates have been updated")
    i = input("press enter to change the coordinates, press q to close the link: ")
    if(i == "Q" or i == "q"):
        break

# Cleanup
shm.close()
shm.unlink()
