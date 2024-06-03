import struct
from multiprocessing import shared_memory

# Define the three floating-point values to be stored in shared memory
float_values = [35.5, 2.71828, 1.61803]

# Determine the size of the shared memory block needed
# Each float value requires 4 bytes (32 bits)
size = len(float_values) * 8  # 8 bytes for each double precision float

# Create a new shared memory block
shm = shared_memory.SharedMemory(name = "holosenseData", create=True, size=size)

# Create a buffer to hold the shared memory contents
buffer = shm.buf
while True:
# Write the float values to the shared memory block

    for i, value in enumerate(float_values):

        struct.pack_into('d', buffer, i * 8, value)

    # Demonstrate reading the values back from shared memory
    i = input("press enter to continue: ")

# Cleanup: Unlink the shared memory block
shm.close()
shm.unlink()