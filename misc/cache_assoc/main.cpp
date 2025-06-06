// I saw a post that due to the way the cache is implemented - sometimes powers
// of 2 can actually be slower because they will cause more cache misses - the
// value maps to the same set in the cache so it will evict the same value over
// and over again - where as a non power of 2 will map to a different set and
// not cause as many cache misses.

// I wanted to test this out - haven't been able to reproduce though - here's a
// a link: https://en.algorithmica.org/hpc/cpu-cache/associativity/

// probably just depends a lot on specific hardware to reproduce?

#include <iostream>
#include <vector>
#include <chrono>
#include <cmath>
#include <random>

int main(int argc, char** argv) {
    uint32_t num_elements = std::pow(2, 21);
    uint32_t max_stride = 512;
    std::vector<uint32_t> arr(num_elements * max_stride, 0);

    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <num_elements>" << std::endl;
        return 1;
    }

    num_elements = std::pow(2, std::atoi(argv[1]));


    uint32_t stride = 2;

    // test how long it takes to loop through the array
    // in increments of stride
    auto start = std::chrono::high_resolution_clock::now();
    for (auto i = 0; i < num_elements * stride; i += stride) {
        arr[i]++;
    }
    /*auto end = std::chrono::high_resolution_clock::now();
    std::cout << stride << "," << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() << std::endl;*/

    return 0;
}
