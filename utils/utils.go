package utils

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"time"
)


type funcType func(string) int

func TimeIt(fn funcType) funcType {
	return func(data string) int {
		start := time.Now()
		result := fn(data)
		elapsed := time.Since(start)
		fmt.Printf("  Execution time: %0.5f\n", elapsed.Seconds())
		return result
	}
}


func ReadFile(fileName string) string {
	data, err := ioutil.ReadFile(fileName)
	if err != nil {
		log.Fatal(err)
	}
	return string(data)
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
	fmt.Println("Part 1:", TimeIt(part1func)(string(data)))
	fmt.Println("Part 2:", TimeIt(part2func)(string(data)))
}