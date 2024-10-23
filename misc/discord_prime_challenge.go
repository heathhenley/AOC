package main

import (
	"fmt"
	"time"
	"aoc/utils"
)

func is_prime(n uint64) bool {
	if n < 1 {
		panic("Number must be greater than 0")
	}
	if n < 4 {
		return n == 2 || n == 3
	}
	if n % 2 == 0 || n % 3 == 0 {
		return false
	}
	i := uint64(5)
	for i * i <= n {
		if n % i == 0 || n % (i + 2) == 0 {
			return false
		}
		i += 6
	}
	return true
}


func closest_prime(n uint64) uint64 {
	// get the closest prime number less than n
	if n <= 2 {
		fmt.Println(n)
		panic("that's just not possible, sir")
	}
	candidate := n - 1
	if n % 2 == 1 {
		candidate = n - 2
	}
	for candidate > 1 {
		if is_prime(candidate) {
			return candidate
		}
		candidate -= 2
	}
	return candidate
}


func test_some_primes() {
	primes := []uint64{2, 3, 5, 7, 11, 13, 17, 19, 23, 997, 59_999_999_999}
	for _, p := range primes {
		if !is_prime(p) {
			panic(fmt.Sprintf("%d is prime", p))
		}
	}
}

func main() {

	fmt.Println("Testing 6 billion")
	tic := time.Now()
	p := closest_prime(6_000_000_000)
	toc := time.Since(tic)
	fmt.Printf("Closest prime to 6 billion is %d\n", p)
	fmt.Printf("  Execution time: %0.5f\n", toc.Seconds())

	fmt.Println("Testing 60 billion")
	tic = time.Now() 
	p = closest_prime(60_000_000_000)
	toc = time.Since(tic)
	fmt.Printf("Closest prime to 60 billion is %d\n", p)
	fmt.Printf("  Execution time: %0.5f\n", toc.Seconds())



	for i := 0; i < 64; i += 8 {
		if i < 2 {
			continue
		}
		n := utils.Pow(uint64(2), uint64(i)) - 1
		fmt.Println("Testing 2^%d: %d", i, n)
		tic := time.Now() 
		p := closest_prime(n)
		toc := time.Since(tic)
		fmt.Printf("Closest prime to 2^%d (%d) is %d\n", i, n, p)
		fmt.Printf("  Execution time: %0.5f\n", toc.Seconds())
	}
}
