// Description: Day 1: Not Quite Lisp
package main

import (
	"aoc/utils"
)


func part1(data string) int {
	floorMap := map[rune]int{'(': 1, ')': -1}
	floor := 0
	for _, c := range data {
		floor += floorMap[c]
	}
	return floor
}


func part2(data string) int {
	floorMap := map[rune]int{'(': 1, ')': -1}
	floor := 0
	for i, c := range data {
		floor += floorMap[c]
		if floor == -1 {
			return i + 1
		}
	}
	panic("Basement not found in input")
}


func main() {
	utils.ProblemSetUp(part1, part2)
}