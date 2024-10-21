// Description: Day 1: Not Quite Lisp
package main

import (
	"fmt"
	"os"
	"aoc/utils"
)


func part1(data string) int {
	floor := 0
	for _, c := range data {
		if c == '(' {
			floor++
		} else if c == ')' {
			floor--
		}
	}
	return floor
}


func part2(data string) int {
	floor := 0
	for i, c := range data {
		if c == '(' {
			floor++
		} else if c == ')' {
			floor--
		}
		if floor == -1 {
			return i + 1
		}
	}
	panic("Basement not found in input")
}


func main() {
	args := os.Args[1:]
	if len(args) < 1 {
		fmt.Println("Filename required as argument")
		fmt.Println("  Usage: go run script <filename>")
		os.Exit(1)
	}
	utils.ProblemSetUp(part1, part2, args[0])
}