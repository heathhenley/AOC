package main

import (
	"fmt"
)

func counting_sort(arr []uint16) []uint16 {
	counter := make([]uint16, 65536)
	for _, elem := range arr {
		counter[elem]++
	}

	prefix := make([]uint16, 65536)
	// no elements less than 0
	prefix[0] = 0
	for i := 1; i < 65536; i++ {
		// prefix[i] is the number of elements less than i
		prefix[i] = prefix[i-1] + counter[i-1]
	}

	result := make([]uint16, len(arr))
	for _, val := range arr {
		pos := prefix[val]
		result[pos] = val
		// increment the prefix sum for this value (so we move the next occurrence 
		// of this value to the right)
		prefix[val]++
	}
	return result
}

func main() {
	test_ints := make([]uint16, 0, 4)
	test_ints = append(test_ints, 4, 1, 3, 2)
	fmt.Println("Original array:")
	for _, el := range test_ints {
		fmt.Println(el)
	}
	sorted := counting_sort(test_ints)
	fmt.Println("\nSorted array:")
	for _, el := range sorted {
		fmt.Println(el)
	}
}
