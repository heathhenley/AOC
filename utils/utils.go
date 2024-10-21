package utils

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
	"time"
)



func Min(a, b int) int {
	if a < b {
		return a
	}
	return b
}


func Max(a, b int) int {
	if a > b {
		return a
	}
	return b
}



func TimeIt(fn func(string) int) func(string) int {
	return func(data string) int {
		start := time.Now()
		result := fn(data)
		elapsed := time.Since(start)
		fmt.Printf("  Execution time: %0.5f\n", elapsed.Seconds())
		return result
	}
}


func ReadFile(fileName string) string {
	bytes, err := ioutil.ReadFile(fileName)
	if err != nil {
		log.Fatal(err)
	}
	data := string(bytes)
	data = strings.TrimSpace(data)
	return strings.ReplaceAll(data, "\r\n", "\n")
}


func Map[T any, U any](arr []T, fn func(T) U) []U {
	result := make([]U, len(arr))
	for i, v := range arr {
		result[i] = fn(v)
	}
	return result
}


func Reduce[T any, U any](arr []T, fn func(accum U, cur T) U, init U) U {
	latest := init
	for _, v := range arr {
		latest = fn(latest, v)
	}
	return latest
}


/*
	 Write the functions for each part and pass them in (this part is the same
   each day, so saves a bunch of copy pasta)
*/
func ProblemSetUp(part1func func(string) int, part2func func(string) int) {
	args := os.Args[1:]
	if len(args) < 1 {
		fmt.Println("Filename required as argument")
		fmt.Println("  Usage: go run script <filename>")
		os.Exit(1)
	}
	data := ReadFile(args[0])
	fmt.Println("Part 1:", TimeIt(part1func)(data))
	fmt.Println("Part 2:", TimeIt(part2func)(data))
}