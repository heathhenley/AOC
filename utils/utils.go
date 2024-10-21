package utils

import (
	"fmt"
	"io/ioutil"
	"log"
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


func ProblemSetUp(
		part1func func(string) int, part2func func(string) int, fileName string) {
	data := ReadFile(fileName)
	fmt.Println("Part 1:", TimeIt(part1func)(string(data)))
	fmt.Println("Part 2:", TimeIt(part2func)(string(data)))
}